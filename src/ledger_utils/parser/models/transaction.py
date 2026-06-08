from dataclasses import dataclass, field


@dataclass
class Transaction:
    header: Header
    postings: list[Posting] = field(default_factory=list)
