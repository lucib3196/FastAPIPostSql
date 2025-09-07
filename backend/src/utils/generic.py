import re

def normalize_name(name: str) -> str:
    """
    Normalize a move name into a lowercase, underscore-separated string.
    Removes non-alphanumeric characters for safe identifiers.
    """
    # Lowercase and strip leading/trailing spaces
    name = name.strip().lower()
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    # Remove any characters that are not letters, numbers, or underscores
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name