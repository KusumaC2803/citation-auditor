from backend.contradiction_detector import detect_contradiction


tests = [
    (
        "The model achieved 95% accuracy.",
        "The model achieved 60% accuracy."
    ),
    (
        "The system uses QDA and GBC algorithms.",
        "The system uses Quadratic Discriminant Analysis and Gradient Boosting."
    ),
    (
        "The application was developed using Flask.",
        "The model achieved 95% accuracy."
    )
]


for statement_a, statement_b in tests:
    result = detect_contradiction(statement_a, statement_b)

    print("\n----------------------------------")
    print("Statement A:", result["statement_a"])
    print("Statement B:", result["statement_b"])
    print("Contradiction score:", result["contradiction_score"])
    print("Status:", result["status"])