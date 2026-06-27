import os
from typing import List, Union
from io import BytesIO
import pypdf
import openpyxl
import docx

class DocumentExtractor:
    @staticmethod
    def extract_text_from_pdf(content: bytes) -> str:
        pdf_file = BytesIO(content)
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    @staticmethod
    def extract_text_from_excel(content: bytes) -> str:
        excel_file = BytesIO(content)
        wb = openpyxl.load_workbook(excel_file, data_only=True)
        text = ""
        for sheet in wb.worksheets:
            text += f"Sheet: {sheet.title}\n"
            for row in sheet.iter_rows(values_only=True):
                text += "\t".join([str(cell) if cell is not None else "" for cell in row]) + "\n"
        return text

    @staticmethod
    def extract_text_from_docx(content: bytes) -> str:
        docx_file = BytesIO(content)
        doc = docx.Document(docx_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    @staticmethod
    def extract_text(content: bytes, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            return DocumentExtractor.extract_text_from_pdf(content)
        elif ext in [".xlsx", ".xls"]:
            return DocumentExtractor.extract_text_from_excel(content)
        elif ext in [".docx", ".doc"]:
            return DocumentExtractor.extract_text_from_docx(content)
        elif ext in [".txt", ".csv"]:
            return content.decode("utf-8", errors="replace")
        else:
            return f"[Unsupported format: {ext}]"

def extract_documents_text(files: List[tuple[bytes, str]]) -> str:
    extractor = DocumentExtractor()
    combined_text = ""
    for content, filename in files:
        combined_text += f"--- Document: {filename} ---\n"
        combined_text += extractor.extract_text(content, filename) + "\n"
    return combined_text
