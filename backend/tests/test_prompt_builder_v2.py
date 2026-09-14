"""
Test Prompt Builder V2

Author: Harsh Aryan
Project: Cognisys
"""

from app.ai.multi_embedding_generator import (
    MultiEmbeddingGenerator,
)

from app.ai.multi_vector_store import (
    MultiVectorStore,
)

from app.ai.multi_semantic_search import (
    MultiSemanticSearch,
)

from app.ai.prompt_builder_v2 import (
    PromptBuilderV2,
)


def build_vector_database():

    generator = MultiEmbeddingGenerator()

    embeddings = generator.generate()

    store = MultiVectorStore()

    store.build(embeddings)


def main():

    build_vector_database()

    search_engine = MultiSemanticSearch()

    builder = PromptBuilderV2()

    print("\nPrompt Builder V2")
    print("=" * 70)

    question = input(
        "\nAsk a repository question: "
    )

    results = search_engine.search(
        question,
        top_k=5,
    )

    prompt = builder.build(
        question=question,
        search_results=results,
    )

    print("\nGenerated Prompt")
    print("=" * 70)
    print(prompt)


if __name__ == "__main__":
    main()