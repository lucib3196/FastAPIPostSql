from src.models import Pokemon, ImageDir
from src.db import SessionType
from src.services.pokemon_image_generation import generate_image
from fastapi import Depends
from src.db import get_session
from fastapi import HTTPException
from pathlib import Path
from starlette import status
import asyncio
import json

base_dir = Path("backend/src/images/monsters")
if not base_dir.exists:
    base_dir.mkdir()
paths = ["animations", "base", "user_data"]


def add_pokemon(pokemon: Pokemon, session: SessionType) -> Pokemon:
    session.add(pokemon)
    session.commit()
    session.refresh(pokemon)
    return pokemon


def get_pokemon_by_id(pokemon_id: int, session: SessionType) -> Pokemon:
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(detail="Not Found", status_code=404)
    return pokemon


async def add_pokemon_image_directory(
    pokemon_id: int, image_dir: str, session: SessionType, create_dir: bool = True
) -> Pokemon:
    try:
        pokemon = get_pokemon_by_id(pokemon_id, session)
    except HTTPException as e:
        raise e

    dir_path = base_dir / Path(image_dir).resolve()
    if not dir_path.exists():
        if create_dir:
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Directory for images does not exist",
            )
    pokemon.image_directory = image_dir
    pokemon = add_pokemon(pokemon, session)
    return pokemon


async def add_required_folders_pokemon(
    pokemon_id: int,
    session: SessionType,
    paths: list[str] = paths,
    create_dir: bool = True,
):
    try:

        tasks = [
            add_pokemon_image_directory(pokemon_id, p, session, create_dir)
            for p in paths
        ]
        # Just returns the pokemon as a list
        results = asyncio.gather(*tasks)

        return {"data": "okay"}
    except Exception as e:
        raise e


async def store_pokemon_base_data(
    pokemon_id: int,
    name: str,
    description: str,
    physical_attr: str,
    ptype: str,
    session: SessionType,
):
    try:
        pokemon_dir = get_pokemon_image_directory(
            pokemon_id=pokemon_id, session=session
        )
    except HTTPException as e:
        raise e

    try:
        base_data_path = (Path(pokemon_dir) / "user_data" / "data_user.json").resolve()
        base_data_path.parent.mkdir(parents=True, exist_ok=True)  # ensure dir exists

        data = {
            "name": name,
            "description": description,
            "physical_attr": physical_attr,
            "ptype": ptype,
        }

        # sync write (fine for small JSON)
        base_data_path.write_text(json.dumps(data, indent=2))

        return {"status": "ok", "data": str(base_data_path)}
    except Exception as e:
        raise HTTPException(
            detail=f"Could not save user data: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def get_pokemon_file(pokemon_id: int, filename: str, session: SessionType):
    try:
        pokemon_dir = get_pokemon_image_directory(
            pokemon_id=pokemon_id, session=session
        )
    except HTTPException as e:
        raise e

    try:
        base_data_path = Path(Path(pokemon_dir) / filename).resolve()
        print(base_data_path)
        if not base_data_path.exists():
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, detail="No Content"
            )
        content = base_data_path.read_text(encoding="utf-8")
        return {"content": content}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def get_pokemon_base_data(
    pokemon_id: int, session: SessionType, filename: str = "user_data/data_user.json"
):
    try:
        return await get_pokemon_file(pokemon_id, filename, session)
    except HTTPException as e:
        raise e


def get_pokemon_image_directory(pokemon_id: int, session: SessionType):
    try:
        pokemon = get_pokemon_by_id(pokemon_id, session)
    except HTTPException as e:
        raise e

    if not pokemon.image_directory:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="The pokemon does not have any images",
        )
    return pokemon.image_directory


def get_all_pokemon_images(pokemon_id: int, option: ImageDir, session: SessionType):
    base_dir = get_pokemon_image_directory(pokemon_id, session=session)
    image_dir = Path(base_dir) / option

    if not image_dir.exists():
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The Monster does not contain a directory called option {option}",
        )
    files = list(image_dir.glob("*.png"))
    if not files:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"There are no images available for {option}",
        )
    return files


async def generate_pokemon_image(
    name: str, description: str, physical_attr: str, ptype: str, session: SessionType
):
    prompt = """A Pokémon in the style of the 1990s Pokémon Game Boy games mixed with the classic 90s anime art style. 
    Bold black outlines, flat colors, pixelated shading, limited retro Game Boy color palette, nostalgic vibe. 
    Looks like official Pokémon Red/Blue/Yellow art combined with 90s Saturday morning cartoon anime aesthetics. 
    Retro cel-shaded textures, slightly grainy background that resembles old cartridges and anime cels. 
    Dynamic but simple pose, clear silhouette, authentic to 1990s Pokémon designs. 
    Make sure the design strongly reflects the given description and type while keeping the look faithful to the 90s era.
    When generating the image ensure that it is just the pokemon do not include any text"""

    pokemon_description = f"""
    Here is a description of the Pokémon given from the user. 
    Expand on their ideas but keep the general essence of what they want. 
    Make sure the result looks like an authentic 1990s Pokémon design.

    Name: {name}
    Core Concept: {description}
    Physical Attributes: {physical_attr}
    Pokémon Type: {ptype}
    """

    # final_prompt = prompt + pokemon_description
    # # Create the pokemon first
    # pokemon = add_pokemon(Pokemon(name=name), session=session)
    # result = await generate_image(
    #     prompt=final_prompt, filename=f"{pokemon.name}_{pokemon.id}"
    # )
    # return {"ok": True, "pokemon": pokemon, "save_path": result.get("save_path")}
