"""
Point d'entrée principal de Nexus Réussite Backend
Version production-ready avec architecture modulaire
"""

import os
from datetime import datetime
from typing import Any, Dict

# Configuration du logging structuré
import structlog
from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_compress import Compress
from werkzeug.exceptions import RequestEntityTooLarge
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

# Configuration et initialisation
from config import get_config, validate_config
from database import init_app as init_database
from middleware.cors_enhanced import enhanced_cors
from middleware.security import security_middleware
from services.jwt_blacklist import get_jwt_blacklist_service

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Service de cache
from services.cache_service import init_cache


# Prometheus client pour monitoring
def setup_prometheus_metrics(app):
    from prometheus_client import (
        Counter,
        Summary,
        generate_latest,
    )
    from prometheus_client.exposition import CONTENT_TYPE_LATEST

    # Exemple de métriques simples
    REQUEST_COUNT = Counter(
        "request_count", "Nombre de requêtes", ["method", "endpoint"]
    )
    # REQUEST_LATENCY = Summary(
    #     "request_latency_seconds", "Latence des requêtes", ["endpoint"]
    # )

    @app.before_request
    def before_request():
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

    @app.route("/metrics")
    def prometheus_metrics():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

    logger.info("✅ Metrics Prometheus configurés")


jwt = JWTManager()
limiter = Limiter(
    app=None,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour", "1 per second"],
)
talisman = Talisman()


def create_app(config_name=None):  # pylint: disable=unused-argument
    """Factory pour créer l'application Flask"""

    # Récupération de la configuration
    config_obj = get_config(config_name)

    # Validation de la configuration
    config_report: Dict[str, Any] = validate_config(config_obj)
    if config_report["status"] == "critical":
        logger.error("Configuration critique manquante:")
        for issue in config_report["issues"]:
            logger.error("  - %s", issue)
        raise RuntimeError("Configuration critique manquante")

    if config_report["warnings"]:
        logger.warning("Avertissements de configuration:")
        for warning in config_report["warnings"]:
            logger.warning("  - %s", warning)

    # Initialize Sentry for error tracking in production
    if config_obj.SENTRY_DSN and os.environ.get("FLASK_ENV") == "production":
        sentry_sdk.init(
            dsn=config_obj.SENTRY_DSN,
            integrations=[
                FlaskIntegration(transaction_style="endpoint"),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=config_obj.SENTRY_TRACES_SAMPLE_RATE,
            profiles_sample_rate=config_obj.SENTRY_PROFILES_SAMPLE_RATE,
            environment=os.environ.get("FLASK_ENV", "unknown"),
            release="nexus-reussite@1.0.0",
        )
        logger.info("✅ Sentry initialized for error tracking")

    # Création de l'application Flask
    flask_app = Flask(__name__)

    # Configuration
    flask_app.config.from_object(config_obj)
    config_obj.init_app(flask_app)

    # Initialisation des extensions
    init_database(flask_app)  # Point d'entrée unique pour la base de données
    init_cache(flask_app)  # Initialisation du service de cache
    jwt.init_app(flask_app)
    limiter.init_app(flask_app)

    # Initialize compression
    compress = Compress()
    compress.init_app(flask_app)
    logger.info("✅ Flask-Compress initialized")

    # Enhanced security configuration with Talisman
    is_production = (
        flask_app.config.get("ENV") == "production" or config_name == "production"
    )

    talisman_config = {
        "force_https": is_production,
        "strict_transport_security": is_production,
        "strict_transport_security_max_age": 31536000 if is_production else None,
        "strict_transport_security_include_subdomains": is_production,
        "content_security_policy": (
            flask_app.config.get("SECURITY_CSP") if is_production else None
        ),
        "referrer_policy": "strict-origin-when-cross-origin",
        "feature_policy": {
            "geolocation": "'none'",
            "microphone": "'none'",
            "camera": "'none'",
        },
        "session_cookie_secure": is_production,
        "session_cookie_http_only": True,
        "session_cookie_samesite": "Lax",
    }

    talisman.init_app(flask_app, **talisman_config)
    security_middleware.init_app(flask_app)
    logger.info(f"✅ Security headers configured (Production: {is_production})")

    # Configuration CORS avec middleware amélioré
    enhanced_cors.init_app(flask_app)

    # Configuration du service de blacklist JWT
    # blacklist_service = get_jwt_blacklist_service()

    # Configuration JWT avec blacklist
    setup_jwt_callbacks(flask_app)

    # Middleware de gestion des erreurs
    register_error_handlers(flask_app)

    # Import et enregistrement des blueprints
    register_blueprints(flask_app)

    # Routes principales
    register_main_routes(flask_app)

    # Configuration des métriques Prometheus
    if flask_app.config.get("ENABLE_METRICS", True):
        setup_prometheus_metrics(flask_app)

    # Middleware de logging
    if not flask_app.testing:
        setup_logging_middleware(flask_app)

    # Enregistrement des commandes CLI
    register_cli_commands(flask_app)

    return flask_app


def register_error_handlers(flask_app):
    """Enregistre les gestionnaires d'erreurs globaux"""

    @flask_app.errorhandler(400)
    def bad_request(error):  # pylint: disable=unused-argument
        return jsonify({"error": "Bad Request", "message": "Requête malformée"}), 400

    @flask_app.errorhandler(401)
    def unauthorized(error):  # pylint: disable=unused-argument
        return (
            jsonify({"error": "Unauthorized", "message": "Authentification requise"}),
            401,
        )

    @flask_app.errorhandler(403)
    def forbidden(error):  # pylint: disable=unused-argument
        return jsonify({"error": "Forbidden", "message": "Accès interdit"}), 403

    @flask_app.errorhandler(404)
    def not_found(error):  # pylint: disable=unused-argument
        return jsonify({"error": "Not Found", "message": "Ressource non trouvée"}), 404

    @flask_app.errorhandler(413)
    @flask_app.errorhandler(RequestEntityTooLarge)
    def too_large(error):  # pylint: disable=unused-argument
        return (
            jsonify(
                {
                    "error": "File Too Large",
                    "message": "Fichier trop volumineux (16MB max)",
                }
            ),
            413,
        )

    @flask_app.errorhandler(429)
    def ratelimit_handler(e):  # pylint: disable=unused-argument
        return (
            jsonify(
                {
                    "error": "Rate Limit Exceeded",
                    "message": "Trop de requêtes, veuillez patienter",
                }
            ),
            429,
        )

    @flask_app.errorhandler(500)
    def internal_error(error):
        logger.error("Erreur interne: %s", error)
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "Erreur interne du serveur",
                }
            ),
            500,
        )


