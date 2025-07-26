"""
Factory for creating Student model instances for testing.
"""

import factory
from faker import Faker

from src.database import db
from src.models.student import Student

fake = Faker("fr_FR")  # French locale for realistic test data


class StudentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for Student model."""

    class Meta:
        model = Student
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    full_name = factory.LazyFunction(lambda: fake.name())
    email = factory.LazyAttribute(lambda obj: f"student{obj.id}@nexus-reussite.com")
    grade_level = factory.Iterator(
        [
            "Sixième",
            "Cinquième",
            "Quatrième",
            "Troisième",
            "Seconde",
            "Première",
            "Terminale",
        ]
    )
    school = factory.LazyFunction(lambda: fake.company() + " Lycée")
    preferred_subjects = factory.LazyFunction(
        lambda: fake.random_elements(
            elements=[
                "Mathématiques",
                "NSI",
                "Physique-Chimie",
                "SVT",
                "Français",
                "Histoire-Géo",
            ],
            length=fake.random_int(min=1, max=3),
            unique=True,
        )
    )
    created_at = factory.LazyFunction(fake.date_time_this_year)
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)


class TerminaleStudentFactory(StudentFactory):
    """Factory for Terminale students specifically."""

    grade_level = "Terminale"
    preferred_subjects = ["Mathématiques", "NSI"]


class PremiereStudentFactory(StudentFactory):
    """Factory for Première students specifically."""

    grade_level = "Première"
    preferred_subjects = ["Mathématiques", "Physique-Chimie"]


class CollegeStudentFactory(StudentFactory):
    """Factory for college-level students."""

    grade_level = factory.Iterator(["Sixième", "Cinquième", "Quatrième", "Troisième"])
    preferred_subjects = factory.LazyFunction(
        lambda: fake.random_elements(
            elements=["Mathématiques", "Français", "Histoire-Géo", "SVT"],
            length=2,
            unique=True,
        )
    )
