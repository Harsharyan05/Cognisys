"""
Repository Indexer

Indexes a single repository into repository-specific storage.

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path
from sentence_transformers import SentenceTransformer
from app.ai.embedding_models import Embedding
from app.ai.multi_vector_store import MultiVectorStore
class RepositoryIndexer:
    """
    Repository-specific indexing pipeline.
    """

    def __init__(self, repository_path):
        self.repository_path = Path(repository_path)

        if not self.repository_path.exists():
            raise ValueError(
                "Repository path does not exist."
            )

        if not self.repository_path.is_dir():
            raise ValueError(
                "Repository path must be a directory."
            )

    def discover_files(self):
        """
        Discover files inside the repository.

        Hidden files and common generated directories are ignored.
        """

        ignored_directories = {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            "node_modules",
            ".pytest_cache",
        }

        files = []

        for path in self.repository_path.rglob("*"):

            if not path.is_file():
                continue

            relative_parts = path.relative_to(
                self.repository_path
            ).parts

            if any(
                part in ignored_directories
                for part in relative_parts
            ):
                continue

            files.append(path)

        return sorted(files)

    def create_documents(self):
        """
        Convert repository files into documents suitable
        for chunking and embedding.
        """

        documents = []

        repository_name = self.repository_path.name

        for file_path in self.discover_files():

            try:
                content = file_path.read_text(
                    encoding="utf-8"
                )
            except (UnicodeDecodeError, OSError):
                continue

            relative_path = file_path.relative_to(
                self.repository_path
            )

            documents.append(
                {
                    "content": content,
                    "metadata": {
                        "source": str(relative_path),
                        "repository": repository_name,
                    },
                }
            )

        return documents

    def create_chunks(self):
        """
        Create repository-specific chunks from documents.

        Each repository file is currently represented as one
        chunk while preserving its source metadata.
        """

        chunks = []

        documents = self.create_documents()

        for index, document in enumerate(
            documents,
            start=1,
        ):
            chunks.append(
                {
                    "content": document["content"],
                    "metadata": {
                        "chunk_id": index,
                        "source": document["metadata"]["source"],
                        "repository": document["metadata"]["repository"],
                    },
                }
            )

        return chunks

    def create_embeddings(self, chunks):
        """
        Generate embeddings for repository chunks.
        """

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        embeddings = []

        for chunk in chunks:

            text = chunk["content"]

            vector = model.encode(
                text,
                convert_to_numpy=True,
            )

            metadata = chunk["metadata"]

            source = metadata["source"]

            title = Path(source).name

            embedding = Embedding(
                chunk_id=metadata["chunk_id"],
                title=title,
                source_document=source,
                text=text,
                word_count=len(text.split()),
                vector=vector,
                dimension=len(vector),
                metadata={
                    "repository": metadata["repository"],
                    "source": source,
                },
            )

            embeddings.append(embedding)

        return embeddings

    def index(self):
        """
        Build a repository-specific vector index.
        """

        repository_name = self.repository_path.name

        repository_storage = (
            Path("storage")
            / "repositories"
            / repository_name
        )

        vector_store_directory = (
            repository_storage
            / "vector_db"
        )

        chunks = self.create_chunks()

        if not chunks:
            return {
                "repository": repository_name,
                "chunks": 0,
                "embeddings": 0,
                "vector_store": str(
                    vector_store_directory
                ),
            }

        embeddings = self.create_embeddings(
            chunks
        )

        vector_store = MultiVectorStore(
            output_directory=str(
                vector_store_directory
            )
        )

        vector_store.build(
            embeddings
        )

        return {
            "repository": repository_name,
            "chunks": len(chunks),
            "embeddings": len(embeddings),
            "vector_store": str(
                vector_store_directory
            ),
        }