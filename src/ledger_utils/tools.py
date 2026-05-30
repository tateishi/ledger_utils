from pathlib import Path


def iter_files_recursively(root: Path, pattern: str):
    yield from (p for p in root.rglob(pattern) if p.is_file())


def print_result(total: dict[str, int], header: str | None = None):
    if header is not None:
        print(header)
    for key, value in sorted(total.items(), key=lambda x: (x[1], x[0])):
        print(f"{value:5d}  {key}")
