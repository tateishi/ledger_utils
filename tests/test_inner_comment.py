import pytest
from ledger_utils.parser import parse_inner_comment

@pytest.mark.parametrize("line, expected", [
    (
        "     ; :urgent:tag1:",
        {
            "comment": ":urgent:tag1:",
            "tags": ["urgent", "tag1"],
        }
    ),
    (
        "     ; :urgent:tag1:tag2:",
        {
            "comment": ":urgent:tag1:tag2:",
            "tags": ["urgent", "tag1", "tag2"],
        }
    ),
    (
        "     ; pay_month: 2026-08",
        {
            "comment": "pay_month: 2026-08",
            "meta": dict(name="pay_month", value="2026-08")
        }
    ),
])
def test_parse_inner_comment(line, expected):
    p = parse_inner_comment(line)

    assert p.comment == expected["comment"]

    if "tags" in expected:
        for i, tag in enumerate(expected["tags"]):
            assert p.tags[i].tag == tag

    if "meta" in expected:
        assert p.meta.name == expected["meta"]["name"]
        assert p.meta.value == expected["meta"]["value"]
