import typer
from pathlib import Path

from ledger_utils.count import account_count, payee_count, tags_count
from typing import Callable

app = typer.Typer(help="Count related command.")

@app.command("payee")
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


@app.command("account")
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


@app.command("tags")
def count_tags(path: Path):
    header = "count  tags"

    if not path.exists():
        raise typer.BadParameter(f"{path}は存在しません")

    if path.is_file():
        data = tags_count(path)

        print_result(data, header)

        return

    if path.is_dir():
        total = Counter()

        for file in iter_files_recursively(path, "*.ledger"):
            data = tags_count(file)
            total.update(data)

        print_result(total, header)

        return

    raise typer.BadParameter(f"{path} はファイルでもディレクトリでもありません")
