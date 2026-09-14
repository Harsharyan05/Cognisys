from app.ai.chunker import Chunker
from app.ai.embedding_generator import EmbeddingGenerator


DOCUMENT_PATH = "storage/documents/repository_summary.md"


def test_embedding_generator_creates_embeddings():

    chunker = Chunker(DOCUMENT_PATH)
    chunks = chunker.chunk()

    generator = EmbeddingGenerator()
    embeddings = generator.generate(chunks)

    assert embeddings is not None
    assert isinstance(embeddings, list)
    assert len(embeddings) > 0


def test_embedding_structure():

    chunker = Chunker(DOCUMENT_PATH)
    chunks = chunker.chunk()

    generator = EmbeddingGenerator()
    embeddings = generator.generate(chunks)

    assert len(embeddings) > 0

    embedding = embeddings[0]

    assert hasattr(embedding, "chunk_id")
    assert hasattr(embedding, "title")
    assert hasattr(embedding, "dimension")
    assert hasattr(embedding, "word_count")
    assert hasattr(embedding, "vector")


def test_embedding_vector_is_valid():

    chunker = Chunker(DOCUMENT_PATH)
    chunks = chunker.chunk()

    generator = EmbeddingGenerator()
    embeddings = generator.generate(chunks)

    assert len(embeddings) > 0

    for embedding in embeddings:
        assert embedding.vector is not None
        assert len(embedding.vector) > 0
        assert embedding.dimension == len(embedding.vector)