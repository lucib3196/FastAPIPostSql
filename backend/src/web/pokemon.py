import shutil
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Form, HTTPException
from sqlmodel import select

from src.database.db import SessionType
from src.models import Pokemon, PokemonInput
from src.services import pokemon_full
from src.services import pokemon_folder_service as svc
from src.services import pokemon_crud

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.post("/create/basic/{pokemon_name}")
async def add_pokemon(pokemon_name: str, session: SessionType) -> Pokemon:
    """This route is focused on just creating the base of the pokemon, does
    not add folders directory or create any data purely focused on generating the basic
    data in the database

    Args:
        pokemon_name (str): _description_
        session (SessionType): _description_

    Raises:
        HTTPException: _description_

    Returns:
        Pokemon: _description_
    """
    try:
        p = Pokemon(name=pokemon_name)
        return pokemon_crud.create_pokemon(p, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create/complete/{pokemon_name}")
async def add_pokemon_complete(
    pokemon_name: str, pokemon_data: PokemonInput, session: SessionType
):
    try:
        response = await pokemon_full.create_pokemon_complete(
            pokemon=Pokemon(name=pokemon_name),
            pokemon_data=pokemon_data,
            session=session,
        )
        return response
    except HTTPException as e:
        raise e


@router.get("{pokemon_id}")
async def get_pokemon_by_id(pokemon_id: int, session: SessionType) -> Pokemon:
    try:
        return pokemon_crud.get_pokemon_by_id(pokemon_id, session)
    except HTTPException as e:
        raise e


@router.post("/create_with_image/")
async def create_pokemon_with_image(
    session: SessionType,
    name: str = Form(...),
    description: str = Form(...),
    physical_attr: str = Form(...),
    ptype: str = Form(...),
):
    try:
        result = await pokemon_crud.generate_pokemon_image(
            name, description, physical_attr, ptype, session
        )
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)


@router.delete("/{pokemon_id}")
async def delete_pokemon(pokemon_id: int, session: SessionType):
    try:
        # 1) Ensure the Pokémon exists in the DB
        pokemon = pokemon_crud.get_pokemon_by_id(pokemon_id=pokemon_id, session=session)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokémon not found")

        # 2) Try to resolve its directory (non-fatal if it fails)
        dir_path: Optional[Path] = None
        try:
            data = await svc.get_pokemon_directory(pokemon_id, session)
            if data and getattr(data, "paths", None):
                dir_path = Path(data.paths[0])
        except HTTPException:
            # If directory service raises (e.g., 404), keep going and just delete the DB row
            dir_path = None

        # 3) Delete directory tree if present
        if dir_path and dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)

        # 4) Delete DB row
        pokemon_crud.delete_pokemon(pokemon_id=pokemon_id, session=session)

        return {"detail": f"Pokémon {pokemon_id} deleted successfully."}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get_all")
def list_pokemon(session: SessionType) -> List[Pokemon]:
    return list(session.exec(select(Pokemon)).all())
