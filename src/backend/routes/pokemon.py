from fastapi import APIRouter
from src.backend.models import Pokemon
from src.backend.db import SessionType
from typing import List
from fastapi import HTTPException
from sqlmodel import select


router = APIRouter(prefix="/pokemon")


@router.post("/")
def add_pokemon(pokemon: Pokemon, session: SessionType) -> Pokemon:
    session.add(pokemon)
    session.commit()
    session.refresh(pokemon)
    return pokemon


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
