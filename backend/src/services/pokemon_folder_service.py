import asyncio
import json
from pathlib import Path
from typing import Literal, Any

from anyio import to_thread
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel
from starlette import status
from collections.abc import Mapping
from src.core.pokemon_config import MonsterConfig, ImageDir
from src.database import pokemon as pokemon_db
from src.database.db import SessionType
from src.models import PokemonInput
from src.response_models import PokemonResponse, PokemonResponsePaths
from src.services.pokemon_crud import get_pokemon_by_id
from src.utils.pokemon_utils import format_pokemon_folder_name
from typing import Union
from typing import Optional


async def set_pokemon_directory(pokemon_id: int, session: SessionType):
    """
    Create and assign a directory for a given Pokémon.

    This function fetches a Pokémon by ID, generates a folder name for it,
    creates the directory if it doesn't exist, updates the Pokémon's
    `image_directory` field, and persists the change to the database.

    Args:
        pokemon_id (int): The unique identifier of the Pokémon.
        session (SessionType): Active database session.

    Returns:
        PokemonResponse: A response object with status, detail message,
        and the updated Pokémon.

    Raises:
        HTTPException: If the Pokémon cannot be found, the directory creation fails,
        or an unexpected error occurs.
    """
    try:
        pokemon = get_pokemon_by_id(pokemon_id, session)
        folder_name = format_pokemon_folder_name(pokemon)

        data = await add_directory(name=folder_name)
        pokemon.image_directory = data["path"]

        pokemon_db.create_pokemon(pokemon, session)
        return PokemonResponse(
            status=status.HTTP_200_OK,
            detail="Created image directory succesfully",
            pokemon=pokemon,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def get_pokemon_directory(pokemon_id: int, session: SessionType):
    try:
        pokemon = get_pokemon_by_id(pokemon_id, session)
    except HTTPException as e:
        raise e

    if not pokemon.image_directory:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="The pokemon does not have a directory",
        )
    return PokemonResponsePaths(
        status=status.HTTP_200_OK,
        detail="Retrieved Pokemon Data",
        pokemon=pokemon,
        paths=[pokemon.image_directory],
    )


async def add_directory(
    name: str,
    create_dir: bool = True,
    include_base: bool = True,
):
    """
    Create a directory for storing Pokémon-related data.

    Args:
        name (str): Directory name or relative path to create.
        create_dir (bool, optional): If True, the directory is created if it does not exist.
                                     Defaults to True.
        include_base (bool, optional): If True, the path is joined with MonsterConfig.MONSTER_DIR
                                       as the root. Defaults to True.

    Returns:
        dict: A dictionary containing a detail message and the created directory path.

    Raises:
        HTTPException:
            - 400 if the resolved path escapes the base directory.
            - 404 if the directory does not exist and `create_dir` is False.
    """
    rel = Path(name)

    if include_base:
        base_dir = MonsterConfig.MONSTER_DIR
        if not base_dir.exists():
            if create_dir:
                base_dir.mkdir(parents=True, exist_ok=True)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Directory for images does not exist",
                )

        target_dir = (base_dir / rel).resolve()
        try:
            target_dir.relative_to(base_dir)
        except ValueError:
            raise HTTPException(status_code=400, detail="Path escapes base directory")
    else:
        target_dir = rel

    if not target_dir.exists():
        if create_dir:
            target_dir.mkdir(parents=True, exist_ok=True)
        else:
            raise HTTPException(
                status_code=404, detail="Image subdirectory does not exist"
            )
    return {"detail": f"Added folder {str(target_dir)}", "path": str(target_dir)}


async def add_required_folders_pokemon(
    pokemon_id: int,
    session: SessionType,
):
    """
    Create the required subdirectories for a given Pokémon.

    For each directory name in MonsterConfig.DATA_DIRS, this function builds
    a path using the Pokémon's folder name and ensures the directory exists.

    Args:
        pokemon_id (int): The unique identifier of the Pokémon.
        session (SessionType): Active database session.

    Returns:
        PokemonResponsePaths: A response object with status, detail message,
        the Pokémon object, and the list of created folder paths.

    Raises:
        HTTPException: If the Pokémon cannot be found or an error occurs during
        directory creation.
    """
    try:
        pokemon = get_pokemon_by_id(pokemon_id, session)
        paths = MonsterConfig.DATA_DIRS
        tasks = [
            add_directory(
                name=f"{format_pokemon_folder_name(pokemon)}/{p}",
            )
            for p in paths
        ]
        # Just returns the pokemon as a list
        results = await asyncio.gather(*tasks)
        return PokemonResponsePaths(
            status=status.HTTP_200_OK,
            detail=f"Added folders okay",
            pokemon=pokemon,
            paths=results,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=(str(e))
        )


