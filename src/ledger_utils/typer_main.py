from pathlib import Path

import typer

from ledger_utils.count import payee_count

app = typer.Typer()


@app.command()
def hello():
    print("hello world")


@app.command()
def count(path: Path):
    print(path)
    print(payee_count(path, "abc"))


def main():
    # typer.run(add)
    app()
