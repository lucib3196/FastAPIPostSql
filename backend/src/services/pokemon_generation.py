from pydantic import BaseModel
from typing import List, Optional
from .prompts import *
from src.services.ai_services import client, multimodal_generation
from src.services.pokemon_utils import normalize_input, format_prompt
from src.models import PokemonInput, PokemonData  # ← import the ONE copy


class PokemonDescription(BaseModel):
    name: str
    description: str
    image_description: str


def generate_pokemon_description(
    data: PokemonInput,
    *,
    description_prompt_template: str,
):
    d = normalize_input(data)
    prompt = format_prompt(description_prompt_template, d)

    completion = client.chat.completions.parse(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        response_format=PokemonDescription,
    )
    return completion.choices[0].message.content


class PokemonMoveList(BaseModel):
    move_list: List[str]


def generate_moveset(
    data: PokemonInput,
    *,
    moveset_prompt_template: str,
    image_path: Optional[str] = None,
):
    """
    Battle-oriented moveset (4 moves, with power/accuracy/etc if your template asks for them).
    If image_path is provided, uses your multimodal endpoint; otherwise, falls back to text.
    """
    d = normalize_input(data)
    prompt = format_prompt(moveset_prompt_template, d)

    if image_path:
        return multimodal_generation(
            prompt=prompt,
            image_path=image_path,
            response_model=PokemonMoveList,
        )
    else:
        # text-only fallback (if you have a text completion route)
        completion = client.chat.completions.parse(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            response_format=PokemonMoveList,
        )
        return completion.choices[0].message.content


def generate_cute_moveset(
    data: PokemonInput,
    *,
    cute_prompt_template: str,
    image_path: Optional[str] = None,
):
    """
    Personality/cute-focused moves (no battle stats), same union input pattern as generate_moveset.
    """
    d = normalize_input(data)
    prompt = format_prompt(cute_prompt_template, d)

    if image_path:
        return multimodal_generation(
            prompt=prompt,
            image_path=image_path,
            response_model=PokemonMoveList,
        )
    else:
        completion = client.chat.completions.parse(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            response_format=PokemonMoveList,
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    data_dict = {
        "name": "Tsunamidon",
        "description": "A massive armored blue triceratops Water-type",
        "physical_attr": "Tidal frill, triple horns, heavy plating",
        "ptype": "Water/Steel",
    }
    print(data_dict)

    # Or use the model directly:
    data_model = PokemonData(**data_dict)

    # Description
    desc = generate_pokemon_description(
        data_model,
        description_prompt_template=pokemon_description_prompt,
    )

    # Battle moveset
    battle_moves = generate_moveset(
        data_model,
        moveset_prompt_template=pokemon_moveset_prompt,
        image_path=r"backend\src\images\monsters\Aquaceratops_2\base\Aquaceratops.png",  # optional
    )

    # Cute/personality moves
    cute_moves = generate_cute_moveset(
        data_dict,  # dict works too
        cute_prompt_template=pokemon_cute_animations,
        image_path=None,
    )

    print(desc)
    print(battle_moves)
    print(cute_moves)
