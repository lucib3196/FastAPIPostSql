from pydantic import BaseModel
from typing import List, Optional
from .prompts import *
from src.services.ai_services import client, multimodal_generation, generate_image
from src.utils.pokemon_utils import normalize_input, format_prompt
from src.models import PokemonInput, PokemonData  # ← import the ONE copy
from typing import Literal
from openai import AsyncOpenAI
from dotenv import load_dotenv
import base64

load_dotenv()
async_client = AsyncOpenAI()


class PokemonDescription(BaseModel):
    name: str
    description: str
    physical_attributes: str
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


class PokemonMove(BaseModel):
    name: str
    attack_type: str
    move_type: Literal["attack", "defence"]
    category: Literal["physical", "special"]
    description: str
    sprite_animation: str

    @property
    def to_string(self) -> str:
        return (
            f"Move Name: {self.name}\n"
            f"Type: {self.attack_type}\n"
            f"Move Type: {self.move_type.capitalize()}\n"
            f"Category: {self.category.capitalize()}\n"
            f"Description: {self.description}"
            f"Sprite Animation: {self.sprite_animation}"
        )


class PokemonMoveList(BaseModel):
    move_list: List[PokemonMove]


class PokemonExpression(BaseModel):
    """Defines a playful or personality-based animation/expression for a Pokémon."""

    name: str  # e.g., "Happy Hop", "Sleepy Wiggle", "Sassy Pose"
    mood: Literal["happy", "silly", "sleepy", "curious", "angry", "proud"]
    style: Literal["idle", "dance", "pose", "reaction", "quirk"]
    description: str  # what the animation looks like
    sprite_hint: str | None = (
        None  # optional extra hint for sprite design (e.g. "tail wagging")
    )
    sprite_animation: str

    @property
    def to_string(self) -> str:
        return (
            f"Expression: {self.name}\n"
            f"Mood: {self.mood.capitalize()}\n"
            f"Style: {self.style.capitalize()}\n"
            f"Description: {self.description}\n"
            f"Sprite Hint: {self.sprite_hint or 'N/A'}"
            f"Sprite Animation: {self.sprite_animation}"
        )


class PokemonExpressionSet(BaseModel):
    expressions: List[PokemonExpression]


def generate_moveset(
    data: PokemonInput,
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
            response_model=PokemonExpressionSet,
        )
    else:
        completion = client.chat.completions.parse(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            response_format=PokemonExpressionSet,
        )
        return completion.choices[0].message.content


def generate_pokemon_base_image(
    image_description: str, better_description: str, user_input: PokemonInput
):
    # format the first part of the prompt
    d = normalize_input(user_input)
    prompt = pokemon_image_generation_prompt.format(
        name=d.name,
        new_description=better_description,
        image_description=image_description,
        ptype=d.ptype,
    )
    return generate_image(prompt, transparent=False)


async def fwp_image_generation(response, prompt, transparent: bool = False):
    result = await async_client.images.edit(
        model="gpt-image-1",
        image=[open(response, "rb")],
        prompt=prompt,
        background="opaque",
        size="1024x1024",
        quality="high",
    )
    if not result or not result.data:
        raise ValueError("Image generation failed, no data returned.")
    image_base64 = result.data[0].b64_json
    if not image_base64:
        raise ValueError("Image generation failed, no data returned.")

    # response_fwup = await async_client.responses.create(
    #     model="gpt-5",
    #     previous_response_id=response.id,
    #     input=prompt,
    #     tools=[
    #         {
    #             "type": "image_generation",
    #             "background": "transparent" if transparent else "opaque",
    #             "size": "1024x1024",
    #             "quality": "high",
    #         }
    #     ],
    # )
    # image_data = [
    #     output.result
    #     for output in response_fwup.output
    #     if output.type == "image_generation_call"
    # ]
    return (result, [image_base64])


async def fwp_image_generation_sprite(response, animation: str, transparent=False):
    prompt = pokemon_sprite_base.format(animation=animation)
    return await fwp_image_generation(response, prompt, transparent=transparent)


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
