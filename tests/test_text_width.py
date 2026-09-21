import pytest

from ledger_utils import text


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "abc",
            3,
        ),
        (
            "あいう",
            3,
        ),
        (
            "資産:現金:財布",
            8,
        ),
    ],
)
def test_text_length(input, expected):
    actual = len(input)
    assert actual == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "abc",
            3,
        ),
        (
            "あいう",
            6,
        ),
        (
            "資産:現金:財布",
            14,
        ),
    ],
)
def test_text_width(input, expected):
    actual = text.width.wcswidth(input)
    assert actual == expected
