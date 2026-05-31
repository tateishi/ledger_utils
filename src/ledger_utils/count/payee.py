import re
from collections import defaultdict
from pathlib import Path

from .common import report_count

HEADER_RE = re.compile(r"^\d")

HEADER_PARSE_RE = re.compile(
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


def counter(text: str) -> dict[str, int]:
    """
    {PAYEE: 出現数} の辞書を返す
    """

    counts = defaultdict(int)

    for line in text.splitlines():
        if (m := HEADER_PARSE_RE.match(line)) and (payee := m.group("payee")):
            counts[payee] += 1

    return dict(counts)


def count(path: Path) -> dict[str, int]:
    """
    ファイル path に出現するpayeeの回数を返す
    """

    text = path.read_text()

    return counter(text)


def report(path: Path):
    report_count(path, "count  payee", count)
