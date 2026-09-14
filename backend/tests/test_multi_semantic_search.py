from app.ai.multi_semantic_search import MultiSemanticSearch


def test_multi_semantic_search_initialization():

    search_engine = MultiSemanticSearch()

    assert search_engine is not None
    assert search_engine.model is not None
    assert search_engine.vector_store is not None


def test_multi_semantic_search_returns_results():

    search_engine = MultiSemanticSearch()

    results = search_engine.search(
        "repository architecture",
        top_k=5,
    )

    assert results is not None
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 5


def test_multi_semantic_search_result_structure():

    search_engine = MultiSemanticSearch()

    results = search_engine.search(
        "repository architecture",
        top_k=5,
    )

    assert len(results) > 0

    result = results[0]

    assert isinstance(result, tuple)
    assert len(result) == 2

    embedding, distance = result

    assert hasattr(embedding, "chunk_id")
    assert hasattr(embedding, "source_document")
    assert hasattr(embedding, "title")
    assert hasattr(embedding, "word_count")
    assert hasattr(embedding, "dimension")

    assert isinstance(distance, float)