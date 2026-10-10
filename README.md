# Citation Auditor — Transparency-First RAG

A document question-answering application that retrieves relevant evidence from PDF documents, generates answers with source citations, and audits citation coverage.

The goal is to make document-based answers easier to inspect by showing the source passages used to produce them.

## Overview

Retrieval-Augmented Generation (RAG) systems can produce answers that are difficult to verify without inspecting their sources.

Citation Auditor explores a transparency-first approach by combining PDF ingestion, semantic retrieval, answer generation, citation validation, and evidence auditing.

Users can upload a PDF, ask questions about its contents, inspect the retrieved passages, and review citation audit results.

## Features

- **PDF ingestion:** Extracts text from PDF documents.
- **Text chunking:** Splits document text into smaller passages.
- **Semantic retrieval:** Uses embeddings to retrieve relevant passages.
- **Document isolation:** Filters retrieval results by the selected document.
- **Evidence-based answers:** Generates answers using retrieved passages.
- **Source citations:** Associates answer sentences with chunk IDs and page numbers.
- **Citation auditing:** Checks citation coverage and identifies citation issues.
- **Evidence checking:** Evaluates the similarity between a claim and its evidence.
- **Contradiction detection:** Provides a component for examining potentially contradictory statements.
- **Interactive interface:** Uses Streamlit to provide a simple interface for document questions and audit results.

> Note: Citation validity, semantic similarity, and factual correctness are different concepts. A valid citation does not automatically prove that the cited passage supports the associated claim.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive user interface |
| ChromaDB | Vector storage and retrieval |
| Sentence Transformers | Text embeddings and similarity |
| PyPDF | PDF text extraction |

## Project Structure

```text
citation-auditor/
├── app.py
├── backend/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── retrieval.py
│   ├── answer_generator.py
│   ├── citation_auditor.py
│   ├── evidence_checker.py
│   ├── contradiction_detector.py
│   └── audit_report.py
├── data/
│   ├── documents/
│   └── chroma/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

This is the intended project layout. The actual files and test locations may differ slightly.

## How It Works

1. **Document upload:** The user selects a PDF.
2. **Text extraction:** Text is extracted from the PDF.
3. **Chunk creation:** Extracted text is divided into passages.
4. **Embedding generation:** Sentence Transformers creates vector representations of the passages.
5. **Indexing:** ChromaDB stores the passages, embeddings, and metadata.
6. **Question retrieval:** The user's question is embedded and used to retrieve relevant passages.
7. **Answer generation:** Candidate answer sentences are selected from the retrieved evidence.
8. **Citation assignment:** Answer sentences are associated with source chunk IDs and page numbers.
9. **Audit:** The application displays citation and evidence-related checks.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd citation-auditor
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your actual repository URL.

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it in Command Prompt:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

## Usage

1. Start the application.
2. Upload a PDF document.
3. Process the document.
4. Enter a question about the document.
5. Generate an answer and audit report.
6. Inspect the answer, citations, and audit metrics.
7. Repeat with another PDF to test document isolation.

## Citation Audit Metrics

The application may display metrics such as:

| Metric | Meaning |
|---|---|
| Total Sentences | Number of answer sentences evaluated |
| Validly Cited | Sentences whose citations pass the implemented citation checks |
| Citation Coverage | Percentage of evaluated sentences with accepted citations |
| Uncited Sentences | Sentences without an accepted citation |
| Invalid Citations | Citations that fail the implemented validation checks |

These metrics describe the behavior of the implemented validator. They should not be interpreted as a guarantee of factual accuracy or complete evidence support.

## Testing

The project includes test scripts for individual components.

Run a test script from the project root using:

```bash
python test_retrieval.py
```

Other test scripts can be run similarly, for example:

```bash
python test_ingestion.py
python test_citation_auditor.py
python test_evidence_checker.py
python test_contradiction_detector.py
python test_audit_report.py
```

Run only the scripts that exist in your local repository.

Recommended manual tests:

- Ask a question whose answer appears in the selected document.
- Ask a question whose answer is absent from the document.
- Check whether citations point to the expected chunk and page.
- Switch between two different PDFs and check document isolation.
- Test claims that require verification rather than accepting similarity as proof.

## Limitations

- Semantic similarity does not establish factual correctness.
- Citation coverage does not measure whether every citation fully supports its claim.
- The quality of answers depends on PDF text extraction, chunking, retrieval, and answer-selection logic.
- Keyword-based checks may miss relevant evidence or accept weak matches.
- Contradiction detection should be evaluated separately before relying on it for factual verification.
- The application should be tested with varied documents and unsupported questions before being used for consequential decisions.

## Future Improvements

- Add more robust claim-to-evidence verification.
- Improve contradiction detection and evaluation.
- Add automated end-to-end tests.
- Evaluate retrieval quality using a representative question set.
- Improve answer relevance and reduce unrelated sentences.
- Add downloadable audit reports.
- Add document management and clearer source previews.

## Privacy and Security

Uploaded documents may contain personal or confidential information.

Do not commit private PDFs, API keys, credentials, virtual environments, or local vector databases to a public repository. Review `.gitignore` and verify the files being committed before publishing.

## Author

**Citation Auditor Project**

Developed as a project exploring document retrieval, evidence transparency, and citation auditing with Python.

## License

Choose and add a suitable open-source license before distributing the project. Do not claim a license until the corresponding license file has been added.