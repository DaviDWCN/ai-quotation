import pytest
import os
import pypdf
from src.ai.document_extractor import DocumentExtractor
from docx import Document
import pandas as pd

def test_extract_pdf(tmp_path):
    # Create a simple PDF
    pdf_path = tmp_path / "test.pdf"
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(pdf_path, "wb") as f:
        writer.write(f)

    extractor = DocumentExtractor()
    text = extractor.extract_text(str(pdf_path))
    assert isinstance(text, str)

def test_extract_docx(tmp_path):
    docx_path = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("Hello World")
    doc.save(docx_path)

    extractor = DocumentExtractor()
    text = extractor.extract_text(str(docx_path))
    assert "Hello World" in text

def test_extract_excel(tmp_path):
    xlsx_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df.to_excel(xlsx_path, index=False)

    extractor = DocumentExtractor()
    text = extractor.extract_text(str(xlsx_path))
    assert "Sheet: Sheet1" in text
    assert "1" in text
    assert "2" in text

def test_extract_plain_text():
    extractor = DocumentExtractor()
    file_path = "packages/api/tests/fixtures/sample_quotation.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write("Mock Customer\nMOCK-001\n10\npcs\n100")

    text = extractor.extract_text(file_path)
    assert "Mock Customer" in text
    assert "MOCK-001" in text

def test_extract_non_existent_file():
    extractor = DocumentExtractor()
    text = extractor.extract_text("non_existent_file.pdf")
    assert text == ""
