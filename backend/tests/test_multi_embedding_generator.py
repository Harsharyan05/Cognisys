from app.ai.multi_embedding_generator import MultiEmbeddingGenerator


def test_multi_embedding_generator_initialization():

    generator = MultiEmbeddingGenerator()

    assert generator is not None


def test_multi_embedding_generator_generates_embeddings():

    generator = MultiEmbeddingGenerator()

    embeddings = generator.generate()

    assert embeddings is not None
    assert isinstance(embeddings, list)
    assert len(embeddings) > 0


def test_multi_embedding_structure():

    generator = MultiEmbeddingGenerator()

    embeddings = generator.generate()

    assert len(embeddings) > 0

    embedding = embeddings[0]

    assert hasattr(embedding, "chunk_id")
    assert hasattr(embedding, "source_document")
    assert hasattr(embedding, "title")
    assert hasattr(embedding, "word_count")
    assert hasattr(embedding, "dimension")