import re
from pathlib import Path


def count(path: Path, text: str) -> dict[str, int]:
    print(f"count: {path}")

    result = dict()

    result["abc"] = 1
    result["def"] = 2

    return result
