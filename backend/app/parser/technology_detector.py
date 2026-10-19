
"""
Technology Detector

Author: Harsh Aryan
Project: Cognisys
"""

import json
from pathlib import Path


class TechnologyDetector:
    """Detect technologies from repository configuration files."""

    IGNORED_DIRS = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        "storage",
    }


    def _find_files(self, root: Path, filename: str):
        """Find matching configuration files, including nested projects."""
        for path in root.rglob(filename):
            relative_path = path.relative_to(root)

            if any(
                part in self.IGNORED_DIRS
                for part in relative_path.parts[:-1]
            ):
                continue

            if path.is_file():
                yield path


    def detect(self, repository_path: str) -> dict:
        root = Path(repository_path)

        if not root.exists() or not root.is_dir():
            raise FileNotFoundError(
                f"Repository not found: {repository_path}"
            )

        technologies = {
            "languages": set(),
            "frameworks": set(),
            "databases": set(),
            "deployment": set(),
            "ml_libraries": set(),
        }

        # Python dependencies
        for requirements in self._find_files(root, "requirements.txt"):
            technologies["languages"].add("Python")

            raw = requirements.read_bytes()

            if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
                packages = raw.decode("utf-16").lower()
            else:
                packages = raw.decode("utf-8-sig", errors="replace").lower()

            if "fastapi" in packages:
                technologies["frameworks"].add("FastAPI")

            if "sqlalchemy" in packages:
                technologies["databases"].add("SQLAlchemy")

            if "psycopg" in packages:
                technologies["databases"].add("PostgreSQL")

            if "langchain" in packages:
                technologies["ml_libraries"].add("LangChain")

            if "networkx" in packages:
                technologies["ml_libraries"].add("NetworkX")

        # JavaScript / TypeScript dependencies
        for package_file in self._find_files(root, "package.json"):
            try:
                data = json.loads(
                    package_file.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                )
            except (json.JSONDecodeError, OSError):
                continue

            all_dependencies = {}
            all_dependencies.update(data.get("dependencies", {}))
            all_dependencies.update(data.get("devDependencies", {}))

            if all_dependencies:
                if "typescript" in all_dependencies:
                    technologies["languages"].add("TypeScript")

                if any(
                    name in all_dependencies
                    for name in ("react", "next", "vite", "express")
                ):
                    technologies["languages"].add("JavaScript")

            if "react" in all_dependencies:
                technologies["frameworks"].add("React")

            if "next" in all_dependencies:
                technologies["frameworks"].add("Next.js")

            if "tailwindcss" in all_dependencies:
                technologies["frameworks"].add("TailwindCSS")

        # Deployment
        if any(self._find_files(root, "Dockerfile")):
            technologies["deployment"].add("Docker")

        return {
            key: sorted(value)
            for key, value in technologies.items()
        }
