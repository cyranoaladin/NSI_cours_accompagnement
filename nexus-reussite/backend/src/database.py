"""
Configuration centralisée de la base de données pour Nexus Réussite
Instance SQLAlchemy partagée entre tous les modules
"""

from flask_sqlalchemy import SQLAlchemy

# Instance SQLAlchemy centralisée
db = SQLAlchemy()

def init_database(app):
    """
    Initialise la base de données avec l'application Flask

    Args:
        app: Instance Flask
    """
    db.init_app(app)

    # Importer tous les modèles pour la création des tables
    from .models import user, student, formulas, content_system

    with app.app_context():
        db.create_all()
        print("✅ Tables de base de données créées avec succès")

__all__ = ["db", "init_database"]
