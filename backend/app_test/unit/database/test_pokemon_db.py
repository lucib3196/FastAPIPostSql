from src.models import Pokemon
from src.database import pokemon as pokemon_db
from app_test.unit.database.fixture_pokemon_db import *


def test_add_pokemon(db_session, pokemon_payload):
    p_created = pokemon_db.create_pokemon(pokemon_payload, db_session)
    assert p_created.name == pokemon_payload.name
    assert (
        p_created.id == 1
    )  # This is the first pokemon and simply working with increasing ingts


def test_get_pokemon(db_session, pokemon_payload):
    p_created = pokemon_db.create_pokemon(pokemon_payload, db_session)
    p_retrieved = pokemon_db.get_pokemon(p_created, db_session)
    assert p_created == p_retrieved


def test_delete_pokemon(db_session, pokemon_payload):
    p_created = pokemon_db.create_pokemon(pokemon_payload, db_session)
    # delete
    pokemon_db.delete_pokemon(p_created, db_session)
    p_retrieved = pokemon_db.get_pokemon(p_created, db_session)
    assert p_retrieved == None


def test_create_multiple_pokemon(db_session, multiple_pokemon):
    p_created = [pokemon_db.create_pokemon(p, db_session) for p in multiple_pokemon]
    assert len(p_created) == len(multiple_pokemon)
    for p in p_created:
        assert pokemon_db.get_pokemon(p, db_session) != None


def test_get_all_pokemon(db_session, multiple_pokemon):
    p_created = [pokemon_db.create_pokemon(p, db_session) for p in multiple_pokemon]
    assert (
        len(p_created)
        == len(multiple_pokemon)
        == len(pokemon_db.get_all_pokemon(db_session))
    )


def test_get_all_pokemon_empty(db_session):
    assert (pokemon_db.get_all_pokemon(db_session)) == []
