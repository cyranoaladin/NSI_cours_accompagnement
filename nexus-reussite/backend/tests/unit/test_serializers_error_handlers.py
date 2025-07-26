"""
Unit tests for serializers and error handlers.
"""

from unittest.mock import patch

import pytest
from marshmallow import ValidationError

from src.models.schemas import ContentSchema, UserSchema


class TestSerializers:
    """Test suite for data serializers."""

    @pytest.fixture
    def valid_user_data(self):
        """Provide valid user data for serialization."""
        return {
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "first_name": "Test",
            "last_name": "User",
            "role": "student",
            "is_active": True,
            "email_verified": True,
        }

    def test_user_serialization_valid(self, valid_user_data):
        """Test serialization of valid user data."""
        # Arrange
        schema = UserSchema()

        # Act
        result = schema.load(valid_user_data)

        # Assert
        assert result["email"] == valid_user_data["email"]
        assert result["first_name"] == valid_user_data["first_name"]

    def test_user_serialization_invalid(self):
        """Test serialization of invalid user data raises error."""
        # Arrange
        schema = UserSchema()
        invalid_data = {
            "email": "",
            "password": "123",
            "first_name": "",
            "last_name": "",
        }

        # Act  Assert
        with pytest.raises(ValidationError):
            schema.load(invalid_data)

    def test_content_serialization_valid(self):
        """Test serialization of valid content data."""
        # Arrange
        schema = ContentSchema()
        valid_data = {
            "title": "Introduction to Algorithms",
            "content": "Algorithms are essential in CS...",
            "subject": "NSI",
            "grade_level": "Terminale",
            "difficulty_level": "Moyen",
            "tags": ["algorithms", "programming"],
        }

        # Act
        result = schema.load(valid_data)

        # Assert
        assert result["title"] == valid_data["title"]
        assert result["subject"] == valid_data["subject"]

    def test_content_serialization_invalid(self):
        """Test serialization of invalid content data raises error."""
        # Arrange
        schema = ContentSchema()
        invalid_data = {
            "title": "",
            "content": "",
            "subject": "",
            "grade_level": "",
            "difficulty_level": "",
        }

        # Act  Assert
        with pytest.raises(ValidationError):
            schema.load(invalid_data)


class TestErrorHandlers:
    """Test suite for error handling mechanisms."""

    def test_handle_validation_error(self, client):
        """Test the handling of JSON validation errors in route calls."""
        # Arrange
        invalid_payload = '{"email": "invalid"}'

        with patch("flask.jsonify") as mock_jsonify:
            mock_jsonify.return_value = "Mock Response"

            # Act
            response = client.post("/api/v1/users", json=invalid_payload)

            # Assert
            assert response == "Mock Response"
            mock_jsonify.assert_called_once()

    def test_custom_error_handler(self, client):
        """Test custom error handler for custom exceptions."""
        # Arrange
        invalid_endpoint = "/non/existent/route"

        # Act
        response = client.get(invalid_endpoint)

        # Assert
        assert response.status_code == 404
        assert "Page Not Found" in response.get_json().get("message")
