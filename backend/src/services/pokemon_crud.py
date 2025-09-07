from src.models import Pokemon
from src.database.db import SessionType
from fastapi import HTTPException
from src.database import pokemon as pokemon_db
from starlette import status


def create_pokemon(pokemon: Pokemon, session: SessionType):
    return pokemon_db.create_pokemon(pokemon, session)


def get_pokemon_by_id(pokemon_id: int, session: SessionType) -> Pokemon:
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(detail="Not Found", status_code=404)
    return pokemon


def delete_pokemon(pokemon_id: int, session: SessionType):
    try:
        pokemon = get_pokemon_by_id(pokemon_id, session)
    except HTTPException as e:
        raise e
    session.delete(pokemon)
    session.commit()
    return {"ok": True}


def get_all_pokemon(session: SessionType):
    try:
        results = pokemon_db.get_all_pokemon(session)
        if results is None or []:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, detail="No Monsters Available"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=(str(e))
        )


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
