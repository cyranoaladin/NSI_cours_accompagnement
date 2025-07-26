"""
Modèles pour le système de production de contenu personnalisé
Nexus Réussite - Content Management System
"""

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from ..database import db
from .base import BaseModel, SoftDeleteMixin


class BrickType(Enum):
    """Types de briques de contenu disponibles"""

    DEFINITION = "definition"
    THEOREME = "theoreme"
    PROPRIETE = "propriete"
    EXEMPLE = "exemple"
    EXERCICE = "exercice"
    CORRECTION = "correction"
    CONSEIL_METHODE = "conseil_methode"
    HISTOIRE_SCIENCES = "histoire_sciences"
    SCHEMA = "schema"
    FORMULE = "formule"


class Subject(Enum):
    """Matières disponibles"""

    MATHEMATIQUES = "mathematiques"
    NSI = "nsi"
    PHYSIQUE = "physique"
    CHIMIE = "chimie"
    FRANCAIS = "francais"
    PHILOSOPHIE = "philosophie"
    HISTOIRE_GEO = "histoire_geo"
    SES = "ses"


class TargetProfile(Enum):
    """Profils d'élèves ciblés"""

    STRUGGLING = "struggling"  # En difficulté
    AVERAGE = "average"  # Niveau moyen
    EXCELLENCE = "excellence"  # Visant l'excellence
    REMEDIATION = "remediation"  # Remédiation spécifique


class LearningStep(Enum):
    """Étapes d'apprentissage"""

    DISCOVERY = "discovery"  # Découverte du concept
    TRAINING = "training"  # Entraînement
    DEEPENING = "deepening"  # Approfondissement
    REVISION = "revision"  # Révision
    EVALUATION = "evaluation"  # Évaluation


class ContentBrick(BaseModel, SoftDeleteMixin):
    """Modèle d'une brique de contenu"""

    __tablename__ = "content_bricks"

    # Contenu principal
    content = db.Column(db.Text, nullable=False)  # Contenu en Markdown/HTML
    brick_type = db.Column(db.Enum(BrickType), nullable=False)
    title = db.Column(db.String(200), nullable=False)

    # Métadonnées pour la personnalisation
    subject = db.Column(db.Enum(Subject), nullable=False)
    chapter = db.Column(
        db.String(100), nullable=False
    )  # Ex: "Suites numériques", "Graphes"
    difficulty = db.Column(
        db.Integer, nullable=False
    )  # De 1 (très facile) à 5 (expert)
    target_profiles = db.Column(db.JSON, nullable=False)  # Liste des profils ciblés
    learning_steps = db.Column(
        db.JSON, nullable=False
    )  # Liste des étapes d'apprentissage

    # Métadonnées additionnelles
    tags = db.Column(db.JSON, nullable=True)  # Tags libres pour recherche
    prerequisites = db.Column(db.JSON, nullable=True)  # IDs des briques prérequises
    duration_minutes = db.Column(db.Integer, nullable=False)  # Temps estimé de travail

    # Informations de création
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)

    # Statistiques d'utilisation
    usage_count = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    total_ratings = db.Column(db.Integer, default=0)

    # Relations
    document_bricks = db.relationship(
        "DocumentBrick", backref="content_brick", lazy=True
    )
    ratings = db.relationship("ContentBrickRating", backref="content_brick", lazy=True)

    def to_dict(self) -> Dict[str, Any]:
        """Conversion en dictionnaire pour stockage JSON"""
        return {
            "id": self.id,
            "content": self.content,
            "type": self.brick_type.value,
            "title": self.title,
            "subject": self.subject.value,
            "chapter": self.chapter,
            "difficulty": self.difficulty,
            "target_profiles": self.target_profiles or [],
            "learning_steps": self.learning_steps or [],
            "tags": self.tags or [],
            "prerequisites": self.prerequisites or [],
            "duration_minutes": self.duration_minutes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "author_id": self.author_id,
            "author_name": self.author_name,
            "usage_count": self.usage_count,
            "average_rating": self.average_rating,
            "total_ratings": self.total_ratings,
        }


class DocumentRequest(BaseModel):
    """Requête de génération de document personnalisé"""

    __tablename__ = "document_requests"

    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    student_profile = db.Column(db.Enum(TargetProfile), nullable=False)
    subject = db.Column(db.Enum(Subject), nullable=False)
    chapter = db.Column(db.String(100), nullable=False)
    document_type = db.Column(
        db.String(50), nullable=False
    )  # "fiche_revision", "exercices", "cours_complet"

    # Difficulté (min et max)
    difficulty_min = db.Column(db.Integer, nullable=False)
    difficulty_max = db.Column(db.Integer, nullable=False)

    learning_step = db.Column(db.Enum(LearningStep), nullable=False)
    duration_target = db.Column(db.Integer, nullable=False)  # Durée cible en minutes
    specific_topics = db.Column(db.JSON, nullable=True)  # Sujets spécifiques à couvrir
    exclude_topics = db.Column(db.JSON, nullable=True)  # Sujets à éviter
    requested_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # ID du demandeur

    # Préférences de format
    include_examples = db.Column(db.Boolean, default=True)
    include_exercises = db.Column(db.Boolean, default=True)
    include_corrections = db.Column(db.Boolean, default=True)
    include_methods = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=1)  # 1=normal, 2=urgent, 3=critique

    # Statut de traitement
    status = db.Column(
        db.String(20), default="pending"
    )  # pending, processing, completed, failed
    processed_at = db.Column(db.DateTime, nullable=True)

    # Relations
    generated_documents = db.relationship(
        "GeneratedDocument", backref="request", lazy=True
    )


