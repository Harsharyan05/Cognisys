"""
Test RAG Pipeline

Interactive test for the Cognisys
Retrieval-Augmented Generation Pipeline.

Author: Harsh Aryan
Project: Cognisys
"""

from app.ai.rag_pipeline import (
    RAGPipeline,
)


def main():

    print("=" * 80)
    print("Cognisys Repository AI")
    print("=" * 80)

    pipeline = RAGPipeline()

    print("\nAvailable Commands")
    print("-" * 80)
    print("exit   -> Quit")
    print("memory -> Show conversation history")
    print("stats  -> Show memory statistics")
    print("reset  -> Clear conversation history")
    print("=" * 80)

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":

            print("\nGoodbye!")
            break

        elif question.lower() == "memory":

            pipeline.show_memory()
            continue

        elif question.lower() == "stats":

            pipeline.statistics()
            continue

        elif question.lower() == "reset":

            pipeline.reset()
            print("\nConversation memory cleared.")
            continue

        result = pipeline.ask(
            question
        )

        print("\n" + "=" * 80)
        print("Answer")
        print("=" * 80)
        print(result["answer"])

        print("\n" + "=" * 80)
        print("Citations")
        print("=" * 80)

        citations = result.get(
            "citations",
            [],
        )

        if citations:

            if isinstance(citations, list):

                for citation in citations:

                    print(f"- {citation}")

            else:

                print(citations)

        else:

            print("No citations found.")

        print("\n" + "=" * 80)
        print("Performance")
        print("=" * 80)

        performance = result.get(
            "performance"
        )

        if performance:

            print(performance)

        else:

            print("No performance report.")

        print("\nConversation Size:",
              result.get(
                  "conversation_size",
                  0,
              ))


if __name__ == "__main__":

    main()