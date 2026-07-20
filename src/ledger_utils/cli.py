import typer

from ledger_utils.count.app import app as count_app
from ledger_utils.rewrite.app import app as rewrite_app
from ledger_utils.format.app import app as format_app


app = typer.Typer()

app.add_typer(rewrite_app, name="rewrite")
app.add_typer(count_app, name="count")
app.add_typer(format_app, name="format")


def main():
    app()
