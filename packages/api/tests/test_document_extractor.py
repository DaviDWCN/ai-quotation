import os
import pytest
from pathlib import Path
from src.ai.document_extractor import (
    extract_text,
    extract_text_from_txt
)

@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"

def test_extract_text_from_txt(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test.txt"
    content = "Hello, world!"
    p.write_text(content)

    extracted = extract_text_from_txt(str(p))
    assert extracted == content

def test_extract_text_from_eml(fixtures_dir):
    fixture_path = fixtures_dir / "sample_email.eml"
    if fixture_path.exists():
        extracted = extract_text(str(fixture_path))
        assert "Solar Panels" in extracted
        assert "SP-500" in extracted

def test_extract_text_routing(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("plain text")
    assert extract_text(str(p)) == "plain text"

def test_extract_text_non_existent():
    with pytest.raises(FileNotFoundError):
        extract_text("non_existent_file.txt")
