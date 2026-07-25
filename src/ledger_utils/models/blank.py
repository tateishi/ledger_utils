from dataclasses import dataclass

@dataclass
class Blank:
    raw_text: str = ""
    line_no: int | None = None
    filename: str | None = None
