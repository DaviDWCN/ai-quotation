import os
from typing import Optional
import pypdf
import openpyxl
import docx
import pandas as pd
from io import BytesIO

class DocumentExtractor:
    def extract_text(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return ""

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return self._extract_pdf(file_path)
        elif ext in [".xlsx", ".xls"]:
            return self._extract_excel(file_path)
        elif ext == ".docx":
            return self._extract_docx(file_path)
        elif ext in [".txt", ".csv"]:
            return self._extract_plain_text(file_path)
        else:
            return ""

    def _extract_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += (page.extract_text() or "") + "\n"
        except Exception as e:
            print(f"Error extracting PDF: {e}")
        return text

    def _extract_excel(self, file_path: str) -> str:
        text = ""
        try:
            df_dict = pd.read_excel(file_path, sheet_name=None)
            if isinstance(df_dict, dict):
                for sheet_name, df in df_dict.items():
                    text += f"Sheet: {sheet_name}\n"
                    text += df.to_string(index=False) + "\n"
            else:
                text += df_dict.to_string(index=False) + "\n"
        except Exception as e:
            print(f"Error extracting Excel: {e}")
        return text

    def _extract_docx(self, file_path: str) -> str:
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
        return text

    def _extract_plain_text(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(f"Error extracting plain text: {e}")
            return ""
