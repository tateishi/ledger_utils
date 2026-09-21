import re

from ledger_utils.models import InnerComment

from .meta_parser import parse_meta
from .tags_parser import parse_tags

INNER_COMMENT_RE = re.compile(
    r"""
    ^
    \s+;
    (?:\s*(?P<comment>.*))
    $
    """,
    re.VERBOSE
)


def parse_inner_comment(
    text: str, line_no: int | None=None, filename: str | None=None
) -> InnerComment:
    m = INNER_COMMENT_RE.match(text)
    if not m:
        raise ValueError(f"Invalid comment: {text}")

    tags = parse_tags(m["comment"])
    meta = parse_meta(m["comment"])

    return InnerComment(
        raw_text=text,
        line_no=line_no,
        filename=filename,
        tags=tags,
        meta=meta,
        **m.groupdict(),
    )
