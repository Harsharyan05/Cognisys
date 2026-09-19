"""
RAG Pipeline

Central orchestration pipeline for Cognisys.

Coordinates:
- Conversation Memory
- Prompt Builder V3
- LLM Engine
- Citation Engine
- Answer Formatter
- Performance Monitor

Author: Harsh Aryan
Project: Cognisys
"""

from app.ai.conversation_memory import (
    ConversationMemory,
)

from app.ai.prompt_builder_v3 import (
    PromptBuilderV3,
)

from app.ai.llm_engine import (
    LLMEngine,
)

from app.ai.citation_engine import (
    CitationEngine,
)

from app.ai.answer_formatter import (
    AnswerFormatter,
)

from app.ai.performance_monitor import (
    PerformanceMonitor,
)

from app.ai.hybrid_retriever import (
    HybridRetriever,
)

class RAGPipeline:
    """
    Central Retrieval-Augmented Generation Pipeline.

    Responsible for coordinating the
    complete AI workflow.
    """

    def __init__(
        self,
        memory_size: int = 10,
    ):

        print("Initializing RAG Pipeline...")

        # ---------------------------------------------------------
        # Conversation Memory
        # ---------------------------------------------------------

        self.memory = ConversationMemory(
            max_history=memory_size,
        )
        
        # ---------------------------------------------------------
        # Hybrid_Retriever
        # ---------------------------------------------------------
        self.hybrid_retriever = HybridRetriever()

        # ---------------------------------------------------------
        # Prompt Builder
        # ---------------------------------------------------------

        self.prompt_builder = PromptBuilderV3()

        # ---------------------------------------------------------
        # LLM Engine
        # ---------------------------------------------------------

        self.llm = LLMEngine()

        # ---------------------------------------------------------
        # Citation Engine
        # ---------------------------------------------------------

        self.citation_engine = CitationEngine()

        # ---------------------------------------------------------
        # Answer Formatter
        # ---------------------------------------------------------

        self.answer_formatter = AnswerFormatter()

        # ---------------------------------------------------------
        # Performance Monitor
        # ---------------------------------------------------------

        self.performance_monitor = PerformanceMonitor()

        print("RAG Pipeline Ready.")
        
    # ---------------------------------------------------------
    # Reset Conversation
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Clears the conversation memory.
        """

        self.memory.clear()

    # ---------------------------------------------------------
    # Conversation Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
    ) -> None:
        """
        Displays conversation statistics.
        """

        self.memory.statistics()

    # ---------------------------------------------------------
    # Show Conversation
    # ---------------------------------------------------------

    def show_memory(
        self,
    ) -> None:
        """
        Displays stored conversations.
        """

        self.memory.display()

    # ---------------------------------------------------------
    # Generate Answer
    # ---------------------------------------------------------

    def _generate(
        self,
        prompt: str,
    ) -> str:
        """
        Sends the prompt to the configured
        language model.
        """

        return self.llm.ask(
            prompt
        )

    # ---------------------------------------------------------
    # Store Conversation
    # ---------------------------------------------------------

    def _store_memory(
        self,
        question: str,
        answer: str,
    ) -> None:
        """
        Stores the completed conversation.
        """

        self.memory.add(
            question=question,
            answer=answer,
        )
        
    # ---------------------------------------------------------
    # Ask
    # ---------------------------------------------------------

    def ask(
        self,
        question: str,
        architecture_context=None,
    ):
        """
        Complete Retrieval-Augmented Generation
        workflow.

        Flow

        User Question
        ↓
        Hybrid Retriever
                ↓
        Citation Engine
                ↓
        Prompt Builder
                ↓
        LLM
                ↓
        Answer Formatter
                ↓
        Conversation Memory
                ↓
        Return Response
        """

        question = question.strip()

        if not question:

            return {
                "question": "",
                "answer": "Question cannot be empty.",
                "citations": [],
                "performance": None,
                "conversation_size": self.memory.size(),
            }

        try:

            # ---------------------------------------------------------
            # Start Monitoring
            # ---------------------------------------------------------

            self.performance_monitor.reset()

            self.performance_monitor.start(
                "Total Pipeline"
            )

            # ---------------------------------------------------------
            # Retriever
            # ---------------------------------------------------------

            self.performance_monitor.start(
                "Retriever"
            )

            retrieved_results = (
                self.hybrid_retriever.retrieve(
                    question
                )
            )

            self.performance_monitor.stop(
                "Retriever"
            )
            
            # ---------------------------------------------------------
            # Prompt Builder
            # ---------------------------------------------------------

            self.performance_monitor.start(
                "Prompt Builder"
            )

            prompt = self.prompt_builder.build(
                question=question,
                retrieved_results=retrieved_results,
                history=self.memory.formatted_history(),
                debug=False,
                architecture_context=architecture_context,
            )

            self.performance_monitor.stop(
                "Prompt Builder"
            )

            # ---------------------------------------------------------
            # LLM
            # ---------------------------------------------------------

            self.performance_monitor.start(
                "LLM"
            )

            answer = self._generate(
                prompt
            )

            self.performance_monitor.stop(
                "LLM"
            )

            # ---------------------------------------------------------
            # Citation Engine
            # ---------------------------------------------------------

            self.performance_monitor.start(
                "Citation Engine"
            )

            citations = self.citation_engine.extract(
                retrieved_results
            )

            self.performance_monitor.stop(
                "Citation Engine"
            )

            # ---------------------------------------------------------
            # Answer Formatter
            # ---------------------------------------------------------

            self.performance_monitor.start(
                "Answer Formatter"
            )

            formatted_answer = (
                self.answer_formatter.format(
                    answer=answer,
                    citations=citations,
                    markdown=False,
                )
            )

            self.performance_monitor.stop(
                "Answer Formatter"
            )

            # ---------------------------------------------------------
            # Store Conversation
            # ---------------------------------------------------------

            self._store_memory(
                question,
                formatted_answer,
            )

            # ---------------------------------------------------------
            # Stop Monitoring
            # ---------------------------------------------------------

            self.performance_monitor.stop(
                "Total Pipeline"
            )

            return {

                "question": question,

                "answer": formatted_answer,

                "raw_answer": answer,

                "citations": citations,

                "performance":
                    self.performance_monitor.report(),

                "conversation_size":
                    self.memory.size(),

            }

        except Exception as error:

            try:
                self.performance_monitor.stop(
                    "Total Pipeline"
                )
            except Exception:
                pass

            return {

                "question": question,

                "answer":
                    f"Pipeline Error\n\n{error}",

                "raw_answer": "",

                "citations": [],

                "performance":
                    self.performance_monitor.report(),

                "conversation_size":
                    self.memory.size(),

            }



            