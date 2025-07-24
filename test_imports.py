#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Ajouter les chemins nécessaires
project_root = Path("/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite")
backend_src = project_root / "backend" / "src"
sys.path.insert(0, str(backend_src))

print("🔍 Test des imports Nexus Réussite...")

try:
    # Test de la configuration
    from config import get_config, validate_config
    print("✅ Configuration importée")
    
    # Test du config
    config = get_config()
    report = validate_config(config)
    print(f"✅ Configuration validée: {report['status']}")
    
    # Test de l'app
    from main_production import create_app
    print("✅ Application importée")
    
    # Créer l'app
    app = create_app()
    print("✅ Application créée")
    
    print("\n🎉 Tous les imports sont fonctionnels!")
    print("🚀 Prêt à démarrer les services")
    
except Exception as e:
    print(f"❌ Erreur lors des imports: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
