from app.ai.citation_engine import Citation, CitationEngine
from app.ai.embedding_models import Embedding


def create_embedding(
    document,
    title,
    chunk_id,
):
    return Embedding(
        chunk_id=chunk_id,
        title=title,
        source_document=document,
        text="Test content",
        word_count=10,
        dimension=384,
    )


def test_citation_engine_initialization():

    engine = CitationEngine()

    assert engine is not None


def test_extract_citations():

    engine = CitationEngine()

    embedding = create_embedding(
        "architecture.md",
        "Architecture",
        1,
    )

    retrieved_results = [
        (
            8.5,
            embedding,
            0.25,
        )
    ]

    citations = engine.extract(
        retrieved_results
    )

    assert isinstance(citations, list)
    assert len(citations) == 1

    citation = citations[0]

    assert isinstance(citation, Citation)
    assert citation.document == "architecture.md"
    assert citation.title == "Architecture"
    assert citation.chunk_id == 1
    assert citation.score == 8.5


def test_remove_duplicate_citations():

    engine = CitationEngine()

    citation_1 = Citation(
        document="architecture.md",
        title="Architecture",
        chunk_id=1,
        score=8.0,
    )

    citation_2 = Citation(
        document="architecture.md",
        title="Architecture",
        chunk_id=1,
        score=7.0,
    )

    citation_3 = Citation(
        document="services.md",
        title="Services",
        chunk_id=2,
        score=6.0,
    )

    result = engine.remove_duplicates(
        [
            citation_1,
            citation_2,
            citation_3,
        ]
    )

    assert len(result) == 2
    assert result[0] == citation_1
    assert result[1] == citation_3


def test_sort_by_score():

    engine = CitationEngine()

    citations = [
        Citation(
            document="a.md",
            title="A",
            chunk_id=1,
            score=3.0,
        ),
        Citation(
            document="b.md",
            title="B",
            chunk_id=2,
            score=9.0,
        ),
        Citation(
            document="c.md",
            title="C",
            chunk_id=3,
            score=6.0,
        ),
    ]

    result = engine.sort_by_score(
        citations
    )

    assert [citation.score for citation in result] == [
        9.0,
        6.0,
        3.0,
    ]


def test_markdown_formatting():

    engine = CitationEngine()

    citations = [
        Citation(
            document="architecture.md",
            title="Architecture",
            chunk_id=10,
            score=8.75,
        )
    ]

    markdown = engine.to_markdown(
        citations
    )

    assert isinstance(markdown, str)
    assert "## Sources" in markdown
    assert "architecture.md" in markdown
    assert "Architecture" in markdown
    assert "10" in markdown
    assert "8.75" in markdown


def test_text_formatting():

    engine = CitationEngine()

    citations = [
        Citation(
            document="services.md",
            title="Services",
            chunk_id=5,
            score=7.50,
        )
    ]

    text = engine.to_text(
        citations
    )

    assert isinstance(text, str)
    assert "Repository Sources" in text
    assert "services.md" in text
    assert "Services" in text
    assert "5" in text
    assert "7.50" in text


def test_empty_citations():

    engine = CitationEngine()

    assert (
        engine.to_markdown([])
        == "No citations available."
    )

    assert (
        engine.to_text([])
        == "No citations available."
    )


def test_extract_sorts_citations_by_score():

    engine = CitationEngine()

    embedding_1 = create_embedding(
        "architecture.md",
        "Architecture",
        1,
    )

    embedding_2 = create_embedding(
        "services.md",
        "Services",
        2,
    )

    retrieved_results = [
        (
            5.0,
            embedding_1,
            0.5,
        ),
        (
            10.0,
            embedding_2,
            0.2,
        ),
    ]

    citations = engine.extract(
        retrieved_results
    )

    assert len(citations) == 2
    assert citations[0].score == 10.0
    assert citations[1].score == 5.0