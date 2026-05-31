from pathlib import Path


def iter_files_recursively(root: Path, pattern: str):
    yield from (p for p in root.rglob(pattern) if p.is_file())
