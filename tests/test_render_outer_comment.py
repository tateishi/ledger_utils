import pytest
from ledger_utils import models, render


@pytest.mark.parametrize(
    "token, expected",
    [
        (
            models.OuterComment(raw_text=";;;;"),
            {
                "text": ";;;;",
            },
        ),
        (
            models.OuterComment(raw_text="* test"),
            {
                "text": "* test",
            },
        ),
    ],
)
def test_display(token, expected):
    text = render.render_comment(token)

    if "text" in expected:
        assert text == expected["text"]
