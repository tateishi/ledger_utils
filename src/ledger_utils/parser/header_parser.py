import re
from datetime import datetime

from ledger_utils.models import Header, Meta, Tag

from .meta_parser import parse_meta
from .tags_parser import parse_tags

HEADER_RE = re.compile(
    r"""
    ^
    (?P<date>\d{4}[/-]\d{1,2}[/-]\d{1,2})         # 日付 YYYY-MM-DD / YYYY/MM/DD
    (?:=(?P<date2>\d{4}[/-]\d{1,2}[/-]\d{1,2}))?  # 決済日 (=YYYY-MM-DD / =YYYY/MM/DD)
    (?:\s+\((?P<code>[^)]+)\))?                   # コード (任意の文字)
    (?:\s+(?P<flag>[*!]))?                        # フラグ * または !
    (?:\s+(?P<description>[^;]+?))?               # 説明（; の前まで）
    (?:\s*;\s*(?P<comment>.*))?                   # コメント ; 以降
    $
    """,
    re.VERBOSE,
)


def parse_header(
    text: str, line_no: int | None = None, filename: str | None = None
) -> Header:
    m = HEADER_RE.match(text)
    if not m:
        raise ValueError(f"Invalid header: {text}")

    tags = parse_tags(m["comment"])
    meta = parse_meta(m["comment"])

    return Header(
        raw_text=text,
        line_no=line_no,
        filename=filename,
        tags=tags,
        meta=meta,
        **m.groupdict()
    )
