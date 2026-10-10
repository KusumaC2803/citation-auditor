from transformers import pipeline


# Load the natural language inference model.
nli_model = pipeline(
    "text-classification",
    model="cross-encoder/nli-deberta-v3-small",
    top_k=None
)


def detect_contradiction(statement_a, statement_b):
    """Estimate the relationship between two statements."""

    predictions = nli_model(
        statement_a,
        text_pair=statement_b
    )

    # Handle the model's prediction output.
    if predictions and isinstance(predictions[0], list):
        predictions = predictions[0]

    scores = {
        item["label"].lower(): item["score"]
        for item in predictions
    }

    contradiction_score = scores.get("contradiction", 0.0)
    entailment_score = scores.get("entailment", 0.0)
    neutral_score = scores.get("neutral", 0.0)

    if contradiction_score >= 0.70:
        status = "POTENTIAL_CONTRADICTION"
    elif entailment_score >= 0.70:
        status = "POSSIBLE_ENTAILMENT"
    else:
        status = "INCONCLUSIVE"

    return {
        "statement_a": statement_a,
        "statement_b": statement_b,
        "contradiction_score": round(contradiction_score, 3),
        "entailment_score": round(entailment_score, 3),
        "neutral_score": round(neutral_score, 3),
        "status": status
    }