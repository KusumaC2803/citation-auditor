import re
from pypdf import PdfReader


def load_pdf(file_path):
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    return pages


def create_chunks(pages, chunk_size=1000):
    chunks = []
    chunk_number = 1

    for page in pages:
        sentences = re.split(r'(?<=[.!?])\s+', page["text"])

        current_chunk = ""

        for sentence in sentences:
            if not sentence.strip():
                continue

            if len(current_chunk) + len(sentence) > chunk_size:
                if current_chunk:
                    chunks.append({
                        "chunk_id": f"C{chunk_number:04d}",
                        "page": page["page"],
                        "text": current_chunk.strip()
                    })

                    chunk_number += 1

                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence

        if current_chunk.strip():
            chunks.append({
                "chunk_id": f"C{chunk_number:04d}",
                "page": page["page"],
                "text": current_chunk.strip()
            })

            chunk_number += 1

    return chunks