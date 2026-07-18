import re

from ledger_utils.parser.models import Blank

def parse_blank(
    text: str, line_no: int | None=None, filename: str | None=None
) -> Blank:
    blank = text.strip()
    if blank != "":
        raise ValueError(f"Invalid line: {text}")

    return Blank(
        raw_text=text,
        line_no=line_no,
        filename=filename,
    )
