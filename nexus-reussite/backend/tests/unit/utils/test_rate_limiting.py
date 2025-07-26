"""
Unit tests for rate limiting utilities.
"""

import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from src.utils.rate_limit import RateLimiter, RateLimitExceeded
from tests.factories import UserFactory


class TestRateLimiter:
    """Test suite for rate limiting functionality."""

    @pytest.fixture
    def rate_limiter(self, mock_redis):
        """Create rate limiter instance with mocked Redis."""
        return RateLimiter(redis_client=mock_redis)

    def test_rate_limiter_initialization(self, rate_limiter):
        """Test rate limiter initialization."""
        assert rate_limiter is not None
        assert hasattr(rate_limiter, "is_allowed")
        assert hasattr(rate_limiter, "get_remaining_requests")

    def test_first_request_allowed(self, rate_limiter, mock_redis):
        """Test that first request is always allowed."""
        # Arrange
        user_id = "test_user_123"
        endpoint = "/api/aria/chat"
        mock_redis.get.return_value = None  # No previous requests
        mock_redis.incr.return_value = 1

        # Act
        result = rate_limiter.is_allowed(user_id, endpoint)

        # Assert
        assert result is True
        mock_redis.incr.assert_called_once()
        mock_redis.expire.assert_called_once()

    def test_requests_within_limit_allowed(self, rate_limiter, mock_redis):
        """Test that requests within limit are allowed."""
        # Arrange
        user_id = "test_user_123"
        endpoint = "/api/aria/chat"
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 5  # Within limit of 10

        # Act
        result = rate_limiter.is_allowed(user_id, endpoint, limit=10)

        # Assert
        assert result is True

    def test_requests_exceeding_limit_denied(self, rate_limiter, mock_redis):
        """Test that requests exceeding limit are denied."""
        # Arrange
        user_id = "test_user_123"
        endpoint = "/api/aria/chat"
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 11  # Exceeds limit of 10

        # Act & Assert
        with pytest.raises(RateLimitExceeded):
            rate_limiter.is_allowed(user_id, endpoint, limit=10)

    def test_different_endpoints_separate_limits(self, rate_limiter, mock_redis):
        """Test that different endpoints have separate rate limits."""
        # Arrange
        user_id = "test_user_123"
        endpoint1 = "/api/aria/chat"
        endpoint2 = "/api/exercises/generate"

        # Mock different counters for different endpoints
        def mock_incr(key):
            if endpoint1 in key:
                return 5
            elif endpoint2 in key:
                return 3
            return 1

        mock_redis.incr.side_effect = mock_incr
        mock_redis.get.return_value = None

        # Act
        result1 = rate_limiter.is_allowed(user_id, endpoint1, limit=10)
        result2 = rate_limiter.is_allowed(user_id, endpoint2, limit=10)

        # Assert
        assert result1 is True
        assert result2 is True

    def test_different_users_separate_limits(
        self, rate_limiter, mock_redis, user_factory
    ):
        """Test that different users have separate rate limits."""
        # Arrange
        user1 = user_factory.create()
        user2 = user_factory.create()
        endpoint = "/api/aria/chat"

        # Mock different counters for different users
        def mock_incr(key):
            if str(user1.id) in key:
                return 10
            elif str(user2.id) in key:
                return 1
            return 1

        mock_redis.incr.side_effect = mock_incr
        mock_redis.get.return_value = None

        # Act
        result1 = rate_limiter.is_allowed(str(user1.id), endpoint, limit=10)
        result2 = rate_limiter.is_allowed(str(user2.id), endpoint, limit=10)

        # Assert
        assert result1 is True  # User1 at limit
        assert result2 is True  # User2 well within limit

    def test_get_remaining_requests(self, rate_limiter, mock_redis):
        """Test getting remaining request count."""
        # Arrange
        user_id = "test_user_123"
        endpoint = "/api/aria/chat"
        current_count = 7
        limit = 10

        mock_redis.get.return_value = str(current_count).encode()

        # Act
        remaining = rate_limiter.get_remaining_requests(user_id, endpoint, limit)

        # Assert
        assert remaining == 3  # 10 - 7 = 3

    def test_reset_user_limit(self, rate_limiter, mock_redis):
        """Test resetting rate limit for a user."""
        # Arrange
        user_id = "test_user_123"
        endpoint = "/api/aria/chat"

        # Act
        rate_limiter.reset_user_limit(user_id, endpoint)

        # Assert
        expected_key = f"rate_limit:{user_id}:{endpoint}"
        mock_redis.delete.assert_called_with(expected_key)

    def test_rate_limit_with_custom_window(self, rate_limiter, mock_redis):
        """Test rate limiting with custom time window."""
        # Arrange
        user_id = "test_user_123"
        endpoint = "/api/aria/chat"
        custom_window = 3600  # 1 hour
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 1

        # Act
        result = rate_limiter.is_allowed(
            user_id, endpoint, limit=100, window=custom_window
        )

        # Assert
        assert result is True
        # Verify custom window was used for expiration
        mock_redis.expire.assert_called_with(
            f"rate_limit:{user_id}:{endpoint}", custom_window
        )

    def test_rate_limit_key_format(self, rate_limiter, mock_redis):
        """Test that rate limit keys are formatted correctly."""
        # Arrange
        user_id = "test_user_123"
        endpoint = "/api/aria/chat"
        expected_key = f"rate_limit:{user_id}:{endpoint}"
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 1

        # Act
        rate_limiter.is_allowed(user_id, endpoint)

        # Assert
        mock_redis.incr.assert_called_with(expected_key)

    def test_rate_limit_decorator(self):
        """Test rate limit decorator functionality."""
        # Arrange
        with patch("src.utils.rate_limit.RateLimiter") as MockRateLimiter:
            mock_limiter = MockRateLimiter.return_value
            mock_limiter.is_allowed.return_value = True

            from src.utils.rate_limit import rate_limit

            @rate_limit(limit=5, window=60)
            def test_function(user_id):
                return f"Success for {user_id}"

            # Act
            result = test_function("test_user")

            # Assert
            assert result == "Success for test_user"
            mock_limiter.is_allowed.assert_called_once()

    def test_rate_limit_decorator_with_exceeded_limit(self):
        """Test rate limit decorator when limit is exceeded."""
        # Arrange
        with patch("src.utils.rate_limit.RateLimiter") as MockRateLimiter:
            mock_limiter = MockRateLimiter.return_value
            mock_limiter.is_allowed.side_effect = RateLimitExceeded(
                "Rate limit exceeded"
            )

            from src.utils.rate_limit import rate_limit

            @rate_limit(limit=5, window=60)
            def test_function(user_id):
                return f"Success for {user_id}"

            # Act & Assert
            with pytest.raises(RateLimitExceeded):
                test_function("test_user")

    def test_burst_requests_handling(self, rate_limiter, mock_redis):
        """Test handling of burst requests."""
        # Arrange
        user_id = "test_user_123"
        endpoint = "/api/aria/chat"
        limit = 5

        # Simulate burst of requests
        request_count = 0

        def mock_incr(key):
            nonlocal request_count
            request_count += 1
            return request_count

        mock_redis.incr.side_effect = mock_incr
        mock_redis.get.return_value = None

        # Act & Assert
        # First 5 requests should succeed
        for i in range(5):
            assert rate_limiter.is_allowed(user_id, endpoint, limit=limit) is True

        # 6th request should fail
        with pytest.raises(RateLimitExceeded):
            rate_limiter.is_allowed(user_id, endpoint, limit=limit)

    def test_redis_connection_error_handling(self, rate_limiter):
        """Test handling of Redis connection errors."""
        # Arrange
        with patch.object(rate_limiter, "redis_client") as mock_redis:
            mock_redis.incr.side_effect = ConnectionError("Redis connection failed")

            # Act & Assert
            # Should allow request if Redis is unavailable (fail-open)
            result = rate_limiter.is_allowed("user", "/api/test", fail_open=True)
            assert result is True

    def test_rate_limit_with_ip_address(self, rate_limiter, mock_redis):
        """Test rate limiting by IP address."""
        # Arrange
        ip_address = "192.168.1.1"
        endpoint = "/api/public/search"
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 1

        # Act
        result = rate_limiter.is_allowed_by_ip(ip_address, endpoint, limit=100)

        # Assert
        assert result is True
        expected_key = f"rate_limit:ip:{ip_address}:{endpoint}"
        mock_redis.incr.assert_called_with(expected_key)
