from src.models import Pokemon
from src.database.db import SessionType
from sqlmodel import select, delete
from typing import Sequence


def add_pokemon(pokemon: Pokemon, session: SessionType) -> Pokemon:
    session.add(pokemon)
    session.commit()
    session.refresh(pokemon)
    return pokemon


def get_pokemon(pokemon: Pokemon, session: SessionType) -> Pokemon | None:
    statement = select(Pokemon).where(Pokemon.id == pokemon.id)
    return session.exec(statement).first()


def delete_pokemon(pokemon: Pokemon, session: SessionType) -> None:
    session.delete(pokemon)
    session.commit()
    session.flush()


def get_all_pokemon(session: SessionType) -> Sequence[Pokemon]:
    return session.exec(select(Pokemon)).all()
