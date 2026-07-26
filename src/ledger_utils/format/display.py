import decimal

from ledger_utils.models import (Blank, OuterComment, Header, InnerComment,
                                 Posting)
from ledger_utils.parser import LedgerItem, TransactionPart
from ledger_utils.text import width


def display_ledger(items: list[LedgerItem]) -> str:
    lines = list()
    for item in items:
        match item:
            case c if isinstance(c, Blank):
                lines.append(display_blank(c))
            case c if isinstance(c, OuterComment):
                lines.append(display_comment(c))
            case c if isinstance(c, TransactionPart):
                lines.extend(display_transaction(c))
            case _:
                raise ValueError(f"Invalid token: f{c}")
    text = "\n".join(lines)
    return text


def display_blank(token: Blank) -> str:
    return token.raw_text


def display_comment(token: OuterComment) -> str:
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


def render_with_subunits(
    amount: decimal.Decimal,
    decimal_places: int = 0,
    rounding: str = decimal.ROUND_HALF_UP,
) -> str:
    if not (1 <= decimal_places <= 10):
        return f"{amount}"
    format = "0." + "0" * decimal_places
    v = amount.quantize(decimal.Decimal(format), rounding=rounding)
    return f"{v}"


def display_posting(item: Posting) -> str:
    indent_width = 4
    target = 52
    comment_target = 54
    currencies_with_subunits = {
        "USD": 2,
        "EUR": 2,
        "AUD": 2,
        "NZD": 2,
        "BRL": 2,
        "ZAR": 2,
    }

    result = " " * indent_width + f"{item.account}"

    if item.amount is not None:
        commodity_width = (
            0 if item.commodity_pre is None else width.wcswidth(item.commodity_pre) + 1
        )
        gap_width = target - (
            indent_width
            + width.wcswidth(item.account)
            + commodity_width
            + width.integer_part_width(item.amount)
        )
        if gap_width < 2:
            gap_width = 2
        result += " " * gap_width

    if (item.commodity_pre is not None) and (item.amount is not None):
        result += f"{item.commodity_pre}"
        result += " "
        result += f"{item.amount}"
    else:
        if item.commodity_pre is not None:
            result += f"{item.commodity_pre}"
        if item.amount is not None:
            if item.commodity in currencies_with_subunits:
                decimal_places = currencies_with_subunits[item.commodity]
                amount_str = render_with_subunits(item.amount, decimal_places)
            else:
                amount_str = f"{item.amount}"
            result += amount_str

    if item.commodity_post is not None:
        result += f" {item.commodity_post}"

    comment_gap_width = comment_target - width.wcswidth(result)
    if comment_gap_width < 2:
        comment_gap_width = 2

    if item.meta is not None:
        result += " " * comment_gap_width
        result += f"; {item.meta.name}: {item.meta.value}"
    elif item.tags is not None:
        result += " " * comment_gap_width
        result += f"; :{':'.join([e.tag for e in item.tags])}:"
    elif item.comment is not None:
        result += " " * comment_gap_width
        result += f"; {item.comment}"

    return result


def display_posting_comment(item: InnerComment) -> str:
    if item.meta is not None:
        result = f"    ; {item.meta.name}: {item.meta.value}"
    elif item.tags is not None:
        result = f"    ; :{':'.join([e.tag for e in item.tags])}:"
    elif item.comment is not None:
        result = f"    ; {item.comment}"

    return result
