from backend.evidence_checker import check_evidence_support
from backend.contradiction_detector import detect_contradiction

import re


def create_audit_report(answer, sources, answer_sentences=None):
    """Audit answer citations against retrieved source records."""

    audited_sentences = []

    # Use structured sentences when available.
    if answer_sentences is not None:
        sentence_items = answer_sentences
    else:
        sentence_items = []

        # Basic fallback for a complete answer string.
        for text in re.split(r"(?<=[.!?])\s+", answer):
            text = text.strip()

            if text:
                sentence_items.append({"text": text})

    # Build a lookup of the retrieved sources.
    source_lookup = {
        (
            str(source["chunk_id"]),
            int(source["page"])
        ): source
        for source in sources
    }

    # Audit every answer sentence exactly once.
    for item in sentence_items:
        text = item["text"].strip()
        citation = item.get("citation", "")

        if not citation:
            match = re.search(
                r"\[(C\d+),\s*Page\s*(\d+)\]",
                text
            )

            if match:
                citation = match.group(0)
                claim = text[:match.start()].strip()
            else:
                claim = text
        else:
            claim = text

        match = re.search(
            r"\[(C\d+),\s*Page\s*(\d+)\]",
            citation
        )

        if not match:
            status = "UNCITED"
            cited_sources = []
        else:
            chunk_id = match.group(1)
            page = int(match.group(2))

            source = source_lookup.get((chunk_id, page))

            if source is None:
                status = "INVALID_CITATION"
                cited_sources = []
            else:
                status = "CITATION_FOUND"
                cited_sources = [source]

        sentence_report = {
            "sentence": claim,
            "citation_status": status,
            "citations": [],
            "evidence_checks": [],
            "contradictions": []
        }

        # Check the actual source associated with the citation.
        for source in cited_sources:
            sentence_report["citations"].append({
                "chunk_id": source["chunk_id"],
                "page": source["page"],
                "evidence": source["text"]
            })

            evidence_result = check_evidence_support(
                claim=claim,
                evidence=source["text"]
            )

            sentence_report["evidence_checks"].append({
                "chunk_id": source["chunk_id"],
                "page": source["page"],
                "similarity": evidence_result["similarity"],
                "support_status": evidence_result["status"]
            })

        audited_sentences.append(sentence_report)

    # Flag potential contradictions between validly cited claims.
    for i in range(len(audited_sentences)):
        for j in range(i + 1, len(audited_sentences)):

            first = audited_sentences[i]
            second = audited_sentences[j]

            if first["citation_status"] != "CITATION_FOUND":
                continue

            if second["citation_status"] != "CITATION_FOUND":
                continue

            result = detect_contradiction(
                first["sentence"],
                second["sentence"]
            )

            if result["status"] == "POTENTIAL_CONTRADICTION":
                first["contradictions"].append({
                    "other_sentence": second["sentence"],
                    "score": result["contradiction_score"]
                })

                second["contradictions"].append({
                    "other_sentence": first["sentence"],
                    "score": result["contradiction_score"]
                })

    total = len(audited_sentences)

    cited = sum(
        item["citation_status"] == "CITATION_FOUND"
        for item in audited_sentences
    )

    uncited = sum(
        item["citation_status"] == "UNCITED"
        for item in audited_sentences
    )

    invalid = sum(
        item["citation_status"] == "INVALID_CITATION"
        for item in audited_sentences
    )

    return {
        "total_sentences": total,
        "cited_sentences": cited,
        "uncited_sentences": uncited,
        "invalid_citations": invalid,
        "citation_coverage_percent": round(
            cited / total * 100, 2
        ) if total else 0,
        "sentences": audited_sentences
    }