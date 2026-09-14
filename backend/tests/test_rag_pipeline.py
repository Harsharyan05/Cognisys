from app.ai.rag_pipeline import RAGPipeline
from app.ai.citation_engine import Citation


class FakeRetriever:
    def __init__(self):
        self.called_with = None

    def retrieve(self, question):
        self.called_with = question
        return [
            (
                8.5,
                type(
                    "FakeEmbedding",
                    (),
                    {
                        "source_document": "app/main.py",
                        "title": "FastAPI Application",
                        "chunk_id": 1,
                        "word_count": 10,
                    },
                )(),
                0.5,
            )
        ]


class FakePromptBuilder:
    def __init__(self):
        self.called_with = None

    def build(
        self,
        question,
        retrieved_results,
        history,
        debug=False,
    ):
        self.called_with = {
            "question": question,
            "retrieved_results": retrieved_results,
            "history": history,
            "debug": debug,
        }

        return f"PROMPT: {question}"


class FakeLLM:
    def __init__(self):
        self.called_with = None

    def ask(self, prompt):
        self.called_with = prompt
        return "The repository uses FastAPI."


class FakeCitationEngine:
    def __init__(self):
        self.called_with = None

    def extract(self, retrieved_results):
        self.called_with = retrieved_results

        return [
            Citation(
                document="app/main.py",
                title="FastAPI Application",
                chunk_id=1,
                score=8.5,
            )
        ]


class FakeAnswerFormatter:
    def __init__(self):
        self.called_with = None

    def format(
        self,
        answer,
        citations,
        markdown=False,
    ):
        self.called_with = {
            "answer": answer,
            "citations": citations,
            "markdown": markdown,
        }

        return "FORMATTED ANSWER"


def create_pipeline():
    pipeline = RAGPipeline.__new__(RAGPipeline)

    from app.ai.conversation_memory import ConversationMemory
    from app.ai.performance_monitor import PerformanceMonitor

    pipeline.memory = ConversationMemory(max_history=10)
    pipeline.hybrid_retriever = FakeRetriever()
    pipeline.prompt_builder = FakePromptBuilder()
    pipeline.llm = FakeLLM()
    pipeline.citation_engine = FakeCitationEngine()
    pipeline.answer_formatter = FakeAnswerFormatter()
    pipeline.performance_monitor = PerformanceMonitor()

    return pipeline


def test_rag_pipeline_initialization_without_real_dependencies():
    pipeline = create_pipeline()

    assert pipeline.memory is not None
    assert pipeline.hybrid_retriever is not None
    assert pipeline.prompt_builder is not None
    assert pipeline.llm is not None
    assert pipeline.citation_engine is not None
    assert pipeline.answer_formatter is not None
    assert pipeline.performance_monitor is not None


def test_ask_empty_question():
    pipeline = create_pipeline()

    result = pipeline.ask("   ")

    assert result["question"] == ""
    assert result["answer"] == "Question cannot be empty."
    assert result["citations"] == []
    assert result["performance"] is None
    assert result["conversation_size"] == 0


def test_generate_delegates_to_llm():
    pipeline = create_pipeline()

    result = pipeline._generate("TEST PROMPT")

    assert result == "The repository uses FastAPI."
    assert pipeline.llm.called_with == "TEST PROMPT"


def test_store_memory():
    pipeline = create_pipeline()

    pipeline._store_memory(
        "What framework is used?",
        "FastAPI is used.",
    )

    assert pipeline.memory.size() == 1

    history = pipeline.memory.get_history()

    assert history[0][0] == "What framework is used?"
    assert history[0][1] == "FastAPI is used."


def test_ask_successful_pipeline():
    pipeline = create_pipeline()

    result = pipeline.ask(
        "What framework does the repository use?"
    )

    assert result["question"] == (
        "What framework does the repository use?"
    )

    assert result["answer"] == "FORMATTED ANSWER"

    assert result["raw_answer"] == (
        "The repository uses FastAPI."
    )

    assert len(result["citations"]) == 1

    assert result["citations"][0].document == "app/main.py"

    assert result["conversation_size"] == 1

    assert result["performance"] is not None


def test_retriever_receives_question():
    pipeline = create_pipeline()

    question = "What APIs exist?"

    pipeline.ask(question)

    assert pipeline.hybrid_retriever.called_with == question


def test_prompt_builder_receives_retrieved_results():
    pipeline = create_pipeline()

    pipeline.ask("What framework is used?")

    called = pipeline.prompt_builder.called_with

    assert called["question"] == "What framework is used?"
    assert len(called["retrieved_results"]) == 1
    assert called["debug"] is False


def test_llm_receives_generated_prompt():
    pipeline = create_pipeline()

    pipeline.ask("Explain the architecture.")

    assert pipeline.llm.called_with == (
        "PROMPT: Explain the architecture."
    )


def test_citation_engine_receives_retrieved_results():
    pipeline = create_pipeline()

    pipeline.ask("What framework is used?")

    assert pipeline.citation_engine.called_with is not None
    assert len(pipeline.citation_engine.called_with) == 1


def test_answer_formatter_receives_answer_and_citations():
    pipeline = create_pipeline()

    pipeline.ask("What framework is used?")

    called = pipeline.answer_formatter.called_with

    assert called["answer"] == (
        "The repository uses FastAPI."
    )

    assert len(called["citations"]) == 1

    assert called["markdown"] is False


def test_conversation_memory_is_updated():
    pipeline = create_pipeline()

    pipeline.ask("What framework is used?")

    assert pipeline.memory.size() == 1

    history = pipeline.memory.get_history()

    assert history[0][0] == "What framework is used?"
    assert history[0][1] == "FORMATTED ANSWER"


def test_multiple_questions_update_memory():
    pipeline = create_pipeline()

    pipeline.ask("What framework is used?")
    pipeline.ask("What APIs exist?")

    assert pipeline.memory.size() == 2

    history = pipeline.memory.get_history()

    assert history[0][0] == "What framework is used?"
    assert history[1][0] == "What APIs exist?"


def test_reset_clears_memory():
    pipeline = create_pipeline()

    pipeline.ask("What framework is used?")
    pipeline.ask("What APIs exist?")

    assert pipeline.memory.size() == 2

    pipeline.reset()

    assert pipeline.memory.size() == 0


def test_pipeline_error_handling():
    pipeline = create_pipeline()

    def failing_retrieve(question):
        raise RuntimeError("Retriever failed")

    pipeline.hybrid_retriever.retrieve = failing_retrieve

    result = pipeline.ask("Test failure")

    assert result["question"] == "Test failure"
    assert result["answer"] == (
        "Pipeline Error\n\nRetriever failed"
    )
    assert result["raw_answer"] == ""
    assert result["citations"] == []
    assert result["conversation_size"] == 0


def test_pipeline_performance_report_contains_stages():
    pipeline = create_pipeline()

    result = pipeline.ask("What framework is used?")

    performance = result["performance"]

    assert "Performance Report" in performance
    assert "Retriever" in performance
    assert "Prompt Builder" in performance
    assert "LLM" in performance
    assert "Citation Engine" in performance
    assert "Answer Formatter" in performance
    assert "Total Time" in performance