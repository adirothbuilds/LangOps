import pytest
from unittest.mock import MagicMock, AsyncMock
from langops.llm import OpenAILLM


@pytest.fixture
def llm():
    return OpenAILLM(api_key="test_key", model="gpt-3.5-turbo")


def test_initialization():
    llm_instance = OpenAILLM(api_key="test_key")
    assert llm_instance.api_key == "test_key"


def test_is_chat_model(llm):
    assert llm._is_chat_model("gpt-3.5-turbo")
    assert not llm._is_chat_model("text-davinci-003")


def test_prepare_messages_chat_model(llm):
    prompt = "Hello, AI!"
    messages = llm._prepare_messages(prompt)
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello, AI!"


def test_prepare_messages_chat_model_list(llm):
    llm.model = "gpt-3.5-turbo"  # Set to a chat model
    prompt = [
        {"role": "user", "content": "Hello, AI!"},
        {"role": "assistant", "content": "Hi there!"},
    ]
    messages = llm._prepare_messages(prompt)
    assert messages == prompt


def test_prepare_messages_non_chat_model(llm):
    llm.model = "text-davinci-003"  # Set to a non-chat model
    prompt = [
        {"role": "user", "content": "Hello, AI!"},
        {"role": "assistant", "content": "Hi there!"},
    ]
    formatted_prompt = llm._prepare_messages(prompt)
    assert formatted_prompt == "Hello, AI!\nHi there!"


def test_prepare_messages_non_chat_model_empty_content(llm):
    llm.model = "text-davinci-003"  # Set to a non-chat model
    prompt = [
        {"role": "user", "content": ""},
        {"role": "assistant", "content": ""},
    ]
    formatted_prompt = llm._prepare_messages(prompt)
    assert formatted_prompt == "\n"


def test_prepare_messages_non_chat_model_partial_content(llm):
    llm.model = "text-davinci-003"  # Set to a non-chat model
    prompt = [
        {"role": "user", "content": "Hello, AI!"},
        {"role": "assistant", "content": None},  # Explicitly None "content"
        {"role": "user", "content": "Hi there!"},
    ]
    formatted_prompt = llm._prepare_messages(prompt)
    assert formatted_prompt == "Hello, AI!\n\nHi there!"


def test_prepare_messages_non_chat_model_edge_case(llm):
    llm.model = "text-davinci-003"  # Set to a non-chat model
    prompt = [
        {"role": "user", "content": "Hello, AI!"},
        {"role": "assistant", "content": ""},  # Empty string "content"
        {"role": "user", "content": "Hi there!"},
    ]
    formatted_prompt = llm._prepare_messages(prompt)
    assert formatted_prompt == "Hello, AI!\n\nHi there!"


def test_extract_text_from_response(llm):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock(content="Hello, AI!")
    text = llm._extract_text_from_response(mock_response)
    assert text == "Hello, AI!"


def test_extract_text_from_response_no_choices(llm):
    mock_response = MagicMock()
    mock_response.choices = []
    text = llm._extract_text_from_response(mock_response)
    assert text == ""


def test_extract_chat_content_no_content(llm):
    mock_choice = MagicMock()
    mock_choice.message = MagicMock(content=None)
    text = llm._extract_chat_content(mock_choice)
    assert text == ""


def test_extract_non_chat_text_no_text(llm):
    mock_choice = MagicMock()
    mock_choice.text = None
    text = llm._extract_non_chat_text(mock_choice)
    assert text == ""


def test_create_metadata(llm):
    mock_response = MagicMock(
        id="123", object="chat.completion", created=1234567890, usage={"tokens": 100}
    )
    metadata = llm._create_metadata(mock_response)
    assert metadata["model_used"] == "gpt-3.5-turbo"
    assert metadata["id"] == "123"
    assert metadata["object"] == "chat.completion"
    assert metadata["created"] == 1234567890
    assert metadata["usage"] == {"tokens": 100}


def test_complete_chat_model(llm):
    llm.model = "gpt-3.5-turbo"  # Set to a chat model
    prompt = "Hello, AI!"
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock(content="Hi there!")
    llm.client.chat.completions.create = MagicMock(return_value=mock_response)

    response = llm.complete(prompt)
    assert response.text == "Hi there!"
    assert response.metadata["model_used"] == "gpt-3.5-turbo"


def test_complete_non_chat_model(llm):
    llm.model = "text-davinci-003"  # Set to a non-chat model
    prompt = "Hello, AI!"
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.text = "Hi there!"
    mock_response.choices = [mock_choice]
    llm.client.completions.create = MagicMock(return_value=mock_response)

    response = llm.complete(prompt)
    assert response.text == "Hi there!"
    assert response.metadata["model_used"] == "text-davinci-003"


@pytest.mark.asyncio
async def test_acomplete_chat_model(llm):
    llm.model = "gpt-3.5-turbo"  # Set to a chat model
    mock_response = AsyncMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock(content="Hi there!")
    llm.async_client.chat.completions.create = AsyncMock(return_value=mock_response)

    response = await llm.acomplete("Hello, AI!")
    assert response.text == "Hi there!"
    assert response.metadata["model_used"] == "gpt-3.5-turbo"


@pytest.mark.asyncio
async def test_acomplete_non_chat_model(llm):
    llm.model = "text-davinci-003"  # Set to a non-chat model
    prompt = "Hello, AI!"
    mock_response = AsyncMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].text = "Hi there!"
    llm.async_client.completions.create = AsyncMock(return_value=mock_response)

    response = await llm.acomplete(prompt)
    assert response.text == "Hi there!"
    assert response.metadata["model_used"] == "text-davinci-003"
