"""
Routes API pour Nexus Réussite
Organisation modulaire par domaine fonctionnel
"""

from .user import user_bp
from .students import students_bp
from .formulas import formulas_bp
from .aria import aria_bp
from .documents import documents_bp

# Routes additionnelles disponibles mais non enregistrées par défaut
# from .openai_routes import openai_bp
# from .video_conference_routes import video_bp
# from .websocket_routes import websocket_bp

# Liste des blueprints à enregistrer
BLUEPRINTS = [
    user_bp,
    students_bp,
    formulas_bp,
    aria_bp,
    documents_bp
]

__all__ = [
    "BLUEPRINTS",
    "user_bp",
    "students_bp",
    "formulas_bp",
    "aria_bp",
    "documents_bp"
]
