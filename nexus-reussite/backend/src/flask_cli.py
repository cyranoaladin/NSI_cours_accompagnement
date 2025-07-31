#!/usr/bin/env python3
"""
Flask CLI script for Nexus Réussite
Gestion des migrations de base de données avec Alembic
"""

import os
from pathlib import Path

# Ajouter le répertoire du projet au Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configuration de l'environnement Flask
os.environ["FLASK_APP"] = "src.main_production:create_default_app"
os.environ["FLASK_ENV"] = "development"

if __name__ == "__main__":
    # Charger les variables d'environnement
    try:
        from dotenv import load_dotenv

        env_path = project_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except ImportError:
        pass

    # Lancer Flask CLI
    from flask.cli import main

    sys.exit(main())
