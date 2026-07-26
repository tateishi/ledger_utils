import pytest
from ledger_utils import models
from ledger_utils.render import display

@pytest.mark.parametrize("token, expected", [
    (
        models.OuterComment(raw_text=";;;;"),
        {
            "text": ";;;;",
        }
    ),
    (
        models.OuterComment(raw_text="* test"),
        {
            "text": "* test",
        }
    ),
])
def test_display(token, expected):
    text = display.display_comment(token)

    if "text" in expected:
        assert text == expected["text"]
