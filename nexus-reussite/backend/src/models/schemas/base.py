"""
Schémas de validation de base pour Nexus Réussite
Utilise Marshmallow pour la validation et sérialisation
"""

import json

from marshmallow import Schema, ValidationError, fields, pre_load, validate


class BaseSchema(Schema):
    """Schéma de base avec fonctionnalités communes"""

    # Champs de base pour tous les modèles
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        # Configuration par défaut
        ordered = True
        unknown = "EXCLUDE"  # Ignore les champs inconnus
        load_instance = False  # Ne pas créer d'instances automatiquement


class TimestampSchema(BaseSchema):
    """Schéma pour les modèles avec timestamps"""

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class SoftDeleteSchema(BaseSchema):
    """Schéma pour les modèles avec suppression logique"""

    is_deleted = fields.Boolean(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True, allow_none=True)


class AuditSchema(BaseSchema):
    """Schéma pour les modèles avec audit"""

    created_by = fields.Integer(allow_none=True)
    updated_by = fields.Integer(allow_none=True)


# Validateurs personnalisés
def validate_email(email: str) -> str:
    """Validation d'email améliorée"""
    if not email:
        raise ValidationError("L'email est requis")

    # Validation basique
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValidationError("Format d'email invalide")

    # Domaines interdits
    forbidden_domains = ["tempmail.org", "10minutemail.com"]
    domain = email.split("@")[1].lower()
    if domain in forbidden_domains:
        raise ValidationError("Domaine d'email non autorisé")

    return email.lower().strip()


def validate_phone(phone: str) -> str:
    """Validation de numéro de téléphone"""
    if not phone:
        return phone

    # Supprimer les espaces et caractères spéciaux
    cleaned = "".join(c for c in phone if c.isdigit() or c in "+- ()")

    # Validation basique
    digits_only = "".join(c for c in cleaned if c.isdigit())
    if len(digits_only) < 8 or len(digits_only) > 15:
        raise ValidationError("Numéro de téléphone invalide (8-15 chiffres)")

    return cleaned


def validate_password_strength(password: str) -> str:
    """Validation de la force du mot de passe"""
    if len(password) < 8:
        raise ValidationError("Le mot de passe doit contenir au moins 8 caractères")

    # Vérifications de complexité
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if score < 3:
        raise ValidationError(
            "Le mot de passe doit contenir au moins 3 des éléments suivants: "
            "majuscule, minuscule, chiffre, caractère spécial"
        )

    return password


def validate_json_list(value) -> list:
    """Validation d'une liste JSON"""
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        try:

            result = json.loads(value)
            if not isinstance(result, list):
                raise ValidationError("Doit être une liste JSON valide")
            return result
        except json.JSONDecodeError:
            raise ValidationError("JSON invalide")

    raise ValidationError("Doit être une liste ou une chaîne JSON valide")


def validate_json_dict(value) -> dict:
    """Validation d'un dictionnaire JSON"""
    if value is None:
        return {}

    if isinstance(value, dict):
        return value

    if isinstance(value, str):
        try:

            result = json.loads(value)
            if not isinstance(result, dict):
                raise ValidationError("Doit être un objet JSON valide")
            return result
        except json.JSONDecodeError:
            raise ValidationError("JSON invalide")

    raise ValidationError("Doit être un objet ou une chaîne JSON valide")


def validate_difficulty_level(level: int) -> int:
    """Validation du niveau de difficulté"""
    if not isinstance(level, int) or level < 1 or level > 5:
        raise ValidationError("Le niveau de difficulté doit être entre 1 et 5")
    return level


def validate_duration_minutes(duration: int) -> int:
    """Validation de durée en minutes"""
    if not isinstance(duration, int) or duration < 1 or duration > 600:
        raise ValidationError("La durée doit être entre 1 et 600 minutes")
    return duration


def validate_rating(rating: int) -> int:
    """Validation d'une note de 1 à 5"""
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        raise ValidationError("La note doit être entre 1 et 5")
    return rating


def validate_percentage(value: float) -> float:
    """Validation d'un pourcentage (0.0 à 1.0)"""
    if not isinstance(value, (int, float)) or value < 0.0 or value > 1.0:
        raise ValidationError("Le pourcentage doit être entre 0.0 et 1.0")
    return float(value)


class PaginationSchema(Schema):
    """Schéma pour les paramètres de pagination"""

    page = fields.Integer(
        load_default=1,
        validate=validate.Range(min=1, max=1000),
        error_messages={"invalid": "Le numéro de page doit être un entier positif"},
    )
    per_page = fields.Integer(
        load_default=20,
        validate=validate.Range(min=1, max=100),
        error_messages={
            "invalid": "Le nombre d'éléments par page doit être entre 1 et 100"
        },
    )
    sort_by = fields.String(load_default="created_at")
    sort_order = fields.String(
        load_default="desc",
        validate=validate.OneOf(["asc", "desc"]),
        error_messages={"invalid": 'L\'ordre de tri doit être "asc" ou "desc"'},
    )


class SearchSchema(Schema):
    """Schéma pour les paramètres de recherche"""

    query = fields.String(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={"required": "La requête de recherche est requise"},
    )
    filters = fields.Dict(load_default=dict)

    @pre_load
    def clean_query(self, data, **kwargs):
        """Nettoie la requête de recherche"""
        if "query" in data and data["query"]:
            data["query"] = data["query"].strip()
        return data
