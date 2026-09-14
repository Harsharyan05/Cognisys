from app.ai.chunker import Chunker


def test_chunker_generates_chunks():

    chunker = Chunker(
        "storage/documents/repository_summary.md"
    )

    chunks = chunker.chunk()

    assert chunks is not None
    assert isinstance(chunks, list)
    assert len(chunks) > 0


def test_chunker_chunk_structure():

    chunker = Chunker(
        "storage/documents/repository_summary.md"
    )

    chunks = chunker.chunk()

    assert len(chunks) > 0

    chunk = chunks[0]

    assert hasattr(chunk, "id")
    assert hasattr(chunk, "title")
    assert hasattr(chunk, "word_count")
    assert hasattr(chunk, "line_count")