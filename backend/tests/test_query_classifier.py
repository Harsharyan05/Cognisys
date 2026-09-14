from app.ai.query_classifier import QueryClassifier


def test_query_classifier_initialization():

    classifier = QueryClassifier()

    assert classifier is not None


def test_query_classifier_returns_classification():

    classifier = QueryClassifier()

    result = classifier.classify(
        "What is the repository architecture?"
    )

    assert result is not None

    assert hasattr(result, "category")
    assert hasattr(result, "confidence")
    assert hasattr(result, "top_k")
    assert hasattr(result, "overview")
    assert hasattr(result, "keywords")


def test_query_classifier_classification_values():

    classifier = QueryClassifier()

    result = classifier.classify(
        "What is the repository architecture?"
    )

    assert isinstance(result.category, str)
    assert result.category != ""

    assert isinstance(result.confidence, float)
    assert 0.0 <= result.confidence <= 1.0

    assert isinstance(result.top_k, int)
    assert result.top_k > 0

    assert isinstance(result.overview, bool)

    assert isinstance(result.keywords, list)


def test_query_classifier_different_queries():

    classifier = QueryClassifier()

    architecture = classifier.classify(
        "Explain the repository architecture"
    )

    services = classifier.classify(
        "What services are available?"
    )

    assert architecture is not None
    assert services is not None

    assert architecture.category != ""
    assert services.category != ""