def register_blueprints(flask_app):
    """Enregistre tous les blueprints de l'application"""

    # Import centralisé depuis routes.__init__
    # pylint: disable=import-outside-toplevel
    from routes import BLUEPRINTS

    # Enregistrement des blueprints avec préfixe API
    for blueprint in BLUEPRINTS:
        flask_app.register_blueprint(blueprint, url_prefix="/api")

    logger.info("✅ %d blueprints enregistrés avec succès", len(BLUEPRINTS))


def register_main_routes(flask_app):
    """Enregistre les routes principales de l'application"""

    @flask_app.route("/")
    def index():
        """Page d'accueil - sert le frontend React"""
        try:
            return send_from_directory("static", "index.html")
        except FileNotFoundError:
            logger.error("Frontend index.html not found")
            return (
                jsonify(
                    {
                        "error": "Page not found",
                        "message": "Frontend not built or not found",
                        "suggestion": "Run 'npm run build' in frontend directory",
                    }
                ),
                404,
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error("Erreur lors du service de la page d'accueil: %s", str(exc))
            return (
                jsonify(
                    {
                        "error": "Internal server error",
                        "message": "Error serving homepage",
                    }
                ),
                500,
            )

    @flask_app.route("/health")
    @flask_app.route("/api/health")
    @limiter.exempt
    def health_check():
        """Point de contrôle de santé complet pour le monitoring"""
        import psutil

        from database import get_query_stats
        from services.cache_service import cache_service

        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": os.environ.get("FLASK_ENV", "unknown"),
            "services": {},
            "performance": {},
            "resources": {},
        }

        overall_healthy = True

        # Vérification de la base de données
        try:
            from sqlalchemy import text

            from database import db

            start_time = datetime.utcnow()
            db.session.execute(text("SELECT 1"))
            db_response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            health_data["services"]["database"] = {
                "status": "healthy",
                "response_time_ms": round(db_response_time, 2),
            }
        except Exception as exc:
            logger.error("Base de données non disponible", error=str(exc))
            health_data["services"]["database"] = {
                "status": "unhealthy",
                "error": str(exc),
            }
            overall_healthy = False

        # Vérification du cache
        try:
            cache_stats = cache_service.get_stats()
            health_data["services"]["cache"] = {
                "status": "healthy" if cache_stats["redis_available"] else "degraded",
                "type": cache_stats["cache_type"],
                "hit_rate": cache_stats.get("hit_rate", "N/A"),
            }
        except Exception as exc:
            health_data["services"]["cache"] = {
                "status": "unhealthy",
                "error": str(exc),
            }

        # Vérification OpenAI
        openai_configured = bool(flask_app.config.get("OPENAI_API_KEY"))
        health_data["services"]["openai"] = {
            "status": "configured" if openai_configured else "not_configured"
        }

        # Statistiques de performance
        try:
            query_stats = get_query_stats()
            health_data["performance"]["database"] = {
                "total_queries": query_stats["total_queries"],
                "average_query_time": round(query_stats["average_time"], 4),
                "slow_queries_count": query_stats["slow_queries_count"],
            }
        except Exception:
            pass

        # Ressources système
        try:
            health_data["resources"]["memory"] = {
                "usage_percent": psutil.virtual_memory().percent,
                "available_mb": round(
                    psutil.virtual_memory().available / 1024 / 1024, 2
                ),
            }
            health_data["resources"]["cpu"] = {"usage_percent": psutil.cpu_percent()}
        except Exception:
            pass

        # Statut global
        health_data["status"] = "healthy" if overall_healthy else "unhealthy"
        status_code = 200 if overall_healthy else 503

        return jsonify(health_data), status_code

    @flask_app.route("/ready")
    @flask_app.route("/api/ready")
    @limiter.exempt
    def readiness_check():
        """Probe de prêt pour Kubernetes - vérifie si l'app peut recevoir du trafic"""
        try:
            # Vérifications critiques pour le readiness
            from sqlalchemy import text

            from database import db

            # Test de base de données
            db.session.execute(text("SELECT 1"))

            # Vérification que l'application est complètement initialisée
            # (tous les blueprints sont enregistrés, etc.)

            return (
                jsonify(
                    {
                        "status": "ready",
                        "timestamp": datetime.utcnow().isoformat(),
                        "checks": {"database": "ok", "application": "initialized"},
                    }
                ),
                200,
            )

        except Exception as exc:
            logger.error("Readiness check failed", error=str(exc))
            return (
                jsonify(
                    {
                        "status": "not_ready",
                        "timestamp": datetime.utcnow().isoformat(),
                        "error": str(exc),
                    }
                ),
                503,
            )

    @flask_app.route("/live")
    @flask_app.route("/api/live")
    @limiter.exempt
    def liveness_check():
        """Probe de vivacité pour Kubernetes - vérifie si l'app doit être redémarrée"""
        try:
            # Vérifications basiques pour s'assurer que l'application répond
            import threading

            # Vérifier que l'application n'est pas bloquée
            thread_count = threading.active_count()

            # Vérifications légères
            return (
                jsonify(
                    {
                        "status": "alive",
                        "timestamp": datetime.utcnow().isoformat(),
                        "checks": {
                            "application": "responding",
                            "thread_count": thread_count,
                        },
                    }
                ),
                200,
            )

        except Exception as exc:
            logger.error("Liveness check failed", error=str(exc))
            return (
                jsonify(
                    {
                        "status": "dead",
                        "timestamp": datetime.utcnow().isoformat(),
                        "error": str(exc),
                    }
                ),
                503,
            )

    @flask_app.route("/api/config")
    @limiter.limit("10 per minute")
    def config_info():
        """Informations de configuration (publiques uniquement)"""
        current_config = get_config()
        config_report: Dict[str, Any] = validate_config(current_config)

        return jsonify(
            {
                "app_name": "Nexus Réussite",
                "version": "1.0.0",
                "environment": os.environ.get("FLASK_ENV", "unknown"),
                "features": {
                    "ai_enabled": bool(flask_app.config.get("OPENAI_API_KEY")),
                    "email_enabled": bool(flask_app.config.get("MAIL_USERNAME")),
                    "demo_data": flask_app.config.get("ENABLE_DEMO_DATA", False),
                },
                "config_status": config_report["status"],
            }
        )

    # Route pour servir les assets statiques
    @flask_app.route("/assets/<path:filename>")
    def serve_assets(filename):
        """Sert les assets statiques avec cache"""
        try:
            response = send_from_directory("static/assets", filename)
            # Cache pour 1 heure en développement, 1 jour en production
            cache_timeout = (
                86400 if flask_app.config.get("ENV") == "production" else 3600
            )
            response.cache_control.max_age = cache_timeout
            return response
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error("Erreur lors du service de l'asset %s: %s", filename, exc)
            return jsonify({"error": "Asset not found"}), 404

    # Route catch-all pour le frontend React (SPA)
    @flask_app.route("/<path:path>")
    def react_app(path):
        """Route catch-all pour servir l'application React"""
        # Ne pas intercepter les routes API
        if path.startswith("api/"):
            return jsonify({"error": "API endpoint not found"}), 404

        try:
            # Essayer de servir le fichier statique
            return send_from_directory("static", path)
        except FileNotFoundError:
            # Si le fichier n'existe pas, servir index.html (SPA)
            try:
                return send_from_directory("static", "index.html")
            except FileNotFoundError:
                return (
                    jsonify(
                        {
                            "error": "Frontend not available",
                            "message": "Please build the frontend first",
                        }
                    ),
                    404,
                )


