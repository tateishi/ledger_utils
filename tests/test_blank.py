import pytest
from ledger_utils.parser import parse_blank

@pytest.mark.parametrize("line, expected", [
    (
        "",
        {
            "raw_text": "",
        }
    ),
    (
        "   ",
        {
            "raw_text": "   ",
        }
    ),
])
def test_parse_blank(line, expected):
    p = parse_blank(line)

    assert p.raw_text == expected["raw_text"]
