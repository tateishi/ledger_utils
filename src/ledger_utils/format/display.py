from ledger_utils.models import Blank, GlobalComment, Header, InnerComment, Posting
from ledger_utils.parser import LedgerItem, TransactionPart


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


def display_blank(token: Blank) -> str:
    return token.raw_text


def display_comment(token: GlobalComment) -> str:
    return token.raw_text


def display_transaction(token: TransactionPart) -> list[str]:
    result = list()

    result.append(display_header(token.header.header))
    result += [display_header_comment(item) for item in token.header.comments]
    for post in token.postings:
        result.append(display_posting(post.posting))
        result += [display_posting_comment(item) for item in post.comments]
    return result


def display_header(item: Header) -> str:
    result = item.date.strftime("%Y-%m-%d")
    if item.date2 is not None:
        result += f" ={item.date2.strftime('%Y-%m-%d')}"
    if item.code is not None:
        result += f" ({item.code})"
    if item.flag is not None:
        result += f" {item.flag}"
    if item.description is not None:
        result += f" {item.description}"
    if item.meta is not None:
        result += f"  ; {item.meta.name}: {item.meta.value}"
    elif item.tags is not None:
        result += f"  ; :{':'.join([e.tag for e in item.tags])}:"
    elif item.comment is not None:
        result += f"  ; {item.comment}"

    return result


def display_header_comment(item: InnerComment) -> str:
    if item.meta is not None:
        result = f"    ; {item.meta.name}: {item.meta.value}"
    elif item.tags is not None:
        result = f"    ; :{':'.join([e.tag for e in item.tags])}:"
    elif item.comment is not None:
        result = f"    ; {item.comment}"

    return result


def display_posting(item: Posting) -> str:
    return item.raw_text


def display_posting_comment(item: InnerComment) -> str:
    if item.meta is not None:
        result = f"    ; {item.meta.name}: {item.meta.value}"
    elif item.tags is not None:
        result = f"    ; :{':'.join([e.tag for e in item.tags])}:"
    elif item.comment is not None:
        result = f"    ; {item.comment}"

    return result
