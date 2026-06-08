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

def test_header_dash_2nd():
    line = "2025-03-15=2025-03-20 * 利払い"
    m = HEADER_RE.match(line)
    assert m is not None

    gd = m.groupdict()
    assert gd["date"] == "2025-03-15"
    assert gd["date2"] == "2025-03-20"
    assert gd["flag"] == "*"
    assert gd["description"].strip() == "利払い"

def test_header_slash_2nd():
    line = "2025/03/15=2025/03/20 * 利払い"
    m = HEADER_RE.match(line)
    assert m is not None

    gd = m.groupdict()
    assert gd["date"] == "2025/03/15"
    assert gd["date2"] == "2025/03/20"
    assert gd["flag"] == "*"
    assert gd["description"].strip() == "利払い"
