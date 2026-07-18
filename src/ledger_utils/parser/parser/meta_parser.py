import re

from ledger_utils.parser.models import Meta

META_RE = re.compile(
    r"""
    (?P<name>[^:]+):
    (?:\s*(?P<value>.+))
    """,
    re.VERBOSE
)

def parse_meta(text: str) -> Meta | None:
    if not isinstance(text, str):
        return None
    m = META_RE.match(text)
    if not m:
        return None
    meta = Meta(**m.groupdict())

    return meta
