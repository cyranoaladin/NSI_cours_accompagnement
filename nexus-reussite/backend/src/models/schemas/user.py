"""
Schémas de validation pour les modèles utilisateur
"""

from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validate
from marshmallow_enum import EnumField

from ..user import AcademicLevel, LearningStyle, UserRole, UserStatus
from .base import (
    BaseSchema,
    TimestampSchema,
    validate_email,
    validate_json_dict,
    validate_json_list,
    validate_password_strength,
    validate_phone,
)


class UserSchema(TimestampSchema):
    """Schéma de validation pour le modèle User"""

    # Champs requis
    email = fields.String(
        required=True,
        validate=[validate_email, validate.Length(max=120)],
        error_messages={"required": "L'email est requis"},
    )
    first_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=50),
        error_messages={"required": "Le prénom est requis"},
    )
    last_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=50),
        error_messages={"required": "Le nom est requis"},
    )
    role = EnumField(
        UserRole, required=True, error_messages={"required": "Le rôle est requis"}
    )

    # Champs optionnels
    phone = fields.String(allow_none=True, validate=validate_phone)
    avatar_url = fields.String(allow_none=True, validate=validate.Length(max=500))
    status = EnumField(UserStatus, load_default=UserStatus.ACTIVE)

    # Métadonnées
    last_login = fields.DateTime(dump_only=True, allow_none=True)
    email_verified = fields.Boolean(dump_only=True)
    preferences = fields.Dict(load_default=dict, validate=validate_json_dict)
    timezone = fields.String(
        load_default="Africa/Tunis", validate=validate.Length(max=50)
    )
    language = fields.String(load_default="fr", validate=validate.Length(max=5))

    # Champs sensibles (load only)
    password = fields.String(
        load_only=True,
        required=True,
        validate=validate_password_strength,
        error_messages={"required": "Le mot de passe est requis"},
    )

    @pre_load
    def clean_data(self, data, **kwargs):
        """Nettoie les données avant validation"""
        # Nettoyer l'email
        if "email" in data and data["email"]:
            data["email"] = data["email"].lower().strip()

        # Nettoyer les noms
        for field in ["first_name", "last_name"]:
            if field in data and data[field]:
                data[field] = data[field].strip().title()

        return data


class UserRegistrationSchema(Schema):
    """Schéma pour l'inscription d'un utilisateur"""

    email = fields.String(
        required=True, validate=[validate_email, validate.Length(max=120)]
    )
    password = fields.String(required=True, validate=validate_password_strength)
    password_confirm = fields.String(
        required=True,
        error_messages={"required": "La confirmation du mot de passe est requise"},
    )
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    role = EnumField(UserRole, required=True)
    phone = fields.String(allow_none=True, validate=validate_phone)

    @post_load
    def validate_passwords(self, data, **kwargs):
        """Valide que les mots de passe correspondent"""
        if data["password"] != data["password_confirm"]:
            raise ValidationError(
                "Les mots de passe ne correspondent pas", field_name="password_confirm"
            )

        # Supprimer la confirmation après validation
        data.pop("password_confirm", None)
        return data


class UserLoginSchema(Schema):
    """Schéma pour la connexion utilisateur"""

    email = fields.String(
        required=True,
        validate=validate_email,
        error_messages={"required": "L'email est requis"},
    )
    password = fields.String(
        required=True, error_messages={"required": "Le mot de passe est requis"}
    )
    remember_me = fields.Boolean(load_default=False)


class StudentProfileSchema(TimestampSchema):
    """Schéma pour le profil étudiant"""

    user_id = fields.Integer(required=True)
    grade_level = fields.String(
        required=True,
        validate=validate.OneOf(["seconde", "premiere", "terminale"]),
        error_messages={"required": "Le niveau scolaire est requis"},
    )
    school = fields.String(allow_none=True, validate=validate.Length(max=100))
    specialties = fields.List(
        fields.String(), load_default=list, validate=validate_json_list
    )
    learning_style = fields.String(
        allow_none=True,
        validate=validate.OneOf(["visual", "auditory", "kinesthetic", "mixed"]),
    )
    cognitive_profile = fields.Dict(load_default=dict, validate=validate_json_dict)
    performance_data = fields.Dict(load_default=dict, validate=validate_json_dict)
    goals = fields.List(fields.String(), load_default=list, validate=validate_json_list)
    interests = fields.List(
        fields.String(), load_default=list, validate=validate_json_list
    )
    motivation_level = fields.String(
        load_default="medium", validate=validate.OneOf(["low", "medium", "high"])
    )
    parent_ids = fields.List(
        fields.Integer(), load_default=list, validate=validate_json_list
    )


class ParentProfileSchema(TimestampSchema):
    """Schéma pour le profil parent"""

    user_id = fields.Integer(required=True)
    profession = fields.String(allow_none=True, validate=validate.Length(max=100))
    address = fields.String(allow_none=True)
    emergency_contact = fields.String(allow_none=True, validate=validate_phone)
    children_ids = fields.List(
        fields.Integer(), load_default=list, validate=validate_json_list
    )
    preferred_contact_method = fields.String(
        load_default="email", validate=validate.OneOf(["email", "phone", "sms"])
    )
    notification_preferences = fields.Dict(
        load_default=dict, validate=validate_json_dict
    )
    report_frequency = fields.String(
        load_default="weekly", validate=validate.OneOf(["daily", "weekly", "monthly"])
    )


