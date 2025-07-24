"""
Point d'entrée principal de Nexus Réussite Backend
Version production-ready avec architecture modulaire
"""
import os
import logging
from typing import Dict, Any
from datetime import datetime
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import RequestEntityTooLarge

# Configuration et initialisation
from .config import get_config, validate_config
from .database import db

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation des extensions Flask (sans SQLAlchemy car il est importé)
jwt = JWTManager()
limiter = Limiter(
    app=None,
    key_func=get_remote_address,
    default_limits=["100 per hour", "20 per minute"]
)


def create_app(config_name=None):  # pylint: disable=unused-argument
    """Factory pour créer l'application Flask"""

    # Récupération de la configuration
    config_obj = get_config(config_name)

    # Validation de la configuration
    config_report: Dict[str, Any] = validate_config(config_obj)
    if config_report['status'] == 'critical':
        logger.error("Configuration critique manquante:")
        for issue in config_report['issues']:
            logger.error("  - %s", issue)
        raise RuntimeError("Configuration critique manquante")

    if config_report['warnings']:
        logger.warning("Avertissements de configuration:")
        for warning in config_report['warnings']:
            logger.warning("  - %s", warning)

    # Création de l'application Flask
    flask_app = Flask(__name__)

    # Configuration
    flask_app.config.from_object(config_obj)
    config_obj.init_app(flask_app)

    # Initialisation des extensions
    db.init_app(flask_app)
    jwt.init_app(flask_app)
    limiter.init_app(flask_app)

    # Initialisation de la base de données (vérification si déjà initialisée)
    if not hasattr(flask_app, 'extensions') or 'sqlalchemy' not in flask_app.extensions:
        db.init_app(flask_app)

    # Configuration CORS
    CORS(flask_app, resources={
        r"/api/*": {
            "origins": flask_app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Middleware de gestion des erreurs
    register_error_handlers(flask_app)

    # Import et enregistrement des blueprints
    register_blueprints(flask_app)

    # Routes principales
    register_main_routes(flask_app)

    # Middleware de logging
    if not flask_app.testing:
        setup_logging_middleware(flask_app)

    return flask_app


def register_error_handlers(flask_app):
    """Enregistre les gestionnaires d'erreurs globaux"""

    @flask_app.errorhandler(400)
    def bad_request(error):  # pylint: disable=unused-argument
        return jsonify({
            'error': 'Bad Request',
            'message': 'Requête malformée'
        }), 400

    @flask_app.errorhandler(401)
    def unauthorized(error):  # pylint: disable=unused-argument
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentification requise'
        }), 401

    @flask_app.errorhandler(403)
    def forbidden(error):  # pylint: disable=unused-argument
        return jsonify({
            'error': 'Forbidden',
            'message': 'Accès interdit'
        }), 403

    @flask_app.errorhandler(404)
    def not_found(error):  # pylint: disable=unused-argument
        return jsonify({
            'error': 'Not Found',
            'message': 'Ressource non trouvée'
        }), 404

    @flask_app.errorhandler(413)
    @flask_app.errorhandler(RequestEntityTooLarge)
    def too_large(error):  # pylint: disable=unused-argument
        return jsonify({
            'error': 'File Too Large',
            'message': 'Fichier trop volumineux (16MB max)'
        }), 413

    @flask_app.errorhandler(429)
    def ratelimit_handler(e):  # pylint: disable=unused-argument
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Trop de requêtes, veuillez patienter'
        }), 429

    @flask_app.errorhandler(500)
    def internal_error(error):
        logger.error("Erreur interne: %s", error)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Erreur interne du serveur'
        }), 500


def register_blueprints(flask_app):
    """Enregistre tous les blueprints de l'application"""

    # Import centralisé depuis routes.__init__
    # pylint: disable=import-outside-toplevel
    from .routes import BLUEPRINTS

    # Enregistrement des blueprints avec préfixe API
    for blueprint in BLUEPRINTS:
        flask_app.register_blueprint(blueprint, url_prefix='/api')

    logger.info("✅ %d blueprints enregistrés avec succès", len(BLUEPRINTS))


