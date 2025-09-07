import pytest
from src.models import Pokemon
from typing import List


@pytest.fixture
def pokemon_payload(name="pickachu") -> Pokemon:
    return Pokemon(name=name)


@pytest.fixture
def multiple_pokemon(names=["pickachu", "geodude", "charizard"]) -> List[Pokemon]:
    return [Pokemon(name=n) for n in names]
