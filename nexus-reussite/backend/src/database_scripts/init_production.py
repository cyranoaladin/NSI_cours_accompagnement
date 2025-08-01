#!/usr/bin/env python3
"""
Script d'initialisation de la base de données pour la PRODUCTION
IMPORTANT: Ce script ne crée AUCUNE donnée de démonstration
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from config import get_config
from database import db
from secrets_loader import secrets_loader

# Import des modèles
from models.user import User, UserRole, UserStatus
from models.student import Student
from models.formulas import Formula, FormulaType, FormulaLevel


def init_production_database():
    """Initialise la base de données pour la production"""

    print("🚀 INITIALISATION BASE DE DONNÉES PRODUCTION")
    print("=" * 60)

    # Vérifications de sécurité CRITIQUES
    config = get_config()

    # Vérifier que nous ne sommes pas en mode développement
    if os.environ.get('FLASK_ENV') == 'development':
        print("❌ ERREUR: FLASK_ENV=development détecté!")
        print("   Changez FLASK_ENV=production avant de continuer")
        sys.exit(1)

    # Vérifier la base de données PostgreSQL
    if 'sqlite' in config.DATABASE_URL.lower():
        print("❌ ERREUR: Base de données SQLite détectée!")
        print("   Utilisez PostgreSQL pour la production")
        print("   DATABASE_URL doit commencer par 'postgresql://'")
        sys.exit(1)

    # Vérifier les secrets critiques
    required_secrets = ['SECRET_KEY', 'JWT_SECRET_KEY', 'DATABASE_URL']
    missing_secrets = []

    for secret in required_secrets:
        value = os.environ.get(secret)
        if not value or value in ['dev-key', 'your-secret-key']:
            missing_secrets.append(secret)

    if missing_secrets:
        print("❌ ERREUR: Secrets manquants ou non sécurisés:")
        for secret in missing_secrets:
            print(f"   - {secret}")
        print("\n   Configurez des secrets de production avant de continuer")
        sys.exit(1)

    print("✅ Vérifications de sécurité passées")
    print(f"📊 Base de données: {config.DATABASE_URL[:20]}...")
    print(f"🔐 Environnement: {os.environ.get('FLASK_ENV', 'non défini')}")

    # Confirmation utilisateur
    print("\n⚠️  ATTENTION: Cette opération va initialiser la base de données de PRODUCTION")
    confirmation = input("Tapez 'CONFIRMER' pour continuer: ")

    if confirmation != 'CONFIRMER':
        print("❌ Opération annulée")
        sys.exit(0)

    # Création de l'application
    app = create_app('production')

    with app.app_context():
        print("\n🗄️  Création des tables...")

        # Supprimer toutes les tables existantes (ATTENTION!)
        db.drop_all()

        # Créer toutes les tables
        db.create_all()

        print("✅ Tables créées avec succès")

        # Créer uniquement l'administrateur principal
        create_admin_user()

        # Créer les formules de base (tarifs réels)
        create_production_formulas()

        # Commit final
        db.session.commit()

        print("\n🎉 BASE DE DONNÉES PRODUCTION INITIALISÉE AVEC SUCCÈS")
        print("=" * 60)
        print("📋 COMPTE ADMINISTRATEUR CRÉÉ:")
        print("   Email: admin@nexus-reussite.com")
        print("   Mot de passe: [Défini via ADMIN_PASSWORD]")
        print("\n⚠️  PROCHAINES ÉTAPES:")
        print("   1. Connectez-vous avec le compte admin")
        print("   2. Créez les comptes enseignants réels")
        print("   3. Configurez les contenus pédagogiques")
        print("   4. Testez toutes les fonctionnalités")


def create_admin_user():
    """Crée uniquement le compte administrateur principal"""

    print("\n👤 Création du compte administrateur...")

    # Mot de passe admin depuis les variables d'environnement
    admin_password = os.environ.get('ADMIN_PASSWORD')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@nexus-reussite.com')

    if not admin_password:
        print("❌ ERREUR: ADMIN_PASSWORD non défini dans les variables d'environnement")
        print("   Définissez un mot de passe fort pour l'administrateur")
        sys.exit(1)

    # Vérifier la force du mot de passe
    if len(admin_password) < 12:
        print("❌ ERREUR: Mot de passe administrateur trop faible")
        print("   Minimum 12 caractères requis")
        sys.exit(1)

    # Créer l'administrateur
    admin = User(
        email=admin_email,
        password=admin_password,  # Sera hashé automatiquement
        first_name="Administrateur",
        last_name="Nexus Réussite",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        email_verified=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(admin)
    print(f"✅ Administrateur créé: {admin_email}")


def create_production_formulas():
    """Crée les formules tarifaires réelles (pas de demo)"""

    print("\n💰 Création des formules tarifaires...")

    # Formules réelles basées sur l'étude de marché tunisienne
    production_formulas = [
        {
            "name": "Cours Particulier - Mathématiques",
            "type": FormulaType.INDIVIDUAL,
            "level": FormulaLevel.INTERMEDIATE,
            "price_dt": 45.0,
            "hours_per_month": 8,
            "description": "Cours particuliers de mathématiques adaptés au programme tunisien",
            "features": [
                "Suivi personnalisé",
                "Exercices adaptés au niveau",
                "Préparation aux examens",
                "Support pédagogique inclus"
            ],
            "subject": "mathematiques",
            "grade_levels": ["terminale", "premiere", "seconde"]
        },
        {
            "name": "Cours Particulier - NSI",
            "type": FormulaType.INDIVIDUAL,
            "level": FormulaLevel.ADVANCED,
            "price_dt": 50.0,
            "hours_per_month": 8,
            "description": "Numérique et Sciences Informatiques - Spécialité Terminale",
            "features": [
                "Programmation Python",
                "Algorithmique avancée",
                "Projets pratiques",
                "Préparation Grand Oral"
            ],
            "subject": "nsi",
            "grade_levels": ["terminale", "premiere"]
        },
        {
            "name": "Cours Particulier - Physique-Chimie",
            "type": FormulaType.INDIVIDUAL,
            "level": FormulaLevel.INTERMEDIATE,
            "price_dt": 45.0,
            "hours_per_month": 8,
            "description": "Sciences physiques et chimiques programme français",
            "features": [
                "Expériences et manipulations",
                "Résolution de problèmes",
                "Préparation BAC",
                "Suivi régulier"
            ],
            "subject": "physique",
            "grade_levels": ["terminale", "premiere", "seconde"]
        },
        {
            "name": "Stage Intensif - Préparation BAC",
            "type": FormulaType.WORKSHOP,
            "level": FormulaLevel.ADVANCED,
            "price_dt": 180.0,
            "hours_per_month": 0,  # Stage ponctuel
            "description": "Stage intensif de préparation au Baccalauréat (5 jours)",
            "features": [
                "Révisions complètes",
                "Examens blancs",
                "Méthodologie",
                "Gestion du stress",
                "Groupe de 8 élèves maximum"
            ],
            "subject": "multi-disciplinaire",
            "grade_levels": ["terminale"]
        },
        {
            "name": "Accompagnement Grand Oral",
            "type": FormulaType.WORKSHOP,
            "level": FormulaLevel.ADVANCED,
            "price_dt": 120.0,
            "hours_per_month": 4,
            "description": "Préparation spécialisée au Grand Oral du Baccalauréat",
            "features": [
                "Choix et construction du projet",
                "Entraînements filmés",
                "Techniques de présentation",
                "Gestion du stress"
            ],
            "subject": "transversal",
            "grade_levels": ["terminale"]
        }
    ]

    for formula_data in production_formulas:
        formula = Formula(
            name=formula_data["name"],
            type=formula_data["type"],
            level=formula_data["level"],
            price_dt=formula_data["price_dt"],
            hours_per_month=formula_data["hours_per_month"],
            description=formula_data["description"],
            features=formula_data["features"],
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(formula)

    print(f"✅ {len(production_formulas)} formules tarifaires créées")


def verify_production_setup():
    """Vérifie que la configuration de production est correcte"""

    print("\n🔍 VÉRIFICATION CONFIGURATION PRODUCTION")
    print("-" * 50)

    # Vérifications environnement
    checks = [
        ("FLASK_ENV", "production"),
        ("SECRET_KEY", "Défini et sécurisé"),
        ("JWT_SECRET_KEY", "Défini et sécurisé"),
        ("DATABASE_URL", "PostgreSQL configuré"),
        ("REDIS_URL", "Cache configuré"),
        ("OPENAI_API_KEY", "IA configurée (optionnel)"),
        ("SENTRY_DSN", "Monitoring configuré (optionnel)")
    ]

    all_good = True

    for var, description in checks:
        value = os.environ.get(var)
        if value:
            if var in ['SECRET_KEY', 'JWT_SECRET_KEY']:
                status = "✅" if len(value) >= 32 and value != 'dev-key' else "❌"
            elif var == 'DATABASE_URL':
                status = "✅" if 'postgresql://' in value else "❌"
            else:
                status = "✅"

            print(f"{status} {var}: {description}")
            if status == "❌":
                all_good = False
        else:
            if var in ['OPENAI_API_KEY', 'SENTRY_DSN']:
                print(f"⚠️  {var}: {description} (optionnel)")
            else:
                print(f"❌ {var}: NON DÉFINI")
                all_good = False

    return all_good


if __name__ == "__main__":
    print("🎯 NEXUS RÉUSSITE - INITIALISATION PRODUCTION")
    print("Version: 1.0.0")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Vérification préalable
    if not verify_production_setup():
        print("\n❌ CONFIGURATION INCOMPLÈTE")
        print("Corrigez les erreurs avant de continuer")
        sys.exit(1)

    # Initialisation
    init_production_database()
