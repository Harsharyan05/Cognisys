from app.ai.answer_formatter import AnswerFormatter
from app.ai.citation_engine import Citation


def make_citation(
    document="app/main.py",
    title="FastAPI Application",
    chunk_id=1,
    score=8.5,
):
    return Citation(
        document=document,
        title=title,
        chunk_id=chunk_id,
        score=score,
    )


def test_answer_formatter_initialization():
    formatter = AnswerFormatter()

    assert formatter is not None


def test_clean_answer():
    formatter = AnswerFormatter()

    answer = "   This is an answer.   "

    result = formatter._clean_answer(answer)

    assert result == "This is an answer."


def test_clean_empty_answer():
    formatter = AnswerFormatter()

    result = formatter._clean_answer("")

    assert result == "No answer generated."


def test_clean_answer_removes_excessive_newlines():
    formatter = AnswerFormatter()

    answer = "Line one\n\n\nLine two\n\n\nLine three"

    result = formatter._clean_answer(answer)

    assert result == "Line one\n\nLine two\n\nLine three"


def test_format_header():
    formatter = AnswerFormatter()

    result = formatter._format_header("Repository Answer")

    assert "Repository Answer" in result
    assert "=" * 80 in result


def test_format_citations():
    formatter = AnswerFormatter()

    citations = [
        make_citation(
            document="app/main.py",
            title="FastAPI Application",
            chunk_id=1,
            score=8.5,
        )
    ]

    result = formatter._format_citations(citations)

    assert "1. app/main.py" in result
    assert "Title : FastAPI Application" in result
    assert "Chunk : 1" in result
    assert "Score : 8.50" in result


def test_format_empty_citations():
    formatter = AnswerFormatter()

    result = formatter._format_citations([])

    assert result == "No repository sources available."


def test_format_text():
    formatter = AnswerFormatter()

    citations = [
        make_citation()
    ]

    result = formatter.format_text(
        "The repository uses FastAPI.",
        citations,
    )

    assert "Repository Answer" in result
    assert "The repository uses FastAPI." in result
    assert "Repository Sources" in result
    assert "app/main.py" in result
    assert "FastAPI Application" in result
    assert "8.50" in result


def test_format_markdown():
    formatter = AnswerFormatter()

    citations = [
        make_citation()
    ]

    result = formatter.format_markdown(
        "The repository uses FastAPI.",
        citations,
    )

    assert "# Repository Answer" in result
    assert "The repository uses FastAPI." in result
    assert "## Repository Sources" in result
    assert "**app/main.py**" in result
    assert "Title: FastAPI Application" in result
    assert "Chunk ID: 1" in result
    assert "Score: 8.50" in result


def test_format_markdown_without_citations():
    formatter = AnswerFormatter()

    result = formatter.format_markdown(
        "The repository uses FastAPI.",
        [],
    )

    assert "# Repository Answer" in result
    assert "## Repository Sources" in result
    assert "_No citations available._" in result


def test_format_plain_text_without_citations():
    formatter = AnswerFormatter()

    result = formatter.format(
        "Repository analysis completed.",
        [],
    )

    assert "Repository Answer" in result
    assert "Repository analysis completed." in result
    assert "Repository Sources" in result
    assert "No repository sources available." in result


def test_format_markdown_mode():
    formatter = AnswerFormatter()

    result = formatter.format(
        "Repository analysis completed.",
        [],
        markdown=True,
    )

    assert "# Repository Answer" in result
    assert "_No citations available._" in result


def test_format_defaults_to_plain_text():
    formatter = AnswerFormatter()

    result = formatter.format(
        "Repository analysis completed.",
        [],
    )

    assert "# Repository Answer" not in result
    assert "Repository Answer" in result


def test_multiple_citations():
    formatter = AnswerFormatter()

    citations = [
        make_citation(
            document="app/main.py",
            title="Main Application",
            chunk_id=1,
            score=9.0,
        ),
        make_citation(
            document="app/api/router.py",
            title="API Router",
            chunk_id=2,
            score=7.5,
        ),
    ]

    result = formatter.format_text(
        "The application exposes API routes.",
        citations,
    )

    assert "1. app/main.py" in result
    assert "2. app/api/router.py" in result
    assert "Main Application" in result
    assert "API Router" in result
    assert "9.00" in result
    assert "7.50" in result