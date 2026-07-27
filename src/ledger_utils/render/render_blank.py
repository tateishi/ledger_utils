from ledger_utils.models import (Blank)


def render_blank(token: Blank) -> str:
    return token.raw_text
