#!/usr/bin/env python3
"""
Configuration de production pour Nexus Réussite
Remplace la configuration de développement par des paramètres sécurisés
"""

import os
import secrets
from typing import Dict, Any


class ProductionConfig:
    """Configuration sécurisée pour la production"""

    # ===== FLASK CONFIGURATION =====
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY must be set in production")

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY must be set in production")

    # ===== DATABASE CONFIGURATION =====
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL or 'sqlite' in DATABASE_URL.lower():
        raise RuntimeError("PostgreSQL DATABASE_URL required in production")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', 20)),
        'pool_timeout': int(os.environ.get('DB_POOL_TIMEOUT', 60)),
        'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', 3600)),
        'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', 40)),
        'pool_pre_ping': True,
        'echo': False  # Désactivé en production
    }

    # ===== REDIS CONFIGURATION =====
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TTL_SHORT = int(os.environ.get('CACHE_TTL_SHORT', 300))
    CACHE_TTL_MEDIUM = int(os.environ.get('CACHE_TTL_MEDIUM', 3600))
    CACHE_TTL_LONG = int(os.environ.get('CACHE_TTL_LONG', 86400))

    # ===== SECURITY CONFIGURATION =====
    # CORS - Domaines autorisés uniquement
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    if not CORS_ORIGINS or CORS_ORIGINS == ['']:
        raise RuntimeError("CORS_ORIGINS must be defined in production")

    # Headers de sécurité
    SECURITY_ENFORCE_HTTPS = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CSP (Content Security Policy)
    SECURITY_CSP = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' https://cdn.tailwindcss.com",
        'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com",
        'font-src': "'self' https://fonts.gstatic.com",
        'img-src': "'self' data: https:",
        'connect-src': "'self' https://api.openai.com wss:",
        'frame-ancestors': "'none'",
        'base-uri': "'self'",
        'form-action': "'self'"
    }

    # ===== JWT CONFIGURATION =====
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1h
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000))  # 30j
    JWT_ALGORITHM = 'HS256'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # ===== EMAIL CONFIGURATION =====
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # ===== AI CONFIGURATION =====
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4')
    OPENAI_MAX_TOKENS = int(os.environ.get('OPENAI_MAX_TOKENS', 4000))
    OPENAI_TEMPERATURE = float(os.environ.get('OPENAI_TEMPERATURE', 0.7))

    # ===== MONITORING =====
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', 0.1))
    SENTRY_PROFILES_SAMPLE_RATE = float(os.environ.get('SENTRY_PROFILES_SAMPLE_RATE', 0.1))

    # ===== PERFORMANCE =====
    COMPRESS_MIMETYPES = [
        'text/html', 'text/css', 'text/xml', 'application/json',
        'application/javascript', 'text/javascript', 'application/xml'
    ]
    COMPRESS_LEVEL = int(os.environ.get('COMPRESS_LEVEL', 6))
    COMPRESS_MIN_SIZE = int(os.environ.get('COMPRESS_MIN_SIZE', 500))

    # ===== LOGGING =====
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING').upper()
    LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

    # ===== RATE LIMITING =====
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "200 per day,50 per hour,1 per second"
    RATELIMIT_HEADERS_ENABLED = True

    # ===== UPLOAD CONFIGURATION =====
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = '/var/lib/nexus-reussite/uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'gif'}

    # ===== PRODUCTION SPECIFIC =====
    DEBUG = False
    TESTING = False
    ENV = 'production'

    # Désactiver les fonctionnalités de développement
    ENABLE_DEMO_DATA = False
    ENABLE_SQL_PROFILING = False
    SQLALCHEMY_ECHO = False

    def init_app(self, app):
        """Initialise l'application avec cette configuration"""
        app.config.from_object(self)

        # Validation des variables critiques
        self._validate_critical_config()

        return app

    def _validate_critical_config(self):
        """Valide que toutes les configurations critiques sont définies"""
        critical_vars = [
            'SECRET_KEY', 'JWT_SECRET_KEY', 'DATABASE_URL'
        ]

        missing = []
        for var in critical_vars:
            if not getattr(self, var, None):
                missing.append(var)

        if missing:
            raise RuntimeError(f"Critical configuration missing: {', '.join(missing)}")

        # Vérifier la force des secrets
        if len(self.SECRET_KEY) < 32:
            raise RuntimeError("SECRET_KEY must be at least 32 characters")

        if len(self.JWT_SECRET_KEY) < 32:
            raise RuntimeError("JWT_SECRET_KEY must be at least 32 characters")


class StagingConfig(ProductionConfig):
    """Configuration pour l'environnement de staging"""

    DEBUG = False
    TESTING = False
    ENV = 'staging'

    # Logging plus verbeux en staging
    LOG_LEVEL = 'INFO'

    # Rate limiting plus souple
    RATELIMIT_DEFAULT = "1000 per day,200 per hour,5 per second"

    # Headers CSP moins stricts pour les tests
    SECURITY_CSP = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'connect-src': "'self' https: wss: ws:",
    }


def get_config(config_name: str = None) -> ProductionConfig:
    """
    Retourne la configuration appropriée

    Args:
        config_name: 'production', 'staging', ou None (auto-detect)
    """

    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'production')

    config_map = {
        'production': ProductionConfig,
        'staging': StagingConfig,
    }

    config_class = config_map.get(config_name, ProductionConfig)
    return config_class()


def validate_production_environment() -> Dict[str, Any]:
    """
    Valide que l'environnement de production est correctement configuré
    """

    validation_report = {
        'status': 'healthy',
        'issues': [],
        'warnings': [],
        'environment': os.environ.get('FLASK_ENV', 'unknown')
    }

    # Variables obligatoires
    required_vars = [
        'SECRET_KEY', 'JWT_SECRET_KEY', 'DATABASE_URL',
        'CORS_ORIGINS', 'MAIL_SERVER'
    ]

    for var in required_vars:
        if not os.environ.get(var):
            validation_report['issues'].append(f"Missing required variable: {var}")
            validation_report['status'] = 'critical'

    # Variables recommandées
    recommended_vars = [
        'OPENAI_API_KEY', 'SENTRY_DSN', 'REDIS_URL'
    ]

    for var in recommended_vars:
        if not os.environ.get(var):
            validation_report['warnings'].append(f"Recommended variable not set: {var}")

    # Vérifications de sécurité
    secret_key = os.environ.get('SECRET_KEY', '')
    if secret_key and len(secret_key) < 32:
        validation_report['issues'].append("SECRET_KEY too short (minimum 32 characters)")
        validation_report['status'] = 'critical'

    # Vérification base de données
    db_url = os.environ.get('DATABASE_URL', '')
    if 'sqlite' in db_url.lower():
        validation_report['issues'].append("SQLite database detected - use PostgreSQL in production")
        validation_report['status'] = 'critical'

    return validation_report


# Configuration par défaut pour la production
config = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'default': ProductionConfig
}
