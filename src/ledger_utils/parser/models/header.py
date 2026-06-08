from dataclasses import dataclass
from datetime import date

from .comment import Comment


@dataclass
class Header:
    raw_text: str
    date: date
    date2: date | None
    code: str | None
    flag: str | None
    description: str | None
    comment: Comment | None

    def __post_init__(self):
        # 1. date は必須
        if not isinstance(self.date, date):
            raise TypeError("date must be a datetime.date")

        # 2. date2 があるなら date <= date2
        if self.date2 is not None and self.date2 < self.date:
            raise ValueError("date2 must be >= date")

        # 3. flag は *, !, None のいずれか
        if self.flag not in (None, "*", "!"):
            raise ValueError("flag must be '*', '!', or None")

        # 4. description は空文字なら None に正規化
        if self.description is not None and not self.description.strip():
            self.description = None
