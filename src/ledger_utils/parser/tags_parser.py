from ledger_utils.models import Tag

def parse_tags(text: str | None) -> list[Tag] | None:
    if not isinstance(text, str):
        return None
    cand = text.strip()
    if cand[0] != ":" or cand[-1] != ":":
        return None
    tags_str = cand[1:-1].split(":")
    tags = [Tag(item) for item in tags_str]

    return tags