def register_main_routes(flask_app):
    """Enregistre les routes principales de l'application"""

    @flask_app.route('/')
    def index():
        """Page d'accueil - sert le frontend React"""
        try:
            return send_from_directory('static', 'index.html')
        except FileNotFoundError:
            logger.error("Frontend index.html not found")
            return jsonify({
                "error": "Page not found",
                "message": "Frontend not built or not found",
                "suggestion": "Run 'npm run build' in frontend directory"
            }), 404
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error("Erreur lors du service de la page d'accueil: %s", str(exc))
            return jsonify({
                "error": "Internal server error",
                "message": "Error serving homepage"
            }), 500

    @flask_app.route('/health')
    @flask_app.route('/api/health')
    @limiter.exempt
    def health_check():
        """Point de contrôle de santé pour le monitoring"""
        try:
            # Vérification de la base de données
            # pylint: disable=import-outside-toplevel
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db_status = 'healthy'
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error("Base de données non disponible: %s", exc)
            db_status = 'unhealthy'

        # Vérification OpenAI
        openai_status = 'configured' if flask_app.config.get('OPENAI_API_KEY') else 'not_configured'

        status_code = 200 if db_status == 'healthy' else 503

        return jsonify({
            'status': 'healthy' if status_code == 200 else 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'environment': os.environ.get('FLASK_ENV', 'unknown'),
            'services': {
                'database': db_status,
                'openai': openai_status
            }
        }), status_code

    @flask_app.route('/api/config')
    @limiter.limit("10 per minute")
    def config_info():
        """Informations de configuration (publiques uniquement)"""
        current_config = get_config()
        config_report: Dict[str, Any] = validate_config(current_config)

        return jsonify({
            'app_name': 'Nexus Réussite',
            'version': '1.0.0',
            'environment': os.environ.get('FLASK_ENV', 'unknown'),
            'features': {
                'ai_enabled': bool(flask_app.config.get('OPENAI_API_KEY')),
                'email_enabled': bool(flask_app.config.get('MAIL_USERNAME')),
                'demo_data': flask_app.config.get('ENABLE_DEMO_DATA', False)
            },
            'config_status': config_report['status']
        })

    # Route pour servir les assets statiques
    @flask_app.route('/assets/<path:filename>')
    def serve_assets(filename):
        """Sert les assets statiques avec cache"""
        try:
            response = send_from_directory('static/assets', filename)
            # Cache pour 1 heure en développement, 1 jour en production
            cache_timeout = 86400 if flask_app.config.get('ENV') == 'production' else 3600
            response.cache_control.max_age = cache_timeout
            return response
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error("Erreur lors du service de l'asset %s: %s", filename, exc)
            return jsonify({"error": "Asset not found"}), 404

    # Route catch-all pour le frontend React (SPA)
    @flask_app.route('/<path:path>')
    def react_app(path):
        """Route catch-all pour servir l'application React"""
        # Ne pas intercepter les routes API
        if path.startswith('api/'):
            return jsonify({"error": "API endpoint not found"}), 404

        try:
            # Essayer de servir le fichier statique
            return send_from_directory('static', path)
        except FileNotFoundError:
            # Si le fichier n'existe pas, servir index.html (SPA)
            try:
                return send_from_directory('static', 'index.html')
            except FileNotFoundError:
                return jsonify({
                    "error": "Frontend not available",
                    "message": "Please build the frontend first"
                }), 404


def setup_logging_middleware(flask_app):
    """Configure le middleware de logging pour les requêtes"""

    @flask_app.before_request
    def log_request_info():
        """Log des informations de requête"""
        if not request.path.startswith('/health'):  # Éviter le spam des health checks
            logger.info("Request: %s %s from %s", request.method, request.path, request.remote_addr)

    @flask_app.after_request
    def log_response_info(response):
        """Log des informations de réponse"""
        if not request.path.startswith('/health'):
            logger.info("Response: %s for %s %s", response.status_code,
                       request.method, request.path)
        return response


# Factory pour créer l'app avec configuration par défaut
def create_default_app():
    """Crée l'application avec la configuration par défaut"""
    return create_app()


# Instance par défaut pour gunicorn et tests - commentée pour éviter l'initialisation automatique
# app = create_default_app()

# Import des modèles pour les migrations - commenté pour éviter les imports circulaires
# from .models import user, student, content_system, formulas

if __name__ == '__main__':
    # Développement uniquement
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    logger.info("Starting Nexus Réussite on port %s", port)
    application = create_default_app()  # pylint: disable=redefined-outer-name
    application.run(host='0.0.0.0', port=port, debug=debug)
