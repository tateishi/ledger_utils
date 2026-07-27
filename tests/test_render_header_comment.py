import pytest
from ledger_utils import models, render
from ledger_utils.render import display


@pytest.mark.parametrize(
    "token, expected",
    [
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
    ],
)
def test_display(token, expected):
    text = render.render_header_comment(token)

    if "text" in expected:
        assert text == expected["text"]
