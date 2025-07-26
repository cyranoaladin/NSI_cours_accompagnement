#!/usr/bin/env python3
"""
Serveur de développement minimal pour Nexus Réussite
Version simplifiée pour tester rapidement l'application
"""

import os
import sys
from flask import Flask, jsonify
from datetime import datetime

# Ajouter le répertoire src au PATH Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_minimal_app():
    """
    Crée une version minimale de l'application pour les tests
    """
    app = Flask(__name__)
    
    # Configuration de base
    app.config['SECRET_KEY'] = 'dev-secret-key-for-testing'
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    
    # Routes de base
    @app.route('/')
    def index():
        return jsonify({
            "message": "Nexus Réussite Backend API",
            "version": "1.0.0",
            "status": "running",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    @app.route('/api/health')
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "mode": "development"
        })
    
    @app.route('/api/config')
    def config():
        return jsonify({
            "app_name": "Nexus Réussite",
            "version": "1.0.0",
            "environment": "development",
            "features": {
                "minimal_mode": True,
                "full_features": False
            }
        })
    
    # Route de test pour vérifier que l'application fonctionne
    @app.route('/api/test')
    def test():
        return jsonify({
            "message": "L'API fonctionne correctement",
            "endpoints": [
                "/",
                "/api/health",
                "/api/config",
                "/api/test"
            ]
        })
    
    return app

def run_dev_server():
    """Lance le serveur de développement"""
    print("🚀 Démarrage du serveur de développement Nexus Réussite...")
    
    app = create_minimal_app()
    
    print("✅ Application minimale créée")
    print("🌐 Serveur disponible sur: http://localhost:5000")
    print("📊 Endpoints disponibles:")
    print("  - GET /                 - Page d'accueil")
    print("  - GET /api/health       - Statut de santé")
    print("  - GET /api/config       - Configuration")
    print("  - GET /api/test         - Test de l'API")
    print("\n💡 Appuyez sur Ctrl+C pour arrêter le serveur")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur de développement")

if __name__ == "__main__":
    run_dev_server()
