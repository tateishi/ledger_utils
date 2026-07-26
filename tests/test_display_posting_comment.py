import pytest
from ledger_utils import models
from ledger_utils.format import display

@pytest.mark.parametrize("token, expected", [
    (
        models.InnerComment(comment="食費"),
        {
            "text": "    ; 食費",
        },
    ),
    (
        models.InnerComment(tags=[models.Tag("a"), models.Tag("b")]),
        {
            "text": "    ; :a:b:",
        },
    ),
    (
        models.InnerComment(meta=models.Meta(name="key", value="value")),
        {
            "text": "    ; key: value",
        },
    ),
])
def test_display(token, expected):
    text = display.display_posting_comment(token)

    if "text" in expected:
        assert text == expected["text"]
