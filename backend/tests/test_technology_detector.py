
from pathlib import Path

import pytest

from app.parser.technology_detector import TechnologyDetector


@pytest.mark.parametrize(
    "encoding",
    ["utf-8", "utf-16"],
)
def test_detects_technologies_from_requirements(
    tmp_path: Path,
    encoding: str,
):
    """Detect dependencies from UTF-8 and UTF-16 requirements files."""
    requirements = tmp_path / "requirements.txt"
    requirements.write_text(
        "\n".join(
            [
                "fastapi==0.139.0",
                "SQLAlchemy==2.0.0",
                "psycopg2-binary==2.9.0",
                "langchain==1.0.0",
                "networkx==3.0",
            ]
        ),
        encoding=encoding,
    )

    result = TechnologyDetector().detect(str(tmp_path))

    assert "Python" in result["languages"]
    assert "FastAPI" in result["frameworks"]
    assert "PostgreSQL" in result["databases"]
    assert "SQLAlchemy" in result["databases"]
    assert "LangChain" in result["ml_libraries"]
    assert "NetworkX" in result["ml_libraries"]


def test_detects_dockerfile(tmp_path: Path):
    """Detect Docker deployment configuration."""
    (tmp_path / "Dockerfile").write_text(
        "FROM python:3.13-slim\n",
        encoding="utf-8",
    )

    result = TechnologyDetector().detect(str(tmp_path))

    assert "Docker" in result["deployment"]
