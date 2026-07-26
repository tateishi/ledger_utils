from ledger_utils import parser, render, models


def display_ledger(items: list[parser.LedgerItem]) -> str:
    lines = list()
    for item in items:
        match item:
            case c if isinstance(c, models.Blank):
                lines.append(render.display.display_blank(c))
            case c if isinstance(c, models.OuterComment):
                lines.append(render.display.display_comment(c))
            case c if isinstance(c, models.TransactionPart):
                lines.extend(render.display.display_transaction(c))
            case _:
                raise ValueError(f"Invalid token: f{c}")
    text = "\n".join(lines)
    return text
