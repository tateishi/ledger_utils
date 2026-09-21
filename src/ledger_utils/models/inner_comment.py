from dataclasses import dataclass

from .meta import Meta
from .tag import Tag


@dataclass
class InnerComment:
    comment: str = ""
    tags: list[Tag] | None = None
    meta: Meta | None = None
    raw_text: str = ""
    line_no: int | None = None
    filename: str | None = None
