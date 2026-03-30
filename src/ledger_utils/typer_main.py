from collections import Counter
from pathlib import Path

import typer

from ledger_utils.count import payee_count
from ledger_utils.count import account_count

app = typer.Typer()


def iter_files_recursively(root: Path, pattern: str):
    yield from (p for p in root.rglob(pattern) if p.is_file())


def print_result(total: dict[str, int], header: str | None = None):
    if header is not None:
        print(header)
    for key, value in sorted(total.items(), key=lambda x: (x[1], x[0])):
        print(f"{value:5d}  {key}")


@app.command()
def hello():
    print("hello world")


@app.command()
def count_payee(path: Path):
    header = "count  payee"

    if not path.exists():
        raise typer.BadParameter(f"{path}は存在しません")

    if path.is_file():
        data = payee_count(path)

        print_result(data, header)

        return

    if path.is_dir():
        total = Counter()

        for file in iter_files_recursively(path, "*.ledger"):
            data = payee_count(file)
            total.update(data)

        print_result(total, header)

        return

    raise typer.BadParameter(f"{path} はファイルでもディレクトリでもありません")


@app.command()
def count_account(path: Path):
    header = "count  account"

    if not path.exists():
        raise typer.BadParameter(f"{path}は存在しません")

    if path.is_file():
        data = account_count(path)

        print_result(data, header)

        return

    if path.is_dir():
        total = Counter()

        for file in iter_files_recursively(path, "*.ledger"):
            data = account_count(file)
            total.update(data)

        print_result(total, header)

        return

    raise typer.BadParameter(f"{path} はファイルでもディレクトリでもありません")

def main():
    # typer.run(add)
    app()
