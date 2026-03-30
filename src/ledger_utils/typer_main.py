from pathlib import Path

import typer

from ledger_utils.count import payee_count

from collections import Counter

app = typer.Typer()

def iter_ledger_files(root:Path):
    yield from (p for p in root.rglob("*.ledger") if p.is_file())

def print_result(total: dict[str, int]):
    for key, value in sorted(total.items(), key=lambda x: (x[1], x[0])):
        print(f"count: {value:5d}, payee: {key}")

@app.command()
def hello():
    print("hello world")


@app.command()
def count(path: Path):
    if not path.is_dir():
        print(path)
        data = payee_count(path)

        for key, value in sorted(data.items(), key=lambda x: (x[1], x[0])):
            print(f"count: {value:3d}, payee: {key}")
    else:
        total = Counter()

        for file in iter_ledger_files(path):
            data = payee_count(file)
            total.update(data)

        print_result(total)


def main():
    # typer.run(add)
    app()
