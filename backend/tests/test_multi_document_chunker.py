from app.ai.multi_document_chunker import MultiDocumentChunker


def test_multi_document_chunker_initialization():

    chunker = MultiDocumentChunker()

    assert chunker is not None


def test_multi_document_chunker_generates_chunks():

    chunker = MultiDocumentChunker()

    chunks = chunker.chunk()

    assert chunks is not None
    assert isinstance(chunks, list)
    assert len(chunks) > 0


def test_multi_document_chunk_structure():

    chunker = MultiDocumentChunker()

    chunks = chunker.chunk()

    assert len(chunks) > 0

    chunk = chunks[0]

    assert hasattr(chunk, "chunk_id")
    assert hasattr(chunk, "source_document")
    assert hasattr(chunk, "title")
    assert hasattr(chunk, "word_count")