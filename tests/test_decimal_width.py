from decimal import Decimal

import pytest
from ledger_utils import text


@pytest.mark.parametrize(
    "amount, expected",
    [
        (
            Decimal("1"),
            {
                "width": 1,
            },
        ),
        (
            Decimal("-1"),
            {
                "width": 2,
            },
        ),
        (
            Decimal("1.15"),
            {
                "width": 1,
            },
        ),
        (
            Decimal("-100.15"),
            {
                "width": 4,
            },
        ),
    ],
)
def test_decimal_width(amount, expected):
    w = text.width.integer_part_width(amount)

    if "width" in expected:
        assert w == expected["width"]
