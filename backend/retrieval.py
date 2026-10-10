from pathlib import Path
import hashlib

import chromadb
from sentence_transformers import SentenceTransformer

from backend.ingestion import load_pdf, create_chunks


# Load the embedding model.
model = SentenceTransformer("all-MiniLM-L6-v2")


# Create a persistent ChromaDB database.
client = chromadb.PersistentClient(path="data/chroma")

collection = client.get_or_create_collection(
    name="citation_auditor"
)


def get_document_id(file_path):
    """Create a stable ID based on the document's contents."""

    file_path = Path(file_path)

    file_hash = hashlib.sha256()

    with file_path.open("rb") as file:
        for block in iter(lambda: file.read(8192), b""):
            file_hash.update(block)

    return file_hash.hexdigest()


def index_document(file_path):
    """Extract, split, and store passages for one document."""

    file_path = Path(file_path)
    document_id = get_document_id(file_path)

    pages = load_pdf(file_path)
    chunks = create_chunks(pages)

    if not chunks:
        print("No text found in the document.")
        return document_id

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts).tolist()

    chunk_ids = [
        f"{document_id}_{chunk['chunk_id']}"
        for chunk in chunks
    ]

    metadata = [
        {
            "document_id": document_id,
            "document_name": file_path.name,
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=chunk_ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadata,
    )

    print(
        f"Indexed {len(chunks)} chunks successfully "
        f"for {file_path.name}."
    )

    return document_id


def search_document(question, top_k=3, document_id=None):
    """
    Retrieve relevant passages.

    If document_id is supplied, search only within that document.
    """

    # Return immediately if the database is empty.
    if collection.count() == 0:
        return []

    # Create the question embedding.
    question_embedding = model.encode([question]).tolist()

    # Prepare the retrieval query.
    query_options = {
        "query_embeddings": question_embedding,
        "n_results": min(top_k, collection.count()),
    }

    # Restrict retrieval to the selected document.
    if document_id:
        query_options["where"] = {
            "document_id": document_id
        }

        # Do not use collection.count(where=...).
        # Instead, retrieve the count using get().
        matching_records = collection.get(
            where={"document_id": document_id},
            include=[]
        )

        matching_count = len(matching_records["ids"])

        # Return an empty list if this document has not been indexed.
        if matching_count == 0:
            return []

        # Limit retrieval to the number of chunks in this document.
        query_options["n_results"] = min(
            top_k,
            matching_count
        )

    # Search the database.
    results = collection.query(**query_options)

    matches = []

    if not results["ids"] or not results["ids"][0]:
        return matches

    # Format the retrieved passages.
    for i, stored_id in enumerate(results["ids"][0]):
        metadata = results["metadatas"][0][i]

        matches.append({
            "chunk_id": metadata["chunk_id"],
            "page": metadata["page"],
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i],
            "document_id": metadata["document_id"],
            "document_name": metadata["document_name"],
            "stored_id": stored_id,
        })

    return matches