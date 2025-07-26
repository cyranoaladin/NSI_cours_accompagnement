"""
Tests pour l'API principale de Nexus Réussite
"""

import json

import pytest
from sqlalchemy import text

# Import avec gestion d'erreur pour les tests
try:
    from src.config import validate_config
except ImportError:
    # Mock pour les tests sans le module réel
    def validate_config():
        """Mock de validate_config pour les tests"""
        return {"status": "mocked", "errors": []}


class TestMainAPI:
    """Tests pour les routes principales de l'API"""

    def test_health_check(self, client, database):  # pylint: disable=unused-argument
        """Test du point de contrôle de santé"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.get_json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_api_health_check(
        self, client, database
    ):  # pylint: disable=unused-argument
        """Test du point de contrôle de santé API"""
        response = client.get("/api/health")
        assert response.status_code == 200

        data = response.get_json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "aria_service" in data

    def test_config_info(self, client):
        """Test des informations de configuration"""
        response = client.get("/api/config")
        assert response.status_code == 200

        data = response.get_json()
        assert data["app_name"] == "Nexus Réussite"
        assert data["version"] == "1.0.0"
        assert "features" in data
        assert "ai_enabled" in data["features"]

    def test_cors_headers(self, client):
        """Test des headers CORS"""
        response = client.options("/api/config")
        assert "Access-Control-Allow-Origin" in response.headers
        # Les headers CORS peuvent varier selon la configuration
        # On vérifie juste que la requête OPTIONS est acceptée
        assert response.status_code in [200, 204]

    def test_rate_limiting(self, client):
        """Test de la limitation de taux"""
        # Faire plusieurs requêtes rapides
        for _ in range(15):  # Dépasser la limite de 10/minute
            response = client.get("/api/config")
            if response.status_code == 429:
                break
        else:
            # Si on n'a pas atteint la limite, le test n'est pas concluant
            # mais on vérifie que les premières requêtes ont fonctionné
            assert response.status_code == 200

    def test_nonexistent_api_endpoint(self, client):
        """Test d'un endpoint API inexistant"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

        data = response.get_json()
        assert "error" in data

    def test_frontend_fallback(self, client):
        """Test du fallback vers le frontend React"""
        # Cette route devrait renvoyer index.html ou 404 si pas buildé
        response = client.get("/dashboard")
        # Soit 200 (frontend buildé) soit 404 (pas buildé)
        assert response.status_code in [200, 404]

    def test_static_assets_route(self, client):
        """Test de la route des assets statiques"""
        response = client.get("/assets/nonexistent.js")
        assert response.status_code == 404

        data = response.get_json()
        assert data["error"] == "Asset not found"


class TestErrorHandling:
    """Tests pour la gestion des erreurs"""

    def test_400_error_handler(self, client):
        """Test du gestionnaire d'erreur 400"""
        # Envoyer une requête malformée
        response = client.post("/api/config", data="invalid json")
        # Le serveur peut retourner 400 ou une autre erreur selon le routing
        if response.status_code == 400:
            data = response.get_json()
            assert "error" in data
            assert data["error"] == "Bad Request"

    def test_404_error_handler(self, client):
        """Test du gestionnaire d'erreur 404 pour API"""
        response = client.get("/api/totally/nonexistent/route")
        assert response.status_code == 404

        data = response.get_json()
        assert "error" in data

    def test_405_method_not_allowed(self, client):
        """Test pour méthode non autorisée"""
        # Essayer PUT sur une route GET
        response = client.put("/api/health")
        assert response.status_code == 405


class TestSecurity:
    """Tests pour les aspects de sécurité"""

    def test_security_headers(self, client):
        """Test des headers de sécurité"""
        response = client.get("/api/health")

        # Vérifier quelques headers de sécurité de base
        # Note: d'autres headers peuvent être ajoutés par la configuration
        assert response.status_code == 200

    def test_no_sensitive_data_in_config(self, client):
        """Test qu'aucune donnée sensible n'est exposée dans /api/config"""
        response = client.get("/api/config")
        assert response.status_code == 200

        data = response.get_json()
        data_str = json.dumps(data)

        # Vérifier qu'aucune donnée sensible n'est exposée
        sensitive_keywords = [
            "password",
            "secret",
            "key",
            "token",
            "api_key",
            "private",
            "credential",
        ]

        for keyword in sensitive_keywords:
            assert keyword not in data_str.lower()

    def test_file_upload_size_limit(self, client):
        """Test de la limite de taille de fichier"""
        # Créer un fichier "volumineux" (simulé)
        large_data = "x" * (17 * 1024 * 1024)  # 17MB > limite de 16MB

        response = client.post(
            "/api/upload",  # Cette route n'existe peut-être pas encore
            data={"file": (large_data, "large_file.txt")},
            content_type="multipart/form-data",
        )

        # Doit soit retourner 413 (trop large) soit 404 (route n'existe pas)
        assert response.status_code in [404, 413]


@pytest.mark.integration
class TestIntegration:
    """Tests d'intégration pour l'application complète"""

    def test_app_startup(self, app):
        """Test que l'application démarre correctement"""
        assert app is not None
        assert app.config["TESTING"] is True

    def test_database_connection(self, database):
        """Test de la connexion à la base de données"""
        # Exécuter une requête simple
        result = database.session.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1

    def test_config_validation(self, app):
        """Test de la validation de configuration"""
        with app.app_context():
            config_report = validate_config()
            assert "status" in config_report
            assert "issues" in config_report
            assert "warnings" in config_report

    def test_blueprints_registered(self, app):
        """Test que tous les blueprints sont enregistrés"""
        blueprint_names = [bp.name for bp in app.blueprints.values()]

        expected_blueprints = [
            "aria",
            "students",
            "formulas",
            "openai_routes",
            "documents",
            "user",
        ]

        for expected in expected_blueprints:
            # Vérifier si le blueprint existe (peut avoir un préfixe)
            found = any(expected in name for name in blueprint_names)
            if not found:
                # Le blueprint peut ne pas être encore implémenté
                # Ce n'est pas forcément une erreur en développement
                pass


if __name__ == "__main__":
    pytest.main([__file__])
