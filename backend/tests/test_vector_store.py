from app.ai.embedding_generator import EmbeddingGenerator
from app.ai.chunker import Chunker
from app.ai.vector_store import VectorStore


DOCUMENT_PATH = "storage/documents/repository_summary.md"


def test_vector_store_builds():

    chunker = Chunker(DOCUMENT_PATH)
    chunks = chunker.chunk()

    embeddings = EmbeddingGenerator().generate(
        chunks,
        source_document=DOCUMENT_PATH,
    )

    assert embeddings is not None
    assert len(embeddings) > 0

    store = VectorStore()

    store.build()
    store.load()

    assert store.index is not None
    assert len(store.metadata) == len(embeddings)


def test_vector_store_search():

    chunker = Chunker(DOCUMENT_PATH)
    chunks = chunker.chunk()

    embeddings = EmbeddingGenerator().generate(
        chunks,
        source_document=DOCUMENT_PATH,
    )

    assert len(embeddings) > 0

    store = VectorStore()

    store.build()
    store.load()

    results = store.search(
        embeddings[0].vector,
        top_k=3,
    )

    assert results is not None
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 3


def test_vector_store_result_structure():

    chunker = Chunker(DOCUMENT_PATH)
    chunks = chunker.chunk()

    embeddings = EmbeddingGenerator().generate(
        chunks,
        source_document=DOCUMENT_PATH,
    )

    store = VectorStore()

    store.build()
    store.load()

    results = store.search(
        embeddings[0].vector,
        top_k=3,
    )

    assert len(results) > 0

    result = results[0]

    assert "chunk_id" in result
    assert "title" in result
    assert "distance" in result
    assert "vector" in result