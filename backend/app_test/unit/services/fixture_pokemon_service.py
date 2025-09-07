import pytest
from src.models import Pokemon
from typing import List
from src.database import pokemon as pokemon_db


@pytest.fixture
def pokemon_payload(db_session, name="pickachu") -> Pokemon:
    return pokemon_db.create_pokemon(Pokemon(name=name), db_session)


@pytest.fixture
def multiple_pokemon(
    db_session, names=["pickachu", "geodude", "charizard"]
) -> List[Pokemon]:
    return [pokemon_db.create_pokemon(Pokemon(name=n), db_session) for n in names]
