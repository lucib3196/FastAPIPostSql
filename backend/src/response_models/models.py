from pydantic import BaseModel
from typing import List, Any
from src.models import Pokemon


class PokemonResponse(BaseModel):
    status: str | int
    detail: str
    pokemon: Pokemon


class PokemonResponsePaths(PokemonResponse):
    paths: List[Any]
