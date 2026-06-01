import re
from collections import defaultdict
from pathlib import Path

from .common import report_count

POSTING_RE: re.Pattern[str] = re.compile(
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


def parse_account(line: str, posting_re: re.Pattern[str] = POSTING_RE) -> str | None:
    """
    lineからACCOUNTを抽出する。なければNoneを返す。
    """

    if (m := posting_re.match(line)) is not None:
        return m.group("account") or None
    return None


def counter(text: str, posting_re: re.Pattern[str] = POSTING_RE) -> dict[str, int]:
    """
    {ACCOUNT: 出現数}の辞書を返す
    """

    counts = defaultdict(int)
    for line in text.splitlines():
        if account := parse_account(line, posting_re):
            counts[account] += 1
    return dict(counts)


def count(path: Path, posting_re: re.Pattern[str] = POSTING_RE) -> dict[str, int]:
    """
    ファイル Path に出現する accountの回数を返す
    """

    text = path.read_text()
    return counter(text, posting_re)


def report(path: Path):
    report_count(path, "count  account", count)
