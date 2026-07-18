from dataclasses import dataclass

@dataclass
class GlobalComment:
    raw_text: str
    line_no: int | None
    filename: str | None
    leader: str
    comment: str
