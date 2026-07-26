import sys
from pathlib import Path

import typer
from ledger_utils.parser import parse_text

from ledger_utils.render.display import display_ledger

app = typer.Typer(help="Format related command.")


@app.command("raw_copy")
def format_raw(path: Path):
    from pprint import pprint

    if path.suffix == ".ledger":
        text = path.read_text()
        ast = parse_text(text)
        print(display_ledger(ast.items))