def setup_jwt_callbacks(flask_app):
    """Configure les callbacks JWT avec blacklist"""
    from services.jwt_blacklist import get_jwt_blacklist_service

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Vérifie si un token est révoqué"""
        jti = jwt_payload["jti"]
        blacklist_service = get_jwt_blacklist_service()
        return blacklist_service.is_token_blacklisted(jti)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Callback pour token révoqué"""
        return (
            jsonify(
                {"success": False, "error": "Token révoqué", "code": "TOKEN_REVOKED"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Callback pour token expiré"""
        return (
            jsonify(
                {"success": False, "error": "Token expiré", "code": "TOKEN_EXPIRED"}
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Callback pour token invalide"""
        return (
            jsonify(
                {"success": False, "error": "Token invalide", "code": "TOKEN_INVALID"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Callback pour token manquant"""
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Token d'authentification requis",
                    "code": "TOKEN_MISSING",
                }
            ),
            401,
        )


def setup_logging_middleware(flask_app):
    """Configure le middleware de logging pour les requêtes"""

    @flask_app.before_request
    def log_request_info():
        """Log des informations de requête"""
        if not request.path.startswith("/health"):  # Éviter le spam des health checks
            logger.info(
                "Request: %s %s from %s",
                request.method,
                request.path,
                request.remote_addr,
            )

    @flask_app.after_request
    def log_response_info(response):
        """Log des informations de réponse"""
        if not request.path.startswith("/health"):
            logger.info(
                "Response: %s for %s %s",
                response.status_code,
                request.method,
                request.path,
            )
        return response


def register_cli_commands(flask_app):
    """Enregistre les commandes CLI personnalisées"""
    import click
    from redis import Redis
    from sqlalchemy import create_engine, text

    from config import get_config

    @flask_app.cli.command("diagnose")
    def diagnose():
        """Diagnostique de l'application - vérifie DB et Redis"""
        config = get_config()

        click.echo("=== Diagnostic Nexus Réussite ===")
        click.echo("Version: 1.0.0")
        click.echo(f"Environment: {os.environ.get('FLASK_ENV', 'unknown')}")
        click.echo()

        # Vérification de la base de données
        click.echo("Vérification de la base de données...")
        try:
            engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1")).fetchone()
            click.echo("  ✓ Base de données: CONNECTÉE")
            click.echo(f"  URI: {config.SQLALCHEMY_DATABASE_URI}")
        except Exception as e:
            click.echo(f"  ✗ Base de données: ÉCHEC ({str(e)})")

        # Vérification de Redis
        click.echo("\nVérification de Redis...")
        try:
            redis_client = Redis.from_url(config.REDIS_URL)
            redis_client.ping()
            info = redis_client.info()
            click.echo("  ✓ Redis: CONNECTÉ")
            click.echo(f"  URL: {config.REDIS_URL}")
            click.echo(f"  Version: {info.get('redis_version', 'Unknown')}")
        except Exception as e:
            click.echo(f"  ✗ Redis: ÉCHEC ({str(e)})")

        # Vérification des configurations
        click.echo("\nVérification des configurations...")

        # JWT Secret
        if config.JWT_SECRET_KEY:
            click.echo("  ✓ JWT Secret: CONFIGURÉ")
        else:
            click.echo("  ✗ JWT Secret: MANQUANT")

        # Mail configuration
        if config.MAIL_USERNAME and config.MAIL_PASSWORD:
            click.echo("  ✓ Configuration Mail: COMPLÈTE")
            click.echo(f"    Serveur: {config.MAIL_SERVER}:{config.MAIL_PORT}")
            click.echo(f"    TLS: {config.MAIL_USE_TLS}")
        else:
            click.echo("  ⚠ Configuration Mail: INCOMPLÈTE")

        # OpenAI API
        if config.OPENAI_API_KEY and config.OPENAI_API_KEY != "demo-key-for-testing":
            click.echo("  ✓ OpenAI API: CONFIGURÉE")
            click.echo(f"    Modèle: {config.OPENAI_MODEL}")
        else:
            click.echo("  ⚠ OpenAI API: CLÉ DEMO OU MANQUANTE")

        click.echo("\n=== Fin du diagnostic ===")

    logger.info("✓ Commandes CLI enregistrées")


# Factory pour créer l'app avec configuration par défaut
def create_default_app():
    """Crée l'application avec la configuration par défaut"""
    return create_app()


# Instance par défaut pour gunicorn et tests - commentée pour éviter l'initialisation automatique
# app = create_default_app()

# Import des modèles pour les migrations - commenté pour éviter les imports circulaires
# from .models import user, student, content_system, formulas

if __name__ == "__main__":
    # Développement uniquement
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"

    logger.info("Starting Nexus Réussite on port %s", port)
    application = create_default_app()
    application.run(host="0.0.0.0", port=port, debug=debug)
