from app.ai.semantic_search import SemanticSearch


def test_semantic_search_initialization():

    search_engine = SemanticSearch()

    assert search_engine is not None


def test_semantic_search_returns_results():

    search_engine = SemanticSearch()

    results = search_engine.search(
        "repository architecture",
        top_k=5,
    )

    assert results is not None
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 5


def test_semantic_search_result_structure():

    search_engine = SemanticSearch()

    results = search_engine.search(
        "repository architecture",
        top_k=5,
    )

    assert len(results) > 0

    result = results[0]

    assert "chunk_id" in result
    assert "title" in result
    assert "distance" in result
    assert "word_count" in result