async def write_pokemon_data(
    pokemon_id: int,
    pokemon_data: BaseModel | dict[str, Any] | Mapping[str, Any],
    session: SessionType,
    data_type: Literal["base_data", "description", "animation"] = "base_data",
    animation_dir: Optional[str] = None,
):
    """
    Persist Pokémon base data (or description) to the per-Pokémon data folder.

    - Resolves the Pokémon’s data directory via `get_pokemon_directory`.
    - Chooses the target filename from `MonsterConfig.FILES[data_type]`.
    - Serializes `pokemon_data` to JSON deterministically.
    - Ensures parent directories exist and writes atomically.

    Raises:
        HTTPException 404: If the Pokémon directory cannot be resolved.
        HTTPException 400: If `data_type` is invalid.
        HTTPException 500: On serialization or write failures.
    """
    try:
        # Resolve the base folder (first path returned)
        dir_resp = await get_pokemon_directory(pokemon_id=pokemon_id, session=session)
        if not dir_resp or not getattr(dir_resp, "paths", None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pokémon data directory not found",
            )

        pokemon_dir = Path(dir_resp.paths[0])

        # Validate data_type and compute target path
        try:
            if data_type != "animation":
                filename = MonsterConfig.FILES[data_type]
                file_path = pokemon_dir / "data" / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)

            elif data_type == "animation":
                assert animation_dir
                file_path = pokemon_dir / "animations" / f"{str(animation_dir)}.json"
                file_path.parent.mkdir(parents=True, exist_ok=True)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid data_type '{data_type}'. Expected one of {list(MonsterConfig.FILES.keys())}.",
            )

        # Serialize content to JSON (consistent & readable)
        if isinstance(pokemon_data, BaseModel):
            payload = pokemon_data.model_dump(exclude_none=True)  # pydantic v2
        else:
            # Accept dict-like/user-provided data; ensure JSON serializable
            payload = pokemon_data

        try:
            json_text = json.dumps(payload, ensure_ascii=False, indent=2)
        except TypeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Data is not JSON serializable: {e}",
            )

        # Atomic write to avoid partial files on crash
        def _atomic_write(target: Path, text: str):
            tmp = target.with_suffix(target.suffix + ".tmp")
            tmp.write_text(text, encoding="utf-8", newline="\n")
            tmp.replace(target)

        await to_thread.run_sync(_atomic_write, file_path, json_text)

        return PokemonResponsePaths(
            status=status.HTTP_200_OK,
            detail="Saved base data",
            pokemon=get_pokemon_by_id(pokemon_id, session),
            paths=[str(file_path)],
        )

    except HTTPException:
        # Bubble up intentional HTTP errors
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def get_pokemon_file(
    pokemon_id: int,
    folder: Literal["animations", "base", "data"],  # ✅ fixed Literal
    filename: str,
    session: SessionType,
):
    """
    Retrieve the contents of a specific file within a Pokémon's data directory.

    Args:
        pokemon_id (int): ID of the Pokémon.
        folder (Literal): One of the configured subfolders from MonsterConfig.DATA_DIRS.
        filename (str): Name of the file to retrieve.
        session (SessionType): Active database session.

    Returns:
        dict: A dictionary containing the file content as a UTF-8 string.

    Raises:
        HTTPException 204: If the file does not exist.
        HTTPException 500: On unexpected errors (e.g., read failure).
    """
    try:
        # Resolve the Pokémon’s base directory
        response = await get_pokemon_directory(pokemon_id=pokemon_id, session=session)
        pokemon_dir = Path(response.paths[0]).resolve()

        # Build target file path
        file_path = (pokemon_dir / folder / filename).resolve()

        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED, detail="No Content"
            )

        return {"content": file_path.read_text(encoding="utf-8")}

    except HTTPException:
        # Pass through HTTP errors unchanged
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def add_pokemon_image(
    pokemon_id: int,
    option: Literal["base", "animations"],
    session: SessionType,
    file: UploadFile | None = None,
):
    try:
        response = await get_pokemon_directory(pokemon_id, session=session)
        base_dir = response.paths[0]
        image_path = Path(base_dir) / option / file.filename  # type: ignore
        if file:
            with image_path.open("wb") as buffer:
                buffer.write(file.file.read())
        else:
            # Just touch the file if no content passed
            image_path.touch()
        return PokemonResponsePaths(
            status=200,
            detail=f"Added image, {image_path}",
            pokemon=get_pokemon_by_id(pokemon_id, session),
            paths=[image_path],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save image: {e}",
        )


async def get_all_pokemon_images(
    pokemon_id: int, option: Literal["base", "animations"], session: SessionType
):
    try:
        response = await get_pokemon_directory(pokemon_id, session=session)
        base_dir = response.paths[0]
        image_dir = Path(base_dir) / option

        if not image_dir.exists():
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED,
                detail=f"The Monster does not contain a directory called option {option}",
            )
        files = list(image_dir.glob("*.png"))
        if not files:
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED,
                detail=f"There are no images available for {option}",
            )
        return files
    except HTTPException as e:
        raise e
