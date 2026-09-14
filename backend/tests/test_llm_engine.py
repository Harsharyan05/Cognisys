import pytest

from app.ai.llm_engine import (
    LLMEngine,
    OllamaLLM,
)


def test_ollama_initialization():

    llm = OllamaLLM(
        model_name="test-model"
    )

    assert llm is not None
    assert llm.model_name == "test-model"


def test_llm_engine_selects_ollama(monkeypatch):

    monkeypatch.setenv(
        "LLM_PROVIDER",
        "ollama",
    )

    monkeypatch.setenv(
        "LLM_MODEL",
        "test-model",
    )

    engine = LLMEngine()

    assert engine is not None
    assert isinstance(engine.client, OllamaLLM)
    assert engine.client.model_name == "test-model"


def test_llm_engine_ask(monkeypatch):

    monkeypatch.setenv(
        "LLM_PROVIDER",
        "ollama",
    )

    engine = LLMEngine()

    expected_answer = "Test response"

    def fake_generate(prompt):

        assert prompt == "Test prompt"

        return expected_answer

    monkeypatch.setattr(
        engine.client,
        "generate",
        fake_generate,
    )

    answer = engine.ask(
        "Test prompt"
    )

    assert answer == expected_answer


def test_ollama_error_handling(monkeypatch):

    llm = OllamaLLM(
        model_name="test-model"
    )

    def fake_chat(**kwargs):

        raise RuntimeError(
            "Test Ollama failure"
        )

    monkeypatch.setattr(
        "app.ai.llm_engine.ollama.chat",
        fake_chat,
    )

    result = llm.generate(
        "Test prompt"
    )

    assert isinstance(result, str)
    assert result.startswith("Ollama Error:")
    assert "Test Ollama failure" in result


def test_unsupported_provider(monkeypatch):

    monkeypatch.setenv(
        "LLM_PROVIDER",
        "unsupported_provider",
    )

    with pytest.raises(ValueError):

        LLMEngine()