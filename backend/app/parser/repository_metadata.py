
from collections import Counter
from pathlib import Path
from typing import Any


class RepositoryMetadataAnalyzer:
    """Collect basic structural metadata about a repository."""

    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".idea",
        ".vscode",
        ".pytest_cache",
        "dist",
        "build",
    }

    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript (React)",
        ".ts": "TypeScript",
        ".tsx": "TypeScript (React)",
        ".java": "Java",
        ".cpp": "C++",
        ".cc": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".hpp": "C++ Header",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".rb": "Ruby",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".html": "HTML",
        ".css": "CSS",
        ".sql": "SQL",
        ".sh": "Shell",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".json": "JSON",
        ".md": "Markdown",
    }

    PROJECT_FILES = {
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".gitignore",
        ".env.example",
    }

    def __init__(self, repository_path: str = "."):
        self.repository_path = Path(repository_path).resolve()

    def analyze(self) -> dict[str, Any]:
        """Return a structured summary of repository contents."""
        if not self.repository_path.is_dir():
            raise NotADirectoryError(
                f"Repository directory not found: {self.repository_path}"
            )

        extension_counts = Counter()
        language_counts = Counter()
        directory_counts = Counter()
        project_files = []
        total_files = 0

        for file_path in self.repository_path.rglob("*"):
            relative_path = file_path.relative_to(self.repository_path)

            if any(
                part in self.IGNORE_DIRS
                for part in relative_path.parts
            ):
                continue

            if file_path.is_dir():
                continue

            total_files += 1
            extension = file_path.suffix.lower() or "[no extension]"
            extension_counts[extension] += 1

            language = self.LANGUAGE_MAP.get(extension)
            if language:
                language_counts[language] += 1

            if file_path.name in self.PROJECT_FILES:
                project_files.append(relative_path.as_posix())

            if len(relative_path.parts) > 1:
                directory_counts[relative_path.parts[0]] += 1
            else:
                directory_counts["[root]"] += 1

        return {
            "repository_name": self.repository_path.name,
            "repository_root": str(self.repository_path),
            "total_files": total_files,
            "extension_counts": dict(
                sorted(extension_counts.items())
            ),
            "language_counts": dict(
                sorted(language_counts.items())
            ),
            "directory_file_counts": dict(
                sorted(directory_counts.items())
            ),
            "project_files": sorted(project_files),
        }
