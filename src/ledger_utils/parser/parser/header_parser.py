import re
from datetime import datetime

from ledger_utils.parser.models import Header, Comment

HEADER_RE = re.compile(
    r"""
    ^(?P<date>\d{4}[/-]\d{1,2}[/-]\d{1,2})        # 日付 YYYY-MM-DD / YYYY/MM/DD
    (?:=(?P<date2>\d{4}[/-]\d{1,2}[/-]\d{1,2}))?  # 決済日 (=YYYY-MM-DD / =YYYY/MM/DD)
    (?:\s+\((?P<code>[^)]+)\))?                   # コード (任意の文字)
    (?:\s+(?P<flag>[*!]))?                        # フラグ * または !
    (?:\s+(?P<description>[^;]+?))?               # 説明（; の前まで）
    (?:\s*;\s*(?P<comment>.*))?                   # コメント ; 以降
    $
    """,
    re.VERBOSE,
)

def parse_header(text: str, line_no: int | None=None, filename: str | None=None) -> Header:
    m = HEADER_RE.match(text)
    if not m:
        raise ValueError(f"Invalid header: {text}")

    gd = m.groupdict()

    def to_date(s: str) -> datetime | None:
        if s is None: return None
        for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                pass
        return None

    comment = None
    if gd["comment"]:
        comment = Comment(
            raw_text=gd["comment"],
            text=gd["comment"],
        )

    return Header(
        raw_text=text,
        date=to_date(gd["date"]),
        date2=to_date(gd["date2"]),
        code=gd["code"],
        flag=gd["flag"],
        description=gd["description"].strip() if gd["description"] else None,
        comment=comment,
    )
