import pytest
from ledger_utils import models
from ledger_utils.render import display
from datetime import date

@pytest.mark.parametrize("token, expected", [
    (
        models.Header(
            date=date(2026,7,1),
            flag="*",
            description="支払い",
        ),
        {
            "text": "2026-07-01 * 支払い",
        }
    ),
    (
        models.Header(
            date=date(2026,7,1),
            flag="*",
            description="支払い",
            meta=models.Meta(name="pay_month", value="2026-08")
        ),
        {
            "text": "2026-07-01 * 支払い  ; pay_month: 2026-08",
        }
    ),
])
def test_display(token, expected):
    text = display.display_header(token)

    if "text" in expected:
        assert text == expected["text"]
