from dataclasses import dataclass, field


@dataclass
class Comment:
    raw_text: str
    text: str
    tags: list[Tag] = field(default_factory=list)
    meta: list[Meta] = field(default_factory=list)
