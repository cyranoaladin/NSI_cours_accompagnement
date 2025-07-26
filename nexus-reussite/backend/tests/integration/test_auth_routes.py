"""
Tests d'intégration pour les routes d'authentification
"""

# pylint: disable=import-error,unused-import

import json  # noqa: F401 - Used in Flask test client json parameter

import pytest

from src.database import db
from src.main_production import create_app
from src.models.user import User


class TestAuthRoutes:
    """Tests d'intégration pour l'authentification"""

    @pytest.fixture
    def client(self):
        """Fixture client de test avec base de données en mémoire"""
        app = create_app(testing=True)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["JWT_SECRET_KEY"] = "test-secret-key"

        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()

    def test_register_new_user_success(self, client):
        """Test inscription nouvel utilisateur avec succès"""
        # Arrange
        user_data = {
            "email": "nouveau@test.com",
            "password": "MotDePasse123!",
            "first_name": "Jean",
            "last_name": "Dupont",
            "role": "student",
        }

        # Act
        response = client.post(
            "/api/auth/register", json=user_data, content_type="application/json"
        )

        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Utilisateur créé avec succès"
        assert "user_id" in data
        assert "token" in data

        # Vérifier que l'utilisateur existe en base
        user = User.query.filter_by(email="nouveau@test.com").first()
        assert user is not None
        assert user.first_name == "Jean"
        assert user.role == "student"

    def test_register_duplicate_email(self, client):
        """Test inscription avec email déjà existant"""
        # Arrange - Créer un utilisateur existant
        existing_user_data = {
            "email": "existant@test.com",
            "password": "Password123!",
            "first_name": "Marie",
            "last_name": "Martin",
            "role": "student",
        }
        client.post("/api/auth/register", json=existing_user_data)

        # Tentative d'inscription avec même email
        duplicate_data = {
            "email": "existant@test.com",
            "password": "AutrePassword123!",
            "first_name": "Paul",
            "last_name": "Durand",
            "role": "teacher",
        }

        # Act
        response = client.post("/api/auth/register", json=duplicate_data)

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert "déjà utilisé" in data["error"].lower()

    def test_register_invalid_email(self, client):
        """Test inscription avec email invalide"""
        # Arrange
        invalid_data = {
            "email": "email-invalide",
            "password": "Password123!",
            "first_name": "Test",
            "last_name": "User",
        }

        # Act
        response = client.post("/api/auth/register", json=invalid_data)

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert "email" in data["error"].lower()

    def test_register_weak_password(self, client):
        """Test inscription avec mot de passe faible"""
        # Arrange
        weak_password_data = {
            "email": "test@example.com",
            "password": "123",  # Trop faible
            "first_name": "Test",
            "last_name": "User",
        }

        # Act
        response = client.post("/api/auth/register", json=weak_password_data)

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert "mot de passe" in data["error"].lower()

    def test_login_valid_credentials(self, client):
        """Test connexion avec identifiants valides"""
        # Arrange - Créer un utilisateur
        user_data = {
            "email": "login@test.com",
            "password": "MotDePasse123!",
            "first_name": "Login",
            "last_name": "Test",
        }
        client.post("/api/auth/register", json=user_data)

        # Act
        login_data = {"email": "login@test.com", "password": "MotDePasse123!"}
        response = client.post("/api/auth/login", json=login_data)

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["email"] == "login@test.com"

    def test_login_invalid_credentials(self, client):
        """Test connexion avec identifiants invalides"""
        # Arrange - Créer un utilisateur
        user_data = {
            "email": "user@test.com",
            "password": "CorrectPassword123!",
            "first_name": "User",
            "last_name": "Test",
        }
        client.post("/api/auth/register", json=user_data)

        # Act - Tentative avec mauvais mot de passe
        login_data = {"email": "user@test.com", "password": "WrongPassword123!"}
        response = client.post("/api/auth/login", json=login_data)

        # Assert
        assert response.status_code == 401
        data = response.get_json()
        assert "identifiants" in data["error"].lower()

    def test_login_nonexistent_user(self, client):
        """Test connexion avec utilisateur inexistant"""
        # Act
        login_data = {"email": "inexistant@test.com", "password": "Password123!"}
        response = client.post("/api/auth/login", json=login_data)

        # Assert
        assert response.status_code == 401
        data = response.get_json()
        assert "utilisateur" in data["error"].lower()

    def test_protected_route_without_token(self, client):
        """Test accès route protégée sans token"""
        # Act
        response = client.get("/api/user/profile")

        # Assert
        assert response.status_code == 401
        data = response.get_json()
        assert "token" in data["error"].lower()

    def test_protected_route_with_valid_token(self, client):
        """Test accès route protégée avec token valide"""
        # Arrange - Créer utilisateur et obtenir token
        user_data = {
            "email": "protected@test.com",
            "password": "Password123!",
            "first_name": "Protected",
            "last_name": "User",
        }
        client.post("/api/auth/register", json=user_data)

        login_response = client.post(
            "/api/auth/login",
            json={"email": "protected@test.com", "password": "Password123!"},
        )
        token = login_response.get_json()["token"]

        # Act
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/user/profile", headers=headers)

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data["email"] == "protected@test.com"
        assert data["first_name"] == "Protected"

    def test_protected_route_with_invalid_token(self, client):
        """Test accès route protégée avec token invalide"""
        # Act
        headers = {"Authorization": "Bearer invalid-token-12345"}
        response = client.get("/api/user/profile", headers=headers)

        # Assert
        assert response.status_code == 401
        data = response.get_json()
        assert "token" in data["error"].lower()

    def test_logout_endpoint(self, client):
        """Test déconnexion utilisateur"""
        # Arrange - Créer utilisateur et se connecter
        user_data = {
            "email": "logout@test.com",
            "password": "Password123!",
            "first_name": "Logout",
            "last_name": "Test",
        }
        client.post("/api/auth/register", json=user_data)

        login_response = client.post(
            "/api/auth/login",
            json={"email": "logout@test.com", "password": "Password123!"},
        )
        token = login_response.get_json()["token"]

        # Act
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/auth/logout", headers=headers)

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert "déconnecté" in data["message"].lower()

    def test_refresh_token_endpoint(self, client):
        """Test renouvellement token"""
        # Arrange - Créer utilisateur et se connecter
        user_data = {
            "email": "refresh@test.com",
            "password": "Password123!",
            "first_name": "Refresh",
            "last_name": "Test",
        }
        client.post("/api/auth/register", json=user_data)

        login_response = client.post(
            "/api/auth/login",
            json={"email": "refresh@test.com", "password": "Password123!"},
        )
        token = login_response.get_json()["token"]

        # Act
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/auth/refresh", headers=headers)

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert "token" in data
        assert data["token"] != token  # Nouveau token différent
