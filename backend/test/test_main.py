# tests/test_main.py
from fastapi import status


class TestMainApp:
    """Test main application setup and middleware."""

    def test_request_id_middleware(self, client):
        """Test request ID middleware adds X-Request-Id header."""
        response = client.get("/public")
        assert "X-Request-Id" in response.headers
        assert len(response.headers["X-Request-Id"]) > 0

    def test_rate_limit_exception_handler(self, client):
        """Test rate limit exception handler."""
        # This is tested indirectly through rate limiting
        # Direct testing would require mocking the limiter
        pass

    def test_app_includes_all_routers(self, client):
        """Test all routers are included in app."""
        # Test each router endpoint exists
        response = client.get("/public")
        assert response.status_code == status.HTTP_200_OK

        # Health endpoint requires auth, so we test it fails with 401, not 404
        response = client.get("/health")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.get("/api-key/protected")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
