from backend.retrieval import index_document, search_document


file_path = "data/documents/synopsissss.pdf"

# Store the document passages
index_document(file_path)

# Ask a question about the document
question = "What is the objective of the sleep disorder prediction project?"

results = search_document(question)

print("\nSearch Results:")

for result in results:
    print("\n------------------------------")
    print("Chunk ID:", result["chunk_id"])
    print("Page:", result["page"])
    print("Distance:", result["distance"])
    print("Evidence:", result["text"])