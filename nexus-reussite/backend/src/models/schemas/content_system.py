"""
Schémas de validation pour le système de contenu
"""

from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validate
from marshmallow_enum import EnumField

from ..content_system import BrickType, LearningStep, Subject, TargetProfile
from .base import (
    SoftDeleteSchema,
    TimestampSchema,
    validate_difficulty_level,
    validate_duration_minutes,
    validate_json_dict,
    validate_rating,
)


class ContentBrickSchema(SoftDeleteSchema):
    """Schéma pour les briques de contenu"""

    # Contenu principal
    content = fields.String(
        required=True,
        validate=validate.Length(min=10, max=50000),
        error_messages={"required": "Le contenu est requis"},
    )
    brick_type = EnumField(
        BrickType,
        required=True,
        error_messages={"required": "Le type de brique est requis"},
    )
    title = fields.String(
        required=True,
        validate=validate.Length(min=3, max=200),
        error_messages={"required": "Le titre est requis"},
    )

    # Métadonnées pour la personnalisation
    subject = EnumField(
        Subject, required=True, error_messages={"required": "La matière est requise"}
    )
    chapter = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "Le chapitre est requis"},
    )
    difficulty = fields.Integer(
        required=True,
        validate=validate_difficulty_level,
        error_messages={"required": "Le niveau de difficulté est requis"},
    )
    target_profiles = fields.List(
        EnumField(TargetProfile),
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Au moins un profil cible est requis"},
    )
    learning_steps = fields.List(
        EnumField(LearningStep),
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Au moins une étape d'apprentissage est requise"},
    )

    # Métadonnées additionnelles
    tags = fields.List(
        fields.String(validate=validate.Length(min=2, max=50)), load_default=list
    )
    prerequisites = fields.List(fields.Integer(), load_default=list)
    duration_minutes = fields.Integer(
        required=True,
        validate=validate_duration_minutes,
        error_messages={"required": "La durée estimée est requise"},
    )

    # Informations de création
    author_id = fields.Integer(required=True)
    author_name = fields.String(required=True, validate=validate.Length(min=2, max=100))

    # Statistiques (dump only)
    usage_count = fields.Integer(dump_only=True)
    average_rating = fields.Float(dump_only=True)
    total_ratings = fields.Integer(dump_only=True)

    @pre_load
    def clean_data(self, data, **kwargs):
        """Nettoie les données avant validation"""
        if "title" in data and data["title"]:
            data["title"] = data["title"].strip()

        if "chapter" in data and data["chapter"]:
            data["chapter"] = data["chapter"].strip()

        # Nettoyer les tags
        if "tags" in data and isinstance(data["tags"], list):
            data["tags"] = [
                tag.strip().lower() for tag in data["tags"] if tag and tag.strip()
            ]

        return data


class DocumentRequestSchema(TimestampSchema):
    """Schéma pour les demandes de génération de document"""

    student_id = fields.Integer(required=True)
    student_profile = EnumField(
        TargetProfile,
        required=True,
        error_messages={"required": "Le profil étudiant est requis"},
    )
    subject = EnumField(
        Subject, required=True, error_messages={"required": "La matière est requise"}
    )
    chapter = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "Le chapitre est requis"},
    )
    document_type = fields.String(
        required=True,
        validate=validate.OneOf(
            ["fiche_revision", "exercices", "cours_complet", "evaluation", "td", "tp"]
        ),
        error_messages={"required": "Le type de document est requis"},
    )

    # Difficulté (min et max)
    difficulty_min = fields.Integer(required=True, validate=validate_difficulty_level)
    difficulty_max = fields.Integer(required=True, validate=validate_difficulty_level)

    learning_step = EnumField(
        LearningStep,
        required=True,
        error_messages={"required": "L'étape d'apprentissage est requise"},
    )
    duration_target = fields.Integer(
        required=True,
        validate=validate_duration_minutes,
        error_messages={"required": "La durée cible est requise"},
    )

    # Sujets spécifiques
    specific_topics = fields.List(
        fields.String(validate=validate.Length(min=2, max=100)), load_default=list
    )
    exclude_topics = fields.List(
        fields.String(validate=validate.Length(min=2, max=100)), load_default=list
    )

    requested_by = fields.Integer(required=True)

    # Préférences de format
    include_examples = fields.Boolean(load_default=True)
    include_exercises = fields.Boolean(load_default=True)
    include_corrections = fields.Boolean(load_default=True)
    include_methods = fields.Boolean(load_default=True)

    priority = fields.Integer(load_default=1, validate=validate.Range(min=1, max=3))

    # Statut (dump only)
    status = fields.String(dump_only=True)
    processed_at = fields.DateTime(dump_only=True, allow_none=True)

    @post_load
    def validate_difficulty_range(self, data, **kwargs):
        """Valide que difficulty_max >= difficulty_min"""
        if data["difficulty_max"] < data["difficulty_min"]:
            raise ValidationError(
                "La difficulté maximale doit être supérieure ou égale à la difficulté minimale",
                field_name="difficulty_max",
            )
        return data


