from fastapi import APIRouter
from src.models import Pokemon
from src.db import SessionType
from typing import List
from fastapi import HTTPException
from sqlmodel import select
from src.services import pokemon_service

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.post("/create")
def add_pokemon(pokemon_name: str, session: SessionType) -> Pokemon:
    print(f"Got name, {pokemon_name}")
    try:
        p = Pokemon(name=pokemon_name)
        return pokemon_service.add_pokemon(p, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{pokemon_id}")
def get_pokemon(pokemon_id: int, session: SessionType) -> Pokemon:
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(detail="Not Found", status_code=404)
    return pokemon


@router.post("/{pokemon_id}")
def delete_pokemon(pokemon_id: int, session: SessionType):
    try:
        pokemon = get_pokemon(pokemon_id, session)
    except HTTPException as e:
        raise e
    session.delete(pokemon)
    session.commit()
    return {"ok": True}


@router.post("/")
def list_pokemon(session: SessionType) -> List[Pokemon]:
    return list(session.exec(select(Pokemon)).all())
