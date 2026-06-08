from ledger_utils.parser import HEADER_RE, parse_header


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

def test_header_parser_simple():
    import datetime
    line = "2025-03-15 * 利払い"
    header = parse_header(line)

    assert header is not None
    assert header.raw_text == line
    assert header.date == datetime.date(2025,3,15)
    assert header.date2 is None
    assert header.code is None
    assert header.flag == "*"
    assert header.description == "利払い"
    assert header.comment == None
