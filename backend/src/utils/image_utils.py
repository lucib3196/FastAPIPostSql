# Standard library
import base64
from pathlib import Path

# Third-party
from fastapi import HTTPException

# Local application


def write_image_data(image_data, folder_path, filename):
    try:
        fpath = Path(folder_path)
        if not fpath.exists:
            fpath.mkdir()
        image_base64 = image_data[0]
        save_path = fpath / f"{filename}.png"
        with open(save_path, "wb") as f:
            f.write(base64.b64decode(image_base64))
        return {"status": "ok", "filepath": save_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save image {str(e)}")
