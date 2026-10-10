"""
Citation Auditor — Transparency-First RAG

Backend package for document ingestion, semantic retrieval,
answer generation, citation validation, evidence checking,
contradiction detection, and audit report generation.

Modules:
    ingestion:
        Extracts text from PDF documents and splits it into chunks.

    retrieval:
        Generates embeddings, indexes document chunks, and retrieves
        relevant passages from the selected document.

    answer_generator:
        Generates evidence-based answers with source citations.

    citation_auditor:
        Validates citations associated with generated answers.

    evidence_checker:
        Evaluates the relevance of evidence to a given claim or answer.

    contradiction_detector:
        Identifies potential contradictions between statements.

    audit_report:
        Produces an audit report containing citation and evidence results.
"""

__version__ = "1.0.0"
__author__ = "Citation Auditor Project"