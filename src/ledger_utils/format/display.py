from ledger_utils.models import Blank, GlobalComment
from ledger_utils.parser import TransactionPart, LedgerItem


def display_ledger(items: list[LedgerItem]) -> str:
    lines = list()
    for item in items:
        match item:
            case c if isinstance(c, Blank):
                lines.append(display_blank(c))
            case c if isinstance(c, GlobalComment):
                lines.append(display_comment(c))
            case c if isinstance(c, TransactionPart):
                lines.extend(display_transaction(c))
            case _:
                raise ValueError(f"Invalid token: f{c}")
    text = "\n".join(lines)
    return text


def display_blank(item: Blank) -> str:
    return ""


def display_comment(item: GlobalComment) -> str:
    return item.raw_text


def display_transaction(item: TransactionPart) -> list[str]:
    result = list()
    result.append(item.header.header.raw_text)
    result += [el.raw_text for el in item.header.comments]
    for post in item.postings:
        result.append(post.posting.raw_text)
        result += [el.raw_text for el in post.comments]
    return result
