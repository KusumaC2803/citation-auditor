import re


def split_into_sentences(answer):
    """Split an answer into individual sentences."""

    sentences = re.split(r"(?<=[.!?])\s+", answer.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def audit_citations(answer, sources):
    """Check whether answer sentences have source citations."""

    sentences = split_into_sentences(answer)
    audited_sentences = []

    for sentence in sentences:
        citation_pattern = r"\[(C\d+),\s*Page\s+(\d+)\]"
        citations = re.findall(citation_pattern, sentence)

        valid_citations = []

        for chunk_id, page_number in citations:
            for source in sources:
                if (
                    source["chunk_id"] == chunk_id
                    and str(source["page"]) == page_number
                ):
                    valid_citations.append({
                        "chunk_id": chunk_id,
                        "page": int(page_number),
                        "evidence": source["text"]
                    })

        if not citations:
            status = "UNCITED"
        elif valid_citations:
            status = "CITATION_FOUND"
        else:
            status = "INVALID_CITATION"

        audited_sentences.append({
            "sentence": sentence,
            "status": status,
            "citations": valid_citations
        })

    return audited_sentences