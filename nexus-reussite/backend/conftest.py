"""
Configuration globale des tests pour Nexus Réussite Backend
"""
from unittest.mock import patch

import pytest

from src.main_production import create_app
from src.database import db
from src.models.user import User
from src.models.student import Student

@pytest.fixture(scope='session')
def app():
    """
    Fixture application Flask pour les tests
    Utilise une base de données SQLite en mémoire pour l'isolation
    """
    # Configuration de test
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key',
        'JWT_SECRET_KEY': 'test-jwt-secret',
        'WTF_CSRF_ENABLED': False,
        'OPENAI_API_KEY': 'test-openai-key'
    }

    # Créer l'application avec la config de test
    app = create_app(test_config)  # pylint: disable=redefined-outer-name

    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        yield app
        # Nettoyer après les tests
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
def test_user(app):  # pylint: disable=redefined-outer-name
    """Créer un utilisateur de test"""
    with app.app_context():
        user = User(
            email='test@nexus-reussite.com',
            password='TestPassword123!',
            first_name='Test',
            last_name='User',
            role='student'
        )
        db.session.add(user)
        db.session.commit()
        yield user
        # Cleanup automatique avec la session

@pytest.fixture
def test_student(app, test_user):  # pylint: disable=redefined-outer-name
    """Créer un étudiant de test"""
    with app.app_context():
        student = Student(
            full_name=f"{test_user.first_name} {test_user.last_name}",
            email=test_user.email,
            grade_level='Terminale',
            school='Lycée Test',
            preferred_subjects=['Mathématiques', 'NSI']
        )

        db.session.add(student)
        db.session.commit()
        yield student

@pytest.fixture
def auth_headers(client, test_user):  # pylint: disable=redefined-outer-name
    """Headers d'authentification avec token JWT"""
    login_data = {
        'email': 'test@nexus-reussite.com',
        'password': 'TestPassword123!'
    }

    # Simuler la route de login (à adapter selon votre implémentation)
    with patch('src.services.auth_service.verify_user_credentials') as mock_verify:
        mock_verify.return_value = test_user

        response = client.post('/api/auth/login', json=login_data)

        if response.status_code == 200:
            token = response.get_json().get('token')
            return {'Authorization': f'Bearer {token}'}
        # Fallback si pas d'implémentation JWT encore
        return {'X-User-ID': str(test_user.id)}

@pytest.fixture
def mock_openai():
    """Mock OpenAI API pour éviter les appels réels"""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {
            "choices": [{
                "message": {
                    "content": "Réponse de test d'ARIA."
                }
            }]
        }
        yield mock
