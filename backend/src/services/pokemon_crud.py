from src.models import Pokemon
from src.database.db import SessionType
from fastapi import HTTPException
from src.database import pokemon as pokemon_db
from starlette import status


def create_pokemon(pokemon: Pokemon, session: SessionType):
    return pokemon_db.create_pokemon(pokemon, session)


def get_pokemon_by_id(pokemon_id: int, session: SessionType) -> Pokemon:
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(detail="Not Found", status_code=404)
    return pokemon


def delete_pokemon(pokemon_id: int, session: SessionType):
    try:
        pokemon = get_pokemon_by_id(pokemon_id, session)
    except HTTPException as e:
        raise e
    session.delete(pokemon)
    session.commit()
    return {"ok": True}


def get_all_pokemon(session: SessionType):
    try:
        results = pokemon_db.get_all_pokemon(session)
        if results is None or []:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, detail="No Monsters Available"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=(str(e))
        )
