#!/usr/bin/env python3
"""
Script d'initialisation professionnel pour Nexus Réussite
Vérifie l'environnement, initialise la base de données et lance l'application
"""

import os
import sys
import logging
from pathlib import Path

# Ajouter le répertoire du projet au Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_environment():
    """Vérifie que l'environnement est correctement configuré"""
    logger.info("🔍 Vérification de l'environnement...")

    # Vérifier les variables d'environnement critiques
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []

    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        logger.error("❌ Variables d'environnement manquantes: %s", ', '.join(missing_vars))
        logger.error("💡 Copiez .env.example vers .env et configurez vos variables")
        return False

    logger.info("✅ Environnement configuré correctement")
    return True


def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    logger.info("📦 Vérification des dépendances...")

    try:
        # Import pour vérifier la disponibilité sans utiliser les modules
        __import__('flask')
        __import__('sqlalchemy')
        __import__('openai')
        __import__('redis')
        logger.info("✅ Toutes les dépendances principales sont installées")
        return True
    except ImportError as e:
        logger.error("❌ Dépendance manquante: %s", str(e))
        logger.error("💡 Exécutez: pip install -r requirements.txt")
        return False


def initialize_database():
    """Initialise la base de données"""
    logger.info("🗄️  Initialisation de la base de données...")

    try:
        # Import dynamique pour éviter les problèmes circulaires
        from src.main_production import create_app

        app = create_app()

        with app.app_context():
            # Import des modèles après la création du contexte
            from src.main_production import db
            from src.models.user import User, UserRole

            # Créer les tables
            db.create_all()

            # Vérifier si un admin existe déjà
            admin = User.query.filter_by(role=UserRole.ADMIN).first()
            if not admin:
                logger.info("👤 Création de l'utilisateur admin par défaut...")
                admin = User(
                    email='admin@nexus-reussite.com',
                    first_name='Admin',
                    last_name='Nexus',
                    role=UserRole.ADMIN,
                    password='admin123'  # Sera hashé automatiquement
                )
                db.session.add(admin)
                db.session.commit()
                logger.info("✅ Utilisateur admin créé (admin@nexus-reussite.com / admin123)")

        logger.info("✅ Base de données initialisée avec succès")
        return True

    except (ImportError, AttributeError, ValueError) as e:
        logger.error("❌ Erreur lors de l'initialisation de la base de données: %s", str(e))
        return False


def run_development_server():
    """Lance le serveur de développement"""
    logger.info("🚀 Lancement du serveur de développement...")

    try:
        from src.main_production import create_app

        app = create_app()
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )

    except (ImportError, OSError) as e:
        logger.error("❌ Erreur lors du lancement du serveur: %s", str(e))
        sys.exit(1)


def main():
    """Fonction principale"""
    logger.info("🎓 Initialisation de Nexus Réussite...")

    # Changer vers le répertoire du script
    os.chdir(project_root)

    # Charger les variables d'environnement
    try:
        from dotenv import load_dotenv
        env_path = project_root / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            logger.info("📋 Fichier .env chargé")
        else:
            logger.warning("⚠️  Aucun fichier .env trouvé, utilisation des variables système")
    except ImportError:
        logger.warning("⚠️  python-dotenv non installé, variables d'environnement non chargées")

    # Vérifications préalables
    if not check_dependencies():
        sys.exit(1)

    if not check_environment():
        sys.exit(1)

    # Initialisation de la base de données
    if not initialize_database():
        sys.exit(1)

    # Lancement du serveur
    logger.info("🎉 Nexus Réussite prêt à démarrer!")
    run_development_server()


if __name__ == "__main__":
    main()
