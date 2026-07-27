from ledger_utils.models import OuterComment


def render_comment(token: OuterComment) -> str:
    return token.raw_text
