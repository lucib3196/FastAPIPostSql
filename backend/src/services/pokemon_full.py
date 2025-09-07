# Standard library
import inspect
import json
import logging
from pathlib import Path

# Third-party
from fastapi import HTTPException
from openai import OpenAI
from starlette import status
import asyncio
from typing import cast

# Local application
from src.database.db import SessionType
from src.models import Pokemon, PokemonData, PokemonInput
from src.response_models import PokemonResponse
from src.services import pokemon_crud, pokemon_folder_service as svc, pokemon_generation
from src.services.pokemon_generation import (
    PokemonDescription,
    PokemonExpressionSet,
    PokemonMoveList,
)
from src.services.prompts import (
    pokemon_cute_animations,
    pokemon_description_prompt,
    pokemon_moveset_prompt,
)
from src.utils import write_image_data, normalize_input, normalize_name

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s :: %(message)s"
)
logger = logging.getLogger("pokemon.pipeline")  # configure handlers/level elsewhere

client = OpenAI()


async def run_sprite_tasks(sprite_tasks):
    import asyncio

    coros = [t["task"] for t in sprite_tasks]
    # return_exceptions=True so one failure doesn't cancel all
    results = await asyncio.gather(*coros, return_exceptions=True)

    completed = []
    for meta, res in zip(sprite_tasks, results):
        if isinstance(res, Exception):
            completed.append(
                {
                    "id": meta["id"],
                    "name": meta["name"],
                    "error": res,
                    "result": None,
                    "data": meta.get("data", {}),
                }
            )
        else:
            completed.append(
                {
                    "id": meta["id"],
                    "name": meta["name"],
                    "result": res,
                    "data": meta.get("data", {}),
                }
            )
    return completed


async def basic_pokemon_setup(
    pokemon: Pokemon, pokemon_data: PokemonInput, session: SessionType
):
    """
    Perform the initial setup for a new Pokémon entry.

    This function:
      1. Persists a new Pokémon object to the database.
      2. Validates and normalizes the provided input data.
      3. Creates the required directory structure for the Pokémon.
      4. Writes the base metadata (`base_data`) for the Pokémon.

    Args:
        pokemon (Pokemon): The Pokémon model instance to create.
        pokemon_data (PokemonInput): User-provided input data describing the Pokémon.
        session (SessionType): Active database session used for persistence.

    Returns:
        tuple[int, PokemonInput]:
            - The unique Pokémon ID created in the database.
            - The normalized Pokémon input data.

    Raises:
        HTTPException: If Pokémon creation fails (e.g., `pokemon.id` is None).
    """
    try:

        pokemon = pokemon_crud.create_pokemon(pokemon, session)
        logger.debug("Created pokemon object: id=%s", getattr(pokemon, "id", None))
        if pokemon.id is None:
            logger.error("Failed to create Pokémon: pokemon.id is None")
            raise HTTPException(status_code=500, detail="Failed to create Pokémon.")

        pokemon_id = pokemon.id
        logger.debug("Normalizing input for pokemon_id=%s", pokemon_id)
        pokemon_data = normalize_input(pokemon_data)

        logger.debug("Setting up directories for pokemon_id=%s", pokemon_id)

        # Set up directories
        await svc.set_pokemon_directory(pokemon_id, session)
        await svc.add_required_folders_pokemon(pokemon_id, session)

        logger.debug("Writing base_data for pokemon_id=%s", pokemon_id)
        await svc.write_pokemon_data(
            pokemon_id, pokemon_data, session, data_type="base_data"
        )
        logger.info("✅ Base data written for pokemon_id=%s", pokemon_id)
        return pokemon_id, pokemon_data
    except HTTPException as e:
        raise e


