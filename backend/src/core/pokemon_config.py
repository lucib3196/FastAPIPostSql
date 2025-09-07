from pathlib import Path
from enum import Enum


class ImageDir(str, Enum):
    animations = "animations"
    base = "base"


class MonsterConfig:
    """Central config for Monster data and asset storage."""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    MONSTER_DIR = (BASE_DIR / "src" / "images" / "monsters").resolve()

    DATA_DIRS = ["animations", "data", "base"]


    FILES = {
        "base_data": "data_user.json",  # stores raw form data
        "description": "monster_data.json",  # stores cleaned description
    }
