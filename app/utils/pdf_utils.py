import re

import pymupdf

from app.config import settings


def clean_text(text: str):
    # Removing non-alphanumeric characters and extra spaces
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'[^A-Za-z0-9.,!?\'"\s]+', '', text)  # Remove unwanted chars
    return text


def chunk_text(text: str, chunk_size: int = settings.chunk_length):
    if chunk_size is None:
        chunk_size = settings.chunk_length

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero")

    if chunk_size > len(text):
        raise ValueError("Chunk size must be less than or equal to length of text")

    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def extract_text_from_pdf(pdf_path: str):
    text = ""

    try:
        with  pymupdf.open(pdf_path) as doc:
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
    except Exception as e:
        raise Exception(f'Error while extracting text from {pdf_path}: {e}')

    return text
