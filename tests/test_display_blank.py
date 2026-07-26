import pytest
from ledger_utils import models
from ledger_utils.render import display

@pytest.mark.parametrize("token, expected", [
    (
        models.Blank(),
        {
            "text": "",
        }
    ),
    (
        models.Blank(raw_text=" "),
        {
            "text": " ",
        }
    ),
])
def test_display(token, expected):
    text = display.display_blank(token)

    if "text" in expected:
        assert text == expected["text"]