async def generate_enhance_description(
    pokemon_id, pokemon_data: PokemonData, session: SessionType
):
    logger.debug("Generating enhanced description for pokemon_id=%s", pokemon_id)
    desc_json = pokemon_generation.generate_pokemon_description(
        pokemon_data, description_prompt_template=pokemon_description_prompt
    )
    if not desc_json:
        logger.error(
            "Description generation returned empty/None for pokemon_id=%s",
            pokemon_id,
        )
        raise HTTPException(status_code=500, detail="Description generation failed.")
    logger.debug(
        "Description JSON length=%d",
        len(desc_json) if isinstance(desc_json, str) else -1,
    )

    desc = PokemonDescription.model_validate(json.loads(desc_json))
    logger.debug(
        "Validated PokemonDescription with keys: %s", list(desc.model_dump().keys())
    )

    better_description = PokemonData(
        name=pokemon_data.name,
        description=desc.description,
        physical_attr=desc.physical_attributes,
        ptype=pokemon_data.ptype,
        image_description=desc.image_description,
    )
    logger.debug("Writing improved description for pokemon_id=%s", pokemon_id)
    await svc.write_pokemon_data(
        pokemon_id, better_description, session, data_type="description"
    )
    logger.info("Improved description written for pokemon_id=%s", pokemon_id)
    return better_description


async def generate_base_image(
    pokemon_id: int, desc: PokemonData, user_data: PokemonInput, base_dir: str | Path
):
    # 4) Base image
    logger.debug("Generating base image for pokemon_id=%s", pokemon_id)
    base_img_resp, base_image_bytes = pokemon_generation.generate_pokemon_base_image(
        image_description=str(desc.image_description),
        better_description=desc.description,
        user_input=user_data,
    )
    logger.debug(
        "Base image generated: resp_type=%s, image_bytes=%s",
        type(base_img_resp).__name__,
        (len(base_image_bytes) if hasattr(base_image_bytes, "__len__") else "unknown"),
    )

    save_path = Path(base_dir) / "base"
    logger.debug("Saving base image to %s (filename=base)", save_path)
    save_r = write_image_data(base_image_bytes, save_path, filename="base")
    base_filepath = save_r["filepath"]
    logger.info("Base image saved: %s", base_filepath)
    return base_img_resp, base_filepath


async def generate_expressive_moveset(
    pokemon_id: int, description, reference_image_path: str | Path
) -> PokemonExpressionSet:
    logger.debug("Generating cute moveset for pokemon_id=%s", pokemon_id)
    cute_moves_json = pokemon_generation.generate_cute_moveset(
        data=description,
        cute_prompt_template=pokemon_cute_animations,
        image_path=str(reference_image_path),
    )
    if not cute_moves_json:
        logger.error(
            "Moveset generation returned empty/None for pokemon_id=%s", pokemon_id
        )
        raise HTTPException(status_code=500, detail="Moveset generation failed.")
    logger.debug(
        "Moveset JSON length=%d",
        len(cute_moves_json) if isinstance(cute_moves_json, str) else -1,
    )

    cute_moves_data: PokemonExpressionSet = PokemonExpressionSet.model_validate(
        json.loads(cute_moves_json)
    )
    logger.info(
        " Parsed moveset: %d moves", len(getattr(cute_moves_data, "move_list", []))
    )
    return cute_moves_data


async def generate_moveset(
    pokemon_id: int, description, reference_image_path: str | Path
) -> PokemonMoveList:
    logger.debug("Generating  moveset for pokemon_id=%s", pokemon_id)
    moves_json = pokemon_generation.generate_moveset(
        data=description,
        moveset_prompt_template=pokemon_moveset_prompt,
        image_path=str(reference_image_path),
    )
    if not moves_json:
        logger.error(
            "Moveset generation returned empty/None for pokemon_id=%s", pokemon_id
        )
        raise HTTPException(status_code=500, detail="Moveset generation failed.")
    logger.debug(
        "Moveset JSON length=%d",
        len(moves_json) if isinstance(moves_json, str) else -1,
    )

    moves_data: PokemonMoveList = PokemonMoveList.model_validate(json.loads(moves_json))
    logger.info(" Parsed moveset: %d moves", len(getattr(moves_data, "move_list", [])))
    return moves_data


async def parse_moveset(moveset: PokemonMoveList, prev_response):
    sprite_tasks = []
    for i, move in enumerate(moveset.move_list, start=1):
        sprite_description = move.to_string  # property
        logger.debug("Queueing sprite task %d: name=%s", i, getattr(move, "name", None))
        # NOTE: pass the base_img_resp as you intended
        task = pokemon_generation.fwp_image_generation_sprite(
            prev_response,
            sprite_description,
        )
        sprite_tasks.append(
            {
                "id": f"move_{i}",
                "name": normalize_name(move.name),
                "task": task,
                "data": move.model_dump(),  # keep original move meta
            }
        )
        last = sprite_tasks[-1]
        logger.debug(
            "Queued sprite task: id=%s name=%s task_type=%s awaitable=%s "
            "base_img_resp_type=%s sprite_desc_len=%s",
            last["id"],
            last["name"],
            type(last["task"]).__name__,
            inspect.isawaitable(last["task"]),
            type(prev_response).__name__,
            (len(sprite_description) if isinstance(sprite_description, str) else "n/a"),
        )
    return sprite_tasks


