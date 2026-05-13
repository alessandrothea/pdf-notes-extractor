from pathlib import Path

import pymupdf
import pytest

from extract_pdf_annotations import extract_annotations

PROCUREMENT_PDF = Path("/Users/ale/Desktop/procurement.pdf")


def test_regression_marked_text_when_run_starts_before_quad(highlight_pdf):
    """Marked text must be non-empty even when the text run starts before the highlight region.

    This was the original bug: _extract_quad_text checked only the run's starting x-coordinate
    against QuadPoints, so any run beginning before the highlight region returned ''.
    """
    result = extract_annotations(highlight_pdf)
    assert len(result) == 1
    assert result[0]["marked_text"] != "", "marked_text was empty — regression!"
    assert "brown" in result[0]["marked_text"]
    assert "fox" in result[0]["marked_text"]


def test_highlight_returns_expected_fields(highlight_pdf):
    result = extract_annotations(highlight_pdf)
    a = result[0]
    assert set(a.keys()) == {"page", "section", "type", "author", "date", "subject", "content", "marked_text", "color"}
    assert a["page"] == 1
    assert a["type"] == "Highlight"


def test_note_annotation_content_and_author(note_pdf):
    result = extract_annotations(note_pdf)
    assert len(result) == 1
    a = result[0]
    assert a["type"] == "Note"
    assert a["content"] == "Test note content"
    assert a["author"] == "Alice"
    assert a["marked_text"] == ""


def test_annotation_color_as_hex(colored_highlight_pdf):
    result = extract_annotations(colored_highlight_pdf)
    assert len(result) == 1
    assert result[0]["color"] == "#00FF00"


def test_multi_page_section_assignment(multi_page_pdf):
    result = extract_annotations(multi_page_pdf)
    assert len(result) == 2
    assert result[0]["page"] == 1
    assert result[0]["section"] == "Introduction"
    assert result[1]["page"] == 2
    assert result[1]["section"] == "Chapter One"


def test_skip_types_excluded(tmp_path):
    doc = pymupdf.Document()
    doc.new_page()
    page = doc[0]
    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(50, 50, 150, 70), "uri": "https://example.com"})
    path = tmp_path / "links.pdf"
    doc.save(str(path))
    doc.close()
    assert extract_annotations(path) == []


def test_empty_pdf(tmp_path):
    doc = pymupdf.Document()
    doc.new_page()
    doc[0].insert_text((50, 72), "No annotations here", fontsize=12)
    path = tmp_path / "empty.pdf"
    doc.save(str(path))
    doc.close()
    assert extract_annotations(path) == []


def test_multi_quad_highlight(tmp_path):
    """Multi-line highlight produces 8 vertices; both quads must be extracted."""
    doc = pymupdf.Document()
    doc.new_page()
    page = doc[0]
    page.insert_text((50, 72), "First line to highlight", fontsize=12)
    page.insert_text((50, 92), "Second line to highlight", fontsize=12)
    r1 = page.search_for("First line")[0]
    r2 = page.search_for("Second line")[0]
    annot = page.add_highlight_annot([r1, r2])
    annot.update()
    assert len(annot.vertices) == 8  # verify fixture before saving
    path = tmp_path / "multi_quad.pdf"
    doc.save(str(path))
    doc.close()
    result = extract_annotations(path)
    assert len(result) == 1
    assert result[0]["marked_text"] != ""


@pytest.mark.skipif(not PROCUREMENT_PDF.exists(), reason="procurement.pdf not present on Desktop")
def test_procurement_pdf_real_world():
    """Pins the real-world case that originally surfaced the marked-text bug."""
    result = extract_annotations(PROCUREMENT_PDF)
    assert len(result) == 1
    assert result[0]["marked_text"] != ""
    assert result[0]["content"] == "This is a tesrt"
