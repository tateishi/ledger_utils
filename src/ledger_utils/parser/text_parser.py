from dataclasses import dataclass, field

from ledger_utils.models import (Blank, GlobalComment, Header, InnerComment,
                                 Posting)
from ledger_utils.parser import (parse_blank, parse_global_comment,
                                 parse_header, parse_inner_comment,
                                 parse_posting)


@dataclass
class BlankPart:
    """
    トランザクションの間のコメント・空白行（ファイル先頭・末尾含む）
    """
    item: GlobalComment | Blank

@dataclass
class HeaderPart:
    """
    トランザクションヘッダーとコメント
    """
    header: Header
    comments: list[InnerComment]

@dataclass
class PostingPart:
    """
    ポスティング一つ分のデータ
    """
    posting: Posting
    comments: list[InnerComment]

@dataclass
class TransactionPart:
    """
    トランザクション一つ分のデータ
    """
    header: HeaderPart
    postings: list[PostingPart]

@dataclass
class LedgerItem:
    """
    上記のファイル要素のunion
    """
    item: BlankPart | TransactionPart

@dataclass
class Context:
    state: str = "outside"
    items: list[LedgerItem] = field(default_factory=list)


def parse_text(text: str, filename: str | None=None):
    ctx = Context()

    header: HeaderPart = None
    posting: PostingPart = None
    postings: list[PostingPart] = []

    blanks: list[BlankPart] = []
    transactions: list[TransactionPart] = []

    lines = text.splitlines()
    for i, line in enumerate(lines):
        match ctx.state:
            case "outside":
                if len(line) < 1:
                    item = parse_blank(line, i, filename)
                    ctx.state = "outside"

                    # push blank
                    blanks.append(item)

                    continue

                match line[0]:
                    case c if c in ";#%|*":
                        ctx.state = "outside"

                        # push global comment
                        item = parse_global_comment(line, i, filename)
                        blanks.append(item)

                        continue

                    case c if "0" <= c <= "9":
                        # output
                        if len(blanks) > 0:
                            ctx.items.extend(blanks)
                        blanks = []

                        ctx.state = "header"

                        # push header
                        item = parse_header(line, i, filename)
                        header = HeaderPart(header=item, comments=list())

                        continue

                    case _:
                        item = parse_blank(line, i, filename)
                        ctx.state = "outside"

                        # push blank
                        blanks.append(item)

                        continue

            case "header":
                if len(line) < 1:
                    # output
                    transaction = TransactionPart(header=header, postings=postings)
                    transactions.append(transaction)
                    header = None
                    postings = []
                    ctx.items.extend(transactions)
                    transactions = []

                    ctx.state = "outside"

                    # push blank
                    item = parse_blank(line, i, filename)
                    blanks.append(item)

                    continue

                match line[0]:
                    case c if c in ";#%|*":
                        # output
                        item = TransactionPart(header=header, postings=postings)
                        transactions.append(item)
                        header = None
                        postings = []
                        ctx.items.extend(transactions)
                        transactions = []

                        ctx.state = "outside"

                        # push global comment
                        item = parse_global_comment(line, i, filename)
                        blanks.append(item)

                        continue

                    case c if "0" <= c <= "9":
                        # output
                        item = TransactionPart(header=header, postings=postings)
                        transactions.append(item)
                        header = None
                        postings = []

                        ctx.state = "header"

                        # push header
                        item = parse_header(line, i, filename)
                        header = HeaderPart(header=item, comments=list())

                        continue

                    case _:
                        try:
                            item = parse_inner_comment(line, i, filename)
                            ctx.state = "header"

                            # push inner_comment
                            header.comments.append(item)

                            continue
                        except ValueError:
                            pass

                        item = parse_posting(line, i, filename)
                        # output and begin collecting posting

                        ctx.state = "posting"

                        # push posting
                        posting = PostingPart(posting=item, comments=list())

                        continue

            case "posting":
                if len(line) < 1:
                    # output
                    postings.append(posting)
                    posting = None

                    transaction = TransactionPart(header=header, postings=postings)
                    transactions.append(transaction)
                    header = None
                    postings = []
                    ctx.items.extend(transactions)
                    transactions = []

                    ctx.state = "outside"

                    # push blank
                    item = parse_blank(line, i, filename)
                    blanks.append(item)

                    continue

                match line[0]:
                    case c if c in ";#%|*":
                        # output
                        postings.append(posting)
                        posting = None

                        item = TransactionPart(header=header, postings=postings)
                        transactions.append(item)
                        header = None
                        postings = []

                        ctx.items.extend(transactions)
                        transactions = []

                        ctx.state = "outside"

                        # push global comment
                        item = parse_global_comment(line, i, filename)
                        blanks.append(item)

                        continue

                    case c if "0" <= c <= "9":
                        # output
                        postings.append(posting)
                        posting = None

                        item = TransactionPart(header=header, postings=postings)
                        transactions.append(item)
                        header = None
                        postings = []

                        ctx.state = "header"

                        # push header
                        item = parse_header(line, i, filename)
                        header = HeaderPart(header=item, comments=list())

                        continue

                    case _:
                        try:
                            item = parse_blank(line, i, filename)

                            # output
                            postings.append(posting)
                            posting = None

                            transaction = TransactionPart(header=header, postings=postings)
                            transactions.append(transaction)
                            header = None
                            postings = []
                            ctx.items.extend(transactions)
                            transactions = []

                            ctx.state = "outside"

                            # push blank
                            blanks.append(item)

                            continue

                        except ValueError:
                            pass

                        try:
                            item = parse_inner_comment(line, i, filename)
                            ctx.state = "posting"

                            # push inner comment
                            posting.comments.append(item)

                            continue
                        except ValueError:
                            pass

                        try:
                            item = parse_posting(line, i, filename)

                            # output posting and begin collecting next posting
                            postings.append(posting)

                            ctx.state = "posting"

                            # push posting
                            posting = PostingPart(posting=item, comments=list())

                            continue
                        except Exception as e:
                            raise e

    match ctx.state:
        case "outside":
            # output
            if len(blanks) > 0:
                ctx.items.extend(blanks)
            blanks = []

        case "header":
            # output
            transaction = TransactionPart(header=header, postings=postings)
            transactions.append(transaction)
            header = None
            postings = []
            ctx.items.extend(transactions)
            transactions = []

            ctx.state = "outside"

        case "posting":
            # output
            postings.append(posting)

            transaction = TransactionPart(header=header, postings=postings)
            transactions.append(transaction)
            header = None
            postings = []
            ctx.items.extend(transactions)
            transactions = []

            ctx.state = "outside"

    return ctx
