"""Point d'entrée simplifié pour tester Nexus Réussite Backend Compatible avec les
dépendances actuelles."""

import os

from flask import Flask, jsonify
from flask_cors import CORS


def create_simple_app():
    """Créer une application Flask simplifiée pour les tests."""
    app = Flask(__name__)

    # Configuration de base
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["DEBUG"] = True

    # CORS pour permettre les requêtes du frontend Next.js
    CORS(app, origins=["http://localhost:3000"])

    # Routes de test
    @app.route("/")
    def home():
        return jsonify(
            {
                "message": "Nexus Réussite Backend API",
                "status": "running",
                "version": "1.0.0",
            }
        )

    @app.route("/api/v1/health")
    def health():
        return jsonify(
            {
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "service": "nexus-backend",
            }
        )

    @app.route("/api/v1/auth/test")
    def auth_test():
        return jsonify({"message": "Auth endpoint accessible", "authenticated": False})

    @app.route("/api/v1/courses")
    def courses():
        return jsonify(
            {
                "courses": [
                    {
                        "id": 1,
                        "title": "Introduction à Python",
                        "level": "premiere",
                        "description": "Bases de la programmation Python",
                    },
                    {
                        "id": 2,
                        "title": "Structures de données",
                        "level": "terminale",
                        "description": "Listes, dictionnaires et algorithmes",
                    },
                ]
            }
        )

    return app


if __name__ == "__main__":
    app = create_simple_app()
    print("🚀 Lancement du serveur Flask Nexus Réussite")
    print("📡 API disponible sur http://localhost:5000")
    print("🌐 Frontend Next.js sur http://localhost:3000")

    app.run(host="0.0.0.0", port=5000, debug=True)
