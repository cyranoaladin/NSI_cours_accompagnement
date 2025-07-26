"""
Load testing configuration for Nexus Réussite Backend using Locust.
"""

import json
import random

from locust import HttpUser, between, task


class NexusReussiteUser(HttpUser):
    """
    Simulate user behavior for load testing Nexus Réussite backend.
    """

    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Called on start - simulate user login."""
        self.login()

    def login(self):
        """Simulate user login to get authentication token."""
        login_data = {
            "email": f"testuser{random.randint(1, 1000)}@nexus-reussite.com",
            "password": "TestPassword123!",
        }

        with self.client.post(
            "/api/auth/login", json=login_data, catch_response=True
        ) as response:
            if response.status_code == 200:
                self.token = response.json().get("token")
                response.success()
            else:
                response.failure(f"Login failed: {response.status_code}")

    @property
    def auth_headers(self):
        """Get authentication headers."""
        return {"Authorization": f"Bearer {getattr(self, 'token', 'test-token')}"}

    @task(3)
    def chat_with_aria(self):
        """Test ARIA chat functionality - most common user action."""
        questions = [
            "Comment résoudre une équation du second degré?",
            "Explique-moi les listes en Python",
            "Qu'est-ce qu'une fonction mathématique?",
            "Comment créer une classe en Python?",
            "Peux-tu m'aider avec les probabilités?",
        ]

        payload = {
            "message": random.choice(questions),
            "context": {
                "grade_level": random.choice(["Terminale", "Première", "Seconde"]),
                "subject": random.choice(["Mathématiques", "NSI", "Physique-Chimie"]),
            },
        }

        with self.client.post(
            "/api/aria/chat",
            json=payload,
            headers=self.auth_headers,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 429:  # Rate limited
                response.success()  # This is expected behavior
            else:
                response.failure(f"ARIA chat failed: {response.status_code}")

    @task(2)
    def get_exercises(self):
        """Test exercise retrieval."""
        params = {
            "subject": random.choice(["Mathématiques", "NSI", "Physique-Chimie"]),
            "grade_level": random.choice(["Terminale", "Première", "Seconde"]),
            "difficulty": random.choice(["Facile", "Moyen", "Difficile"]),
        }

        with self.client.get(
            "/api/exercises",
            params=params,
            headers=self.auth_headers,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get exercises failed: {response.status_code}")

    @task(1)
    def generate_exercise(self):
        """Test exercise generation - less frequent action."""
        payload = {
            "subject": random.choice(["Mathématiques", "NSI"]),
            "grade_level": random.choice(["Terminale", "Première"]),
            "difficulty": random.choice(["Moyen", "Difficile"]),
            "exercise_type": random.choice(["QCM", "OPEN_QUESTION", "CODE", "MATH"]),
        }

        with self.client.post(
            "/api/exercises/generate",
            json=payload,
            headers=self.auth_headers,
            catch_response=True,
        ) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            elif response.status_code == 429:  # Rate limited
                response.success()  # Expected for resource-intensive operations
            else:
                response.failure(f"Generate exercise failed: {response.status_code}")

    @task(1)
    def get_documents(self):
        """Test document retrieval."""
        params = {
            "subject": random.choice(["Mathématiques", "NSI", "Physique-Chimie"]),
            "document_type": random.choice(["COURS", "FICHE", "METHODOLOGIE"]),
        }

        with self.client.get(
            "/api/documents",
            params=params,
            headers=self.auth_headers,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get documents failed: {response.status_code}")

    @task(1)
    def get_user_profile(self):
        """Test user profile retrieval."""
        with self.client.get(
            "/api/users/profile", headers=self.auth_headers, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get profile failed: {response.status_code}")


class AnonymousUser(HttpUser):
    """
    Simulate anonymous user behavior for public endpoints.
    """

    wait_time = between(2, 5)

    @task(1)
    def get_public_content(self):
        """Test public content access."""
        with self.client.get("/api/public/subjects", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Public content failed: {response.status_code}")

    @task(1)
    def attempt_register(self):
        """Test user registration."""
        user_data = {
            "email": f"newuser{random.randint(1, 10000)}@example.com",
            "password": "StrongPassword123!",
            "first_name": "Test",
            "last_name": "User",
            "role": "student",
        }

        with self.client.post(
            "/api/auth/register", json=user_data, catch_response=True
        ) as response:
            if response.status_code in [200, 201, 409]:  # 409 = user exists
                response.success()
            else:
                response.failure(f"Registration failed: {response.status_code}")


class AdminUser(HttpUser):
    """
    Simulate admin user behavior - heavier operations.
    """

    wait_time = between(3, 8)
    weight = 1  # Lower weight = fewer admin users

    def on_start(self):
        """Admin login."""
        login_data = {
            "email": "admin@nexus-reussite.com",
            "password": "AdminPassword123!",
        }

        with self.client.post(
            "/api/auth/login", json=login_data, catch_response=True
        ) as response:
            if response.status_code == 200:
                self.token = response.json().get("token")
                response.success()
            else:
                response.failure(f"Admin login failed: {response.status_code}")

    @property
    def auth_headers(self):
        """Get admin authentication headers."""
        return {"Authorization": f"Bearer {getattr(self, 'token', 'admin-token')}"}

    @task(2)
    def get_system_metrics(self):
        """Test system metrics endpoint."""
        with self.client.get(
            "/api/admin/metrics", headers=self.auth_headers, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Metrics failed: {response.status_code}")

    @task(1)
    def manage_users(self):
        """Test user management endpoints."""
        with self.client.get(
            "/api/admin/users", headers=self.auth_headers, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"User management failed: {response.status_code}")

    @task(1)
    def content_moderation(self):
        """Test content moderation."""
        with self.client.get(
            "/api/admin/content/pending", headers=self.auth_headers, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Content moderation failed: {response.status_code}")
