from ..services.prompts import *
from src.models import *

PokemonSearchInput = Union[Pokemon, Mapping[str, int | str]]


def normalize_input(data: PokemonInput):
    """
    Accepts either a PokemonData model or a dict-like object and returns a validated PokemonData.
    Also tolerates a few common misspellings/legacy keys.
    """
    if isinstance(data, PokemonData):
        return data

    # tolerate legacy/misspelled keys
    src = dict(data)
    if "physical_att" in src and "physical_attr" not in src:
        src["physical_attr"] = src.pop("physical_att")
    if "pytpe" in src and "ptype" not in src:
        src["ptype"] = src.pop("pytpe")

    try:
        return PokemonData(**src)  # type: ignore
    except ValidationError as e:
        # Raise a clearer error about required fields
        missing = [e["loc"] for e in e.errors()]
        raise ValueError(f"Pokemon data missing/invalid fields: {missing}") from e


def format_prompt(template: str, data: PokemonData) -> str:
    """Safe formatter for your existing string templates."""
    return template.format(
        name=data.name,
        description=data.description,
        physical_attr=data.physical_attr,
        ptype=data.ptype,
    )


def format_pokemon_folder_name(data: PokemonSearchInput):
    try:
        if isinstance(data, Pokemon):
            pokemon_name = data.name
            pokemon_id = data.id
        else:
            pokemon_name = data["name"]
            pokemon_id = data["id"]
        name = f"{pokemon_name}_{pokemon_id}"
        return name.strip().lower()
    except Exception as e:
        raise e
