from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
from typing import Union, Mapping, Any, Optional, List, TypedDict
from pydantic import BaseModel
from pydantic import BaseModel, ValidationError


class Region(Enum):
    kanto = "Kanto"
    johto = "Jothto"


class ImageDir(str, Enum):
    animations = "animations"
    base = "base"


class Pokemon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    name: str
    image_directory: str | None = Field(default_factory=None)


class PokemonData(BaseModel):
    name: str
    description: str
    physical_attr: str
    ptype: str


class PokemonDescription(BaseModel):
    # fill out with the shape you expect back
    summary: str


class PokemonMoveList(BaseModel):
    move_list: List[str]


# Optional: help type-check plain dicts
class PokemonDict(TypedDict):
    name: str
    description: str
    physical_attr: str
    ptype: str


PokemonInput = Union[PokemonData, Mapping[str, Any], PokemonDict]
