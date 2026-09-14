from app.ai.multi_embedding_generator import (
    MultiEmbeddingGenerator,
)

from app.ai.multi_vector_store import (
    MultiVectorStore,
)


def main():

    generator = MultiEmbeddingGenerator()

    embeddings = generator.generate()

    store = MultiVectorStore()

    store.build(
        embeddings
    )

    print("\nVector Database Built")

    print("=" * 60)

    print(
        f"Vectors Indexed : {len(embeddings)}"
    )

    print("\nPerforming Sample Search\n")

    results = store.search(
        embeddings[0].vector,
        k=5,
    )

    for embedding, distance in results:

        print(
            f"Chunk {embedding.chunk_id}"
        )

        print(
            f"Document : {embedding.source_document}"
        )

        print(
            f"Title : {embedding.title}"
        )

        print(
            f"Distance : {distance:.4f}"
        )

        print("-" * 40)


if __name__ == "__main__":
    main()