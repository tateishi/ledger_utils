import unicodedata
from decimal import Decimal


def wcwidth(ch: str) -> int:
    w = unicodedata.east_asian_width(ch)
    return 2 if w in ("F", "W") else 1


def wcswidth(text: str) -> int:
    return sum(wcwidth(ch) for ch in text)


def integer_part_width(amount: Decimal) -> int:
    text = str(amount)

    if "." not in text:
        return len(text)

    ip, fp = text.split(".")
    return len(ip)
