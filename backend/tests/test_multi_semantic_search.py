from pathlib import Path

import numpy as np

import app.ai.multi_semantic_search as semantic_search_module
from app.ai.multi_semantic_search import MultiSemanticSearch


class FakeModel:
    def encode(self, query, convert_to_numpy=True):
        return np.array([0.1, 0.2, 0.3])


class FakeVectorStore:
    def __init__(self, output_directory="storage/vector_db"):
        self.output_directory = Path(output_directory)

    def search(self, query_vector, k=15):
        return [
            ("result", 0.5)
        ]


def test_semantic_search_accepts_repository_vector_store(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        semantic_search_module,
        "SentenceTransformer",
        lambda model_name: FakeModel(),
    )

    monkeypatch.setattr(
        semantic_search_module,
        "MultiVectorStore",
        FakeVectorStore,
    )

    vector_store_directory = (
        tmp_path
        / "repositories"
        / "repo_a"
        / "vector_db"
    )

    search = MultiSemanticSearch(
        vector_store_directory=str(
            vector_store_directory
        )
    )

    assert (
        search.vector_store.output_directory
        == vector_store_directory
    )


def test_different_repositories_use_different_vector_stores(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        semantic_search_module,
        "SentenceTransformer",
        lambda model_name: FakeModel(),
    )

    monkeypatch.setattr(
        semantic_search_module,
        "MultiVectorStore",
        FakeVectorStore,
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

    search_a = MultiSemanticSearch(
        vector_store_directory=str(
            repo_a_directory
        )
    )

    search_b = MultiSemanticSearch(
        vector_store_directory=str(
            repo_b_directory
        )
    )

    assert (
        search_a.vector_store.output_directory
        != search_b.vector_store.output_directory
    )

    assert (
        search_a.vector_store.output_directory
        == repo_a_directory
    )

    assert (
        search_b.vector_store.output_directory
        == repo_b_directory
    )


def test_semantic_search_passes_query_to_vector_store(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        semantic_search_module,
        "SentenceTransformer",
        lambda model_name: FakeModel(),
    )

    class TrackingVectorStore(FakeVectorStore):

        def __init__(
            self,
            output_directory="storage/vector_db",
        ):
            super().__init__(output_directory)

            self.received_query_vector = None
            self.received_k = None

        def search(self, query_vector, k=15):
            self.received_query_vector = query_vector
            self.received_k = k

            return [
                ("result", 0.5)
            ]

    monkeypatch.setattr(
        semantic_search_module,
        "MultiVectorStore",
        TrackingVectorStore,
    )

    search = MultiSemanticSearch(
        vector_store_directory=str(
            tmp_path / "repo" / "vector_db"
        )
    )

    results = search.search(
        "authentication",
        top_k=5,
    )

    assert results == [
        ("result", 0.5)
    ]

    assert np.array_equal(
        search.vector_store.received_query_vector,
        np.array([0.1, 0.2, 0.3]),
    )

    assert search.vector_store.received_k == 5


def test_default_vector_store_directory_is_preserved(
    monkeypatch,
):
    monkeypatch.setattr(
        semantic_search_module,
        "SentenceTransformer",
        lambda model_name: FakeModel(),
    )

    monkeypatch.setattr(
        semantic_search_module,
        "MultiVectorStore",
        FakeVectorStore,
    )

    search = MultiSemanticSearch()

    assert (
        search.vector_store.output_directory
        == Path("storage/vector_db")
    )


def test_semantic_search_uses_repository_specific_store(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        semantic_search_module,
        "SentenceTransformer",
        lambda model_name: FakeModel(),
    )

    created_stores = []

    class TrackingVectorStore(FakeVectorStore):

        def __init__(
            self,
            output_directory="storage/vector_db",
        ):
            super().__init__(output_directory)
            created_stores.append(self)

    monkeypatch.setattr(
        semantic_search_module,
        "MultiVectorStore",
        TrackingVectorStore,
    )

    repository_directory = (
        tmp_path
        / "repositories"
        / "my_repo"
        / "vector_db"
    )

    search = MultiSemanticSearch(
        vector_store_directory=str(
            repository_directory
        )
    )

    search.search(
        "authentication",
        top_k=5,
    )

    assert len(created_stores) == 1

    assert (
        created_stores[0].output_directory
        == repository_directory
    )


def test_semantic_search_returns_vector_store_results(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        semantic_search_module,
        "SentenceTransformer",
        lambda model_name: FakeModel(),
    )

    expected_results = [
        ("auth.py", 0.12),
        ("login.py", 0.25),
    ]

    class ResultVectorStore(FakeVectorStore):

        def search(self, query_vector, k=15):
            return expected_results

    monkeypatch.setattr(
        semantic_search_module,
        "MultiVectorStore",
        ResultVectorStore,
    )

    search = MultiSemanticSearch(
        vector_store_directory=str(
            tmp_path / "repo" / "vector_db"
        )
    )

    results = search.search(
        "authentication",
        top_k=5,
    )

    assert results == expected_results