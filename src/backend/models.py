from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class Region(Enum):
    kanto = "Kanto"
    johto = "Jothto"


class Pokemon(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    name: str
