import re

from backend.retrieval import search_document
from backend.evidence_checker import model


def get_question_type(question):
    """Identify the type of information requested."""

    question = question.lower().strip()

    if any(word in question for word in [
        "guarantee", "guarantees", "guaranteed",
        "prove", "proves", "proven",
    ]):
        return "verification"

    if any(word in question for word in [
        "algorithm", "algorithms", "classifier",
        "model", "models",
    ]):
        return "algorithms"

    if any(word in question for word in [
        "objective", "purpose", "goal", "aim",
    ]):
        return "objective"

    if any(word in question for word in [
        "technology", "technologies", "framework",
        "programming language", "tools used",
    ]):
        return "technology"

    return "general"


def sentence_matches_question_type(sentence, question_type):
    """Check whether a sentence matches the requested topic."""

    text = sentence.lower()

    if question_type == "verification":
        return any(term in text for term in [
            "guarantee",
            "guaranteed",
            "100% accuracy",
            "perfect accuracy",
            "accuracy of 100%",
            "prediction accuracy",
            "accuracy rate",
        ])

    if question_type == "algorithms":
        return any(term in text for term in [
            "algorithm",
            "classifier",
            "qda",
            "quadratic discriminant analysis",
            "gbc",
            "gradient boosting",
            "random forest",
            "linear regression",
            "decision tree",
            "decision trees",
            "neural network",
        ])

    if question_type == "objective":
        return any(term in text for term in [
            "objective",
            "purpose",
            "aim",
            "goal",
            "predict sleep disorders",
            "identifying conditions",
            "health-related data",
        ])

    if question_type == "technology":
        return any(term in text for term in [
            "python",
            "django",
            "javascript",
            "html",
            "css",
            "framework",
            "technology",
            "sqlite",
            "react",
        ])

    return True


def split_into_sentences(text):
    """Split retrieved text into sentences and useful headings."""

    parts = re.split(r"(?<=[.!?])\s+|\n+", text)

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def generate_answer(question, top_k=3, document_id=None):
    """
    Generate an evidence-based answer from the selected document.

    Each returned answer sentence retains its source chunk and page.
    """

    sources = search_document(
        question,
        top_k=top_k,
        document_id=document_id,
    )

    if not sources:
        return {
            "question": question,
            "answer": (
                "I could not find relevant evidence in the selected "
                "document to answer this question."
            ),
            "sources": [],
            "sentences": [],
        }

    question_embedding = model.encode(
        question,
        convert_to_tensor=True,
    )

    question_type = get_question_type(question)

    answer_sentences = []
    seen_sentences = set()

    for source in sources:
        text = source.get("text", "").strip()

        if not text:
            continue

        sentences = split_into_sentences(text)

        for sentence in sentences:
            normalized_sentence = sentence.lower().strip()

            if normalized_sentence in seen_sentences:
                continue

            # Exclude very short fragments, but allow meaningful headings.
            if len(sentence.split()) < 2:
                continue

            # Verification questions require explicit supporting language.
            if question_type == "verification":
                if not sentence_matches_question_type(
                    sentence, question_type
                ):
                    continue

            # Apply topic filtering for specialized questions.
            elif question_type != "general":
                if not sentence_matches_question_type(
                    sentence, question_type
                ):
                    continue

            sentence_embedding = model.encode(
                sentence,
                convert_to_tensor=True,
            )

            similarity = model.similarity(
                question_embedding,
                sentence_embedding,
            ).item()

            # Use a more permissive threshold for candidate evidence.
            if similarity < 0.20:
                continue

            seen_sentences.add(normalized_sentence)

            citation = (
                f'[{source["chunk_id"]}, Page {source["page"]}]'
            )

            answer_sentences.append({
                "text": sentence,
                "citation": citation,
                "similarity": round(float(similarity), 3),
                "chunk_id": source["chunk_id"],
                "page": source["page"],
            })

    if not answer_sentences:
        if question_type == "verification":
            message = (
                "The retrieved evidence does not establish the "
                "guarantee asked about. This does not prove that "
                "the guarantee is false; the available evidence "
                "is insufficient to verify it."
            )
        else:
            message = (
                "I could not find sufficiently relevant evidence "
                "in the selected document to answer this question."
            )

        return {
            "question": question,
            "answer": message,
            "sources": sources,
            "sentences": [],
        }

    # Rank the candidate sentences by similarity to the question.
    answer_sentences.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    # Keep the answer concise.
    answer_sentences = answer_sentences[:5]

    answer = " ".join(
        f'{item["text"]} {item["citation"]}'
        for item in answer_sentences
    )

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "sentences": answer_sentences,
    }