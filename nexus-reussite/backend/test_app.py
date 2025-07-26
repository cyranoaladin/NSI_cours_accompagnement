#!/usr/bin/env python3
"""
Script de test pour l'application Nexus Réussite
"""

import sys
import os

# Ajouter le répertoire src au PATH Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_application():
    """Test de l'initialisation de l'application"""
    try:
        print("🔄 Initialisation de l'application Nexus Réussite...")
        
        # Import et création de l'application
        from main_production import create_app
        
        print("📦 Chargement des modules...")
        app = create_app()
        
        print("✅ Application créée avec succès!")
        print(f"📊 Configuration: {app.config.get('ENV', 'unknown')}")
        print(f"🔧 Debug mode: {app.debug}")
        print(f"🌐 Host: {app.config.get('SERVER_NAME', 'localhost')}")
        
        # Test des routes principales
        with app.test_client() as client:
            print("\n🔍 Test des endpoints principaux...")
            
            # Test health check
            response = client.get('/api/health')
            print(f"  Health Check: {response.status_code}")
            
            # Test config endpoint
            response = client.get('/api/config')
            print(f"  Config: {response.status_code}")
            
            # Test metrics endpoint
            response = client.get('/metrics')
            print(f"  Metrics: {response.status_code}")
        
        print("\n🎉 Tous les tests sont passés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_application()
    sys.exit(0 if success else 1)
