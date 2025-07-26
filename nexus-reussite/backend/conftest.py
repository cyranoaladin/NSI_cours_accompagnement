"""
Configuration globale des tests pour Nexus Réussite Backend
"""

import asyncio
from unittest.mock import patch

import pytest
import pytest_asyncio

from src.database import db
from src.main_production import create_app
from src.models.student import Student
from src.models.user import User, UserRole
from tests.factories import (
    DocumentFactory,
    ExerciseFactory,
    StudentFactory,
    StudentUserFactory,
    TeacherUserFactory,
    UserFactory,
)


@pytest.fixture(scope="function")
def app():
    """
    Fixture application Flask pour les tests
    Utilise une base de données SQLite en mémoire pour l'isolation
    """
    import os

    # Configuration de test avec variables d'environnement
    os.environ["TESTING"] = "True"
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["JWT_SECRET_KEY"] = "test-jwt-secret"
    os.environ["OPENAI_API_KEY"] = "test-openai-key"
    os.environ["FLASK_ENV"] = "testing"

    # Créer l'application avec la config de test
    app = create_app("testing")  # pylint: disable=redefined-outer-name

    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        yield app
        # Nettoyer après les tests
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):  # pylint: disable=redefined-outer-name
    """Client de test Flask"""
    return app.test_client()


@pytest.fixture
def runner(app):  # pylint: disable=redefined-outer-name
    """Runner CLI de test"""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):  # pylint: disable=redefined-outer-name,unused-argument
    """Créer un utilisateur de test"""
    # app dependency ensures that the Flask app context is set up first
    user = User(
        email="test@nexus-reussite.com",
        password="TestPassword123!",
        first_name="Test",
        last_name="User",
        role=UserRole.STUDENT,
    )
    db.session.add(user)
    db.session.commit()
    yield user
    # Cleanup automatique avec la session


@pytest.fixture
def test_student(test_user):  # pylint: disable=redefined-outer-name
    """Créer un étudiant de test"""
    student = Student(
        full_name=f"{test_user.first_name} {test_user.last_name}",
        email=test_user.email,
        grade_level="Terminale",
        school="Lycée Test",
        preferred_subjects=["Mathématiques", "NSI"],
    )

    db.session.add(student)
    db.session.commit()
    yield student


@pytest.fixture
def auth_headers(client, test_user):  # pylint: disable=redefined-outer-name
    """Headers d'authentification avec token JWT"""
    login_data = {"email": "test@nexus-reussite.com", "password": "TestPassword123!"}

    # Simuler la route de login (à adapter selon votre implémentation)
    with patch("src.services.auth_service.verify_user_credentials") as mock_verify:
        mock_verify.return_value = test_user

        response = client.post("/api/auth/login", json=login_data)

        if response.status_code == 200:
            token = response.get_json().get("token")
            return {"Authorization": f"Bearer {token}"}
        # Fallback si pas d'implémentation JWT encore
        return {"X-User-ID": str(test_user.id)}


# === FACTORY-BASED FIXTURES ===


@pytest.fixture
def user_factory(app):  # pylint: disable=redefined-outer-name,unused-argument
    """Factory pour créer des utilisateurs de test"""
    return UserFactory


@pytest.fixture
def student_user_factory(app):  # pylint: disable=redefined-outer-name,unused-argument
    """Factory pour créer des utilisateurs étudiants"""
    return StudentUserFactory


@pytest.fixture
def teacher_user_factory(app):  # pylint: disable=redefined-outer-name,unused-argument
    """Factory pour créer des utilisateurs enseignants"""
    return TeacherUserFactory


@pytest.fixture
def student_factory(app):  # pylint: disable=redefined-outer-name,unused-argument
    """Factory pour créer des étudiants"""
    return StudentFactory


@pytest.fixture
def exercise_factory(app):  # pylint: disable=redefined-outer-name,unused-argument
    """Factory pour créer des exercices"""
    return ExerciseFactory


@pytest.fixture
def document_factory(app):  # pylint: disable=redefined-outer-name,unused-argument
    """Factory pour créer des documents"""
    return DocumentFactory


# === ASYNC SUPPORT ===


@pytest_asyncio.fixture
async def async_app(app):  # pylint: disable=redefined-outer-name
    """Fixture application Flask pour les tests asynchrones"""
    yield app


@pytest_asyncio.fixture
async def async_client(async_app):  # pylint: disable=redefined-outer-name
    """Client de test Flask asynchrone"""
    return async_app.test_client()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# === MOCK FIXTURES ===


@pytest.fixture
def mock_openai():
    """Mock OpenAI API pour éviter les appels réels"""
    with patch("openai.ChatCompletion.create") as mock:
        mock.return_value = {
            "choices": [{"message": {"content": "Réponse de test d'ARIA."}}]
        }
        yield mock


@pytest.fixture
def mock_redis():
    """Mock Redis pour les tests de cache et rate limiting"""
    with patch("redis.Redis") as mock:
        mock_instance = mock.return_value
        mock_instance.get.return_value = None
        mock_instance.set.return_value = True
        mock_instance.incr.return_value = 1
        mock_instance.expire.return_value = True
        yield mock_instance


@pytest.fixture
def mock_celery():
    """Mock Celery pour les tests de tâches asynchrones"""
    with patch("celery.Celery") as mock:
        mock_instance = mock.return_value
        mock_instance.send_task.return_value.id = "test-task-id"
        yield mock_instance
