from ledger_utils.parser.parser.header_parser import HEADER_RE


def test_header_simple():
    line = "2025-03-15 * 利払い"
    m = HEADER_RE.match(line)
    assert m is not None

    gd = m.groupdict()
    assert gd["date"] == "2025-03-15"
    assert gd["flag"] == "*"
    assert gd["description"].strip() == "利払い"

def test_header_date_slash():
    line = "2025/03/15 * 利払い"
    m = HEADER_RE.match(line)
    assert m is not None

    gd = m.groupdict()
    assert gd["date"] == "2025/03/15"
    assert gd["flag"] == "*"
    assert gd["description"].strip() == "利払い"
