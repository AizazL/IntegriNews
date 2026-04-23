from io import BytesIO

from docx import Document
from reportlab.pdfgen import canvas

from app.services.file_parser import UnsupportedFileTypeError, extract_text_from_bytes


def test_extract_text_from_txt_bytes():
    text = extract_text_from_bytes("notes.txt", b"Fact-checking still matters.")
    assert text == "Fact-checking still matters."


def test_extract_text_from_docx_bytes():
    buffer = BytesIO()
    document = Document()
    document.add_paragraph("Document based article text.")
    document.save(buffer)

    text = extract_text_from_bytes("article.docx", buffer.getvalue())

    assert "Document based article text." in text


def test_extract_text_from_pdf_bytes():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "PDF based article text.")
    pdf.save()

    text = extract_text_from_bytes("article.pdf", buffer.getvalue())

    assert "PDF based article text." in text


def test_extract_text_rejects_unknown_extensions():
    try:
        extract_text_from_bytes("article.md", b"# nope")
    except UnsupportedFileTypeError as exc:
        assert "Unsupported file type" in str(exc)
    else:
        raise AssertionError("Unsupported file types should raise an error.")
