import textwrap
from datetime import date, datetime
from decimal import Decimal

import pytest
from ledger_utils.parser import parse_text


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            textwrap.dedent("""
        """).strip(),
            {
                "state": "outside",
                "items": [],
            },
        ),
        (
            textwrap.dedent("""
        2026-07-19 * myshop  ;  use-month: 2026-07
        """).strip(),
            {
                "state": "outside",
                "header_date": [date(2026, 7, 19)],
                "header_flag": ["*"],
                "header_desc": ["myshop"],
                "header_meta": [dict(name="use-month", value="2026-07")],
            },
        ),
        (
            textwrap.dedent("""
        2026-07-16 * myshop        ;  use-month: 2026-07
            支出:食費:外食     2000 JPY
            資産:現金:paypay
        """).strip(),
            {
                "state": "outside",
                "header_date": [date(2026, 7, 16)],
                "header_flag": ["*"],
                "header_desc": ["myshop"],
                "header_meta": [dict(name="use-month", value="2026-07")],
                "posting_account": [["支出:食費:外食", "資産:現金:paypay"]],
                "posting_amount": [[Decimal("2000"), None]],
                "posting_commodity": [["JPY", None]],
            },
        ),
        (
            textwrap.dedent("""
        2026-07-16 * myshop                        ;  use-month: 2026-07
            支出:食費:外食              2000 JPY   ;  member: 忠利
            負債:クレジット:楽天カード             ;  pay-month: 2026-08
        """).strip(),
            {
                "state": "outside",
                "header_date": [date(2026, 7, 16)],
                "header_flag": ["*"],
                "header_desc": ["myshop"],
                "header_meta": [dict(name="use-month", value="2026-07")],
                "posting_account": [["支出:食費:外食", "負債:クレジット:楽天カード"]],
                "posting_amount": [[Decimal("2000"), None]],
                "posting_commodity": [["JPY", None]],
                "posting_meta": [
                    [
                        dict(name="member", value="忠利"),
                        dict(name="pay-month", value="2026-08"),
                    ]
                ],
            },
        ),
        (
            textwrap.dedent("""
        2026-07-16 * myshop
            ;  use-month: 2026-07
            支出:食費:外食              2000 JPY
            ;  member: 忠利
            負債:クレジット:楽天カード
            ;  pay-month: 2026-08
        """).strip(),
            {
                "state": "outside",
                "header_date": [date(2026, 7, 16)],
                "header_flag": ["*"],
                "header_desc": ["myshop"],
                "header_comment_meta": [[dict(name="use-month", value="2026-07")]],
                "posting_account": [["支出:食費:外食", "負債:クレジット:楽天カード"]],
                "posting_amount": [[Decimal("2000"), None]],
                "posting_commodity": [["JPY", None]],
                "posting_comment_meta": [
                    [
                        [dict(name="member", value="忠利")],
                        [dict(name="pay-month", value="2026-08")],
                    ]
                ],
            },
        ),
        (
            textwrap.dedent("""
        2026-07-16 * myshop
            支出:食費:外食              2000 JPY
            負債:クレジット:楽天カード

        2026-07-20 * mysupermarket
            支出:食費:食材              1500
            資産:現金:財布
        """).strip(),
            {
                "state": "outside",
                # "items": [],
                "header_date": [date(2026, 7, 16), None, date(2026, 7, 20)],
                "header_flag": ["*", None, "*"],
                "header_desc": ["myshop", None, "mysupermarket"],
                "posting_account": [
                    ["支出:食費:外食", "負債:クレジット:楽天カード"],
                    None,
                    ["支出:食費:食材", "資産:現金:財布"],
                ],
                "posting_amount": [
                    [Decimal("2000"), None],
                    None,
                    [Decimal("1500"), None],
                ],
                "posting_commodity": [
                    ["JPY", None],
                    None,
                    [None, None],
                ],
            },
        ),
    ],
)
def test_parse_posting(line, expected):
    p = parse_text(line)

    assert p.state == expected["state"]
    if "items" in expected:
        assert p.items == expected["items"]

    if "header_date" in expected:
        for i, d in enumerate(expected["header_date"]):
            if d is not None:
                assert p.items[i].header.header.date == d

    if "header_flag" in expected:
        for i, d in enumerate(expected["header_flag"]):
            if d is not None:
                assert p.items[i].header.header.flag == d

    if "header_desc" in expected:
        for i, d in enumerate(expected["header_desc"]):
            if d is not None:
                assert p.items[i].header.header.description == d

    if "header_meta" in expected:
        for i, d in enumerate(expected["header_meta"]):
            if d is not None:
                assert p.items[i].header.header.meta.name == d["name"]
                assert p.items[i].header.header.meta.value == d["value"]

    if "header_comment_meta" in expected:
        for i, part in enumerate(expected["header_comment_meta"]):
            for j, d in enumerate(part):
                if d is not None:
                    assert p.items[i].header.comments[j].meta.name == d["name"]
                    assert p.items[i].header.comments[j].meta.value == d["value"]

    if "posting_account" in expected:
        for i, part in enumerate(expected["posting_account"]):
            if part is not None:
                for j, d in enumerate(part):
                    assert p.items[i].postings[j].posting.account == d

    if "posting_amount" in expected:
        for i, part in enumerate(expected["posting_amount"]):
            if part is not None:
                for j, d in enumerate(part):
                    assert p.items[i].postings[j].posting.amount == d

    if "posting_commodity" in expected:
        for i, part in enumerate(expected["posting_commodity"]):
            if part is not None:
                for j, d in enumerate(part):
                    assert p.items[i].postings[j].posting.commodity == d

    if "posting_meta" in expected:
        for i, part in enumerate(expected["posting_meta"]):
            if part is not None:
                for j, d in enumerate(part):
                    assert p.items[i].postings[j].posting.meta.name == d["name"]
                    assert p.items[i].postings[j].posting.meta.value == d["value"]

    if "posting_comment_meta" in expected:
        for i, part in enumerate(expected["posting_comment_meta"]):
            if part is not None:
                for j, ppp in enumerate(part):
                    for k, d in enumerate(ppp):
                        assert p.items[i].postings[j].comments[k].meta.name == d["name"]
                        assert (
                            p.items[i].postings[j].comments[k].meta.value == d["value"]
                        )
