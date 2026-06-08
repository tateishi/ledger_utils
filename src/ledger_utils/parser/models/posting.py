from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Posting:
    raw_text: str
    account: str
    amount: Decimal | None
    commodity: str | None
    comment: Comment | None
