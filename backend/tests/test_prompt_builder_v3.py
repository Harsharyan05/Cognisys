from app.ai.prompt_builder_v3 import PromptBuilderV3


def test_prompt_builder_v3_initialization():

    builder = PromptBuilderV3()

    assert builder is not None


def test_prompt_builder_v3_builds_prompt():

    builder = PromptBuilderV3()

    prompt = builder.build(
        question="What is the repository architecture?",
        retrieved_results=[],
        history=[],
    )

    assert prompt is not None
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_prompt_contains_question():

    builder = PromptBuilderV3()

    question = "What services are available?"

    prompt = builder.build(
        question=question,
        retrieved_results=[],
        history=[],
    )

    assert question in prompt


def test_prompt_with_conversation_history():

    builder = PromptBuilderV3()

    history = [
        (
            "What is this repository?",
            "It is an AI-powered software intelligence platform.",
        ),
    ]

    prompt = builder.build(
        question="What architecture does it use?",
        retrieved_results=[],
        history=history,
    )

    assert prompt is not None
    assert isinstance(prompt, str)
    assert "What is this repository?" in prompt
    assert "It is an AI-powered software intelligence platform." in prompt


def test_prompt_handles_empty_question():

    builder = PromptBuilderV3()

    prompt = builder.build(
        question="",
        retrieved_results=[],
        history=[],
    )

    assert prompt is not None
    assert isinstance(prompt, str)