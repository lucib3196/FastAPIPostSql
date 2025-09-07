from app_test.unit.services.fixture_pokemon_service import *
from src.services import pokemon_service
from fastapi import HTTPException
from pathlib import Path
from src.core.pokemon_config import MonsterConfig
from backend.src.utils.pokemon_utils import format_pokemon_folder_name


def test_get_pokemon_by_id(db_session, pokemon_payload):
    pokemon_id = pokemon_payload.id
    pokemon_retrieved = pokemon_service.get_pokemon_by_id(pokemon_id, db_session)
    assert pokemon_payload == pokemon_retrieved


def test_get_pokemon_by_id_empty(db_session):
    pokemon_id = 5  # dummy value
    with pytest.raises(HTTPException) as excinfo:
        pokemon_service.get_pokemon_by_id(pokemon_id, db_session)
    assert excinfo.value.status_code == 404
