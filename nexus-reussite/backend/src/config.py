#!/usr/bin/env python3
"""Configuration NEXUS RÉUSSITE"""
import os

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///nexus.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL  # Flask-SQLAlchemy requiert cette variable
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'

    # Configuration JWT
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    # Configuration Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Sentry Configuration
    SENTRY_DSN = os.environ.get('SENTRY_DSN')

    # Performance et debug
    DEBUG = False
    TESTING = False

    def init_app(self, app):
        """Initialise la configuration avec l'app Flask"""
        app.config.from_object(self)
        return app


class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///nexus_dev.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_ECHO = True  # Log des requêtes SQL


class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    TESTING = False
    # Utilise les variables d'environnement sans fallback dangereux

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

def get_config(config_name=None):
    """Get configuration instance"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    config_class = config.get(config_name, DevelopmentConfig)
    return config_class()

def validate_config(config_obj=None):
    """Validate configuration"""
    if config_obj is None:
        config_instance = Config()
    else:
        config_instance = config_obj

    warnings = []
    errors = []

    # Vérifications de base
    if not config_instance.SECRET_KEY or config_instance.SECRET_KEY == 'dev-key':
        warnings.append("Using default SECRET_KEY in production")
        print("⚠️ WARNING: Using default SECRET_KEY in production")

    if not config_instance.DATABASE_URL:
        errors.append("DATABASE_URL not configured")
        print("❌ ERROR: DATABASE_URL not configured")

    if not config_instance.REDIS_URL:
        warnings.append("REDIS_URL not configured")
        print("⚠️ WARNING: REDIS_URL not configured")

    return {
        "status": "error" if errors else "success",
        "message": "Configuration validated",
        "warnings": warnings,
        "errors": errors
    }
