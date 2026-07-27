from ledger_utils.models import Header


def render_header(item: Header) -> str:
    result = item.date.strftime("%Y-%m-%d")
    if item.date2 is not None:
        result += f" ={item.date2.strftime('%Y-%m-%d')}"
    if item.code is not None:
        result += f" ({item.code})"
    if item.flag is not None:
        result += f" {item.flag}"
    if item.description is not None:
        result += f" {item.description}"
    if item.meta is not None:
        result += f"  ; {item.meta.name}: {item.meta.value}"
    elif item.tags is not None:
        result += f"  ; :{':'.join([e.tag for e in item.tags])}:"
    elif item.comment is not None:
        result += f"  ; {item.comment}"

    return result
