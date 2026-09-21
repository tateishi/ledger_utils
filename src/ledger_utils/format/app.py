from pathlib import Path

import typer

from ledger_utils import parser

app = typer.Typer(help="Format related command.")


@app.command("parse")
def parse(path: Path):
    from pprint import pprint

    if path.suffix == ".ledger":
        text = path.read_text()
        ast = parser.parse_text(text, filename=path.as_posix())
        for item in ast.items:
            pprint(item)
        # print(render_convert(ast.items))
