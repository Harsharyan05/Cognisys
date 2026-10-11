"""
Prompt Builder V3

Builds high-quality prompts for Cognisys by combining:
- Repository overview
- Retrieved repository knowledge
- Architecture context
- Conversation history
- User question

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path
from typing import List, Tuple

from app.ai.repository_overview_generator import (
    RepositoryOverviewGenerator,
)


class PromptBuilderV3:
    """
    Builds high-quality prompts for the LLM.
    """

    def __init__(
        self,
        documents_directory: str = "storage/documents",
    ):

        self.documents_directory = Path(
            documents_directory
        )

        self.overview_generator = (
            RepositoryOverviewGenerator(
                documents_directory
            )
        )

    # ---------------------------------------------------------
    # Repository Overview
    # ---------------------------------------------------------

    def _repository_overview(
        self,
    ) -> str:
        """
        Loads the repository overview.

        Generates it automatically if it does
        not already exist.
        """

        overview_file = (
            self.documents_directory
            / "repository_overview.md"
        )

        if not overview_file.exists():

            self.overview_generator.save()

        return overview_file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    # ---------------------------------------------------------
    # System Prompt
    # ---------------------------------------------------------

    def _system_prompt(
        self,
    ) -> str:
        """
        Returns the system prompt used for every
        repository conversation.
        """

        return """
You are Cognisys.

You are an expert AI Software Architect capable of
understanding complete software repositories.

Your responsibility is to answer repository-related
questions ONLY using the provided repository context.

Rules

1. Never hallucinate.

2. Never invent files,
classes,
functions,
APIs,
services,
or architecture.

3. If the information is unavailable,
reply:

"The repository does not contain enough
information to answer this question."

4. Always mention source documents whenever
possible.

5. Prefer structured answers.

Use headings.

Use bullet points.

Use numbered lists whenever appropriate.

If implementation details exist,
mention the corresponding files.

If architecture exists,
explain layer-by-layer.

Be concise,
accurate,
and repository-aware.
""".strip()

    # ---------------------------------------------------------
    # Build Repository Context
    # ---------------------------------------------------------

    def _build_context(
        self,
        retrieved_results,
    ) -> str:
        """
        Builds the repository context supplied
        to the LLM.
        """

        overview = (
            self._repository_overview()
        )

        sections = []

        for index, (
            score,
            embedding,
            distance,
        ) in enumerate(
            retrieved_results,
            start=1,
        ):

            content = embedding.text.strip()

            if len(content) > 1500:

                content = (
                    content[:1500]
                    + "\n\n...[truncated]"
                )

            sections.append(
                f"""
--------------------------------------------------
Chunk {index}
--------------------------------------------------

Document : {embedding.source_document}

Title : {embedding.title}

Chunk ID : {embedding.chunk_id}

Word Count : {embedding.word_count}

Hybrid Score : {score:.2f}

Semantic Distance : {distance:.4f}

Content
--------------------------------------------------

{content}
"""
            )

        retrieved = "\n".join(
            sections
        )

        context = f"""
==================================================
Repository Overview
==================================================

{overview}

==================================================
Relevant Repository Knowledge
==================================================

{retrieved}
"""

        return context.strip()

    # ---------------------------------------------------------
    # Build Architecture Context
    # ---------------------------------------------------------

    def _build_architecture_context(
        self,
        architecture_context,
    ) -> str:
        """
        Builds the architecture context supplied
        to the LLM.

        Architecture context is optional. When it is
        not provided, no architecture section is added.
        """

        if not architecture_context:
            return ""

        if hasattr(
            architecture_context,
            "analysis",
        ):
            architecture_context = (
                architecture_context.analysis
            )

        layers = architecture_context.get(
            "layers",
            {},
        )

        dependency_graph = architecture_context.get(
            "dependency_graph",
            {},
        )

        cycles = architecture_context.get(
            "cycles",
            [],
        )

        hotspots = architecture_context.get(
            "hotspots",
            [],
        )

        patterns = architecture_context.get(
            "patterns",
            [],
        )

        recommendations = architecture_context.get(
            "recommendations",
            [],
        )

        return f"""
==================================================
Architecture Intelligence
==================================================

Layers
--------------------------------------------------
{layers}

Dependency Graph
--------------------------------------------------
{dependency_graph}

Circular Dependencies
--------------------------------------------------
{cycles}

Hotspots
--------------------------------------------------
{hotspots}

Architecture Patterns
--------------------------------------------------
{patterns}