async def parse_expression(expressive: PokemonExpressionSet, prev_response):
    sprite_tasks = []
    for i, move in enumerate(expressive.expressions, start=1):
        logger.debug("Queueing sprite task %d: name=%s", i, getattr(move, "name", None))
        sprite_description = move.to_string
        task = pokemon_generation.fwp_image_generation_sprite(
            prev_response,
            sprite_description,
        )
        sprite_tasks.append(
            {
                "id": f"expression_{i}",
                "name": normalize_name(move.name),
                "task": task,
                "data": move.model_dump(),  # keep original expression meta
            }
        )
        last = sprite_tasks[-1]
        logger.debug(
            "Queued sprite task: id=%s name=%s task_type=%s awaitable=%s "
            "base_img_resp_type=%s sprite_desc_len=%s",
            last["id"],
            last["name"],
            type(last["task"]).__name__,
            inspect.isawaitable(last["task"]),
            type(prev_response).__name__,
            (len(sprite_description) if isinstance(sprite_description, str) else "n/a"),
        )
    return sprite_tasks


async def parse_generic(prev_response):
    logger.debug("Queueing generic fallback sprite task")
    sprite_tasks = []
    sprite_tasks.append(
        {
            "id": "generic",
            "name": normalize_name("generic"),
            "task": pokemon_generation.fwp_image_generation_sprite(
                prev_response,
                (
                    "Generate a default 3/4-view walking animation sprite of the character in GBA pixel art style. "
                    "Keep proportions simple, use a clear silhouette, strong outlines, and high-contrast shading. "
                    "This sprite should serve as a neutral fallback animation usable for any case."
                ),
            ),
            "data": {},  # so downstream access is safe
        }
    )
    last = sprite_tasks[-1]
    logger.debug(
        "Queued GENERIC sprite task: id=%s name=%s task_type=%s awaitable=%s base_img_resp_type=%s",
        last["id"],
        last["name"],
        type(last["task"]).__name__,
        inspect.isawaitable(last["task"]),
        type(prev_response).__name__,
    )
    logger.info("🧵 Total sprite tasks queued: %d", len(sprite_tasks))
    return sprite_tasks


async def write_sprite_to_data(
    pokemon_id: int, base_dir: str | Path, session: SessionType, sprite
):
    if sprite.get("error"):
        logger.exception(
            "Sprite generation failed for id=%s name=%s error=%s",
            sprite.get("id"),
            sprite.get("name"),
            sprite["error"],
        )
        return

    sprite_id = sprite["id"]
    sprite_name = sprite["name"]
    move_meta = sprite["data"]
    result = sprite["result"]

    logger.debug(
        "Persisting sprite id=%s name=%s; result_type=%s",
        sprite_id,
        sprite_name,
        type(result).__name__,
    )

    # Support both tuple (resp, bytes) and raw bytes
    if isinstance(result, tuple) and len(result) == 2:
        _, image_bytes = result
        logger.debug(
            "Result provided as tuple; extracted image_bytes len=%s",
            (len(image_bytes) if hasattr(image_bytes, "__len__") else "unknown"),
        )
    else:
        image_bytes = result  # assume bytes-like
        logger.debug(
            "Result provided as bytes-like; len=%s",
            (len(image_bytes) if hasattr(image_bytes, "__len__") else "unknown"),
        )

    # Save the moveset/animation metadata
    logger.debug("Writing animation metadata for %s (dir=%s)", sprite_name, sprite_name)
    await svc.write_pokemon_data(
        pokemon_id,
        move_meta,
        session,
        data_type="animation",
        animation_dir=sprite_name,
    )
    logger.info("Animation metadata written for %s", sprite_name)

    # Save the sprite image
    anim_dir = Path(base_dir) / "animations"
    logger.debug("Saving sprite image to %s (filename=%s)", anim_dir, sprite_name)
    write_image_data(image_bytes, anim_dir, filename=sprite_name)
    logger.info("Sprite image saved for %s", sprite_name)


