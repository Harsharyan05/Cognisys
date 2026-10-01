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
    
# ============================================================
# GRAPH-AWARE QUERIES
# ============================================================

def test_who_calls_question_is_both():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify(
        "Who calls "
        "service.py:method:AuthService.authenticate?"
    )

    assert result.category == "BOTH"


def test_what_does_symbol_call_is_both():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify(
        "What does "
        "service.py:method:AuthService.authenticate "
        "call?"
    )

    assert result.category == "BOTH"


def test_import_question_is_both():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify(
        "Which modules import "
        "app.services.auth_service?"
    )

    assert result.category == "BOTH"


def test_inheritance_question_is_both():
    classifier = IntelligenceQueryClassifier()

    result = classifier.classify(
        "Which classes inherit from "
        "app.services.BaseService?"
    )

    assert result.category == "BOTH"    