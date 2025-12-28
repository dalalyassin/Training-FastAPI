import pytest
from jose import jwt
from fastapi import HTTPException, status
from backend.core.security import (
    verify_api_key,
    create_access_token,
    get_current_user,
    API_KEY,
    SECRET_KEY,
)


class TestVerifyAPIKey:
    """Test API key verification."""

    def test_valid_api_key(self):
        """Test with valid API key."""
        result = verify_api_key(api_key=API_KEY)
        assert result is None

    def test_invalid_api_key(self):
        """Test with invalid API key."""
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(api_key="wrong-key")

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid or missing API key" in str(exc_info.value.detail)

    def test_missing_api_key(self):
        """Test with missing API key."""
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(api_key=None)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestCreateAccessToken:
    """Test JWT token creation."""

    def test_create_token_success(self):
        """Test successful token creation."""
        data = {"sub": "admin"}
        token = create_access_token(data=data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_contains_data(self):
        """Test token contains encoded data."""
        data = {"sub": "admin", "custom": "value"}
        token = create_access_token(data=data)

        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        assert decoded["sub"] == "admin"
        assert decoded["custom"] == "value"
        assert "exp" in decoded


class TestGetCurrentUser:
    """Test JWT token validation and user extraction."""

    def test_valid_token(self):
        """Test with valid token."""
        data = {"sub": "admin"}
        token = create_access_token(data=data)

        username = get_current_user(token=token)
        assert username == "admin"

    def test_invalid_token(self):
        """Test with invalid token."""
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="invalid-token")

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid or expired token" in str(exc_info.value.detail)

    def test_token_missing_sub(self):
        """Test token without 'sub' claim."""
        data = {"custom": "value"}
        token = create_access_token(data=data)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token)

        assert exc_info.value.status_code == 401

    def test_expired_token(self):
        """Test with expired token."""
        from datetime import datetime, timedelta
        from backend.core.security import ALGORITHM

        # Create expired token
        expire = datetime.utcnow() - timedelta(minutes=1)
        to_encode = {"sub": "admin", "exp": expire}
        expired_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=expired_token)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
