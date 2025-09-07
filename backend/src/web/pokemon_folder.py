from fastapi import APIRouter
from src.database.db import SessionType
from src.models import PokemonInput
from typing import Literal
from src.services import pokemon_folder_service as svc
from fastapi import UploadFile
from fastapi import HTTPException

router = APIRouter(prefix="/pf", tags=["pokemon"])


# ── Directories ────────────────────────────────────────────────────────────────


@router.get("/{pokemon_id}/directory")
async def read_pokemon_directory(pokemon_id: int, session: SessionType):
    """Return info about the Pokémon's root directory."""
    try:
        return await svc.get_pokemon_directory(pokemon_id, session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{pokemon_id}/directories/required")
async def create_required_directories(pokemon_id: int, session: SessionType):
    """Create all required subdirectories for the Pokémon (e.g., base, animations, etc.)."""
    try:
        return await svc.add_required_folders_pokemon(pokemon_id, session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Data (JSON) files ──────────────────────────────────────────────────────────


@router.post("/{pokemon_id}/data")
async def upsert_pokemon_data(
    pokemon_id: int,
    pokemon_data: PokemonInput,
    session: SessionType,
):
    """
    Save base/description JSON for the Pokémon into its data folder.
    (Uses service default of data_type='base_data'; pass different type inside the body if needed.)
    """
    try:
        return await svc.set_pokemon_base_data(pokemon_id, pokemon_data, session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{pokemon_id}/files/{folder}/{filename}")
async def read_pokemon_file(
    pokemon_id: int,
    folder: Literal["animations", "base", "data"],
    filename: str,
    session: SessionType,
):
    """Read a specific file under the Pokémon's folder (e.g., /files/base/data_user.json)."""
    try:
        return await svc.get_pokemon_file(pokemon_id, folder, filename, session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Images ─────────────────────────────────────────────────────────────────────


@router.post("/{pokemon_id}/images/{folder}")
async def upload_pokemon_image(
    pokemon_id: int,
    folder: Literal["animations", "base"],
    file: UploadFile,
    session: SessionType,
):
    """Upload an image into a Pokémon subfolder (e.g., base or animations)."""
    try:
        return await svc.add_pokemon_image(pokemon_id, folder, session, file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{pokemon_id}/images/{folder}")
async def list_pokemon_images(
    pokemon_id: int,
    folder: Literal["base", "animations"],
    session: SessionType,
):
    """List all PNG images available in a specific Pokémon subfolder."""
    try:
        return await svc.get_all_pokemon_images(pokemon_id, folder, session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
