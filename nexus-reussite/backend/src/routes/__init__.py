"""
Routes API pour Nexus Réussite
Organisation modulaire par domaine fonctionnel
"""

from .aria import aria_bp
from .auth import auth_bp
from .formulas import formulas_bp
from .monitoring import monitoring_bp
from .students import students_bp
from .user import user_bp

# from .documents import documents_bp  # Temporairement désactivé

# Routes additionnelles disponibles mais non enregistrées par défaut
# from .openai_routes import openai_bp
# from .video_conference_routes import video_bp
# from .websocket_routes import websocket_bp

# Liste des blueprints à enregistrer
BLUEPRINTS = [
    auth_bp,
    user_bp,
    students_bp,
    formulas_bp,
    aria_bp,
    monitoring_bp,
    # documents_bp  # Temporairement désactivé
]

__all__ = [
    "BLUEPRINTS",
    "auth_bp",
    "user_bp",
    "students_bp",
    "formulas_bp",
    "aria_bp",
    "monitoring_bp",
    # "documents_bp"  # Temporairement désactivé
]
