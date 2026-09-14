from app.ai.hybrid_retriever import HybridRetriever


def test_hybrid_retriever_initialization():

    retriever = HybridRetriever()

    assert retriever is not None
    assert retriever.semantic_search is not None
    assert retriever.classifier is not None
    assert retriever.document_priority is not None


def test_keyword_extraction():

    retriever = HybridRetriever()

    keywords = retriever._extract_keywords(
        "What is the repository architecture?"
    )

    assert isinstance(keywords, list)
    assert "repository" in keywords
    assert "architecture" in keywords
    assert "what" not in keywords
    assert "is" not in keywords
    assert "the" not in keywords


def test_semantic_score():

    retriever = HybridRetriever()

    high_relevance = retriever._semantic_score(0.0)
    lower_relevance = retriever._semantic_score(2.0)

    assert high_relevance == 1.0
    assert lower_relevance < high_relevance


def test_document_priority():

    retriever = HybridRetriever()

    results = retriever.semantic_search.search(
        "repository architecture",
        top_k=1,
    )

    assert len(results) > 0

    embedding, distance = results[0]

    priority = retriever._document_priority(embedding)

    assert isinstance(priority, int)
    assert priority >= 1


def test_hybrid_retrieval():

    retriever = HybridRetriever()

    results = retriever.retrieve(
        "repository architecture",
        top_k=5,
    )

    assert results is not None
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 5


def test_hybrid_result_structure():

    retriever = HybridRetriever()

    results = retriever.retrieve(
        "repository architecture",
        top_k=5,
    )

    assert len(results) > 0

    result = results[0]

    assert isinstance(result, tuple)
    assert len(result) == 3

    score, embedding, distance = result

    assert isinstance(score, float)
    assert hasattr(embedding, "chunk_id")
    assert hasattr(embedding, "source_document")
    assert hasattr(embedding, "title")
    assert hasattr(embedding, "word_count")
    assert hasattr(embedding, "dimension")
    assert isinstance(distance, float)


def test_empty_query_returns_empty_results():

    retriever = HybridRetriever()

    assert retriever.retrieve("") == []
    assert retriever.retrieve("   ") == []