from openai import OpenAI
import base64
from dotenv import load_dotenv
from pathlib import Path
from typing import Any, Dict
from fastapi import HTTPException

load_dotenv()
client = OpenAI()


async def generate_image(
    prompt: str, filename: str, folder_path: str
) -> Dict[str, Any]:
    try:
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

        if image_data:
            image_base64 = image_data[0]
            save_path = Path(folder_path) / f"{filename}.png"
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(image_base64))  # type: ignore
            return {"status": "ok", "filepath": save_path}
        else:
            raise HTTPException(status_code=500, detail="Could not generate image")
    except Exception as e:
        raise e
