import pytest
from ledger_utils import parser


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "",
            {
                "raw_text": "",
            },
        ),
        (
            "   ",
            {
                "raw_text": "   ",
            },
        ),
    ],
)
def test_parse_blank(line, expected):
    p = parser.parse_blank(line)

    assert p.raw_text == expected["raw_text"]
