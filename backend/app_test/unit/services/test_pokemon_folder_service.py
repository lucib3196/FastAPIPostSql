from app_test.unit.services.fixture_pokemon_service import *
from src.services import pokemon_folder_service as pokemon_service
from pathlib import Path
from src.core.pokemon_config import MonsterConfig
from src.services.pokemon_utils import format_pokemon_folder_name
from src.models import PokemonData
import json
from src.response_models import PokemonResponsePaths
from fastapi import UploadFile
from io import BytesIO


@pytest.mark.asyncio
async def test_set_pokemon_directory(
    db_session, pokemon_payload, tmp_path, monkeypatch
):
    # Patch MonsterConfig.MONSTER_DIR to a temp directory
    fake_monster_dir = tmp_path / "monsters"
    monkeypatch.setattr(MonsterConfig, "MONSTER_DIR", fake_monster_dir)

    # Call service
    data = await pokemon_service.set_pokemon_directory(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )
    # Build expected path safely
    expected = fake_monster_dir / format_pokemon_folder_name(pokemon_payload)
    assert Path(str(data.pokemon.image_directory)) == expected
    assert expected.exists()


@pytest.mark.asyncio
async def test_add_required_folders(db_session, pokemon_payload, tmp_path, monkeypatch):
    # Patch MonsterConfig.MONSTER_DIR to a temp directory
    fake_monster_dir = tmp_path / "monsters"
    monkeypatch.setattr(MonsterConfig, "MONSTER_DIR", fake_monster_dir)

    # Call service
    data = await pokemon_service.add_required_folders_pokemon(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )

    # Build expected paths
    expected = [
        fake_monster_dir / format_pokemon_folder_name(pokemon_payload) / subdir
        for subdir in MonsterConfig.DATA_DIRS
    ]

    created_paths = [Path(d["path"]) for d in data.paths]

    assert created_paths == expected

    # Also check the directories actually exist on disk
    for d in expected:
        assert d.exists() and d.is_dir()


@pytest.mark.asyncio
async def test_get_image_directory(pokemon_payload, db_session, tmp_path, monkeypatch):

    fake_monster_dir = tmp_path / "monsters"
    monkeypatch.setattr(MonsterConfig, "MONSTER_DIR", fake_monster_dir)

    # Call service
    await pokemon_service.set_pokemon_directory(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )

    expected = fake_monster_dir / format_pokemon_folder_name(pokemon_payload)

    assert expected.exists()

    data = pokemon_service.get_pokemon_directory(
        pokemon_id=pokemon_payload.id, session=db_session
    )
    assert Path(data.paths[0]) == expected


@pytest.mark.asyncio
async def test_set_base_data(db_session, pokemon_payload, tmp_path, monkeypatch):
    # Patch MONSTER_DIR to a temp directory so tests don't touch real FS
    fake_monster_dir = tmp_path / "monsters"
    monkeypatch.setattr(MonsterConfig, "MONSTER_DIR", fake_monster_dir)

    # Ensure directories exist
    await pokemon_service.set_pokemon_directory(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )
    await pokemon_service.add_required_folders_pokemon(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )

    # Prepare sample payload
    payload = PokemonData(
        name=pokemon_payload.name,
        description="Some pokemon",
        physical_attr="Yellow",
        ptype="Electric",
    )

    # Call service
    result = await pokemon_service.set_pokemon_base_data(
        pokemon_payload.id, pokemon_data=payload, session=db_session
    )

    # --- Assertions ---

    # Return type
    assert isinstance(result, PokemonResponsePaths)
    assert result.status == 200
    assert "Saved" in result.detail

    # File path from response
    assert len(result.paths) == 1
    file_path = Path(result.paths[0])
    assert file_path.exists
    assert file_path.is_file

    # File content check
    content = json.loads(file_path.read_text())
    assert content["name"] == pokemon_payload.name
    assert content["description"] == "Some pokemon"
    assert content["physical_attr"] == "Yellow"
    assert content["ptype"] == "Electric"
    # The Pokémon returned in response should be the same as our payload ID
    assert result.pokemon.id == pokemon_payload.id


@pytest.mark.asyncio
async def test_getting_file(db_session, pokemon_payload, tmp_path, monkeypatch):
    # Patch MONSTER_DIR to a temp directory so tests don't touch real FS
    fake_monster_dir = tmp_path / "monsters"
    monkeypatch.setattr(MonsterConfig, "MONSTER_DIR", fake_monster_dir)

    # Ensure directories exist
    await pokemon_service.set_pokemon_directory(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )
    await pokemon_service.add_required_folders_pokemon(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )

    # Prepare sample payload
    payload = PokemonData(
        name=pokemon_payload.name,
        description="Some pokemon",
        physical_attr="Yellow",
        ptype="Electric",
    )

    await pokemon_service.set_pokemon_base_data(
        pokemon_payload.id, pokemon_data=payload, session=db_session
    )

    content = await pokemon_service.get_pokemon_file(
        pokemon_id=pokemon_payload.id,
        folder="data",
        filename="data_user.json",
        session=db_session,
    )

    assert json.loads(content["content"]) == payload.model_dump()


@pytest.mark.asyncio
async def test_set_pokemon_image(db_session, pokemon_payload, tmp_path, monkeypatch):
    # Monkeypatch the MonsterConfig base directory to tmp_path
    fake_monster_dir = tmp_path / "monsters"
    monkeypatch.setattr(MonsterConfig, "MONSTER_DIR", fake_monster_dir)

    # Ensure the pokemon directory is created (depends on your service flow)
    await pokemon_service.set_pokemon_directory(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )
    await pokemon_service.add_required_folders_pokemon(
        pokemon_id=pokemon_payload.id,
        session=db_session,
    )

    # Fake image data
    image_bytes = b"\x89PNG\r\n\x1a\n" + b"FAKEPNGDATA"
    fake_file = UploadFile(file=BytesIO(image_bytes), filename="pikachu.png")

    response = pokemon_service.add_pokemon_image(
        pokemon_id=pokemon_payload.id,
        option="base",
        session=db_session,
        file=fake_file,
    )
    saved_path = response.paths[0]

    saved_file = Path(saved_path)
    assert saved_file.exists()
    assert saved_file.read_bytes().startswith(b"\x89PNG")
