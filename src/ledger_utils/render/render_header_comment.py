from ledger_utils.models import InnerComment


def render_header_comment(item: InnerComment) -> str:
    if item.meta is not None:
        result = f"    ; {item.meta.name}: {item.meta.value}"
    elif item.tags is not None:
        result = f"    ; :{':'.join([e.tag for e in item.tags])}:"
    elif item.comment is not None:
        result = f"    ; {item.comment}"

    return result
