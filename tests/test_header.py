from datetime import date

import pytest
from ledger_utils import parser


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "2025-03-15 * 利払い",
            {
                "date": date(2025, 3, 15),
                "flag": "*",
                "description": "利払い",
            },
        ),
        (
            "2025/03/15 * 利払い",
            {
                "date": date(2025, 3, 15),
                "flag": "*",
                "description": "利払い",
            },
        ),
        (
            "2025-03-15=2025-03-20 * 利払い",
            {
                "date": date(2025, 3, 15),
                "date2": date(2025, 3, 20),
                "flag": "*",
                "description": "利払い",
            },
        ),
        (
            "2025-03-15=2025-03-20 (abcd) * 利払い",
            {
                "date": date(2025, 3, 15),
                "date2": date(2025, 3, 20),
                "flag": "*",
                "code": "abcd",
                "description": "利払い",
            },
        ),
        (
            "2025/03/15=2025/03/20 * 利払い",
            {
                "date": date(2025, 3, 15),
                "date2": date(2025, 3, 20),
                "flag": "*",
                "description": "利払い",
            },
        ),
        (
            "2025-03-15 * 利払い",
            {
                "date": date(2025, 3, 15),
                "flag": "*",
                "description": "利払い",
            },
        ),
        (
            "2025-03-15 * 利払い  ; 利息",
            {
                "date": date(2025, 3, 15),
                "flag": "*",
                "description": "利払い",
                "comment": "利息",
            },
        ),
        (
            "2025-03-15 * 利払い  ; :month:2026-07:",
            {
                "date": date(2025, 3, 15),
                "flag": "*",
                "description": "利払い",
                "tags": ["month", "2026-07"],
            },
        ),
        (
            "2025-03-15 * 利払い  ; month: 2026-07",
            {
                "date": date(2025, 3, 15),
                "flag": "*",
                "description": "利払い",
                "meta": dict(name="month", value="2026-07"),
            },
        ),
    ],
)
def test_parse_posting(line, expected):
    p = parser.parse_header(line)

    assert p.date == expected["date"]

    if "date2" in expected:
        assert p.date2 == expected["date2"]

    if "code" in expected:
        assert p.code == expected["code"]

    if "flag" in expected:
        assert p.flag == expected["flag"]

    if "description" in expected:
        assert p.description == expected["description"]

    if "comment" in expected:
        assert p.comment == expected["comment"]

    if "tags" in expected:
        for i, tag in enumerate(expected["tags"]):
            assert p.tags[i].tag == tag

    if "meta" in expected:
        assert p.meta.name == expected["meta"]["name"]
        assert p.meta.value == expected["meta"]["value"]
