import pytest
from ledger_utils import models, render


@pytest.mark.parametrize(
    "token, expected",
    [
        (
            models.Blank(),
            {
                "text": "",
            },
        ),
        (
            models.Blank(raw_text=" "),
            {
                "text": " ",
            },
        ),
    ],
)
def test_display(token, expected):
    text = render.render_blank(token)

    if "text" in expected:
        assert text == expected["text"]
