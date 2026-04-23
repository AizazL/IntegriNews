from io import BytesIO
from pathlib import Path

import pdfplumber
from docx import Document
from fastapi import UploadFile


class UnsupportedFileTypeError(ValueError):
    pass


def extract_text_from_bytes(filename: str, payload: bytes) -> str:
    suffix = Path(filename).suffix.lower()

    if suffix == ".txt":
        return payload.decode("utf-8", errors="ignore").strip()

    if suffix == ".docx":
        document = Document(BytesIO(payload))
        return "\n".join(paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()).strip()

    if suffix == ".pdf":
        with pdfplumber.open(BytesIO(payload)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()

    raise UnsupportedFileTypeError(f"Unsupported file type: {suffix or 'unknown'}")


async def extract_text_from_upload(file: UploadFile) -> str:
    payload = await file.read()
    filename = file.filename or "upload.txt"
    return extract_text_from_bytes(filename, payload)
