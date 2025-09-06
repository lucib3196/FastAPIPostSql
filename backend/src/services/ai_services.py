from openai import OpenAI
from dotenv import load_dotenv
from .prompts import *
import base64
from src.models import *

load_dotenv()
client = OpenAI()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def generate_image(prompt: str):
    response = client.responses.create(
        model="gpt-5",
        input=prompt,
        tools=[{"type": "image_generation"}],
    )

    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]
    return image_data


def multimodal_generation(prompt: str, image_path: str, response_model):
    completion = client.chat.completions.parse(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(image_path)}",
                        },
                    },
                ],
            }
        ],
        response_format=response_model,
    )
    return completion.choices[0].message.content
