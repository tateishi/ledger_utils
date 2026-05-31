import typer
from pathlib import Path

from . import account_count, payee_count, tags_count
from .common import report_count


app = typer.Typer(help="Count related command.")

@app.command("payee")
def count_payee(path: Path):
    report_count(path, "count payee", payee_count)

@app.command("account")
def count_account(path: Path):
    report_count(path, "count account", account_count)

@app.command("tags")
def count_tags(path: Path):
    report_count(path, "count tags", tags_count)
