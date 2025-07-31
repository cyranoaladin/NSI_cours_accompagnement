"""
Routes d'authentification pour Nexus Réussite
"""

import logging
import uuid
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    verify_jwt_in_request,
)

from database import db
from models.user import User
from services.jwt_blacklist import get_jwt_blacklist_service
from utils.rate_limit import auth_rate_limit
from utils.validators import validate_email, validate_password

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
@auth_rate_limit.limit("5 per minute")
def login():
    """
    Connexion utilisateur avec email et mot de passe
    """
    try:
        data = request.get_json()

        if not data:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Données manquantes",
                        "code": "MISSING_DATA",
                    }
                ),
                400,
            )

        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        remember_me = data.get("remember_me", False)

        # Validation des données
        if not email or not password:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Email et mot de passe requis",
                        "code": "MISSING_CREDENTIALS",
                    }
                ),
                400,
            )

        if not validate_email(email):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Format d'email invalide",
                        "code": "INVALID_EMAIL",
                    }
                ),
                400,
            )

        # Recherche de l'utilisateur
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            logger.warning("Tentative de connexion échouée pour {email}")
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Email ou mot de passe incorrect",
                        "code": "INVALID_CREDENTIALS",
                    }
                ),
                401,
            )

        # Vérification du statut de l'utilisateur
        if not user.is_active:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Compte désactivé",
                        "code": "ACCOUNT_DISABLED",
                    }
                ),
                403,
            )

        # Calcul de la durée du token
        if remember_me:
            access_expires = timedelta(days=30)
            refresh_expires = timedelta(days=90)
        else:
            access_expires = timedelta(hours=1)
            refresh_expires = timedelta(days=30)

        # Création des tokens avec identifiants uniques
        access_jti = str(uuid.uuid4())
        refresh_jti = str(uuid.uuid4())

        additional_claims = {
            "user_id": user.id,
            "role": user.role.value,
            "email": user.email,
            "jti": access_jti,
        }

        access_token = create_access_token(
            identity=user.id,
            expires_delta=access_expires,
            additional_claims=additional_claims,
        )

        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=refresh_expires,
            additional_claims={"jti": refresh_jti},
        )

        # Mise à jour du dernier login
        user.last_login = datetime.utcnow()

        # Création d'une session utilisateur
        from models.user import UserSession

        session = UserSession(
            user_id=user.id,
            session_token=access_jti,
            refresh_token=refresh_jti,
            expires_at=datetime.utcnow() + access_expires,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent", ""),
            device_type=_detect_device_type(request.headers.get("User-Agent", "")),
        )
        db.session.add(session)

        try:
            db.session.commit()
            logger.info("Connexion réussie pour {user.email}")
        except (RuntimeError, OSError, ValueError):
            db.session.rollback()
            logger.error("Erreur lors de la sauvegarde de session: {e}")
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Erreur interne",
                        "code": "DATABASE_ERROR",
                    }
                ),
                500,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "token": access_token,
                    "refresh_token": refresh_token,
                    "user": user.to_dict(),
                    "expires_in": int(access_expires.total_seconds()),
                    "token_type": "Bearer",
                }
            ),
            200,
        )

    except (ValueError, TypeError, RuntimeError):
        logger.error("Erreur lors de la connexion: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur interne du serveur",
                    "code": "INTERNAL_ERROR",
                }
            ),
            500,
        )


