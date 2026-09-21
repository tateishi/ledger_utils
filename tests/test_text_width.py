import pytest

from ledger_utils import text


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "abc",
            {
                "length": 3,
                "width": 3,
            },
        ),
        (
            "あいう",
            {
                "length": 3,
                "width": 6,
            },
        ),
        (
            "資産:現金:財布",
            {
                "length": 8,
                "width": 14,
            },
        ),
    ],
)
def test_text_utils(line, expected):
    actual_length = len(line)
    actual_width = text.width.wcswidth(line)

    if "length" in expected:
        assert actual_length == expected["length"]

    if "width" in expected:
        assert actual_width == expected["width"]
