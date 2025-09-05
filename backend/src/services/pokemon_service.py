from src.models import Pokemon
from src.db import SessionType


def add_pokemon(pokemon: Pokemon, session: SessionType) -> Pokemon:
    session.add(pokemon)
    session.commit()
    session.refresh(pokemon)
    return pokemon
