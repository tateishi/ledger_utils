from dataclasses import dataclass

from .tag import Tag
from .meta import Meta

@dataclass
class InnerComment:
    comment: str
    tags: list[Tag] | None = None
    meta: Meta | None = None
    raw_text: str
    line_no: int | None
    filename: str | None
