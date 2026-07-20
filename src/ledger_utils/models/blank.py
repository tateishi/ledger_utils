from dataclasses import dataclass

@dataclass
class Blank:
    raw_text: str
    line_no: int | None
    filename: str | None
