import pytest
from pathlib import Path
from src.core.pokemon_config import MonsterConfig


def test_monster_dir_exist():
    assert MonsterConfig.BASE_DIR.is_absolute()
    assert isinstance(MonsterConfig.BASE_DIR, Path)


def test_data_dirs_are_paths():
    # Make sure all DATA_DIRS values are Path objects
    for key, path in MonsterConfig.DATA_DIRS.items():
        assert isinstance(path, Path), f"{key} should be a Path"


def test_get_data_file_returns_path():
    path = MonsterConfig.get_data_file("user")
    assert isinstance(path, Path)
    assert path.name == MonsterConfig.FILES["user"]


def test_get_data_file_returns_path_2():
    path = MonsterConfig.get_data_file("description")
    assert isinstance(path, Path)
    assert path.name == MonsterConfig.FILES["description"]