async def create_pokemon_complete(
    pokemon: Pokemon, pokemon_data: PokemonInput, session: SessionType
):
    try:
        logger.info(
            "Starting create_pokemon_complete for name=%s",
            getattr(pokemon_data, "name", None),
        )

        # 1) Initial setup (DB write is short)
        pokemon_id, pokemon_data = await basic_pokemon_setup(
            pokemon, pokemon_data, session
        )

        # 2) Enhanced description (no DB held open)
        better_description = await generate_enhance_description(
            pokemon_id, pokemon_data, session
        )

        # 3) Paths
        logger.debug("Fetching directory info for pokemon_id=%s", pokemon_id)
        dir_info = await svc.get_pokemon_directory(pokemon_id, session)
        if not getattr(dir_info, "paths", None):
            logger.error("No directory paths for pokemon_id=%s", pokemon_id)
            raise HTTPException(status_code=500, detail="Directory setup failed.")
        base_dir = Path(dir_info.paths[0])
        logger.info("Base directory set to: %s", base_dir)

        # 4) Base image (no DB held open)
        base_img_resp, base_filepath = await generate_base_image(
            pokemon_id, better_description, pokemon_data, base_dir
        )

        # 5) Moveset + expressive set (run concurrently)
        gen_tasks = [
            generate_moveset(pokemon_id, better_description, base_filepath),
            generate_expressive_moveset(pokemon_id, better_description, base_filepath),
        ]
        moveset_raw, expressive_raw = await asyncio.gather(*gen_tasks)

        # Proper typing for editors/type checkers
        moveset = cast(PokemonMoveList, moveset_raw)
        expressive_moveset = cast(PokemonExpressionSet, expressive_raw)

        # 6) Parse to sprite jobs (run concurrently; tolerate partial failures)
        parse_tasks = [
            parse_moveset(moveset=moveset, prev_response=base_img_resp),
            parse_expression(
                expressive=expressive_moveset, prev_response=base_img_resp
            ),
        ]
        parse_results = await asyncio.gather(*parse_tasks, return_exceptions=True)

        sprite_tasks: list = []
        for i, r in enumerate(parse_results):
            if isinstance(r, Exception):
                logger.exception("Parse task %d failed: %s", i, r)
                continue
            if not isinstance(r, list):
                logger.exception("Parse task %d failed: %s", i, r)
            sprite_tasks.extend(r)  # type: ignore

        if not sprite_tasks:
            logger.warning("No sprite tasks generated for pokemon_id=%s", pokemon_id)

        # 7) Run sprite tasks (consider internal throttling/semaphore)
        logger.debug("Running %d sprite tasks concurrently…", len(sprite_tasks))
        completed_sprites = await run_sprite_tasks(sprite_tasks)

        errors = sum(
            1 for s in completed_sprites if isinstance(s, dict) and s.get("error")
        )
        logger.info(
            "Sprite tasks completed: %d (errors=%d)", len(completed_sprites), errors
        )

        # 8) Persist sprites (short DB writes; tolerate partial failures)
        write_tasks = [
            write_sprite_to_data(pokemon_id, base_dir, session, sprite)
            for sprite in completed_sprites
        ]
        write_results = await asyncio.gather(*write_tasks, return_exceptions=True)
        write_errors = [e for e in write_results if isinstance(e, Exception)]
        if write_errors:
            for e in write_errors:
                logger.exception("Sprite persist error: %s", e)
            # Do not fail whole request for partial persist errors; adjust policy if needed.

        # 9) Final response (fetch latest from DB)
        logger.info("Pokemon creation complete for id=%s", pokemon_id)
        created = pokemon_crud.get_pokemon_by_id(pokemon_id, session)  # type: ignore
        return PokemonResponse(
            status=status.HTTP_200_OK,
            detail="Pokemon Created Successfully",
            pokemon=created,
        )

    except HTTPException:
        logger.exception("HTTPException during create_pokemon_complete")
        raise
    except Exception as e:
        logger.exception("Unhandled exception during create_pokemon_complete: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error while creating Pokémon.",  # keep generic
        )
