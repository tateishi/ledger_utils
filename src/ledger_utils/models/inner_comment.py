from dataclasses import dataclass

from .tag import Tag
from .meta import Meta

@dataclass
class InnerComment:
    raw_text: str
    line_no: int | None
    filename: str | None
    comment: str
    tags: list[Tag] | None = None
    meta: Meta | None = None
