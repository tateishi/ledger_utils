from ledger_utils import parser, render, models


def display_ledger(items: list[parser.LedgerItem]) -> str:
    lines = list()
    for item in items:
        match item:
            case c if isinstance(c, models.Blank):
                lines.append(render.render_blank(c))
            case c if isinstance(c, models.OuterComment):
                lines.append(render.render_comment(c))
            case c if isinstance(c, parser.TransactionPart):
                lines.extend(render.render_transaction(c))
            case _:
                raise ValueError(f"Invalid token: f{c}")
    text = "\n".join(lines)
    return text
