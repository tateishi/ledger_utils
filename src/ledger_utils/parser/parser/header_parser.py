from ledger_utils.parser.models import Header
import re

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
