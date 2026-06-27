import os
from typing import Optional
import pypdf
import openpyxl
import pandas as pd
from docx import Document

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_excel(file_path: str) -> str:
    # Use pandas for easier text representation of excel
    df_dict = pd.read_excel(file_path, sheet_name=None)
    text = ""
    for sheet_name, df in df_dict.items():
        text += f"Sheet: {sheet_name}\n"
        text += df.to_string(index=False) + "\n\n"
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_text(file_path: str) -> str:
    _, ext = os.path.splitext(file_path.lower())
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".xlsx", ".xls"]:
        return extract_text_from_excel(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext in [".txt", ".csv", ".eml"]:
        return extract_text_from_txt(file_path)
    else:
        # Fallback to plain text for unknown extensions
        try:
            return extract_text_from_txt(file_path)
        except Exception:
            return ""
