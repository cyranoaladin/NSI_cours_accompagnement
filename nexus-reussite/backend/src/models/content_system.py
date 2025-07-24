"""
Modèles pour le système de production de contenu personnalisé
Nexus Réussite - Content Management System
"""

from enum import Enum
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json

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
    STRUGGLING = "struggling"      # En difficulté
    AVERAGE = "average"           # Niveau moyen
    EXCELLENCE = "excellence"     # Visant l'excellence
    REMEDIATION = "remediation"   # Remédiation spécifique

class LearningStep(Enum):
    """Étapes d'apprentissage"""
    DISCOVERY = "discovery"       # Découverte du concept
    TRAINING = "training"         # Entraînement
    DEEPENING = "deepening"       # Approfondissement
    REVISION = "revision"         # Révision
    EVALUATION = "evaluation"     # Évaluation

@dataclass
class ContentBrick:
    """Modèle d'une brique de contenu"""
    id: str
    content: str                  # Contenu en Markdown/HTML
    type: BrickType
    title: str

    # Métadonnées pour la personnalisation
    subject: Subject
    chapter: str                  # Ex: "Suites numériques", "Graphes"
    difficulty: int               # De 1 (très facile) à 5 (expert)
    target_profiles: List[TargetProfile]
    learning_steps: List[LearningStep]

    # Métadonnées additionnelles
    tags: List[str]              # Tags libres pour recherche
    prerequisites: List[str]      # IDs des briques prérequises
    duration_minutes: int         # Temps estimé de travail

    # Informations de création
    created_at: datetime
    updated_at: datetime
    author_id: str
    author_name: str

    # Statistiques d'utilisation
    usage_count: int = 0
    average_rating: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Conversion en dictionnaire pour stockage JSON"""
        return {
            'id': self.id,
            'content': self.content,
            'type': self.type.value,
            'title': self.title,
            'subject': self.subject.value,
            'chapter': self.chapter,
            'difficulty': self.difficulty,
            'target_profiles': [p.value for p in self.target_profiles],
            'learning_steps': [s.value for s in self.learning_steps],
            'tags': self.tags,
            'prerequisites': self.prerequisites,
            'duration_minutes': self.duration_minutes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author_id': self.author_id,
            'author_name': self.author_name,
            'usage_count': self.usage_count,
            'average_rating': self.average_rating
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentBrick':
        """Création depuis un dictionnaire"""
        return cls(
            id=data['id'],
            content=data['content'],
            type=BrickType(data['type']),
            title=data['title'],
            subject=Subject(data['subject']),
            chapter=data['chapter'],
            difficulty=data['difficulty'],
            target_profiles=[TargetProfile(p) for p in data['target_profiles']],
            learning_steps=[LearningStep(s) for s in data['learning_steps']],
            tags=data['tags'],
            prerequisites=data['prerequisites'],
            duration_minutes=data['duration_minutes'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            author_id=data['author_id'],
            author_name=data['author_name'],
            usage_count=data.get('usage_count', 0),
            average_rating=data.get('average_rating', 0.0)
        )

@dataclass
class DocumentRequest:
    """Requête de génération de document personnalisé"""
    student_id: str
    student_profile: TargetProfile
    subject: Subject
    chapter: str
    document_type: str           # "fiche_revision", "exercices", "cours_complet"
    difficulty_range: tuple      # (min, max) ex: (3, 5)
    learning_step: LearningStep
    duration_target: int         # Durée cible en minutes
    specific_topics: List[str]   # Sujets spécifiques à couvrir
    exclude_topics: List[str]    # Sujets à éviter
    requested_by: str           # ID du demandeur (coach, système, élève)
    request_time: datetime

    # Préférences de format (avec valeurs par défaut)
    include_examples: bool = True
    include_exercises: bool = True
    include_corrections: bool = True
    include_methods: bool = True
    priority: int = 1           # 1=normal, 2=urgent, 3=critique

@dataclass
class GeneratedDocument:
    """Document généré par le système"""
    id: str
    request: DocumentRequest
    bricks_used: List[str]      # IDs des briques utilisées
    content_html: str           # Contenu final en HTML
    content_markdown: str       # Contenu final en Markdown

    # Métadonnées du document
    title: str
    estimated_duration: int     # Durée estimée en minutes
    difficulty_level: float     # Niveau de difficulté moyen

    # Informations de génération
    generated_at: datetime
    generation_time_ms: int     # Temps de génération en millisecondes
    template_used: str          # Template utilisé pour la génération

    # Statistiques et feedback
    views_count: int = 0
    completion_rate: float = 0.0
    student_rating: Optional[int] = None
    teacher_rating: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Conversion en dictionnaire"""
        return {
            'id': self.id,
            'request': {
                'student_id': self.request.student_id,
                'student_profile': self.request.student_profile.value,
                'subject': self.request.subject.value,
                'chapter': self.request.chapter,
                'document_type': self.request.document_type,
                'difficulty_range': self.request.difficulty_range,
                'learning_step': self.request.learning_step.value,
                'duration_target': self.request.duration_target,
                'specific_topics': self.request.specific_topics,
                'exclude_topics': self.request.exclude_topics,
                'include_examples': self.request.include_examples,
                'include_exercises': self.request.include_exercises,
                'include_corrections': self.request.include_corrections,
                'include_methods': self.request.include_methods,
                'requested_by': self.request.requested_by,
                'request_time': self.request.request_time.isoformat(),
                'priority': self.request.priority
            },
            'bricks_used': self.bricks_used,
            'content_html': self.content_html,
            'content_markdown': self.content_markdown,
            'title': self.title,
            'estimated_duration': self.estimated_duration,
            'difficulty_level': self.difficulty_level,
            'generated_at': self.generated_at.isoformat(),
            'generation_time_ms': self.generation_time_ms,
            'template_used': self.template_used,
            'views_count': self.views_count,
            'completion_rate': self.completion_rate,
            'student_rating': self.student_rating,
            'teacher_rating': self.teacher_rating
        }

