from pathlib import Path
from collections import Counter
from typing import Callable

from ..tools import iter_files_recursively


def print_result(total: dict[str, int], header: str | None = None):
    if header is not None:
        print(header)
    for key, value in sorted(total.items(), key=lambda x: (x[1], x[0])):
        print(f"{value:5d}  {key}")


def report_count(
    path: Path, header: str | None, count_func: Callable[[Path], dict[str, int]]
):
    if not path.exists():
        raise typer.BadParameter(f"{path}は存在しません")

    if path.is_file():
        data = count_func(path)
        print_result(date, header)
        return

    if path.is_dir():
        total = Counter()
        for file in iter_files_recursively(path, "*.ledger"):
            data = count_func(file)
            total.update(data)
        print_result(total, header)
        return

    raise typer.BadParameter(f"{path} はファイルでもディレクトリでもありません")
