import re
from pathlib import Path

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

    count_dict = dict()

    lines = text.splitlines()

    for line in lines:
        m_header = re.match(HEADER_PARSE_RE, line)
        if m_header is None:
            continue

        payee = m_header.group("payee")
        count_dict[payee] = count_dict.get(payee, 0) + 1

    return count_dict


def count(path: Path) -> dict[str, int]:
    """
    ファイル path に出現するpayeeの回数を返す
    """

    text = path.read_text()

    return counter(text)
