"""
Tests unitaires pour Nexus Réussite Backend
Configuration de base et fixtures communes
"""
# pylint: disable=redefined-outer-name,unused-argument,import-error
import os

import pytest

from src.main_production import create_app, db
from src.models.user import User, UserRole, UserStatus

# Configuration pour les tests
os.environ['FLASK_ENV'] = 'testing'
os.environ['OPENAI_API_KEY'] = 'test-key-for-testing'


@pytest.fixture(scope='session')
def app():
    """Créer une application Flask pour les tests"""
    # Force l'utilisation de la configuration de test
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('testing')

    # Configuration explicite pour éviter les problèmes
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'connect_args': {'check_same_thread': False}
        },
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'JWT_SECRET_KEY': 'test-jwt-secret',
        'OPENAI_API_KEY': 'test-key',
    })

    return app


@pytest.fixture(scope='function')
def client(app):
    """Client de test Flask"""
    return app.test_client()


@pytest.fixture(scope='function')
def app_context(app):
    """Context d'application pour les tests"""
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def database(app_context):  # pylint: disable=unused-argument
    """Base de données temporaire pour les tests"""
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture
def sample_admin(database):
    """Utilisateur admin pour les tests"""
    admin = User(
        email='admin@test.com',
        password='test123',
        first_name='Test',
        last_name='Admin',
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        email_verified=True
    )
    database.session.add(admin)
    database.session.commit()
    return admin


@pytest.fixture
def sample_student(database):
    """Utilisateur étudiant pour les tests"""
    student = User(
        email='student@test.com',
        password='test123',
        first_name='Test',
        last_name='Student',
        role=UserRole.STUDENT,
        status=UserStatus.ACTIVE,
        email_verified=True
    )
    database.session.add(student)
    database.session.commit()
    return student


@pytest.fixture
def sample_teacher(database):
    """Utilisateur enseignant pour les tests"""
    teacher = User(
        email='teacher@test.com',
        password='test123',
        first_name='Test',
        last_name='Teacher',
        role=UserRole.TEACHER,
        status=UserStatus.ACTIVE,
        email_verified=True
    )
    database.session.add(teacher)
    database.session.commit()
    return teacher


@pytest.fixture
def auth_headers_admin(client, sample_admin):
    """Headers d'authentification pour admin"""
    response = client.post('/api/auth/login', json={
        'email': sample_admin.email,
        'password': 'test123'
    })

    if response.status_code == 200:
        token = response.get_json()['access_token']
        return {'Authorization': f'Bearer {token}'}
    return {}


@pytest.fixture
def auth_headers_student(client, sample_student):
    """Headers d'authentification pour étudiant"""
    response = client.post('/api/auth/login', json={
        'email': sample_student.email,
        'password': 'test123'
    })

    if response.status_code == 200:
        token = response.get_json()['access_token']
        return {'Authorization': f'Bearer {token}'}
    return {}


class TestHelper:
    """Classe d'aide pour les tests"""

    @staticmethod
    def create_test_user(role=UserRole.STUDENT, **kwargs):
        """Crée un utilisateur de test"""
        defaults = {
            'email': f'test_{role.value}@test.com',
            'password': 'test123',
            'first_name': 'Test',
            'last_name': role.value.capitalize(),
            'role': role,
            'status': UserStatus.ACTIVE,
            'email_verified': True
        }
        defaults.update(kwargs)

        user = User(**defaults)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login_user(client, email='test@test.com', password='test123'):
        """Connecte un utilisateur et retourne le token"""
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            return response.get_json()['access_token']
        return None

    @staticmethod
    def get_auth_headers(token):
        """Retourne les headers d'authentification"""
        return {'Authorization': f'Bearer {token}'}


# Configuration pytest
def pytest_configure(config):
    """Configuration globale de pytest"""
    config.addinivalue_line(
        "markers", "unit: marque les tests unitaires"
    )
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration"
    )
    config.addinivalue_line(
        "markers", "slow: marque les tests lents"
    )
    config.addinivalue_line(
        "markers", "api: marque les tests d'API"
    )
    config.addinivalue_line(
        "markers", "auth: marque les tests d'authentification"
    )
