import re

from ledger_utils.models import OuterComment

OUTER_COMMENT_RE = re.compile(
    r"""
    ^
    (?:(?P<leader>[;#%|*]))
    (?:(?P<comment>.*))
    $
    """,
    re.VERBOSE
)


def parse_outer_comment(
    text: str, line_no: int | None=None, filename: str | None=None
) -> OuterComment:
    m = OUTER_COMMENT_RE.match(text)
    if not m:
        raise ValueError(f"Invalid comment: {text}")

    return OuterComment(
        raw_text=text,
        line_no=line_no,
        filename=filename,
        **m.groupdict(),
    )
