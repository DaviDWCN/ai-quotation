import pytest
from src.ai.document_extractor import DocumentExtractor, extract_documents_text

def test_extract_text_from_txt():
    content = b"Hello World"
    filename = "test.txt"
    text = DocumentExtractor.extract_text(content, filename)
    assert "Hello World" in text

def test_extract_documents_text():
    files = [
        (b"Email content", "email.txt"),
        (b"Attachment content", "attachment.txt")
    ]
    combined = extract_documents_text(files)
    assert "--- Document: email.txt ---" in combined
    assert "Email content" in combined
    assert "--- Document: attachment.txt ---" in combined
    assert "Attachment content" in combined

def test_unsupported_format():
    content = b"Some data"
    filename = "test.unknown"
    text = DocumentExtractor.extract_text(content, filename)
    assert "[Unsupported format: .unknown]" in text
