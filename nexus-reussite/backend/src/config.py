"""
Configuration centralisée pour Nexus Réussite Backend
Version améliorée et production-ready
"""

import os
from typing import Any, Dict, List

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class Config:
    """Configuration de base"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "nexus-reussite-secret-key-2024"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///nexus_reussite.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # CORS Configuration
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")

    # Security Headers - Enhanced CSP (Talisman format)
    SECURITY_CSP = {
        "default-src": "'self'",
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        "img-src": ["'self'", "data:", "https:", "blob:"],
        "font-src": ["'self'", "https://fonts.gstatic.com"],
        "connect-src": ["'self'", "https://api.openai.com", "wss:"],
        "media-src": ["'self'", "blob:"],
        "object-src": "'none'",
        "base-uri": "'self'",
        "form-action": "'self'",
        "frame-ancestors": "'none'",
        "upgrade-insecure-requests": True,
    }

    # CORS Configuration avancée
    CORS_TRUSTED_DOMAINS = (
        os.environ.get("CORS_TRUSTED_DOMAINS", "").split(",")
        if os.environ.get("CORS_TRUSTED_DOMAINS")
        else []
    )

    # Configuration CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 heure
    WTF_CSRF_SECRET_KEY = os.environ.get("CSRF_SECRET_KEY") or SECRET_KEY

    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4")

    # Email Configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Redis Configuration
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    # Rate Limiting
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "200 per day;50 per hour;1 per second"

    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    # Performance & Observability
    ENABLE_SQL_PROFILING = (
        os.environ.get("ENABLE_SQL_PROFILING", "False").lower() == "true"
    )
    ENABLE_METRICS = os.environ.get("ENABLE_METRICS", "True").lower() == "true"
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300))
    CACHE_KEY_PREFIX = os.environ.get("CACHE_KEY_PREFIX", "nexus_")
    CACHE_REDIS_DB = int(os.environ.get("CACHE_REDIS_DB", 0))

    # SQLAlchemy Performance
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", "False").lower() == "true"
    SQLALCHEMY_ECHO_POOL = (
        os.environ.get("SQLALCHEMY_ECHO_POOL", "False").lower() == "true"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": int(os.environ.get("DB_POOL_SIZE", 10)),
        "pool_timeout": int(os.environ.get("DB_POOL_TIMEOUT", 30)),
        "pool_recycle": int(os.environ.get("DB_POOL_RECYCLE", 1800)),
        "max_overflow": int(os.environ.get("DB_MAX_OVERFLOW", 20)),
        "pool_pre_ping": True,
    }

    # Sentry Configuration
    SENTRY_DSN = os.environ.get("SENTRY_DSN")
    SENTRY_TRACES_SAMPLE_RATE = float(
        os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.1")
    )
    SENTRY_PROFILES_SAMPLE_RATE = float(
        os.environ.get("SENTRY_PROFILES_SAMPLE_RATE", "0.1")
    )

    # Compression Settings
    COMPRESS_MIMETYPES = [
        "text/html",
        "text/css",
        "text/xml",
        "text/javascript",
        "application/json",
        "application/javascript",
        "application/xml+rss",
        "application/atom+xml",
        "image/svg+xml",
    ]
    COMPRESS_LEVEL = int(os.environ.get("COMPRESS_LEVEL", 6))
    COMPRESS_MIN_SIZE = int(os.environ.get("COMPRESS_MIN_SIZE", 500))

    # Advanced Cache Settings
    CACHE_TTL_SHORT = int(os.environ.get("CACHE_TTL_SHORT", 300))  # 5 minutes
    CACHE_TTL_MEDIUM = int(os.environ.get("CACHE_TTL_MEDIUM", 3600))  # 1 hour
    CACHE_TTL_LONG = int(os.environ.get("CACHE_TTL_LONG", 86400))  # 24 hours
    CACHE_TTL_PERMANENT = int(os.environ.get("CACHE_TTL_PERMANENT", 604800))  # 7 days

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Configuration pour le développement"""

    DEBUG = True


class TestingConfig(Config):
    """Configuration pour les tests"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    # SQLite doesn't support connection pool parameters
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }


class ProductionConfig(Config):
    """Configuration pour la production"""

    DEBUG = False

    # Enhanced rate limiting for production
    RATELIMIT_DEFAULT = "1000 per day;100 per hour;2 per second"

    # Session configuration with secure cookies
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # Security headers enforcement
    SECURITY_ENFORCE_HTTPS = True
    SECURITY_HSTS = {
        "max-age": 31536000,  # 1 year
        "include-subdomains": True,
        "preload": True,
    }

    # Optimized cache TTLs for production
    CACHE_TTL_SHORT = 600  # 10 minutes
    CACHE_TTL_MEDIUM = 7200  # 2 hours
    CACHE_TTL_LONG = 86400  # 24 hours

    # Enhanced SQLAlchemy settings for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 20,
        "pool_timeout": 60,
        "pool_recycle": 3600,
        "max_overflow": 30,
        "pool_pre_ping": True,
        "echo": False,
        "echo_pool": False,
    }


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(config_name=None):
    """Récupère la configuration selon l'environnement"""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    return config.get(config_name, config["default"])


def validate_config(config_obj) -> Dict[str, Any]:
    """Valide la configuration et retourne un rapport détaillé"""
    required_vars = ["SECRET_KEY", "SQLALCHEMY_DATABASE_URI"]
    optional_vars = ["OPENAI_API_KEY", "MAIL_USERNAME", "MAIL_PASSWORD"]

    issues: List[str] = []
    warnings: List[str] = []

    # Vérification des variables requises
    for var in required_vars:
        if not hasattr(config_obj, var) or not getattr(config_obj, var):
            issues.append(f"Variable requise manquante: {var}")

    # Vérification des variables optionnelles
    for var in optional_vars:
        if not hasattr(config_obj, var) or not getattr(config_obj, var):
            warnings.append(f"Variable optionnelle manquante: {var}")

    # Détermination du statut
    if issues:
        status = "critical"
    elif warnings:
        status = "warning"
    else:
        status = "ok"

    return {"status": status, "issues": issues, "warnings": warnings}
