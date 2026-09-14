from pathlib import Path

from app.ai.semantic_search import SemanticSearch
from app.ai.prompt_builder import PromptBuilder


def main():

    search = SemanticSearch()

    builder = PromptBuilder()

    print("\nPrompt Builder Test")
    print("=" * 70)

    question = input(
        "\nAsk a repository question: "
    )

    results = search.search(
        question,
        top_k=3,
    )

    contexts = []

    for result in results:

        chunk_path = Path(
            f"storage/chunks/chunk_{result['chunk_id']:03}.md"
        )

        if chunk_path.exists():

            contexts.append(
                chunk_path.read_text(
                    encoding="utf-8"
                )
            )

    prompt = builder.build(
        question,
        contexts,
    )

    print("\nGenerated Prompt")
    print("=" * 70)

    print(prompt)


if __name__ == "__main__":
    main()