# Standard library
import base64
from pathlib import Path

# Third-party
from fastapi import HTTPException

# Local application
import base64
from fastapi import HTTPException


def extract_base64(image_data) -> bytes:
    """
    Extract and normalize base64 content from various image_data shapes.

    Accepts:
      - list/tuple where first element is str/bytes/dict/object with 'b64_json'
      - dict with 'b64_json' or 'image_base64'
      - plain str/bytes/bytearray

    Returns:
      Decoded raw bytes.

    Raises:
      HTTPException(500) if base64 is missing or cannot be decoded.
    """
    b64_val = None

    if isinstance(image_data, (list, tuple)) and image_data:
        first = image_data[0]
        if isinstance(first, (str, bytes, bytearray)):
            b64_val = first
        elif isinstance(first, dict):
            b64_val = first.get("b64_json") or first.get("image_base64")
        else:
            b64_val = getattr(first, "b64_json", None)

    elif isinstance(image_data, dict):
        b64_val = image_data.get("b64_json") or image_data.get("image_base64")

    elif isinstance(image_data, (str, bytes, bytearray)):
        b64_val = image_data

    if b64_val is None:
        raise HTTPException(status_code=500, detail="Missing base64 image data")

    # Normalize to bytes
    if isinstance(b64_val, str):
        try:
            b64_bytes = b64_val.encode("ascii")
        except Exception:
            b64_bytes = b64_val.encode("utf-8")
    elif isinstance(b64_val, (bytes, bytearray)):
        b64_bytes = bytes(b64_val)
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected type for base64 data: {type(b64_val).__name__}",
        )

    try:
        return base64.b64decode(b64_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Base64 decode failed: {e}")


def write_image_data(image_data, folder_path, filename):
    try:
        fpath = Path(folder_path)
        if not fpath.exists():
            fpath.mkdir(parents=True, exist_ok=True)

        image_base64 = image_data[0]
        save_path = fpath / f"{filename}.png"

        with open(save_path, "wb") as f:
            f.write(base64.b64decode(image_base64))

        return {"status": "ok", "filepath": save_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save image {str(e)}")
