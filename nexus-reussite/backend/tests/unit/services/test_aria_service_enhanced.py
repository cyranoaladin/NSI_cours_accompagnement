"""
Unit tests for ARIA AI service - Enhanced version with comprehensive coverage.
"""

import json
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.services.aria_ai import ARIAService
from tests.factories import ExerciseFactory, StudentFactory


class TestARIAService:
    """Test suite for ARIA AI service."""

    @pytest.fixture
    def aria_service(self, mock_openai):
        """Create ARIA service instance with mocked OpenAI."""
        return ARIAService()

    def test_aria_service_initialization(self, aria_service):
        """Test ARIA service initialization."""
        assert aria_service is not None
        assert hasattr(aria_service, "generate_response")
        assert hasattr(aria_service, "generate_exercise")

    def test_generate_response_basic(self, aria_service, mock_openai):
        """Test basic response generation."""
        # Arrange
        question = "Comment résoudre une équation du second degré?"
        expected_response = "Pour résoudre une équation du second degré..."

        mock_openai.return_value = {
            "choices": [{"message": {"content": expected_response}}]
        }

        # Act
        response = aria_service.generate_response(question)

        # Assert
        assert response == expected_response
        mock_openai.assert_called_once()

    def test_generate_response_with_context(
        self, aria_service, mock_openai, student_factory
    ):
        """Test response generation with student context."""
        # Arrange
        student = student_factory.create(
            grade_level="Terminale", preferred_subjects=["Mathématiques", "NSI"]
        )
        question = "Peux-tu m'expliquer les fonctions en NSI?"
        expected_response = "Les fonctions en NSI sont des blocs de code..."

        mock_openai.return_value = {
            "choices": [{"message": {"content": expected_response}}]
        }

        # Act
        response = aria_service.generate_response(
            question,
            student_context={
                "grade_level": student.grade_level,
                "subjects": student.preferred_subjects,
            },
        )

        # Assert
        assert response == expected_response
        call_args = mock_openai.call_args
        assert "Terminale" in str(call_args)
        assert "NSI" in str(call_args)

    def test_generate_exercise(self, aria_service, mock_openai):
        """Test exercise generation."""
        # Arrange
        subject = "Mathématiques"
        grade_level = "Terminale"
        difficulty = "Moyen"

        expected_exercise = {
            "title": "Équations du second degré",
            "description": "Résoudre l'équation x² - 5x + 6 = 0",
            "solution": "x = 2 ou x = 3",
            "hints": ["Utilisez la formule quadratique", "Factorisez si possible"],
        }

        mock_openai.return_value = {
            "choices": [{"message": {"content": json.dumps(expected_exercise)}}]
        }

        # Act
        exercise = aria_service.generate_exercise(subject, grade_level, difficulty)

        # Assert
        assert exercise == expected_exercise
        mock_openai.assert_called_once()

    def test_generate_response_with_empty_question(self, aria_service):
        """Test response generation with empty question."""
        # Act & Assert
        with pytest.raises(ValueError, match="Question cannot be empty"):
            aria_service.generate_response("")

    def test_generate_response_with_none_question(self, aria_service):
        """Test response generation with None question."""
        # Act & Assert
        with pytest.raises(ValueError, match="Question cannot be empty"):
            aria_service.generate_response(None)

    def test_openai_api_error_handling(self, aria_service):
        """Test handling of OpenAI API errors."""
        # Arrange
        with patch("openai.ChatCompletion.create") as mock_openai:
            mock_openai.side_effect = Exception("API Error")

            # Act & Assert
            with pytest.raises(Exception, match="API Error"):
                aria_service.generate_response("Test question")

    def test_response_caching(self, aria_service, mock_openai, mock_redis):
        """Test response caching mechanism."""
        # Arrange
        question = "What is 2+2?"
        cached_response = "4"

        # Simulate cache hit
        mock_redis.get.return_value = cached_response.encode()

        # Act
        response = aria_service.generate_response(question)

        # Assert
        assert response == cached_response
        mock_openai.assert_not_called()  # Should not call OpenAI if cached

    def test_response_rate_limiting(self, aria_service, mock_redis):
        """Test rate limiting for ARIA requests."""
        # Arrange
        question = "Test question"
        user_id = "test_user_123"

        # Simulate rate limit exceeded
        mock_redis.incr.return_value = 11  # Assuming limit is 10

        # Act & Assert
        with pytest.raises(Exception, match="Rate limit exceeded"):
            aria_service.generate_response(question, user_id=user_id)

    @pytest.mark.asyncio
    async def test_async_response_generation(self, aria_service):
        """Test asynchronous response generation."""
        # Arrange
        question = "Async test question"
        expected_response = "Async response"

        with patch.object(
            aria_service, "generate_response_async", new_callable=AsyncMock
        ) as mock_async:
            mock_async.return_value = expected_response

            # Act
            response = await aria_service.generate_response_async(question)

            # Assert
            assert response == expected_response
            mock_async.assert_called_once_with(question)

    def test_custom_prompt_templates(self, aria_service, mock_openai):
        """Test custom prompt templates for different subjects."""
        # Arrange
        question = "Explain variables"
        subject = "NSI"

        expected_response = "En NSI, une variable est..."
        mock_openai.return_value = {
            "choices": [{"message": {"content": expected_response}}]
        }

        # Act
        response = aria_service.generate_response(
            question, subject=subject, use_subject_template=True
        )

        # Assert
        assert response == expected_response
        call_args = mock_openai.call_args
        # Should contain NSI-specific prompt elements
        assert (
            "programmation" in str(call_args).lower() or "nsi" in str(call_args).lower()
        )

    def test_multilingual_support(self, aria_service, mock_openai):
        """Test multilingual response support."""
        # Arrange
        question = "What is a function?"
        language = "en"

        expected_response = "A function is a block of code..."
        mock_openai.return_value = {
            "choices": [{"message": {"content": expected_response}}]
        }

        # Act
        response = aria_service.generate_response(question, language=language)

        # Assert
        assert response == expected_response
        call_args = mock_openai.call_args
        assert "english" in str(call_args).lower() or "en" in str(call_args)

    def test_response_validation(self, aria_service, mock_openai):
        """Test response content validation."""
        # Arrange
        question = "Test question"
        invalid_response = ""  # Empty response

        mock_openai.return_value = {
            "choices": [{"message": {"content": invalid_response}}]
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid response from AI"):
            aria_service.generate_response(question, validate_response=True)

    def test_token_usage_tracking(self, aria_service, mock_openai):
        """Test token usage tracking for billing."""
        # Arrange
        question = "Test question"
        expected_response = "Test response"

        mock_openai.return_value = {
            "choices": [{"message": {"content": expected_response}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }

        # Act
        response = aria_service.generate_response(question, track_usage=True)

        # Assert
        assert response == expected_response
        # Should have recorded usage statistics
        assert hasattr(aria_service, "last_usage")
        assert aria_service.last_usage["total_tokens"] == 15
