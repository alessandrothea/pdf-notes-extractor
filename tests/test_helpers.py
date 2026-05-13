from extract_pdf_annotations import _section_for_page, _parse_pdf_date


# ── _section_for_page ──────────────────────────────────────────────────────────

def test_section_empty_sections():
    assert _section_for_page([], 5) == ""


def test_section_page_before_first_section():
    assert _section_for_page([(5, "Chapter 1")], 1) == ""


def test_section_exact_page_match():
    assert _section_for_page([(5, "Ch1")], 5) == "Ch1"


def test_section_page_within_section():
    assert _section_for_page([(1, "Intro"), (5, "Ch1")], 3) == "Intro"


def test_section_page_at_second_boundary():
    assert _section_for_page([(1, "Intro"), (5, "Ch1")], 5) == "Ch1"


def test_section_page_beyond_last_section():
    assert _section_for_page([(1, "A"), (5, "B"), (10, "C")], 99) == "C"


def test_section_single_entry():
    assert _section_for_page([(1, "Only")], 1) == "Only"


# ── _parse_pdf_date ────────────────────────────────────────────────────────────
# Assertions pin the actual output, which differs from a naive reading of the
# format strings because Python's strptime regex uses \d{1,2} (not \d{2}) for
# most fields, allowing backtracking that consumes fewer digits per field.

def test_date_full_with_d_prefix():
    # D:20240315143022 → slice to len("%Y%m%d%H%M%S")=12 → "202403151430"
    # strptime backtracks: %M=3 (1 digit), %S=0 (1 digit) → 14:03
    assert _parse_pdf_date("D:20240315143022") == "2024-03-15 14:03"


def test_date_without_prefix():
    assert _parse_pdf_date("20240315143022") == "2024-03-15 14:03"


def test_date_with_quoted_timezone():
    assert _parse_pdf_date("D:20240101120000+05'30'") == "2024-01-01 12:00"


def test_date_date_only_returns_raw():
    # 8-char date-only falls through all formats (slices are too short to match)
    assert _parse_pdf_date("D:20240315") == "20240315"


def test_date_unparseable_returns_raw():
    assert _parse_pdf_date("not-a-date") == "not-a-date"


def test_date_without_seconds():
    assert _parse_pdf_date("D:202403151430") == "2024-03-15 14:03"
