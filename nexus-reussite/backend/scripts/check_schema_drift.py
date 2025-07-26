#!/usr/bin/env python3
"""
Script de vérification de la dérive du schéma de base de données
Vérifie que les modèles SQLAlchemy sont synchronisés avec les migrations Alembic

Usage: python scripts/check_schema_drift.py
"""

import os
import sys
import tempfile
from pathlib import Path

# Ajouter le répertoire racine au path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_schema_drift():
    """
    Vérifie s'il y a une dérive entre les modèles SQLAlchemy et les migrations
    """
    print("🔍 Vérification de la dérive du schéma de base de données...")

    # Configuration de l'environnement pour éviter les erreurs de configuration
    os.environ["FLASK_ENV"] = "testing"
    os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
    os.environ.setdefault("OPENAI_API_KEY", "test-key")

    try:
        import tempfile

        from alembic import command
        from alembic.config import Config
        from alembic.script import ScriptDirectory
        from flask_migrate import stamp, upgrade

        from src.main_production import create_app

        # Créer une application temporaire
        app = create_app()

        with app.app_context():
            # Créer une base de données temporaire
            with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
                temp_db_path = tmp_db.name

            try:
                # Configuration temporaire de la base de données
                app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{temp_db_path}"

                # Appliquer toutes les migrations
                print("📦 Application des migrations...")
                upgrade()

                # Générer une nouvelle migration pour voir s'il y a des changements
                print("🔍 Vérification des changements de modèles...")

                # Utiliser Alembic pour détecter les changements
                from alembic.autogenerate import compare_metadata
                from alembic.migration import MigrationContext
                from alembic.operations import Operations

                from src.database import db

                # Obtenir le contexte de migration
                connection = db.engine.connect()
                context = MigrationContext.configure(connection)

                # Comparer les métadonnées
                diff = compare_metadata(context, db.metadata)

                if diff:
                    print("❌ ERREUR: Dérive du schéma détectée!")
                    print("Les modèles SQLAlchemy ne correspondent pas aux migrations:")
                    print()

                    for change in diff:
                        print(f"  - {change}")

                    print()
                    print("💡 Solution:")
                    print("  1. Générez une nouvelle migration avec:")
                    print('     flask db migrate -m "Description des changements"')
                    print("  2. Committez la nouvelle migration")
                    print("  3. Relancez ce script pour vérifier")

                    return False
                else:
                    print("✅ Aucune dérive détectée - Schéma synchronisé!")
                    return True

            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(temp_db_path):
                    os.unlink(temp_db_path)

    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False


if __name__ == "__main__":
    success = check_schema_drift()
    sys.exit(0 if success else 1)
