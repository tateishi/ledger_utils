import pytest
from ledger_utils.parser import parse_posting
from decimal import Decimal

@pytest.mark.parametrize("line, expected", [
    (
        "    Assets:Cash Reserve Fund    1200 JPY",
        {
            "account": "Assets:Cash Reserve Fund",
            "commodity_pre": None,
            "amount": Decimal("1200"),
            "commodity_post": "JPY",
            "comment": None,
        }
    ),
    (
        "    Expenses:Food:Lunch    -1,200",
        {
            "account": "Expenses:Food:Lunch",
            "commodity_pre": None,
            "amount": Decimal("-1200"),
            "commodity_post": None,
            "comment": None,
        }
    ),
    (
        "    Expenses:Food:Lunch    JPY   -1,200",
        {
            "account": "Expenses:Food:Lunch",
            "commodity_pre": "JPY",
            "amount": Decimal("-1200"),
            "commodity_post": None,
            "comment": None,
        }
    ),
    (
        "    Liabilities:Card 1    5000    ; :urgent:tag1:",
        {
            "account": "Liabilities:Card 1",
            "commodity_pre": None,
            "amount": Decimal("5000"),
            "commodity_post": None,
            "comment": ":urgent:tag1:",
            "tags": ["urgent", "tag1"],
        }
    ),
    (
        "    Liabilities:Card 1    5000    ; month: 2026-07",
        {
            "account": "Liabilities:Card 1",
            "commodity_pre": None,
            "amount": Decimal("5000"),
            "commodity_post": None,
            "comment": "month: 2026-07",
            "meta": dict(name="month", value="2026-07")
        }
    ),
    (
        "    Liabilities:Card 1    50.25 USD   ; month: 2026-07",
        {
            "account": "Liabilities:Card 1",
            "commodity_pre": None,
            "amount": Decimal("50.25"),
            "commodity_post": "USD",
            "comment": "month: 2026-07",
            "meta": dict(name="month", value="2026-07")
        }
    ),
    (
        "    Liabilities:Card 1   USD  50.25 USD",
        {
            "account": "Liabilities:Card 1",
            "commodity_pre": "USD",
            "amount": Decimal("50.25"),
            "commodity_post": "USD",
            "comment": None,
            "commodity": "USD",
            "commodity_order": "both",
        }
    ),
    (
        "    Liabilities:Card 1   USD  50.25 JPY",
        {
            "account": "Liabilities:Card 1",
            "commodity_pre": "USD",
            "amount": Decimal("50.25"),
            "commodity_post": "JPY",
            "comment": None,
            "commodity": "USD",
            "commodity_order": "conflict",
        }
    ),
    (
        "    Liabilities:Card 1   USD  50.25  ",
        {
            "account": "Liabilities:Card 1",
            "commodity_pre": "USD",
            "amount": Decimal("50.25"),
            "commodity_post": None,
            "comment": None,
            "commodity": "USD",
            "commodity_order": "pre",
        }
    ),
    (
        "    Liabilities:Card 1   5025  JPY ",
        {
            "account": "Liabilities:Card 1",
            "commodity_pre": None,
            "amount": Decimal("5025"),
            "commodity_post": "JPY",
            "comment": None,
            "commodity": "JPY",
            "commodity_order": "post",
        }
    ),
    (
        "    Liabilities:Card 1   5025   ",
        {
            "account": "Liabilities:Card 1",
            "commodity_pre": None,
            "amount": Decimal("5025"),
            "commodity_post": None,
            "comment": None,
            "commodity": None,
            "commodity_order": "none",
        }
    ),
])
def test_parse_posting(line, expected):
    p = parse_posting(line)

    assert p.account == expected["account"]
    assert p.commodity_pre == expected["commodity_pre"]
    assert p.amount == expected["amount"]
    assert p.commodity_post == expected["commodity_post"]
    assert p.comment == expected["comment"]

    if "tags" in expected:
        for i, tag in enumerate(expected["tags"]):
            assert p.tags[i].tag == tag

    if "meta" in expected:
        assert p.meta.name == expected["meta"]["name"]
        assert p.meta.value == expected["meta"]["value"]

    if "commodity" in expected:
        assert p.commodity == expected["commodity"]

    if "commodity_order" in expected:
        assert p.commodity_order == expected["commodity_order"]
