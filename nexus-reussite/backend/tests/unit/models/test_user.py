"""
Tests unitaires pour le modèle User
"""

import pytest

try:
    from src.database import db
    from src.models.user import User, UserStatus
except ImportError:
    # Fallback pour les tests - créer des mocks
    class UserStatus:  # pylint: disable=too-few-public-methods
        """Mock UserStatus enum for fallback testing"""

        ACTIVE = "active"
        INACTIVE = "inactive"
        SUSPENDED = "suspended"
        PENDING = "pending"

    class User:
        """Mock User class for fallback testing"""

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.id = getattr(self, "id", 1)
            self.status = getattr(self, "status", UserStatus.ACTIVE)

        def check_password(self, password):
            """Mock check password"""
            return password == getattr(self, "password", "test123")

        def set_password(self, password):
            """Mock set password"""
            # Définir l'attribut password dans le mock
            object.__setattr__(self, "password", password)

        def to_dict(self):
            """Mock to_dict method"""
            return {
                "id": self.id,
                "email": getattr(self, "email", ""),
                "first_name": getattr(self, "first_name", ""),
                "last_name": getattr(self, "last_name", ""),
                "role": getattr(self, "role", "student"),
                "status": self.status,
            }

    class MockDB:  # pylint: disable=too-few-public-methods
        """Mock database for fallback testing"""

        class Session:
            """Mock database session class"""

            @staticmethod
            def add(obj):
                """Mock add method"""
                _ = obj  # Ignore unused parameter

            @staticmethod
            def commit():
                """Mock commit method"""

        session = Session()

    db = MockDB()


class TestUserModel:
    """Tests pour la classe User"""

    def test_user_creation_with_valid_data(self, app):
        """Test création utilisateur avec données valides"""
        with app.app_context():
            # Arrange & Act
            user = User(
                email="john.doe@nexus-reussite.com",
                password="test123",
                first_name="John",
                last_name="Doe",
                role="student",
                status=UserStatus.ACTIVE,
            )

            # Assert
            assert user.email == "john.doe@nexus-reussite.com"
            assert user.first_name == "John"
            assert user.last_name == "Doe"
            assert user.role.value == "student"  # UserRole enum
            assert user.is_active is True
            # created_at sera défini lors de l'insertion en base

    def test_user_full_name_property(self, app):
        """Test propriété full_name calculée"""
        with app.app_context():
            # Arrange
            user = User(
                email="marie.martin@example.com",
                password="test123",
                first_name="Marie",
                last_name="Martin",
                role="student",
            )

            # Act & Assert
            assert user.full_name == "Marie Martin"

    def test_password_hashing_and_verification(self, app):
        """Test hachage et vérification mot de passe"""
        with app.app_context():
            # Arrange
            user = User(
                email="test@example.com",
                password="initial_password",
                first_name="Test",
                last_name="User",
                role="student",
            )
            password = "SecurePassword123!"

            # Act
            user.set_password(password)

            # Assert
            assert user.password_hash is not None
            assert user.password_hash != password
            assert len(user.password_hash) > 50  # Hash bcrypt est long
            assert user.check_password(password) is True
            assert user.check_password("WrongPassword") is False

    def test_user_json_serialization(self, app):
        """Test sérialisation JSON utilisateur (sécurité)"""
        with app.app_context():
            # Arrange
            user = User(
                email="secure@example.com",
                password="secret123",
                first_name="Secure",
                last_name="User",
                role="teacher",
            )

            # Act
            user_dict = (
                user.to_dict()
                if hasattr(user, "to_dict")
                else {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "is_active": user.is_active,
                }
            )

            # Assert
            assert user_dict["email"] == "secure@example.com"
            assert user_dict["full_name"] == "Secure User"
            assert user_dict["role"] == "teacher"
            assert "password_hash" not in user_dict  # Sécurité critique
            assert "password" not in user_dict

    def test_user_role_validation(self, app):
        """Test validation des rôles utilisateur"""
        with app.app_context():
            # Test rôles valides
            valid_roles = ["student", "teacher", "admin", "parent"]

            for role in valid_roles:
                user = User(
                    email=f"test_{role}@example.com",
                    password="TestPass123!",
                    first_name="Test",
                    last_name="User",
                    role=role,
                )
                assert user.role.value == role

    def test_user_email_uniqueness_constraint(self, app):
        """Test contrainte unicité email"""
        with app.app_context():
            # Créer d'abord les tables dans le test
            db.create_all()

            # Arrange
            email = "unique@example.com"

            user1 = User(
                email=email,
                password="Pass123!",
                first_name="User",
                last_name="One",
                role="student",
            )
            db.session.add(user1)
            db.session.commit()

            user2 = User(
                email=email,
                password="Pass123!",
                first_name="User",
                last_name="Two",
                role="student",
            )
            db.session.add(user2)

            # Act & Assert
            with pytest.raises(Exception):  # IntegrityError attendue
                db.session.commit()

    def test_user_string_representation(self, app):
        """Test représentation string de l'utilisateur"""
        with app.app_context():
            # Arrange
            user = User(
                email="display@example.com",
                password="DisplayPass123!",
                first_name="Display",
                last_name="Test",
                role="student",
            )

            # Act & Assert
            user_str = str(user)
            assert (
                "Display Test" in user_str
                or "display@example.com" in user_str
                or "<User" in user_str
            )
