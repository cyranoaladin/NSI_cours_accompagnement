"""
Configuration centralisée pour Nexus Réussite Backend
Version améliorée et production-ready
"""
import os
from typing import Dict, List, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nexus-reussite-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///nexus_reussite.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True


class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Récupère la configuration selon l'environnement"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    return config.get(config_name, config['default'])


def validate_config(config_obj) -> Dict[str, Any]:
    """Valide la configuration et retourne un rapport détaillé"""
    required_vars = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI']
    optional_vars = ['OPENAI_API_KEY', 'MAIL_USERNAME', 'MAIL_PASSWORD']

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
        status = 'critical'
    elif warnings:
        status = 'warning'
    else:
        status = 'ok'

    return {
        'status': status,
        'issues': issues,
        'warnings': warnings
    }
