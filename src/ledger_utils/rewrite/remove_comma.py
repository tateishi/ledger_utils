import re

POSTING_RE = re.compile(
    r"""
    ^
    (?P<prefix>.*?\s{2,})                 # account + 区切りスペース（ここは絶対に変更しない）
    (?P<amount>[+-]?[0-9,]+(?:\.[0-9]+)?) # 金額
    (?P<suffix>.*)$                       # 通貨・コメント・末尾（ここも絶対に変更しない）
    """,
    re.VERBOSE,
)


def convert(text: str) -> str:
    """金額以外は空白を含めて一切変更せず、金額中のカンマだけ削除し、右端位置を維持する"""

    out_lines = []

    for line in text.splitlines():
        m = POSTING_RE.match(line)
        if not m:
            out_lines.append(line)
            continue

        prefix = m.group("prefix")  # 変更禁止
        amount_orig = m.group("amount")
        suffix = m.group("suffix")  # 変更禁止

        # 元の金額の幅
        orig_width = len(amount_orig)

        # カンマ削除後
        amount_new = amount_orig.replace(",", "")
        new_width = len(amount_new)

        # 右端を揃えるための左側スペース
        pad = orig_width - new_width
        if pad < 0:
            pad = 0

        amount_final = " " * pad + amount_new

        # prefix と suffix は絶対に変更しない
        new_line = prefix + amount_final + suffix

        out_lines.append(new_line)

    return "\n".join(out_lines) + "\n"
