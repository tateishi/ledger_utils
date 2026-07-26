from dataclasses import dataclass
from decimal import Decimal

from .tag import Tag
from .meta import Meta


@dataclass
class Posting:
    account: str
    commodity_pre: str | None = None
    amount: Decimal | None = None
    commodity_post: str | None = None
    comment: str | None = None
    tags: list[Tag] | None = None
    meta: Meta | None = None
    raw_text: str = ""
    line_no: int | None = None
    filename: str | None = None

    def __post_init__(self):
        if self.amount is not None:
            amount = self.amount.replace(",","")
            self.amount = Decimal(amount)

    @property
    def commodity(self) -> str | None:
        return self.commodity_pre or self.commodity_post

    @property
    def commodity_order(self) -> str:
        if isinstance(self.commodity_pre, str) and isinstance(self.commodity_post, str):
            if self.commodity_pre == self.commodity_post:
                return "both"
            else:
                return "conflict"
        if isinstance(self.commodity_pre, str):
            return "pre"
        if isinstance(self.commodity_post, str):
            return "post"
        return "none"