class GeneratedDocument(BaseModel, SoftDeleteMixin):
    """Document généré par le système"""

    __tablename__ = "generated_documents"

    request_id = db.Column(
        db.Integer, db.ForeignKey("document_requests.id"), nullable=False
    )

    # Contenu généré
    content_html = db.Column(db.Text, nullable=False)  # Contenu final en HTML
    content_markdown = db.Column(db.Text, nullable=False)  # Contenu final en Markdown
    title = db.Column(db.String(200), nullable=False)

    # Métadonnées du document
    estimated_duration = db.Column(
        db.Integer, nullable=False
    )  # Durée estimée en minutes
    difficulty_level = db.Column(db.Float, nullable=False)  # Niveau de difficulté moyen

    # Informations de génération
    generation_time_ms = db.Column(db.Integer, nullable=False)  # Temps de génération
    template_used = db.Column(db.String(100), nullable=False)  # Template utilisé

    # Statistiques et feedback
    views_count = db.Column(db.Integer, default=0)
    completion_rate = db.Column(db.Float, default=0.0)
    student_rating = db.Column(db.Integer, nullable=True)  # Note de 1 à 5
    teacher_rating = db.Column(db.Integer, nullable=True)  # Note de 1 à 5

    # Relations
    document_bricks = db.relationship("DocumentBrick", backref="document", lazy=True)
    student_interactions = db.relationship(
        "DocumentInteraction", backref="document", lazy=True
    )


class DocumentBrick(BaseModel):
    """Table de liaison entre documents et briques de contenu"""

    __tablename__ = "document_bricks"

    document_id = db.Column(
        db.Integer, db.ForeignKey("generated_documents.id"), nullable=False
    )
    brick_id = db.Column(db.Integer, db.ForeignKey("content_bricks.id"), nullable=False)

    # Ordre d'apparition dans le document
    order_index = db.Column(db.Integer, nullable=False)

    # Contexte d'utilisation
    context_notes = db.Column(db.Text, nullable=True)

    # Contrainte d'unicité
    __table_args__ = (
        db.UniqueConstraint("document_id", "brick_id", name="unique_document_brick"),
    )


class ContentBrickRating(BaseModel):
    """Évaluations des briques de contenu par les utilisateurs"""

    __tablename__ = "content_brick_ratings"

    brick_id = db.Column(db.Integer, db.ForeignKey("content_bricks.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    rating = db.Column(db.Integer, nullable=False)  # Note de 1 à 5
    comment = db.Column(db.Text, nullable=True)

    # Type d'évaluateur
    evaluator_type = db.Column(db.String(20), nullable=False)  # student, teacher, admin

    # Contrainte d'unicité : un utilisateur ne peut évaluer qu'une fois
    __table_args__ = (
        db.UniqueConstraint("brick_id", "user_id", name="unique_brick_rating"),
    )


class DocumentInteraction(BaseModel):
    """Interactions des étudiants avec les documents générés"""

    __tablename__ = "document_interactions"

    document_id = db.Column(
        db.Integer, db.ForeignKey("generated_documents.id"), nullable=False
    )
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Type d'interaction
    interaction_type = db.Column(
        db.String(30), nullable=False
    )  # view, download, print, complete

    # Durée d'interaction
    duration_seconds = db.Column(db.Integer, nullable=True)

    # Progression dans le document
    progress_percentage = db.Column(db.Float, default=0.0)

    # Métadonnées
    device_type = db.Column(db.String(20), nullable=True)  # web, mobile, tablet
    ip_address = db.Column(db.String(45), nullable=True)


class ContentTemplate(BaseModel, SoftDeleteMixin):
    """Templates pour la génération de documents"""

    __tablename__ = "content_templates"

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    # Type de document supporté
    document_type = db.Column(db.String(50), nullable=False)

    # Template au format Jinja2
    template_content = db.Column(db.Text, nullable=False)

    # CSS associé
    css_styles = db.Column(db.Text, nullable=True)

    # Configuration par défaut
    default_config = db.Column(db.JSON, nullable=True)

    # Créateur du template
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Statistiques d'utilisation
    usage_count = db.Column(db.Integer, default=0)

    # Statut
    is_active = db.Column(db.Boolean, default=True)
