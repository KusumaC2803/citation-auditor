from backend.ingestion import load_pdf, create_chunks


file_path = "data/documents/synopsissss.pdf"

pages = load_pdf(file_path)

print("Total pages extracted:", len(pages))

chunks = create_chunks(pages)

print("Total chunks created:", len(chunks))

for chunk in chunks[:5]:
    print("\n----------------------------")
    print("Chunk ID:", chunk["chunk_id"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"][:200])