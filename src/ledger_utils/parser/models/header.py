from dataclasses import dataclass
from datetime import date


@dataclass
class Header:
    raw_text: str
    date: date
    date2: date | None
    code: str | None
    flag: str | None
    description: str | None
    comment: Comment | None
