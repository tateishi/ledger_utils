from ledger_utils.parser import TransactionPart

from .display import (display_header, display_header_comment,
                      display_posting_comment)


def render_transaction(token: TransactionPart) -> list[str]:
    result = list()

    result.append(display_header(token.header.header))
    result += [display_header_comment(item) for item in token.header.comments]
    for post in token.postings:
        result.append(display_posting(post.posting))
        result += [display_posting_comment(item) for item in post.comments]
    return result
