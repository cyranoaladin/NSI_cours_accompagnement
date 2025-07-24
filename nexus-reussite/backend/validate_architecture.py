#!/usr/bin/env python3
"""
Script de validation de l'architecture Nexus Réussite
Vérifie la cohérence des imports, dépendances et configuration
"""

import os
import sys
import importlib.util
from pathlib import Path

def validate_environment():
    """Valide les variables d'environnement requises"""
    required_vars = [
        'OPENAI_API_KEY',
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'DATABASE_URL'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Variables d'environnement manquantes: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Variables d'environnement validées")
        return True

def validate_imports():
    """Vérifie que tous les modules peuvent être importés"""
    try:
        # Test d'import du module principal
        sys.path.insert(0, str(Path(__file__).parent))

        # Import et utilisation des modules pour éviter les warnings
        from src.database import db, init_database
        from src.config import get_config
        from src.routes import BLUEPRINTS
        from src.models.user import User
        from src.models.student import Student

        # Vérification que les imports sont utilisables
        assert db is not None
        assert init_database is not None
        assert get_config is not None
        assert BLUEPRINTS is not None
        assert User is not None
        assert Student is not None

        print("✅ Tous les imports principaux sont valides")
        return True

    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def validate_structure():
    """Vérifie la structure des dossiers"""
    required_dirs = [
        'src',
        'src/models',
        'src/routes',
        'src/services',
        'logs',
        'uploads'
    ]

    base_path = Path(__file__).parent
    missing_dirs = []

    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if not full_path.exists():
            if dir_path in ['logs', 'uploads']:
                # Créer les dossiers manquants
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Dossier créé: {dir_path}")
            else:
                missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"❌ Dossiers manquants: {', '.join(missing_dirs)}")
        return False
    else:
        print("✅ Structure des dossiers validée")
        return True

def validate_dependencies():
    """Vérifie les dépendances Python"""
    required_packages = [
        ('flask', 'flask'),
        ('flask_sqlalchemy', 'flask_sqlalchemy'),
        ('flask_jwt_extended', 'flask_jwt_extended'),
        ('flask_cors', 'flask_cors'),
        ('openai', 'openai'),
        ('python-dotenv', 'dotenv'),
        ('bcrypt', 'bcrypt')
    ]

    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_packages.append(package_name)

    if missing_packages:
        print(f"❌ Packages manquants: {', '.join(missing_packages)}")
        print("   Installez avec: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✅ Toutes les dépendances sont installées")
        return True

def main():
    """Validation complète"""
    print("🔍 VALIDATION DE L'ARCHITECTURE NEXUS RÉUSSITE")
    print("=" * 50)

    # Chargement des variables d'environnement
    from dotenv import load_dotenv
    load_dotenv()

    checks = [
        ("Structure des dossiers", validate_structure),
        ("Dépendances Python", validate_dependencies),
        ("Variables d'environnement", validate_environment),
        ("Imports des modules", validate_imports)
    ]

    results = {}
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        results[name] = check_func()

    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DE LA VALIDATION")

    all_passed = True
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {name}")
        if not result:
            all_passed = False

    if all_passed:
        print("\n🎉 ARCHITECTURE VALIDÉE - PRÊT POUR LE DÉPLOIEMENT!")
        return 0
    else:
        print("\n⚠️  CORRECTIONS NÉCESSAIRES AVANT DÉPLOIEMENT")
        return 1

if __name__ == "__main__":
    sys.exit(main())
