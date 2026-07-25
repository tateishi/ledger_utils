from dataclasses import dataclass

@dataclass
class GlobalComment:
    leader: str = ""
    comment: str = ""
    raw_text: str = ""
    line_no: int | None = None
    filename: str | None = None