Recommendations
--------------------------------------------------
{recommendations}
""".strip()

    # ---------------------------------------------------------
    # Build Conversation History
    # ---------------------------------------------------------

    def _build_history(
        self,
        history: List[Tuple[str, str]] | None,
    ) -> str:
        """
        Formats the previous conversation history.

        Expected format:

        [
            ("Question 1", "Answer 1"),
            ("Question 2", "Answer 2"),
        ]
        """

        if not history:

            return """
No previous conversation available.

Treat this as the first interaction with the user.
""".strip()

        conversation = []

        for index, (
            question,
            answer,
        ) in enumerate(
            history,
            start=1,
        ):

            conversation.append(
                f"""
--------------------------------------------------
Conversation {index}
--------------------------------------------------

User

{question}

Assistant

{answer}
"""
            )

        return "\n".join(
            conversation
        )

    # ---------------------------------------------------------
    # Build User Prompt
    # ---------------------------------------------------------

    def _build_user_prompt(
        self,
        question: str,
    ) -> str:
        """
        Builds the final user instruction
        for the LLM.
        """

        
        return f"""
        Answer the user's repository question directly.

        Question:
        {question}

        Rules:
        1. Use only the supplied repository context.
        2. Never invent files, classes, functions, APIs, or implementation details.
        3. For implementation questions, identify the exact source files,
        classes, and methods supported by the context.
        4. For workflow questions, explain the sequence of method calls
        and how data moves between components.
        5. For ranking or retrieval questions, state the actual scoring
        formula, sorting order, deduplication rule, and top-k behavior
        only when these are explicitly supported by the context.
        6. If a required implementation detail is missing or truncated,
        explicitly say that it cannot be verified from the supplied context.
        7. Distinguish verified implementation behavior from assumptions.
        8. Use a structured answer with headings when the question
        requires multiple implementation stages.
        9. Do not repeat previous answers or reproduce citation/source
        sections; citations are formatted separately by the application.
        """.strip()

    # ---------------------------------------------------------
    # Build Final Prompt
    # ---------------------------------------------------------

    def build(
        self,
        question: str,
        retrieved_results,
        history: List[Tuple[str, str]] | None = None,
        debug: bool = False,
        architecture_context=None,
    ) -> str:
        """
        Builds the complete prompt that will
        be sent to the LLM.

        architecture_context is optional and allows
        architecture intelligence to be supplied
        alongside normal RAG context.
        """

        system_prompt = self._system_prompt()

        repository_context = self._build_context(
            retrieved_results
        )

        architecture_section = (
            self._build_architecture_context(
                architecture_context
            )
        )

        conversation = self._build_history(
            history
        )

        user_prompt = self._build_user_prompt(
            question
        )

        prompt = f"""
==================================================
SYSTEM
==================================================

{system_prompt}

==================================================
CONVERSATION HISTORY
==================================================

{conversation}

==================================================
REPOSITORY CONTEXT
==================================================

{repository_context}
"""

        if architecture_section:

            prompt += f"""

==================================================
ARCHITECTURE CONTEXT
==================================================

{architecture_section}
"""

        prompt += f"""

==================================================
USER QUESTION
==================================================

{user_prompt}
"""

        prompt = prompt.strip()

        if debug:
            self.prompt_statistics(prompt)

        return prompt

    # ---------------------------------------------------------
    # Prompt Statistics
    # ---------------------------------------------------------

    def prompt_statistics(
        self,
        prompt: str,
    ):
        """
        Prints prompt statistics.
        Useful while debugging prompts.
        """

        characters = len(prompt)

        words = len(
            prompt.split()
        )

        lines = len(
            prompt.splitlines()
        )

        estimated_tokens = (
            characters // 4
        )

        print("\n")
        print("=" * 60)
        print("Prompt Statistics")
        print("=" * 60)

        print(
            f"Characters      : {characters}"
        )

        print(
            f"Words           : {words}"
        )

        print(
            f"Lines           : {lines}"
        )

        print(
            f"Estimated Tokens: {estimated_tokens}"
        )

        print("=" * 60)

    # ---------------------------------------------------------
    # Preview Prompt
    # ---------------------------------------------------------

    def preview(
        self,
        question: str,
        retrieved_results,
        history: List[Tuple[str, str]] | None = None,
        architecture_context=None,
    ):
        """
        Prints the generated prompt.
        """

        prompt = self.build(
            question=question,
            retrieved_results=retrieved_results,
            history=history,
            architecture_context=architecture_context,
            debug=False,
        )

        print("\n")
        print("=" * 80)
        print("Generated Prompt")
        print("=" * 80)
        print(prompt)
        print("=" * 80)