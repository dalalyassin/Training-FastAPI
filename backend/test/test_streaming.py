# tests/test_streaming.py
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from backend.core.streaming import stream_tokens
from backend.schemas.chat import Prompt
from backend.services.llm import generate_stream_response


class TestStreamTokens:
    """Test stream_tokens utility function."""

    def test_stream_tokens_basic(self):
        """Test basic token streaming."""
        tokens = ["Hello", " ", "World"]
        result = list(stream_tokens(tokens))

        assert len(result) == 3
        assert result[0] == "data: Hello\n\n"
        assert result[1] == "data:  \n\n"
        assert result[2] == "data: World\n\n"

    def test_stream_tokens_with_trace_id(self, capsys):
        """Test token streaming with trace ID."""
        tokens = ["Test"]
        result = list(
            stream_tokens(
                tokens,
                trace_id="123",
            )
        )

        assert len(result) == 1
        assert result[0] == "data: Test\n\n"

        captured = capsys.readouterr()
        assert "[TRACE 123]" in captured.out

    def test_stream_tokens_empty_list(self):
        """Test streaming empty token list."""
        result = list(stream_tokens([]))
        assert len(result) == 0

    def test_stream_tokens_single_token(self):
        """Test streaming single token."""
        tokens = ["Single"]
        result = list(stream_tokens(tokens))

        assert len(result) == 1
        assert result[0] == "data: Single\n\n"


class TestGenerateStreamResponse:
    """Test LLM streaming response generation."""

    @pytest.mark.asyncio
    @patch("backend.services.llm.client")
    async def test_generate_stream_response_success(
        self,
        mock_client,
    ):
        """Test successful stream generation."""
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [
            MagicMock(
                delta=MagicMock(content="Hello"),
            )
        ]

        mock_chunk2 = MagicMock()
        mock_chunk2.choices = [
            MagicMock(
                delta=MagicMock(content=" World"),
            )
        ]

        async def mock_stream():
            yield mock_chunk1
            yield mock_chunk2

        mock_client.chat.completions.create = AsyncMock(
            return_value=mock_stream(),
        )

        prompt = Prompt(text="Test prompt", talk=1)
        result = []

        async for chunk in generate_stream_response(prompt):
            result.append(chunk)

        assert len(result) == 2
        assert result[0] == "data: Hello\n\n"
        assert result[1] == "data:  World\n\n"

    @pytest.mark.asyncio
    @patch("backend.services.llm.client")
    async def test_generate_stream_response_empty_delta(
        self,
        mock_client,
    ):
        """Test handling of chunks with empty delta."""
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [
            MagicMock(
                delta=MagicMock(content=None),
            )
        ]

        mock_chunk2 = MagicMock()
        mock_chunk2.choices = [
            MagicMock(
                delta=MagicMock(content="Content"),
            )
        ]

        async def mock_stream():
            yield mock_chunk1
            yield mock_chunk2

        mock_client.chat.completions.create = AsyncMock(
            return_value=mock_stream(),
        )

        prompt = Prompt(text="Test", talk=1)
        result = []

        async for chunk in generate_stream_response(prompt):
            result.append(chunk)

        assert len(result) == 1
        assert result[0] == "data: Content\n\n"

    @pytest.mark.asyncio
    @patch("backend.services.llm.client")
    async def test_generate_stream_response_no_content(
        self,
        mock_client,
    ):
        """Test stream with no content chunks."""
        mock_chunk = MagicMock()
        mock_chunk.choices = [
            MagicMock(
                delta=MagicMock(content=None),
            )
        ]

        async def mock_stream():
            yield mock_chunk

        mock_client.chat.completions.create = AsyncMock(
            return_value=mock_stream(),
        )

        prompt = Prompt(text="Test", talk=1)
        result = []

        async for chunk in generate_stream_response(prompt):
            result.append(chunk)

        assert len(result) == 0

    @pytest.mark.asyncio
    @patch("backend.services.llm.client")
    async def test_generate_stream_response_correct_params(
        self,
        mock_client,
    ):
        """Test OpenAI client called with correct parameters."""

        async def mock_stream():
            yield MagicMock(
                choices=[
                    MagicMock(
                        delta=MagicMock(content="Test"),
                    )
                ]
            )

        mock_client.chat.completions.create = AsyncMock(
            return_value=mock_stream(),
        )

        prompt = Prompt(text="User message", talk=1)
        async for _ in generate_stream_response(prompt):
            pass

        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args

        assert call_args.kwargs["model"] == "gpt-4o-mini"
        assert call_args.kwargs["temperature"] == 0.7
        assert call_args.kwargs["stream"] is True
        assert len(call_args.kwargs["messages"]) == 1
        assert call_args.kwargs["messages"][0]["role"] == "user"
        assert call_args.kwargs["messages"][0]["content"] == "User message"
