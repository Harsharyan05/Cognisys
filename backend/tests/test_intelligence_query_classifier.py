from app.intelligence.query_classifier import IntelligenceQueryClassifier


def test_code_question_routes_to_rag():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify("What does the UserService class do?")

    assert result.category == "RAG"


def test_architecture_question_routes_to_architecture():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify(
        "Which layer does UserService belong to?"
    )

    assert result.category == "ARCHITECTURE"


def test_dependency_question_routes_to_architecture():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify(
        "What modules depend on UserService?"
    )

    assert result.category == "ARCHITECTURE"


def test_implementation_question_routes_to_both():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify(
        "Explain the authentication flow and what happens if I modify AuthService."
    )

    assert result.category == "BOTH"


def test_general_question_defaults_to_rag():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify(
        "How is authentication implemented?"
    )

    assert result.category == "RAG"