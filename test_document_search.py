from backend.retrieval import search_document, get_document_id

# Update this path if Main.pdf is stored elsewhere.
pdf_path = "data/documents/uploaded_document.pdf"

document_id = get_document_id(pdf_path)

print("\nDocument ID:")
print(document_id)

question = "Where is the Professional Summary?"

print("\nSearching document...\n")

results = search_document(
    question,
    top_k=5,
    document_id=document_id
)

if not results:
    print("No matching passages found.")

else:
    for result in results:
        print("-" * 60)
        print("Document:", result["document_name"])
        print("Chunk ID:", result["chunk_id"])
        print("Page:", result["page"])
        print("Distance:", result["distance"])
        print("Text:", result["text"])