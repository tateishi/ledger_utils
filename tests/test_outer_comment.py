import pytest
from ledger_utils import parser


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "; normal comment",
            {
                "leader": ";",
                "comment": " normal comment",
            },
        ),
        (
            "# sharp comment",
            {
                "leader": "#",
                "comment": " sharp comment",
            },
        ),
        (
            "% percent comment",
            {
                "leader": "%",
                "comment": " percent comment",
            },
        ),
        (
            "| bar comment",
            {
                "leader": "|",
                "comment": " bar comment",
            },
        ),
        (
            "* star comment",
            {
                "leader": "*",
                "comment": " star comment",
            },
        ),
    ],
)
def test_parse_outer_comment(line, expected):
    p = parser.parse_outer_comment(line)

    assert p.leader == expected["leader"]
    assert p.comment == expected["comment"]
