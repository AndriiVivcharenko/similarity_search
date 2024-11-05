import re

import pymupdf

from app.config import settings


def clean_text(text):
    # Removing non-alphanumeric characters and extra spaces
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'[^A-Za-z0-9.,!?\'"\s]+', '', text)  # Remove unwanted chars
    return text

def chunk_text(text, chunk_size=settings.chunk_length):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def extract_text_from_pdf(pdf_path):
    text = ""
    with  pymupdf.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
    return text