import re
from pathlib import Path

POSTING_RE = re.compile(
    r"""
    ^
    (?P<indent>\s+)                         # インデント（必須）
    (?:
        ;\s*(?P<comment_only>.*)            # インデント直後のコメント行
      |
        (?P<account>\S+(?:\s\S+)*)          # アカウント（空白1つで何語でもOK）
        (?:                                 # 金額・通貨（任意）
            \s{2,}                          # 2つ以上の空白で区切り
            (?P<amount>[-+]?\d[\d,\.]*)     # 金額
            (?:\s+(?P<currency>\S+))?       # 通貨（任意）
        )?
        (?:\s*;\s*(?P<comment>.*))?         # コメント（任意）
    )
    \s*$
    """,
    re.VERBOSE,
)


def counter(text: str) -> dict[str, int]:
    """
    {ACCOUNT: 出現数}の辞書を返す
    """

    count_dict = dict()

    lines = text.splitlines()

    for line in lines:
        m_posting = re.match(POSTING_RE, line)
        if m_posting is None:
            continue

        account = m_posting.group("account")
        if account is None:
            continue
        count_dict[account] = count_dict.get(account, 0) + 1

    return count_dict


def count(path: Path) -> dict[str, int]:
    """
    ファイル Path に出現する accountの回数を返す
    """

    text = path.read_text()
    return counter(text)
