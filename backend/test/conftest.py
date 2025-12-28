import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.main import app

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def client():
    """Test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def api_key_header():
    """API key header for authenticated requests."""
    return {"X-API-Key": "test-api-key"}


@pytest.fixture
def mock_openai_stream():
    """Mock OpenAI streaming response."""

    async def mock_stream():
        chunks = [
            MagicMock(choices=[MagicMock(delta=MagicMock(content="Hello"))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content=" "))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content="World"))]),
        ]
        for chunk in chunks:
            yield chunk

    return mock_stream()


@pytest.fixture
def valid_token():
    """Generate a valid JWT token for testing."""
    from backend.core.security import create_access_token

    return create_access_token(data={"sub": "admin"})
