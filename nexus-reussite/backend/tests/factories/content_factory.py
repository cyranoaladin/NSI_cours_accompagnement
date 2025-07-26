"""
Factory for creating content-related model instances for testing.
"""

import factory
from faker import Faker

from src.database import db
from src.models.content_system import (
    BrickType,
    ContentBrick,
    DocumentRequest,
    GeneratedDocument,
    LearningStep,
    Subject,
    TargetProfile,
)

fake = Faker("fr_FR")


class ContentBrickFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for ContentBrick model."""

    class Meta:
        model = ContentBrick
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    title = factory.LazyFunction(fake.sentence)
    content = factory.LazyFunction(fake.text)
    brick_type = factory.Iterator(BrickType)
    subject = factory.Iterator(Subject)
    chapter = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    difficulty = factory.Iterator([1, 2, 3, 4, 5])
    target_profiles = factory.LazyFunction(
        lambda: [
            profile.value
            for profile in fake.random_elements(
                elements=list(TargetProfile),
                length=fake.random_int(min=1, max=3),
                unique=True,
            )
        ]
    )
    learning_steps = factory.LazyFunction(
        lambda: [
            step.value
            for step in fake.random_elements(
                elements=list(LearningStep),
                length=fake.random_int(min=1, max=3),
                unique=True,
            )
        ]
    )
    tags = factory.LazyFunction(
        lambda: fake.random_elements(
            elements=[
                "algèbre",
                "géométrie",
                "programmation",
                "base_de_données",
                "algorithmes",
            ],
            length=fake.random_int(min=1, max=3),
            unique=True,
        )
    )
    prerequisites = factory.LazyFunction(
        lambda: [
            fake.random_int(min=1, max=100)
            for _ in range(fake.random_int(min=0, max=3))
        ]
    )
    duration_minutes = factory.LazyFunction(lambda: fake.random_int(min=5, max=120))
    author_id = factory.Sequence(lambda n: n)
    author_name = factory.LazyFunction(fake.name)
    usage_count = factory.LazyFunction(lambda: fake.random_int(min=0, max=100))
    average_rating = factory.LazyFunction(
        lambda: round(fake.random.uniform(1.0, 5.0), 1)
    )
    total_ratings = factory.LazyFunction(lambda: fake.random_int(min=0, max=20))


class ExerciseFactory(ContentBrickFactory):
    """Factory for Exercise-type ContentBrick."""

    brick_type = BrickType.EXERCICE
    title = factory.LazyFunction(lambda: f"Exercice: {fake.sentence()}")


class GeneratedDocumentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for GeneratedDocument model."""

    class Meta:
        model = GeneratedDocument
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    request_id = factory.Sequence(lambda n: n)
    content_html = factory.LazyFunction(fake.text)
    content_markdown = factory.LazyFunction(fake.text)
    title = factory.LazyFunction(lambda: f"Document: {fake.sentence()}")
    estimated_duration = factory.LazyFunction(lambda: fake.random_int(min=20, max=120))
    difficulty_level = factory.LazyFunction(lambda: fake.random.uniform(1, 5))
    generation_time_ms = factory.LazyFunction(
        lambda: fake.random_int(min=100, max=5000)
    )
    template_used = factory.LazyFunction(lambda: fake.word())
    views_count = factory.LazyFunction(lambda: fake.random_int(min=0, max=1000))
    completion_rate = factory.LazyFunction(lambda: fake.random.uniform(0, 100))
    student_rating = factory.LazyFunction(lambda: fake.random_int(min=1, max=5))
    teacher_rating = factory.LazyFunction(lambda: fake.random_int(min=1, max=5))


# Alias for backward compatibility
DocumentFactory = GeneratedDocumentFactory
