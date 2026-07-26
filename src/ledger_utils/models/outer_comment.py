from dataclasses import dataclass

@dataclass
class OuterComment:
    leader: str = ""
    comment: str = ""
    raw_text: str = ""
    line_no: int | None = None
    filename: str | None = None
