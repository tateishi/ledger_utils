import re
from pathlib import Path
from collections import defaultdict

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

    count_dict = defaultdict(int)

    for line in text.splitlines():
        if (m := HEADER_PARSE_RE.match(line)):
            count_dict[m.group("payee")] += 1

    return count_dict


def count(path: Path) -> dict[str, int]:
    """
    ファイル path に出現するpayeeの回数を返す
    """

    text = path.read_text()

    return counter(text)


def report(path: Path):
    report_count(path, "count  payee", count)
