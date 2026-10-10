from backend.evidence_checker import check_evidence_support


tests = [
    {
        "name": "Relevant evidence",
        "claim": "The project predicts sleep disorders using machine learning.",
        "evidence": (
            "The project develops a machine-learning system to predict "
            "sleep disorders using lifestyle and health-related data."
        ),
    },
    {
        "name": "Unrelated evidence",
        "claim": "The project predicts sleep disorders using machine learning.",
        "evidence": (
            "The certificate confirms that the students completed "
            "their engineering project requirements."
        ),
    },
    {
        "name": "Empty evidence",
        "claim": "The project predicts sleep disorders.",
        "evidence": "",
    },
]

for test in tests:
    print(f"\n--- {test['name']} ---")

    result = check_evidence_support(
        claim=test["claim"],
        evidence=test["evidence"],
    )

    print("Similarity:", result["similarity"])
    print("Status:", result["status"])
    print("Message:", result["message"])