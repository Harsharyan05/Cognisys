
"""
Answer Formatter

Formats AI responses into clean, structured,
professional repository answers.

Author: Harsh Aryan
Project: Cognisys
"""

import re
from typing import List

from app.ai.citation_engine import Citation


class AnswerFormatter:
    """
    Formats repository answers.

    Features
    --------
    - Cleans generated answers
    - Removes duplicate outer headers
    - Formats citations
    - Supports plain text and Markdown
    - Builds final responses
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Clean Answer
    # ---------------------------------------------------------

    def _clean_answer(self, answer: str) -> str:
        """Remove duplicate headers and normalize whitespace."""

        if not answer or not answer.strip():
            return "No answer generated."

        answer = answer.strip()

        markers = {
            "=" * 80,
            "Repository Answer",
            "Repository Sources",
        }

        lines = answer.splitlines()

        # Remove repeated leading separators and answer headings.
        while lines and (
            not lines[0].strip()
            or lines[0].strip() in markers
        ):
            lines.pop(0)

        # Remove a trailing sources section if the formatter
        # will append the authoritative citations separately.
        for index, line in enumerate(lines):
            if line.strip() == "Repository Sources":
                lines = lines[:index]
                break

        answer = "\n".join(lines).strip()

        # Normalize excessive blank lines.
        answer = re.sub(r"\n{3,}", "\n\n", answer)

        return answer or "No answer generated."

    # ---------------------------------------------------------
    # Format Header
    # ---------------------------------------------------------

    def _format_header(self, title: str) -> str:
        """Create a plain-text section header."""

        return (
            "\n"
            + "=" * 80
            + "\n"
            + title
            + "\n"
            + "=" * 80
        )

    # ---------------------------------------------------------
    # Format Citations
    # ---------------------------------------------------------

    def _format_citations(
        self,
        citations: List[Citation],
    ) -> str:
        """Format repository citations."""

        if not citations:
            return "No repository sources available."

        lines = []

        for index, citation in enumerate(citations, start=1):
            lines.append(f"{index}. {citation.document}")
            lines.append(f"   Title : {citation.title}")
            lines.append(f"   Chunk : {citation.chunk_id}")
            lines.append(f"   Score : {citation.score:.2f}")
            lines.append("")

        return "\n".join(lines).rstrip()

    # ---------------------------------------------------------
    # Format Plain Text
    # ---------------------------------------------------------

    def format_text(
        self,
        answer: str,
        citations: List[Citation],
    ) -> str:
        """Format the final response as plain text."""

        answer = self._clean_answer(answer)

        sections = [
            self._format_header("Repository Answer"),
            answer,
            self._format_header("Repository Sources"),
            self._format_citations(citations),
        ]

        return "\n".join(sections)

    # ---------------------------------------------------------
    # Format Markdown
    # ---------------------------------------------------------

    def format_markdown(
        self,
        answer: str,
        citations: List[Citation],
    ) -> str:
        """Format the final response in Markdown."""

        answer = self._clean_answer(answer)

        markdown = [
            "# Repository Answer",
            "",
            answer,
            "",
            "---",
            "",
            "## Repository Sources",
            "",
        ]

        if not citations:
            markdown.append("_No citations available._")
        else:
            for citation in citations:
                markdown.extend([
                    f"- **{citation.document}**",
                    f"  - Title: {citation.title}",
                    f"  - Chunk ID: {citation.chunk_id}",
                    f"  - Score: {citation.score:.2f}",
                    "",
                ])

        return "\n".join(markdown).rstrip()

    # ---------------------------------------------------------
    # Display Answer
    # ---------------------------------------------------------

    def display(
        self,
        answer: str,
        citations: List[Citation],
    ) -> None:
        """Print the formatted repository answer."""

        print(self.format_text(answer, citations))

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        answer: str,
        citations: List[Citation],
    ) -> None:
        """Display answer formatting statistics."""

        answer = self._clean_answer(answer)

        print("\n")
        print("=" * 60)
        print("Answer Formatter Statistics")
        print("=" * 60)
        print(f"Characters : {len(answer)}")
        print(f"Words      : {len(answer.split())}")
        print(f"Lines      : {len(answer.splitlines())}")
        print(f"Citations  : {len(citations)}")
        print("=" * 60)

    # ---------------------------------------------------------
    # Format Final Response
    # ---------------------------------------------------------

    def format(
        self,
        answer: str,
        citations: List[Citation],
        markdown: bool = False,
    ) -> str:
        """
        Format the final repository response.

        Parameters
        ----------
        answer : str
            Raw LLM response.

        citations : List[Citation]
            Repository citations.

        markdown : bool
            If True, return Markdown.
            Otherwise, return plain text.
        """

        if markdown:
            return self.format_markdown(answer, citations)

        return self.format_text(answer, citations)
