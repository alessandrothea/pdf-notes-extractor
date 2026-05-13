import pytest
import pymupdf


@pytest.fixture
def highlight_pdf(tmp_path):
    """PDF with a highlight whose text run starts before the QuadPoints region.

    This is the primary regression fixture for the marked-text extraction bug.
    """
    doc = pymupdf.Document()
    doc.new_page()
    page = doc[0]
    page.insert_text((50, 72), "The quick brown fox jumps over the lazy dog", fontsize=12)
    rects = page.search_for("brown fox")
    assert rects, "search_for must find 'brown fox'"
    assert rects[0].x0 > 50, "highlight must start after the text run origin (regression condition)"
    annot = page.add_highlight_annot(rects[0])
    annot.update()
    path = tmp_path / "highlight.pdf"
    doc.save(str(path))
    doc.close()
    return path


@pytest.fixture
def note_pdf(tmp_path):
    """PDF with a /Text sticky-note annotation."""
    doc = pymupdf.Document()
    doc.new_page()
    page = doc[0]
    annot = page.add_text_annot((100, 100), "note marker")
    annot.set_info(title="Alice", content="Test note content")
    annot.update()
    path = tmp_path / "note.pdf"
    doc.save(str(path))
    doc.close()
    return path


@pytest.fixture
def colored_highlight_pdf(tmp_path):
    """PDF with a green (#00FF00) highlight annotation."""
    doc = pymupdf.Document()
    doc.new_page()
    page = doc[0]
    page.insert_text((50, 72), "Colored text to mark", fontsize=12)
    rects = page.search_for("Colored text")
    assert rects
    annot = page.add_highlight_annot(rects[0])
    annot.set_colors(stroke=(0.0, 1.0, 0.0))
    annot.update()
    path = tmp_path / "colored.pdf"
    doc.save(str(path))
    doc.close()
    return path


@pytest.fixture
def multi_page_pdf(tmp_path):
    """Two-page PDF with a TOC and one highlight per page."""
    doc = pymupdf.Document()
    doc.new_page()
    doc.new_page()
    # Keep explicit page references alive to avoid stale-object errors.
    p0 = doc[0]
    p1 = doc[1]
    p0.insert_text((50, 72), "Introduction text here", fontsize=12)
    p1.insert_text((50, 72), "Chapter One text here", fontsize=12)
    for page, term in [(p0, "Introduction"), (p1, "Chapter One")]:
        rects = page.search_for(term)
        assert rects
        annot = page.add_highlight_annot(rects[0])
        annot.update()
    doc.set_toc([[1, "Introduction", 1], [1, "Chapter One", 2]])
    path = tmp_path / "multi.pdf"
    doc.save(str(path))
    doc.close()
    return path


@pytest.fixture
def sample_annotations():
    """Synthetic annotation list for exporter tests — no PDF needed."""
    return [
        {
            "page": 1, "section": "", "type": "Highlight",
            "author": "Alice", "date": "2024-03-15 14:30",
            "subject": "", "content": "Great point!",
            "marked_text": "brown fox", "color": "#FFFF00",
        },
        {
            "page": 2, "section": "Methods", "type": "Note",
            "author": "", "date": "",
            "subject": "Key idea", "content": "Remember this",
            "marked_text": "", "color": "",
        },
    ]