class GeneratedDocumentSchema(SoftDeleteSchema):
    """Schéma pour les documents générés"""

    request_id = fields.Integer(required=True)

    # Contenu généré (dump only pour sécurité)
    content_html = fields.String(dump_only=True)
    content_markdown = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=3, max=200))

    # Métadonnées du document
    estimated_duration = fields.Integer(
        required=True, validate=validate_duration_minutes
    )
    difficulty_level = fields.Float(
        required=True, validate=validate.Range(min=1.0, max=5.0)
    )

    # Informations de génération (dump only)
    generation_time_ms = fields.Integer(dump_only=True)
    template_used = fields.String(dump_only=True)

    # Statistiques et feedback
    views_count = fields.Integer(dump_only=True)
    completion_rate = fields.Float(
        allow_none=True, validate=validate.Range(min=0.0, max=1.0)
    )
    student_rating = fields.Integer(allow_none=True, validate=validate_rating)
    teacher_rating = fields.Integer(allow_none=True, validate=validate_rating)


class DocumentBrickSchema(TimestampSchema):
    """Schéma pour les liaisons document-brique"""

    document_id = fields.Integer(required=True)
    brick_id = fields.Integer(required=True)
    order_index = fields.Integer(
        required=True, validate=validate.Range(min=0, max=1000)
    )
    context_notes = fields.String(allow_none=True, validate=validate.Length(max=1000))


class ContentBrickRatingSchema(TimestampSchema):
    """Schéma pour les évaluations de briques"""

    brick_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    rating = fields.Integer(
        required=True,
        validate=validate_rating,
        error_messages={"required": "La note est requise"},
    )
    comment = fields.String(allow_none=True, validate=validate.Length(max=1000))
    evaluator_type = fields.String(
        required=True,
        validate=validate.OneOf(["student", "teacher", "admin"]),
        error_messages={"required": "Le type d'évaluateur est requis"},
    )


class DocumentInteractionSchema(TimestampSchema):
    """Schéma pour les interactions avec les documents"""

    document_id = fields.Integer(required=True)
    student_id = fields.Integer(required=True)
    interaction_type = fields.String(
        required=True,
        validate=validate.OneOf(["view", "download", "print", "complete", "bookmark"]),
        error_messages={"required": "Le type d'interaction est requis"},
    )
    duration_seconds = fields.Integer(
        allow_none=True, validate=validate.Range(min=0, max=86400)  # Max 24h
    )
    progress_percentage = fields.Float(
        load_default=0.0, validate=validate.Range(min=0.0, max=1.0)
    )
    device_type = fields.String(
        allow_none=True, validate=validate.OneOf(["web", "mobile", "tablet"])
    )
    ip_address = fields.String(allow_none=True, validate=validate.Length(max=45))


