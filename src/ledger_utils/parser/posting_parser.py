import re

from ledger_utils.models import Meta, Posting, Tag

from .meta_parser import parse_meta
from .tags_parser import parse_tags

POSTING_RE = re.compile(
    r"""
    ^
    \s+                                          # インデント（必須）
    (?:
        (?P<account>\S+(?:\s\S+)*)               # アカウント（空白1つで何語でもOK）
        (?:                                      # 金額・通貨（任意）
            \s{2,}                               # 2つ以上の空白で区切り
            (?:\s+(?P<commodity_pre>\S+))?       # 通貨（任意）
            (?:\s+(?P<amount>[-+]?\d[\d,\.]*))   # 金額
            (?:\s+(?P<commodity_post>\S+))?      # 通貨（任意）
        )?
        (?:\s*;\s*(?P<comment>.*))?              # コメント（任意）
    )
    \s*$
    """,
    re.VERBOSE
)

def parse_posting(
        text: str, line_no: int | None=None, filename: str | None=None
) -> Posting:
    m = POSTING_RE.match(text)
    if not m:
        raise ValueError(f"Invalid format: {text}")

    tags = parse_tags(m["comment"])
    meta = parse_meta(m["comment"])

    return Posting(
        raw_text=text,
        line_no=line_no,
        filename=filename,
        tags=tags,
        meta=meta,
        **m.groupdict()
    )
