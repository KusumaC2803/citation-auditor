import os
import streamlit as st

from backend.retrieval import index_document
from backend.answer_generator import generate_answer
from backend.audit_report import create_audit_report


st.set_page_config(page_title="Citation Auditor", page_icon="🔎", layout="wide")

st.markdown(
    """
    <style>
        .main-title { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.2rem; }
        .subtitle { color: #777777; font-size: 1rem; margin-bottom: 1.5rem; }
        div[data-testid="stMetric"] {
            background-color: #f7f9fc; padding: 15px; border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">🔎 Citation Auditor</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="subtitle">
        A transparency-first document assistant that helps you inspect
        citations, source evidence, and potential contradictions.
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()


# Initialize session state.
for key, default in {
    "document_processed": False,
    "document_id": None,
    "last_result": None,
    "last_report": None,
    "last_question": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# Sidebar: upload and process a PDF.
with st.sidebar:
    st.header("📄 Document")
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    st.caption("Upload a document to search its contents and inspect citations.")

    if uploaded_file is not None:
        st.write(f"**Selected file:** {uploaded_file.name}")

        if st.button("Process Document", use_container_width=True):
            try:
                os.makedirs("data/documents", exist_ok=True)
                document_path = os.path.join(
                    "data", "documents", "uploaded_document.pdf"
                )

                with open(document_path, "wb") as file:
                    file.write(uploaded_file.getvalue())

                with st.spinner("Extracting text and indexing your document..."):
                    document_id = index_document(document_path)

                st.session_state["document_id"] = document_id
                st.session_state["document_path"] = document_path
                st.session_state["document_name"] = uploaded_file.name
                st.session_state["document_processed"] = True

                # Remove the previous document's answer and audit.
                st.session_state["last_result"] = None
                st.session_state["last_report"] = None
                st.session_state["last_question"] = None
                st.success("Document processed successfully!")

            except Exception as error:
                st.error(f"Document processing failed: {error}")

    if st.session_state.get("document_processed", False):
        st.success(f'Ready: {st.session_state["document_name"]}')

    st.divider()
    st.info(
        "This prototype processes documents locally. Review local storage "
        "and data handling before uploading confidential documents."
    )


# Question input.
if not st.session_state.get("document_processed", False):
    st.info("👈 Upload a PDF and click **Process Document** to get started.")
else:
    st.subheader("💬 Ask a Question")
    question = st.text_input(
        "Enter your question about the document",
        placeholder="What is the objective of the sleep disorder prediction project?",
        key="question_input",
    )

    if st.button("Generate Answer and Audit", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Retrieving evidence and auditing citations..."):
                    result = generate_answer(
                        question,
                        document_id=st.session_state.get("document_id"),
                    )

                answer = result.get("answer", "")
                sources = result.get("sources", [])
                answer_sentences = result.get("sentences")

                if not answer.strip():
                    st.session_state["last_result"] = None
                    st.session_state["last_report"] = None
                    st.session_state["last_question"] = None
                    st.warning("No answer was generated. Try rephrasing your question.")

                elif not sources or (
                    answer_sentences is not None and len(answer_sentences) == 0
                ):
                    # A fallback explanation is not a factual claim to audit.
                    report = {
                        "total_sentences": 0,
                        "cited_sentences": 0,
                        "uncited_sentences": 0,
                        "invalid_citations": 0,
                        "citation_coverage_percent": 0.0,
                        "sentences": [],
                    }
                    st.session_state["last_result"] = result
                    st.session_state["last_report"] = report
                    st.session_state["last_question"] = question

                else:
                    report = create_audit_report(
                        answer=answer,
                        sources=sources,
                        answer_sentences=answer_sentences,
                    )
                    st.session_state["last_result"] = result
                    st.session_state["last_report"] = report
                    st.session_state["last_question"] = question

            except Exception as error:
                st.error(f"Answer generation or auditing failed: {error}")


# Display the latest answer and audit.
if (
    st.session_state.get("last_result") is not None
    and st.session_state.get("last_report") is not None
):
    result = st.session_state["last_result"]
    report = st.session_state["last_report"]
    sources = result.get("sources", [])

    st.divider()
    st.subheader("📝 Answer")

    answer_sentences = result.get("sentences")
    if answer_sentences:
        for sentence in answer_sentences:
            citation = sentence.get("citation", "")
            st.markdown(f'{sentence["text"]} **{citation}**')
    else:
        st.write(result.get("answer", ""))

    st.caption(
        "Answers are assembled from retrieved document sentences. Citation "
        "validity does not guarantee that a claim is factually correct or "
        "adequately supported."
    )

    st.divider()
    st.subheader("📊 Citation Audit")

    if report["total_sentences"] == 0:
        st.info(
            "No evidence-backed answer sentences were available for auditing. "
            "Citation coverage is not applicable because the retrieved evidence "
            "did not provide a sufficiently relevant answer."
        )
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sentences", report["total_sentences"])
        col2.metric("Validly Cited", report["cited_sentences"])
        col3.metric(
            "Citation Coverage",
            f'{report["citation_coverage_percent"]:.2f}%',
        )

        col4, col5 = st.columns(2)
        col4.metric("Uncited Sentences", report["uncited_sentences"])
        col5.metric("Invalid Citations", report["invalid_citations"])

        st.caption(
            "Citation coverage measures the percentage of audited sentences "
            "whose citations match retrieved source records. It is not a "
            "measure of factual accuracy."
        )

    st.divider()
    st.subheader("🔍 Sentence Audit")

    if not report["sentences"]:
        st.warning("No evidence-backed sentences were available for auditing.")
    else:
        for index, item in enumerate(report["sentences"], start=1):
            with st.expander(f'Sentence {index}: {item["sentence"][:100]}'):
                st.write("#### Citation Status")
                citation_status = item["citation_status"]

                if citation_status == "CITATION_FOUND":
                    st.success("Citation found and source reference is valid.")
                elif citation_status == "INVALID_CITATION":
                    st.error("Invalid citation: the referenced source was not found.")
                else:
                    st.warning("This sentence does not have a valid citation.")

                st.write("#### Evidence Verification")
                if item["evidence_checks"]:
                    for check in item["evidence_checks"]:
                        st.write(
                            f'**Source:** {check["chunk_id"]} — Page {check["page"]}'
                        )
                        st.metric(
                            "Semantic Similarity",
                            f'{check["similarity"]:.3f}',
                        )

                        if check["support_status"] == "POSSIBLY_SUPPORTED":
                            st.success(
                                "Possibly supported — manual verification is still recommended."
                            )
                        else:
                            st.warning(
                                "Needs review — the evidence may be insufficient."
                            )

                        matching_source = next(
                            (
                                source for source in item["citations"]
                                if source["chunk_id"] == check["chunk_id"]
                                and source["page"] == check["page"]
                            ),
                            None,
                        )

                        if matching_source:
                            with st.expander("📄 View Cited Evidence"):
                                st.write(matching_source["evidence"])

                        st.caption(
                            "Semantic similarity is an estimate, not proof that "
                            "the passage supports the claim."
                        )
                else:
                    st.info("No evidence checks are available for this sentence.")

                if item["contradictions"]:
                    st.write("#### ⚠️ Potential Contradictions")
                    for contradiction in item["contradictions"]:
                        st.warning(contradiction["other_sentence"])
                        st.caption(
                            f'Contradiction score: {contradiction["score"]:.3f}'
                        )

    st.divider()
    st.subheader("📚 Retrieved Source Evidence")

    if not sources:
        st.info("No source passages were retrieved.")
    else:
        for source in sources:
            with st.expander(f'{source["chunk_id"]} — Page {source["page"]}'):
                st.write(source["text"])
                if "distance" in source:
                    st.caption(f'Retrieval distance: {source["distance"]:.3f}')

    st.divider()
    st.caption(
        "Citation Auditor is a prototype. Citation matching, semantic similarity, "
        "and contradiction detection can produce incorrect results. Verify "
        "important claims against the original document."
    )