class ContentTemplateSchema(SoftDeleteSchema):
    """Schéma pour les templates de contenu"""

    name = fields.String(
        required=True,
        validate=validate.Length(min=3, max=100),
        error_messages={"required": "Le nom du template est requis"},
    )
    description = fields.String(allow_none=True, validate=validate.Length(max=1000))
    document_type = fields.String(
        required=True,
        validate=validate.OneOf(
            ["fiche_revision", "exercices", "cours_complet", "evaluation", "td", "tp"]
        ),
        error_messages={"required": "Le type de document supporté est requis"},
    )
    template_content = fields.String(
        required=True,
        validate=validate.Length(min=10, max=100000),
        error_messages={"required": "Le contenu du template est requis"},
    )
    css_styles = fields.String(allow_none=True, validate=validate.Length(max=50000))
    default_config = fields.Dict(load_default=dict, validate=validate_json_dict)
    author_id = fields.Integer(required=True)
    usage_count = fields.Integer(dump_only=True)
    is_active = fields.Boolean(load_default=True)

    @pre_load
    def clean_data(self, data, **kwargs):
        """Nettoie les données avant validation"""
        if "name" in data and data["name"]:
            data["name"] = data["name"].strip()

        return data


class ContentSearchSchema(Schema):
    """Schéma pour la recherche de contenu"""

    query = fields.String(allow_none=True, validate=validate.Length(min=1, max=200))
    subject = EnumField(Subject, allow_none=True)
    brick_type = EnumField(BrickType, allow_none=True)
    difficulty_min = fields.Integer(allow_none=True, validate=validate_difficulty_level)
    difficulty_max = fields.Integer(allow_none=True, validate=validate_difficulty_level)
    target_profile = EnumField(TargetProfile, allow_none=True)
    learning_step = EnumField(LearningStep, allow_none=True)
    tags = fields.List(fields.String(), load_default=list)
    author_id = fields.Integer(allow_none=True)

    # Filtres de qualité
    min_rating = fields.Float(
        allow_none=True, validate=validate.Range(min=1.0, max=5.0)
    )
    min_usage_count = fields.Integer(allow_none=True, validate=validate.Range(min=0))

    # Tri
    sort_by = fields.String(
        load_default="created_at",
        validate=validate.OneOf(
            [
                "created_at",
                "updated_at",
                "title",
                "difficulty",
                "average_rating",
                "usage_count",
            ]
        ),
    )
    sort_order = fields.String(
        load_default="desc", validate=validate.OneOf(["asc", "desc"])
    )

    @post_load
    def validate_difficulty_range(self, data, **kwargs):
        """Valide la cohérence de la plage de difficulté"""
        if (
            data.get("difficulty_min") is not None
            and data.get("difficulty_max") is not None
            and data["difficulty_max"] < data["difficulty_min"]
        ):
            raise ValidationError(
                "La difficulté maximale doit être supérieure ou égale à la difficulté minimale"
            )
        return data


class BulkContentOperationSchema(Schema):
    """Schéma pour les opérations en lot sur le contenu"""

    operation = fields.String(
        required=True,
        validate=validate.OneOf(
            ["delete", "update_tags", "change_author", "duplicate"]
        ),
        error_messages={"required": "L'opération est requise"},
    )
    brick_ids = fields.List(
        fields.Integer(),
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Au moins un ID de brique est requis"},
    )
    parameters = fields.Dict(load_default=dict)

    @post_load
    def validate_operation_parameters(self, data, **kwargs):
        """Valide les paramètres selon l'opération"""
        operation = data["operation"]
        params = data["parameters"]

        if operation == "update_tags" and "tags" not in params:
            raise ValidationError(
                "Les tags sont requis pour l'opération update_tags",
                field_name="parameters",
            )

        if operation == "change_author" and "new_author_id" not in params:
            raise ValidationError(
                "Le nouvel auteur est requis pour l'opération change_author",
                field_name="parameters",
            )

        return data