class TeacherProfileSchema(TimestampSchema):
    """Schéma pour le profil enseignant"""

    user_id = fields.Integer(required=True)
    subjects = fields.List(
        fields.String(),
        required=True,
        validate=[validate_json_list, validate.Length(min=1)],
        error_messages={"required": "Au moins une matière est requise"},
    )
    qualifications = fields.List(
        fields.String(), load_default=list, validate=validate_json_list
    )
    experience_years = fields.Integer(
        allow_none=True, validate=validate.Range(min=0, max=50)
    )
    is_aefe_certified = fields.Boolean(load_default=False)
    is_nsi_diu = fields.Boolean(load_default=False)
    can_teach_online = fields.Boolean(load_default=True)
    can_teach_in_person = fields.Boolean(load_default=True)
    preferred_formats = fields.List(
        fields.String(), load_default=list, validate=validate_json_list
    )
    hourly_rate_online = fields.Float(
        allow_none=True, validate=validate.Range(min=0, max=1000)
    )
    hourly_rate_in_person = fields.Float(
        allow_none=True, validate=validate.Range(min=0, max=1000)
    )
    hourly_rate_group = fields.Float(
        allow_none=True, validate=validate.Range(min=0, max=1000)
    )
    default_availability = fields.Dict(load_default=dict, validate=validate_json_dict)
    max_hours_per_week = fields.Integer(
        load_default=30, validate=validate.Range(min=1, max=60)
    )
    rating = fields.Float(dump_only=True)
    total_reviews = fields.Integer(dump_only=True)
    total_hours_taught = fields.Integer(dump_only=True)
    bio = fields.String(allow_none=True)
    specialties_description = fields.String(allow_none=True)
    hire_date = fields.Date(allow_none=True)
    is_active_teacher = fields.Boolean(load_default=True)


class AdminProfileSchema(TimestampSchema):
    """Schéma pour le profil administrateur"""

    user_id = fields.Integer(required=True)
    permissions = fields.List(
        fields.String(), load_default=list, validate=validate_json_list
    )
    department = fields.String(allow_none=True, validate=validate.Length(max=50))
    is_super_admin = fields.Boolean(load_default=False)
    can_manage_users = fields.Boolean(load_default=False)
    can_manage_content = fields.Boolean(load_default=False)
    can_view_reports = fields.Boolean(load_default=True)
    can_manage_billing = fields.Boolean(load_default=False)


class UserSessionSchema(TimestampSchema):
    """Schéma pour les sessions utilisateur"""

    user_id = fields.Integer(required=True)
    session_token = fields.String(required=True, load_only=True)
    refresh_token = fields.String(allow_none=True, load_only=True)
    expires_at = fields.DateTime(required=True)
    ip_address = fields.String(allow_none=True, validate=validate.Length(max=45))
    user_agent = fields.String(allow_none=True, validate=validate.Length(max=500))
    device_type = fields.String(
        allow_none=True, validate=validate.OneOf(["web", "mobile", "tablet"])
    )
    location = fields.String(allow_none=True, validate=validate.Length(max=100))
    is_active = fields.Boolean(load_default=True)
    last_activity = fields.DateTime(load_default=fields.DateTime())


class ParentChildRelationSchema(TimestampSchema):
    """Schéma pour les relations parent-enfant"""

    parent_user_id = fields.Integer(required=True)
    child_user_id = fields.Integer(required=True)
    relation_type = fields.String(
        load_default="parent", validate=validate.OneOf(["parent", "guardian", "tutor"])
    )
    is_primary_contact = fields.Boolean(load_default=False)
    can_view_grades = fields.Boolean(load_default=True)
    can_book_sessions = fields.Boolean(load_default=True)
    can_receive_reports = fields.Boolean(load_default=True)
    confirmed_at = fields.DateTime(allow_none=True)


class PasswordResetSchema(Schema):
    """Schéma pour la réinitialisation de mot de passe"""

    email = fields.String(
        required=True,
        validate=validate_email,
        error_messages={"required": "L'email est requis"},
    )


class PasswordChangeSchema(Schema):
    """Schéma pour le changement de mot de passe"""

    current_password = fields.String(
        required=True, error_messages={"required": "Le mot de passe actuel est requis"}
    )
    new_password = fields.String(
        required=True,
        validate=validate_password_strength,
        error_messages={"required": "Le nouveau mot de passe est requis"},
    )
    new_password_confirm = fields.String(
        required=True,
        error_messages={
            "required": "La confirmation du nouveau mot de passe est requise"
        },
    )

    @post_load
    def validate_passwords(self, data, **kwargs):
        """Valide que les nouveaux mots de passe correspondent"""
        if data["new_password"] != data["new_password_confirm"]:
            raise ValidationError(
                "Les nouveaux mots de passe ne correspondent pas",
                field_name="new_password_confirm",
            )

        data.pop("new_password_confirm", None)
        return data


class UserPreferencesSchema(Schema):
    """Schéma pour les préférences utilisateur"""

    theme = fields.String(
        load_default="light", validate=validate.OneOf(["light", "dark", "auto"])
    )
    language = fields.String(
        load_default="fr", validate=validate.OneOf(["fr", "en", "ar"])
    )
    timezone = fields.String(
        load_default="Africa/Tunis", validate=validate.Length(max=50)
    )
    notifications = fields.Dict(load_default=dict)
    dashboard_layout = fields.Dict(load_default=dict)
    accessibility = fields.Dict(load_default=dict)
