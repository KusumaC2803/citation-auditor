from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


# Load the embedding model once.
model = SentenceTransformer("all-MiniLM-L6-v2")


def check_evidence_support(claim, evidence, threshold=0.45):
    """
    Estimate how semantically similar a claim is to its evidence.

    Similarity is a review signal, not proof of factual support.
    """

    if not claim or not claim.strip():
        return {
            "claim": claim,
            "similarity": 0.0,
            "status": "NEEDS_REVIEW",
            "message": "The claim is empty."
        }

    if not evidence or not evidence.strip():
        return {
            "claim": claim,
            "similarity": 0.0,
            "status": "NEEDS_REVIEW",
            "message": "No evidence was provided."
        }

    # Convert the claim and evidence into embeddings.
    claim_embedding = model.encode(
        claim,
        convert_to_tensor=True
    )

    evidence_embedding = model.encode(
        evidence,
        convert_to_tensor=True
    )

    # Calculate semantic similarity.
    similarity = cos_sim(
        claim_embedding,
        evidence_embedding
    ).item()

    similarity = round(float(similarity), 3)

    # Assign a preliminary review status.
    if similarity >= threshold:
        status = "POSSIBLY_SUPPORTED"
        message = (
            "The evidence is semantically similar to the claim. "
            "Check whether it actually supports the statement."
        )
    else:
        status = "NEEDS_REVIEW"
        message = (
            "The evidence has relatively low semantic similarity "
            "to the claim. Manual verification is recommended."
        )

    return {
        "claim": claim,
        "similarity": similarity,
        "status": status,
        "message": message
    }