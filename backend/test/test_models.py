# tests/test_models.py
import pytest
from pydantic import ValidationError
from backend.schemas.auth import Token
from backend.schemas.chat import Prompt, ChatRequest, LLMResponse
from backend.schemas.users import UserCreate


class TestToken:
    """Test Token model validation."""

    def test_valid_token(self):
        token = Token(access_token="test-token", token_type="bearer")
        assert token.access_token == "test-token"
        assert token.token_type == "bearer"

    def test_token_missing_fields(self):
        with pytest.raises(ValidationError):
            Token(access_token="test-token")

        with pytest.raises(ValidationError):
            Token(token_type="bearer")


class TestPrompt:
    """Test Prompt model validation."""

    def test_valid_prompt(self):
        prompt = Prompt(text="Hello", talk=1)
        assert prompt.text == "Hello"
        assert prompt.talk == 1
        assert prompt.user_id is None
        assert prompt.metadata is None

    def test_prompt_with_optional_fields(self):
        prompt = Prompt(
            text="Test",
            talk=2,
            user_id=123,
            metadata={"key": "value"},
        )
        assert prompt.user_id == 123
        assert prompt.metadata == {"key": "value"}

    def test_prompt_missing_required_fields(self):
        with pytest.raises(ValidationError):
            Prompt(text="Hello")

        with pytest.raises(ValidationError):
            Prompt(talk=1)

    def test_prompt_empty_text(self):
        prompt = Prompt(text="", talk=1)
        assert prompt.text == ""


class TestChatRequest:
    """Test ChatRequest model validation."""

    def test_valid_chat_request(self):
        request = ChatRequest(text="Hello", content="World")
        assert request.text == "Hello"
        assert request.content == "World"

    def test_chat_request_missing_fields(self):
        with pytest.raises(ValidationError):
            ChatRequest(text="Hello")

        with pytest.raises(ValidationError):
            ChatRequest(content="World")


class TestLLMResponse:
    """Test LLMResponse model validation."""

    def test_valid_llm_response(self):
        prompt = Prompt(text="Hello", talk=1)
        response = LLMResponse(
            prompt=prompt,
            response_text="Response",
            tokens_used=10,
        )
        assert response.response_text == "Response"
        assert response.tokens_used == 10
        assert response.prompt.text == "Hello"

    def test_llm_response_missing_fields(self):
        prompt = Prompt(text="Hello", talk=1)

        with pytest.raises(ValidationError):
            LLMResponse(
                prompt=prompt,
                response_text="Response",
            )

        with pytest.raises(ValidationError):
            LLMResponse(
                prompt=prompt,
                tokens_used=10,
            )


class TestUserCreate:
    """Test UserCreate model validation."""

    def test_valid_user_create(self):
        user = UserCreate(name="John", email="john@example.com")
        assert user.name == "John"
        assert user.email == "john@example.com"

    def test_user_create_missing_fields(self):
        with pytest.raises(ValidationError):
            UserCreate(name="John")

        with pytest.raises(ValidationError):
            UserCreate(email="john@example.com")

    def test_user_create_empty_strings(self):
        user = UserCreate(name="", email="")
        assert user.name == ""
        assert user.email == ""
