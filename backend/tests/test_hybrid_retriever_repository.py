from pathlib import Path

import app.ai.hybrid_retriever as hybrid_retriever_module
from app.ai.hybrid_retriever import HybridRetriever


class FakeSemanticSearch:

    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        vector_store_directory="storage/vector_db",
    ):
        self.model_name = model_name
        self.vector_store_directory = Path(
            vector_store_directory
        )


def test_hybrid_retriever_accepts_repository_vector_store(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        hybrid_retriever_module,
        "MultiSemanticSearch",
        FakeSemanticSearch,
    )

    vector_store_directory = (
        tmp_path
        / "repositories"
        / "repo_a"
        / "vector_db"
    )

    retriever = HybridRetriever(
        vector_store_directory=str(
            vector_store_directory
        )
    )

    assert (
        retriever.semantic_search.vector_store_directory
        == vector_store_directory
    )


def test_different_hybrid_retrievers_use_different_repositories(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        hybrid_retriever_module,
        "MultiSemanticSearch",
        FakeSemanticSearch,
    )

    repo_a_directory = (
        tmp_path
        / "repositories"
        / "repo_a"
        / "vector_db"
    )

    repo_b_directory = (
        tmp_path
        / "repositories"
        / "repo_b"
        / "vector_db"
    )

    retriever_a = HybridRetriever(
        vector_store_directory=str(
            repo_a_directory
        )
    )

    retriever_b = HybridRetriever(
        vector_store_directory=str(
            repo_b_directory
        )
    )

    assert (
        retriever_a.semantic_search.vector_store_directory
        == repo_a_directory
    )

    assert (
        retriever_b.semantic_search.vector_store_directory
        == repo_b_directory
    )

    assert (
        retriever_a.semantic_search.vector_store_directory
        != retriever_b.semantic_search.vector_store_directory
    )


def test_hybrid_retriever_preserves_default_vector_store(
    monkeypatch,
):
    monkeypatch.setattr(
        hybrid_retriever_module,
        "MultiSemanticSearch",
        FakeSemanticSearch,
    )

    retriever = HybridRetriever()

    assert (
        retriever.semantic_search.vector_store_directory
        == Path("storage/vector_db")
    )
    
def test_hybrid_retriever_retrieve_uses_repository_search(
    monkeypatch,
    tmp_path,
):
    repository_directory = (
        tmp_path
        / "repositories"
        / "repo_a"
        / "vector_db"
    )

    class FakeSemanticSearch:

        def __init__(
            self,
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            vector_store_directory="storage/vector_db",
        ):
            self.vector_store_directory = Path(
                vector_store_directory
            )
            self.received_query = None
            self.received_top_k = None

        def search(self, query, top_k=15):
            self.received_query = query
            self.received_top_k = top_k

            return []

    monkeypatch.setattr(
        hybrid_retriever_module,
        "MultiSemanticSearch",
        FakeSemanticSearch,
    )

    retriever = HybridRetriever(
        vector_store_directory=str(
            repository_directory
        )
    )

    results = retriever.retrieve(
        "How does authentication work?",
        top_k=5,
    )

    assert results == []

    assert (
        retriever.semantic_search.vector_store_directory
        == repository_directory
    )

    assert (
        retriever.semantic_search.received_query
        == "How does authentication work?"
    )

    assert (
        retriever.semantic_search.received_top_k
        >= 5
    )    