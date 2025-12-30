from fastapi import status


class TestPublicEndpoint:
    """Test public endpoint."""

    def test_public_endpoint_success(self, client):
        """Test public endpoint returns success."""
        response = client.get("/public")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "This endpoint is public"}

    def test_public_endpoint_no_auth_required(self, client):
        """Test public endpoint doesn't require authentication."""
        response = client.get("/public")
        assert response.status_code == status.HTTP_200_OK


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check_missing_api_key(self, client):
        """Test health check without API key."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_health_check_invalid_api_key(self, client):
        """Test health check with invalid API key."""
        response = client.get(
            "/health",
            headers={"X-API-Key": "wrong-key"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAPIKeyProtectedEndpoint:
    """Test API key protected endpoint."""

    def test_protected_endpoint_missing_api_key(self, client):
        """Test protected endpoint without API key."""
        response = client.get("/api-key/protected")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_invalid_api_key(self, client):
        """Test protected endpoint with invalid API key."""
        response = client.get(
            "/api-key/protected",
            headers={"X-API-Key": "wrong-key"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestOAuthEndpoints:
    """Test OAuth endpoints."""

    def test_login_success(self, client):
        """Test successful login."""
        response = client.post(
            "/token",
            data={
                "username": "admin",
                "password": "admin",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post(
            "/token",
            data={
                "username": "wrong",
                "password": "wrong",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_wrong_username(self, client):
        """Test login with wrong username."""
        response = client.post(
            "/token",
            data={
                "username": "wrong",
                "password": "admin",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_wrong_password(self, client):
        """Test login with wrong password."""
        response = client.post(
            "/token",
            data={
                "username": "admin",
                "password": "wrong",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_oauth_protected_valid_token(self, client, valid_token):
        """Test OAuth protected endpoint with valid token."""
        response = client.get(
            "/oauth-protected",
            headers={
                "Authorization": f"Bearer {valid_token}",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert "Hello admin" in response.json()["message"]

    def test_oauth_protected_missing_token(self, client):
        """Test OAuth protected endpoint without token."""
        response = client.get("/oauth-protected")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_oauth_protected_invalid_token(self, client):
        """Test OAuth protected endpoint with invalid token."""
        response = client.get(
            "/oauth-protected",
            headers={
                "Authorization": "Bearer invalid-token",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestChatStreamEndpoint:
    """Test chat streaming endpoint."""

    def test_chat_stream_missing_api_key(self, client):
        """Test chat streaming without API key."""
        response = client.post(
            "/message/stream",
            json={
                "text": "Hello",
                "talk": 1,
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
