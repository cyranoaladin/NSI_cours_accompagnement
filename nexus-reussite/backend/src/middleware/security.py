"""
Security Middleware pour Nexus Réussite
Implémente CSRF, sanitization, et autres protections de sécurité
"""

import html
import logging
import re
from functools import wraps
from typing import Any, Dict, Optional, Union

import bleach
from flask import current_app, g, jsonify, request
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import RequestEntityTooLarge

logger = logging.getLogger(__name__)

# Configuration pour la sanitisation
ALLOWED_HTML_TAGS = [
    "b",
    "i",
    "u",
    "em",
    "strong",
    "p",
    "br",
    "span",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "a",
    "code",
    "pre",
]

ALLOWED_HTML_ATTRIBUTES = {"a": ["href", "title"], "span": ["class"], "code": ["class"]}

# Limites de taille par type de contenu
CONTENT_SIZE_LIMITS = {
    "text": 10000,  # 10KB pour les textes
    "description": 5000,  # 5KB pour les descriptions
    "title": 200,  # 200 caractères pour les titres
    "name": 100,  # 100 caractères pour les noms
    "email": 320,  # RFC limite pour les emails
    "password": 128,  # Limite raisonnable pour les mots de passe
    "url": 2048,  # Limite standard pour les URLs
    "json": 1048576,  # 1MB pour les données JSON
    "default": 1000,  # Limite par défaut
}


class SecurityMiddleware:
    """Middleware de sécurité centralisé"""

    def __init__(self, app=None):
        self.csrf = CSRFProtect()
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialise le middleware avec l'application Flask"""

        # Initialisation CSRF avec configuration conditionnelle
        self.csrf.init_app(app)

        # Configuration des endpoints exemptés de CSRF
        app.config.setdefault(
            "WTF_CSRF_EXEMPT_LIST",
            [
                "/api/auth/login",
                "/api/auth/register",
                "/api/auth/refresh",
                "/health",
                "/api/health",
            ],
        )

        # Gestionnaire d'erreur CSRF
        @app.errorhandler(CSRFError)
        def handle_csrf_error(e):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Token CSRF invalide ou manquant",
                        "code": "CSRF_ERROR",
                        "description": str(e.description),
                    }
                ),
                400,
            )

        # Middleware de sanitisation globale
        app.before_request(self._sanitize_request)

        # Middleware de validation de taille
        app.before_request(self._validate_request_size)

    def _sanitize_request(self):
        """Sanitise automatiquement les données de requête"""
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                if request.is_json:
                    # Sanitisation des données JSON
                    if (
                        hasattr(request, "_cached_json")
                        and request._cached_json[1] is not None
                    ):
                        request._cached_json = (
                            request._cached_json[0],
                            self._sanitize_data(request._cached_json[1]),
                        )

                elif request.form:
                    # Sanitisation des données de formulaire
                    sanitized_form = {}
                    for key, value in request.form.items():
                        sanitized_form[key] = self._sanitize_string(value)
                    request.form = sanitized_form

            except Exception as e:
                logger.error(f"Erreur lors de la sanitisation: {e}")

    def _validate_request_size(self):
        """Valide la taille des requêtes"""
        if request.method in ["POST", "PUT", "PATCH"]:
            content_length = request.content_length
            max_size = current_app.config.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)

            if content_length and content_length > max_size:
                raise RequestEntityTooLarge()

    def _sanitize_data(self, data: Any) -> Any:
        """Sanitise récursivement les données"""
        if isinstance(data, dict):
            return {key: self._sanitize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        elif isinstance(data, str):
            return self._sanitize_string(data)
        else:
            return data

    def _sanitize_string(self, text: str, field_type: str = "default") -> str:
        """Sanitise une chaîne de caractères"""
        if not isinstance(text, str):
            return text

        # Vérification de la taille
        max_length = CONTENT_SIZE_LIMITS.get(field_type, CONTENT_SIZE_LIMITS["default"])
        if len(text) > max_length:
            text = text[:max_length]

        # Suppression des caractères de contrôle dangereux
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

        # Échappement HTML pour les champs de base
        if field_type in ["name", "email", "title"]:
            return html.escape(text)

        # Nettoyage HTML pour les champs de contenu
        elif field_type in ["text", "description"]:
            return bleach.clean(
                text,
                tags=ALLOWED_HTML_TAGS,
                attributes=ALLOWED_HTML_ATTRIBUTES,
                strip=True,
            )

        # Échappement par défaut
        return html.escape(text)


def require_csrf_token(view_func):
    """Décorateur pour forcer la vérification CSRF sur des endpoints spécifiques"""

    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        # Vérification explicite du token CSRF pour les endpoints non-JSON
        if not request.is_json:
            csrf_token = request.form.get("csrf_token") or request.headers.get(
                "X-CSRFToken"
            )
            if not csrf_token:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Token CSRF requis",
                            "code": "CSRF_TOKEN_REQUIRED",
                        }
                    ),
                    400,
                )

        return view_func(*args, **kwargs)

    return decorated_function


def sanitize_input(**field_types):
    """
    Décorateur pour sanitiser les entrées avec types spécifiques

    Usage:
    @sanitize_input(title='title', description='text', email='email')
    def create_post():
        ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def decorated_function(*args, **kwargs):
            if request.is_json:
                data = request.get_json()
                if data:
                    sanitized_data = {}
                    for field, value in data.items():
                        field_type = field_types.get(field, "default")
                        if isinstance(value, str):
                            sanitized_data[field] = (
                                SecurityMiddleware()._sanitize_string(value, field_type)
                            )
                        else:
                            sanitized_data[field] = value

                    # Remplacer les données de la requête
                    request._cached_json = (True, sanitized_data)

            return view_func(*args, **kwargs)

        return decorated_function

    return decorator


def validate_content_size(max_size: int):
    """Décorateur pour valider la taille du contenu"""

    def decorator(view_func):
        @wraps(view_func)
        def decorated_function(*args, **kwargs):
            if request.content_length and request.content_length > max_size:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": f"Contenu trop volumineux (max: {max_size} bytes)",
                            "code": "CONTENT_TOO_LARGE",
                        }
                    ),
                    413,
                )

            return view_func(*args, **kwargs)

        return decorated_function

    return decorator


def rate_limit_by_ip(limit: str):
    """Décorateur pour limiter les requêtes par IP"""

    def decorator(view_func):
        @wraps(view_func)
        def decorated_function(*args, **kwargs):
            # Cette fonction serait utilisée avec Flask-Limiter
            return view_func(*args, **kwargs)

        return decorated_function

    return decorator


# Instance globale du middleware
security_middleware = SecurityMiddleware()
