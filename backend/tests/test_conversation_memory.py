from app.ai.conversation_memory import ConversationMemory


def test_conversation_memory_initialization():

    memory = ConversationMemory(
        max_history=5,
    )

    assert memory is not None
    assert memory.size() == 0
    assert memory.is_empty()


def test_add_conversation():

    memory = ConversationMemory(
        max_history=5,
    )

    memory.add(
        "What is Cognisys?",
        "Cognisys is a software intelligence platform.",
    )

    assert memory.size() == 1
    assert not memory.is_empty()

    history = memory.get_history()

    assert len(history) == 1
    assert history[0] == (
        "What is Cognisys?",
        "Cognisys is a software intelligence platform.",
    )


def test_get_recent():

    memory = ConversationMemory(
        max_history=5,
    )

    memory.add("Question 1", "Answer 1")
    memory.add("Question 2", "Answer 2")
    memory.add("Question 3", "Answer 3")

    recent = memory.get_recent(2)

    assert len(recent) == 2
    assert recent[0] == ("Question 2", "Answer 2")
    assert recent[1] == ("Question 3", "Answer 3")


def test_max_history_limit():

    memory = ConversationMemory(
        max_history=2,
    )

    memory.add("Question 1", "Answer 1")
    memory.add("Question 2", "Answer 2")
    memory.add("Question 3", "Answer 3")

    assert memory.size() == 2

    history = memory.get_history()

    assert history[0] == ("Question 2", "Answer 2")
    assert history[1] == ("Question 3", "Answer 3")


def test_formatted_history():

    memory = ConversationMemory(
        max_history=5,
    )

    memory.add(
        "What is Cognisys?",
        "It is a software intelligence platform.",
    )

    formatted = memory.formatted_history()

    assert isinstance(formatted, list)
    assert len(formatted) == 1

    assert formatted[0] == (
        "What is Cognisys?",
        "It is a software intelligence platform.",
    )


def test_remove_last():

    memory = ConversationMemory(
        max_history=5,
    )

    memory.add("Question 1", "Answer 1")
    memory.add("Question 2", "Answer 2")

    memory.remove_last()

    assert memory.size() == 1
    assert memory.last() == (
        "Question 1",
        "Answer 1",
    )


def test_clear():

    memory = ConversationMemory(
        max_history=5,
    )

    memory.add("Question 1", "Answer 1")
    memory.add("Question 2", "Answer 2")

    memory.clear()

    assert memory.size() == 0
    assert memory.is_empty()
    assert memory.get_history() == []