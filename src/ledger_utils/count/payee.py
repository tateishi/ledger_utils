import re
from collections import defaultdict
from pathlib import Path

from .common import report_count

PAYEE_RE: re.Pattern[str] = re.compile(
    r"""^
    (?P<date>\d{4}-\d{2}-\d{2})
    (?:
        \s+
        (?:(?P<flag>[*!])\s+)?     # optional * or !
        (?P<payee>.*?)
    )?
    (?P<comment>\s*;\s*.*)?       # optional trailing comment ; ...
    \s*$
    """,
    re.VERBOSE,
)


def parse_payee(line: str, payee_re: re.Pattern[str] = PAYEE_RE) -> str | None:
    """
    lineからPAYEEを抽出する。なければNoneを返す。
    """

    if (m := payee_re.match(line)) is not None:
        return m.group("payee") or None
    return None


def counter(text: str, payee_re: re.Pattern[str] = PAYEE_RE) -> dict[str, int]:
    """
    {PAYEE: 出現数} の辞書を返す
    """

    counts = defaultdict(int)
    for line in text.splitlines():
        if payee := parse_payee(line, payee_re):
            counts[payee] += 1
    return dict(counts)


def count(path: Path, payee_re: re.Pattern[str] = PAYEE_RE) -> dict[str, int]:
    """
    ファイル path に出現するpayeeの回数を返す
    """

    text = path.read_text()
    return counter(text, payee_re)


def report(path: Path):
    report_count(path, "count  payee", count)