@auth_bp.route("/register", methods=["POST"])
@auth_rate_limit.limit("3 per minute")
def register():
    """
    Inscription d'un nouvel utilisateur
    """
    try:
        data = request.get_json()

        if not data:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Données manquantes",
                        "code": "MISSING_DATA",
                    }
                ),
                400,
            )

        # Extraction des données
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        role = data.get("role", "student")

        # Validation des données
        validation_errors = []

        if not email:
            validation_errors.append("Email requis")
        elif not validate_email(email):
            validation_errors.append("Format d'email invalide")

        if not password:
            validation_errors.append("Mot de passe requis")
        elif not validate_password(password):
            validation_errors.append(
                "Mot de passe trop faible (min 8 caractères, majuscule, minuscule, chiffre)"
            )

        if not first_name:
            validation_errors.append("Prénom requis")

        if not last_name:
            validation_errors.append("Nom requis")

        if validation_errors:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Données invalides",
                        "details": validation_errors,
                        "code": "VALIDATION_ERROR",
                    }
                ),
                400,
            )

        # Vérification de l'unicité de l'email
        if User.query.filter_by(email=email).first():
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Un compte existe déjà avec cet email",
                        "code": "EMAIL_EXISTS",
                    }
                ),
                409,
            )

        # Création de l'utilisateur
        from models.user import UserRole, create_user_with_profile

        try:
            user_role = UserRole(role)
        except ValueError:
            return (
                jsonify(
                    {"success": False, "error": "Rôle invalide", "code": "INVALID_ROLE"}
                ),
                400,
            )

        try:
            user, profile = create_user_with_profile(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=user_role,
                profile_data=data.get("profile_data", {}),
            )

            db.session.commit()

            logger.info("Nouvel utilisateur créé: {user.email} ({user_role.value})")

            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Compte créé avec succès",
                        "user": user.to_dict(),
                    }
                ),
                201,
            )

        except (RuntimeError, OSError, ValueError):
            db.session.rollback()
            logger.error("Erreur lors de la création de l'utilisateur: {e}")
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Erreur lors de la création du compte",
                        "code": "CREATION_ERROR",
                    }
                ),
                500,
            )

    except (ValueError, TypeError, RuntimeError):
        logger.error("Erreur lors de l'inscription: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur interne du serveur",
                    "code": "INTERNAL_ERROR",
                }
            ),
            500,
        )


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Rafraîchissement du token d'accès
    """
    try:
        current_user_id = get_jwt_identity()
        jwt_data = get_jwt()

        # Vérifier si le refresh token est blacklisté
        blacklist_service = get_jwt_blacklist_service()
        if blacklist_service.is_token_blacklisted(jwt_data.get("jti")):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Token révoqué",
                        "code": "TOKEN_REVOKED",
                    }
                ),
                401,
            )

        # Récupération de l'utilisateur
        user = User.query.get(current_user_id)
        if not user or not user.is_active:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Utilisateur non trouvé ou désactivé",
                        "code": "USER_NOT_FOUND",
                    }
                ),
                404,
            )

        # Création d'un nouveau token d'accès
        access_jti = str(uuid.uuid4())
        additional_claims = {
            "user_id": user.id,
            "role": user.role.value,
            "email": user.email,
            "jti": access_jti,
        }

        new_token = create_access_token(
            identity=user.id, additional_claims=additional_claims
        )

        # Mise à jour de la session
        from models.user import UserSession

        session = UserSession.query.filter_by(
            user_id=user.id, refresh_token=jwt_data.get("jti")
        ).first()

        if session:
            session.session_token = access_jti
            session.expires_at = datetime.utcnow() + timedelta(hours=1)
            session.last_activity = datetime.utcnow()
            db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "token": new_token,
                    "expires_in": 3600,
                    "token_type": "Bearer",
                }
            ),
            200,
        )

    except (ValueError, TypeError, RuntimeError):
        logger.error("Erreur lors du rafraîchissement: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur interne du serveur",
                    "code": "INTERNAL_ERROR",
                }
            ),
            500,
        )


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Déconnexion de l'utilisateur avec révocation du token
    """
    try:
        jwt_data = get_jwt()
        jti = jwt_data.get("jti")

        # Ajouter le token à la blacklist
        blacklist_service = get_jwt_blacklist_service()
        blacklist_service.add_token_to_blacklist(jti)

        # Désactiver la session
        from models.user import UserSession

        session = UserSession.query.filter_by(session_token=jti).first()
        if session:
            session.is_active = False
            db.session.commit()

        logger.info("Déconnexion réussie pour le token {jti}")

        return jsonify({"success": True, "message": "Déconnexion réussie"}), 200

    except (ValueError, TypeError, RuntimeError):
        logger.error("Erreur lors de la déconnexion: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur interne du serveur",
                    "code": "INTERNAL_ERROR",
                }
            ),
            500,
        )


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    Récupération des informations de l'utilisateur connecté
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Utilisateur non trouvé",
                        "code": "USER_NOT_FOUND",
                    }
                ),
                404,
            )

        return jsonify({"success": True, "user": user.to_dict()}), 200

    except (ValueError, TypeError, RuntimeError):
        logger.error("Erreur lors de la récupération de l'utilisateur: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur interne du serveur",
                    "code": "INTERNAL_ERROR",
                }
            ),
            500,
        )


@auth_bp.route("/validate-token", methods=["POST"])
def validate_token():
    """
    Validation d'un token JWT
    """
    try:
        verify_jwt_in_request()
        jwt_data = get_jwt()

        # Vérifier si le token est blacklisté
        blacklist_service = get_jwt_blacklist_service()
        if blacklist_service.is_token_blacklisted(jwt_data.get("jti")):
            return (
                jsonify(
                    {
                        "success": False,
                        "valid": False,
                        "error": "Token révoqué",
                        "code": "TOKEN_REVOKED",
                    }
                ),
                401,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "valid": True,
                    "user_id": get_jwt_identity(),
                    "expires_at": jwt_data.get("exp"),
                }
            ),
            200,
        )

    except (RuntimeError, OSError, ValueError):
        return (
            jsonify(
                {
                    "success": False,
                    "valid": False,
                    "error": "Token invalide",
                    "code": "INVALID_TOKEN",
                }
            ),
            401,
        )


def _detect_device_type(user_agent: str) -> str:
    """
    Détecte le type d'appareil basé sur le User-Agent

    Args:
        user_agent: Chaîne User-Agent

    Returns:
        str: Type d'appareil (web, mobile, tablet)
    """
    user_agent = user_agent.lower()

    if any(keyword in user_agent for keyword in ["mobile", "android", "iphone"]):
        return "mobile"
    elif any(keyword in user_agent for keyword in ["tablet", "ipad"]):
        return "tablet"
    else:
        return "web"


# Gestionnaire d'erreur JWT personnalisé
@auth_bp.errorhandler(422)
def handle_jwt_exceptions(error):
    """
    Gestionnaire pour les erreurs JWT
    """
    return (
        jsonify(
            {"success": False, "error": "Token invalide ou expiré", "code": "JWT_ERROR"}
        ),
        422,
    )
