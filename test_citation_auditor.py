from backend.citation_auditor import audit_citations


answer = (
    "The project predicts sleep disorders using machine learning [C0005, Page 4]. "
    "The system uses QDA and GBC algorithms [C0005, Page 4]. "
    "The project guarantees perfect predictions [C9999, Page 99]. "
    "The project improves healthcare."
)

sources = [
    {
        "chunk_id": "C0005",
        "page": 4,
        "text": (
            "The project focuses on developing a machine learning-based "
            "system to predict sleep disorders. It uses QDA and GBC algorithms."
        )
    }
]

results = audit_citations(answer, sources)

for item in results:
    print("\n--------------------------------")
    print("Sentence:", item["sentence"])
    print("Status:", item["status"])