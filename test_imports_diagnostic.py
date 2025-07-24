#!/usr/bin/env python3
"""
Test des imports pour diagnostic des erreurs Pylint
"""
import sys
import os

# Ajouter le répertoire src au Python path
backend_path = "/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend"
src_path = os.path.join(backend_path, "src")
sys.path.insert(0, src_path)

print("🔍 DIAGNOSTIC DES IMPORTS NEXUS RÉUSSITE")
print("=" * 50)

print(f"\n📂 Chemin backend: {backend_path}")
print(f"📂 Chemin src: {src_path}")

print(f"\n🐍 Python path:")
for i, path in enumerate(sys.path[:5]):
    print(f"   {i+1}. {path}")

print(f"\n🔍 Test des imports...")

try:
    print("   ✅ Test import sys - OK")
    
    # Test import config
    from config import get_config, validate_config
    print("   ✅ Import config.get_config - OK")
    print("   ✅ Import config.validate_config - OK")
    
    # Test de la fonction
    config_obj = get_config('development')
    print(f"   ✅ get_config('development') - OK: {config_obj}")
    
    # Test de validation
    validation = validate_config(config_obj)
    print(f"   ✅ validate_config - OK: {validation['status']}")
    
    print("\n🎉 TOUS LES IMPORTS FONCTIONNENT CORRECTEMENT !")
    print("   Le problème vient du cache Pylint/VS Code")
    
except ImportError as e:
    print(f"   ❌ Erreur d'import: {e}")
    print(f"   📁 Contenu du répertoire src:")
    try:
        files = os.listdir(src_path)
        for file in files:
            print(f"      - {file}")
    except Exception as e2:
        print(f"   ❌ Impossible de lister: {e2}")
        
except Exception as e:
    print(f"   ❌ Erreur générale: {e}")

print(f"\n🔧 SOLUTION:")
print("   1. Exécutez: bash nettoyer_cache_vscode.sh")
print("   2. Redémarrez VS Code complètement")
print("   3. Les erreurs Pylint devraient disparaître")

print(f"\n✨ Diagnostic terminé !")
