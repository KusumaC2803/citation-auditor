from backend.audit_report import create_audit_report


answer = (
    "The model achieved 95% accuracy [C0005, Page 4]. "
    "The model achieved 60% accuracy [C0005, Page 4]. "
    "The project guarantees perfect predictions [C9999, Page 99]. "
    "The system uses QDA and GBC algorithms."
)

sources = [
    {
        "chunk_id": "C0005",
        "page": 4,
        "text": (
            "The project uses QDA and GBC algorithms to analyse "
            "sleep-related and health-related features."
        )
    }
]

report = create_audit_report(answer, sources)

print("\n========== CITATION AUDIT REPORT ==========")

print("Total sentences:", report["total_sentences"])
print("Cited sentences:", report["cited_sentences"])
print("Uncited sentences:", report["uncited_sentences"])
print("Invalid citations:", report["invalid_citations"])
print("Citation coverage:", f'{report["citation_coverage_percent"]}%')

for item in report["sentences"]:
    print("\n-------------------------------------------")
    print("Sentence:", item["sentence"])
    print("Citation status:", item["citation_status"])

    for check in item["evidence_checks"]:
        print("Evidence chunk:", check["chunk_id"])
        print("Evidence page:", check["page"])
        print("Similarity:", check["similarity"])
        print("Support status:", check["support_status"])

    for contradiction in item["contradictions"]:
        print("Potential contradiction:", contradiction["other_sentence"])
        print("Contradiction score:", contradiction["score"])