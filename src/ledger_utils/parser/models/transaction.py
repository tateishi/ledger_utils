from dataclasses import dataclass, field

from .header import Header
from .posting import Posting


@dataclass
class Transaction:
    header: Header
    postings: list[Posting] = field(default_factory=list)
