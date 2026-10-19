
from pathlib import Path
from pprint import pprint

from app.ai.repository_indexer import RepositoryIndexer
from app.ai.hybrid_retriever import HybridRetriever


# ==========================================================
# CONFIGURATION
# ==========================================================

REPO = Path("storage/temp/Cognisys/backend").resolve()

QUESTION = (
    "Explain how repository code chunks are retrieved and ranked. "
    "Identify the relevant files and methods, semantic scoring formula, "
    "keyword scoring, document priorities, symbol priorities, "
    "deduplication, candidate top-k, and final top-k. "
    "Clearly state which details cannot be verified from the "
    "retrieved context."
)

TOP_K = 8


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def unpack_result(result):
    """
    Supports:
        (score, embedding, distance)
        (embedding, distance)
        (embedding, distance, keyword_score)
        embedding
    """
    if not isinstance(result, tuple):
        return None, result, None, None

    if len(result) == 3:
        first, second, third = result

        # Prepared symbol results:
        # (embedding, distance, keyword_score)
        if hasattr(first, "source_document"):
            return None, first, second, third

        # Ranked results:
        # (score, embedding, distance)
        if hasattr(second, "source_document"):
            return first, second, third, None

        return None, first, second, third

    if len(result) == 2:
        first, second = result

        if hasattr(first, "source_document"):
            return None, first, second, None

    if len(result) == 1:
        return None, result[0], None, None

    return None, result, None, None


def get_metadata(embedding) -> dict:
    metadata = getattr(embedding, "metadata", {})
    return metadata if isinstance(metadata, dict) else {}


def get_content(embedding) -> str:
    return getattr(embedding, "text", "") or ""


def print_result(number: int, result, result_type: str) -> None:
    score, embedding, distance, keyword_score = unpack_result(result)

    metadata = get_metadata(embedding)
    content = get_content(embedding)

    print(f"\n[{number}] {result_type}")
    print(f"Title:       {getattr(embedding, 'title', 'N/A')}")
    print(f"Source:      {getattr(embedding, 'source_document', 'N/A')}")
    print(f"Word count:  {getattr(embedding, 'word_count', 'N/A')}")

    print(f"Symbol:      {metadata.get('symbol_name', 'N/A')}")
    print(f"Symbol type: {metadata.get('symbol_type', 'N/A')}")
    print(f"Symbol ID:   {metadata.get('symbol_id', 'N/A')}")

    if score is not None:
        print(f"Score:       {score}")

    if distance is not None:
        print(f"Distance:    {distance}")

    if keyword_score is not None:
        print(f"Keyword score: {keyword_score}")

    print("Content preview:")
    print(content[:500] if content else "[No content available]")


# ==========================================================
# MAIN DEBUGGER
# ==========================================================

def main() -> None:
    print_section("COGNISYS RETRIEVAL DEBUGGER")

    # ------------------------------------------------------
    # 1. Validate repository and index
    # ------------------------------------------------------

    if not REPO.is_dir():
        raise FileNotFoundError(
            f"Repository directory does not exist:\n{REPO}"
        )

    indexer = RepositoryIndexer(REPO)

    print(f"Repository path: {REPO}")
    print(f"Vector index:    {indexer.vector_store_directory}")
    print(f"Metadata path:   {indexer.metadata_path}")

    if not indexer.metadata_path.exists():
        raise FileNotFoundError(
            f"Vector metadata not found:\n{indexer.metadata_path}\n"
            "Index the repository before running this debugger."
        )

    # ------------------------------------------------------
    # 2. Initialize retriever
    # ------------------------------------------------------

    retriever = HybridRetriever(
        vector_store_directory=str(indexer.vector_store_directory),
        repository_path=REPO,
    )

    # ------------------------------------------------------
    # 3. Query classification
    # ------------------------------------------------------

    print_section("1. QUERY CLASSIFICATION")

    classification = retriever.classifier.classify(QUESTION)
    pprint(classification)

    # ------------------------------------------------------
    # 4. Retrieval settings
    # ------------------------------------------------------

    print_section("2. RETRIEVAL SETTINGS")

    final_top_k = TOP_K
    candidate_k = max(final_top_k * 2, 15)

    print(f"Requested final top-k: {final_top_k}")
    print(f"Candidate top-k:       {candidate_k}")
    print(f"Question:              {QUESTION}")

    # ------------------------------------------------------
    # 5. Raw semantic file search
    # ------------------------------------------------------

    print_section("3. RAW FILE SEARCH RESULTS")

    file_results = retriever.semantic_search.search(
        QUESTION,
        top_k=candidate_k,
    )

    print(f"Raw file results count: {len(file_results)}")

    for i, result in enumerate(file_results, start=1):
        print_result(i, result, "RAW FILE RESULT")

    # ------------------------------------------------------
    # 6. Raw symbol search
    # ------------------------------------------------------

    print_section("4. RAW SYMBOL SEARCH RESULTS")

    symbol_results = []

    try:
        symbol_results = retriever._retrieve_symbols(
            QUESTION,
            candidate_k=candidate_k,
        )

        print(f"Raw symbol results count: {len(symbol_results)}")

        for i, result in enumerate(symbol_results, start=1):
            print_result(i, result, "RAW SYMBOL RESULT")

    except Exception as exc:
        print(
            f"Symbol search failed: "
            f"{type(exc).__name__}: {exc}"
        )

    # ------------------------------------------------------
    # 7. Prepared symbol results
    # ------------------------------------------------------

    print_section("5. PREPARED SYMBOL RESULTS")

    prepared_symbols = []

    try:
        prepared_symbols = retriever._prepare_symbol_results(
            QUESTION,
            symbol_results,
        )

        print(f"Prepared symbol results: {len(prepared_symbols)}")

        for i, result in enumerate(prepared_symbols, start=1):
            print_result(i, result, "PREPARED SYMBOL")

    except Exception as exc:
        print(
            f"Symbol preparation failed: "
            f"{type(exc).__name__}: {exc}"
        )

    # ------------------------------------------------------
    # 8. Final hybrid retrieval
    # ------------------------------------------------------

    print_section("6. FINAL HYBRID RETRIEVAL RESULTS")

    final_results = retriever.retrieve(
        QUESTION,
        top_k=TOP_K,
    )

    print(f"Final results count: {len(final_results)}")

    for i, result in enumerate(final_results, start=1):
        print_result(i, result, "FINAL HYBRID RESULT")

    # ------------------------------------------------------
    # 9. Summary
    # ------------------------------------------------------

    print_section("7. SUMMARY")

    print(f"Repository:              {REPO}")
    print(f"Raw file results:        {len(file_results)}")
    print(f"Raw symbol results:      {len(symbol_results)}")
    print(f"Prepared symbol results: {len(prepared_symbols)}")
    print(f"Final hybrid results:    {len(final_results)}")
    print(f"Requested final top-k:   {TOP_K}")
    print(f"Candidate top-k:         {candidate_k}")

    print("\nDebug run completed.")


if __name__ == "__main__":
    main()
