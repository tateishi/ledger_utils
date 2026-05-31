from pathlib import Path

import typer

from . import account_report, payee_report, tags_report

app = typer.Typer(help="Count related command.")


@app.command("payee")
def count_payee(path: Path):
    payee_report(path)


@app.command("account")
def count_account(path: Path):
    account_report(path)


@app.command("tags")
def count_tags(path: Path):
    tags_report(path)
