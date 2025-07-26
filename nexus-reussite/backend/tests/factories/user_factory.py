"""
Factory for creating User model instances for testing.
"""

import factory
from faker import Faker

from src.database import db
from src.models.user import User, UserRole

fake = Faker("fr_FR")  # French locale for realistic test data


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base factory for User model."""

    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    email = factory.LazyAttribute(lambda obj: f"user{obj.id}@nexus-reussite.com")
    password = factory.LazyFunction(lambda: "TestPassword123!")
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    role = UserRole.STUDENT
    is_active = True
    email_verified = True
    created_at = factory.LazyFunction(fake.date_time_this_year)
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        """Set hashed password after creation."""
        if not create:
            return
        if extracted:
            obj.set_password(extracted)
        else:
            obj.set_password("TestPassword123!")


class StudentUserFactory(UserFactory):
    """Factory for creating student users."""

    role = UserRole.STUDENT


class TeacherUserFactory(UserFactory):
    """Factory for creating teacher users."""

    role = UserRole.TEACHER
    email = factory.LazyAttribute(lambda obj: f"teacher{obj.id}@nexus-reussite.com")


class AdminUserFactory(UserFactory):
    """Factory for creating admin users."""

    role = UserRole.ADMIN
    email = factory.LazyAttribute(lambda obj: f"admin{obj.id}@nexus-reussite.com")


class InactiveUserFactory(UserFactory):
    """Factory for creating inactive users."""

    is_active = False
    email_verified = False


class UnverifiedUserFactory(UserFactory):
    """Factory for creating unverified users."""

    email_verified = False
