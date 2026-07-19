import textwrap
from datetime import date, datetime
from decimal import Decimal

import pytest
from ledger_utils.parser import parse_text


@pytest.mark.parametrize("line, expected", [
    (
        textwrap.dedent("""
        """).strip(),
        {
            "state": "outside",
            "items": [],
        }
    ),
    (
        textwrap.dedent("""
        2026-07-19 * myshop  ;  use-month: 2026-07
        """).strip(),
        {
            "state": "outside",
            "header_date": [[date(2026, 7, 19)]],
            "header_flag": [["*"]],
            "header_desc": [["myshop"]],
            "header_meta": [[dict(name="use-month", value="2026-07")]],
        }
    ),
    (
        textwrap.dedent("""
        2026-07-16 * myshop        ;  use-month: 2026-07
            支出:食費:外食     2000 JPY
            資産:現金:paypay
        """).strip(),
        {
            "state": "outside",
            "header_date": [[date(2026, 7, 16)]],
            "header_flag": [["*"]],
            "header_desc": [["myshop"]],
            "header_meta": [[dict(name="use-month", value="2026-07")]],
            "posting_account": [[["支出:食費:外食", "資産:現金:paypay"]]],
            "posting_amount": [[[Decimal('2000'), None]]],
            "posting_commodity": [[["JPY", None]]],
        }
    ),
    (
        textwrap.dedent("""
        2026-07-16 * myshop                        ;  use-month: 2026-07
            支出:食費:外食              2000 JPY   ;  member: 忠利
            負債:クレジット:楽天カード             ;  pay-month: 2026-08
        """).strip(),
        {
            "state": "outside",
            "header_date": [[date(2026, 7, 16)]],
            "header_flag": [["*"]],
            "header_desc": [["myshop"]],
            "header_meta": [[dict(name="use-month", value="2026-07")]],
            "posting_account": [[["支出:食費:外食", "負債:クレジット:楽天カード"]]],
            "posting_amount": [[[Decimal('2000'), None]]],
            "posting_commodity": [[["JPY", None]]],
            "posting_meta": [[[
                dict(name="member", value="忠利"),
                dict(name="pay-month", value="2026-08")
            ]]],
        }
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
            "header_date": [[date(2026, 7, 16)]],
            "header_flag": [["*"]],
            "header_desc": [["myshop"]],
            "header_comment_meta": [[[dict(name="use-month", value="2026-07")]]],
            "posting_account": [[["支出:食費:外食", "負債:クレジット:楽天カード"]]],
            "posting_amount": [[[Decimal('2000'), None]]],
            "posting_commodity": [[["JPY", None]]],
            "posting_comment_meta": [[[
                [dict(name="member", value="忠利")],
                [dict(name="pay-month", value="2026-08")],
            ]]],
        }
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
            "header_date": [[date(2026, 7, 16)], [], [date(2026, 7, 20)]],
            "header_flag": [["*"], [], ["*"]],
            "header_desc": [["myshop"], [], ["mysupermarket"]],
            "posting_account": [
                [["支出:食費:外食", "負債:クレジット:楽天カード"]],
                [],
                [["支出:食費:食材", "資産:現金:財布"]],
            ],
            "posting_amount": [
                [[Decimal('2000'), None]],
                [],
                [[Decimal('1500'), None]],
            ],
            "posting_commodity": [
                [["JPY", None]],
                [],
                [[None, None]],
            ],
        }
    ),
])
def test_parse_posting(line, expected):
    p = parse_text(line)

    assert p.state == expected["state"]
    if "items" in expected:
        assert p.items == expected["items"]

    if "header_date" in expected:
        for i, part in enumerate(expected["header_date"]):
            for j, d in enumerate(part):
                assert p.items[i][j].header.header.date == d

    if "header_flag" in expected:
        for i, part in enumerate(expected["header_flag"]):
            for j, d in enumerate(part):
                assert p.items[i][j].header.header.flag == d

    if "header_desc" in expected:
        for i, part in enumerate(expected["header_desc"]):
            for j, d in enumerate(part):
                assert p.items[i][j].header.header.description == d

    if "header_meta" in expected:
        for i, part in enumerate(expected["header_meta"]):
            for j, d in enumerate(part):
                assert p.items[i][j].header.header.meta.name == d["name"]
                assert p.items[i][j].header.header.meta.value == d["value"]

    if "header_comment_meta" in expected:
        for i, part in enumerate(expected["header_comment_meta"]):
            for j, pp in enumerate(part):
                for k, d in enumerate(pp):
                    assert p.items[i][j].header.comments[k].meta.name == d["name"]
                    assert p.items[i][j].header.comments[k].meta.value == d["value"]

    if "posting_account" in expected:
        for i, part in enumerate(expected["posting_account"]):
            for j, pp in enumerate(part):
                for k, d in enumerate(pp):
                    assert p.items[i][j].postings[k].posting.account == d

    if "posting_amount" in expected:
        for i, part in enumerate(expected["posting_amount"]):
            for j, pp in enumerate(part):
                for k, d in enumerate(pp):
                    assert p.items[i][j].postings[k].posting.amount == d

    if "posting_commodity" in expected:
        for i, part in enumerate(expected["posting_commodity"]):
            for j, pp in enumerate(part):
                for k, d in enumerate(pp):
                    assert p.items[i][j].postings[k].posting.commodity == d

    if "posting_meta" in expected:
        for i, part in enumerate(expected["posting_meta"]):
            for j, pp in enumerate(part):
                for k, d in enumerate(pp):
                    assert p.items[i][j].postings[k].posting.meta.name == d["name"]
                    assert p.items[i][j].postings[k].posting.meta.value == d["value"]

    if "posting_comment_meta" in expected:
        for i, part in enumerate(expected["posting_comment_meta"]):
            for j, pp in enumerate(part):
                for k, ppp in enumerate(pp):
                    for l, d in enumerate(ppp):
                        assert p.items[i][j].postings[k].comments[l].meta.name == d["name"]
                        assert p.items[i][j].postings[k].comments[l].meta.value == d["value"]
