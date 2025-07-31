"""
Schémas de validation pour Nexus Réussite
Centralise tous les schémas Marshmallow
"""

# Schémas de base
from .base import (
    AuditSchema,
    BaseSchema,
    PaginationSchema,
    SearchSchema,
    SoftDeleteSchema,
    TimestampSchema,
    validate_difficulty_level,
    validate_duration_minutes,
    validate_email,
    validate_json_dict,
    validate_json_list,
    validate_password_strength,
    validate_percentage,
    validate_phone,
    validate_rating,
)

# Schémas système de contenu
from .content_system import (
    BulkContentOperationSchema,
    ContentBrickRatingSchema,
    ContentBrickSchema,
    ContentSearchSchema,
    ContentTemplateSchema,
    DocumentBrickSchema,
    DocumentInteractionSchema,
    DocumentRequestSchema,
    GeneratedDocumentSchema,
)

# Schémas utilisateur
from .user import (
    AdminProfileSchema,
    ParentChildRelationSchema,
    ParentProfileSchema,
    PasswordChangeSchema,
    PasswordResetSchema,
    StudentProfileSchema,
    TeacherProfileSchema,
    UserLoginSchema,
    UserPreferencesSchema,
    UserRegistrationSchema,
    UserSchema,
    UserSessionSchema,
)

# Alias pour compatibilité
ContentSchema = ContentBrickSchema

# Exports principaux
__all__ = [
    # Classes de base
    "BaseSchema",
    "TimestampSchema",
    "SoftDeleteSchema",
    "AuditSchema",
    "PaginationSchema",
    "SearchSchema",
    # Validateurs
    "validate_email",
    "validate_phone",
    "validate_password_strength",
    "validate_json_list",
    "validate_json_dict",
    "validate_difficulty_level",
    "validate_duration_minutes",
    "validate_rating",
    "validate_percentage",
    # Schémas utilisateur
    "UserSchema",
    "UserRegistrationSchema",
    "UserLoginSchema",
    "StudentProfileSchema",
    "ParentProfileSchema",
    "TeacherProfileSchema",
    "AdminProfileSchema",
    "UserSessionSchema",
    "ParentChildRelationSchema",
    "PasswordResetSchema",
    "PasswordChangeSchema",
    "UserPreferencesSchema",
    # Schémas système de contenu
    "ContentSchema",
    "ContentBrickSchema",
    "DocumentRequestSchema",
    "GeneratedDocumentSchema",
    "DocumentBrickSchema",
    "ContentBrickRatingSchema",
    "DocumentInteractionSchema",
    "ContentTemplateSchema",
    "ContentSearchSchema",
    "BulkContentOperationSchema",
]
