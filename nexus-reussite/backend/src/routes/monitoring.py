"""
Routes de monitoring et observabilité pour Nexus Réussite
Fournit des endpoints pour surveiller les performances et diagnostiquer les problèmes
"""

import os
from datetime import datetime, timedelta

import structlog
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from ..config import get_config
from ..database import (
    analyze_table_performance,
    create_database_indices,
    get_query_stats,
    reset_query_stats,
)
from ..services.cache_service import cache_service

logger = structlog.get_logger()

# Création du blueprint
monitoring_bp = Blueprint("monitoring", __name__)

# Limiter spécifique pour les routes de monitoring
limiter = Limiter(key_func=get_remote_address)


@monitoring_bp.route("/performance", methods=["GET"])
@jwt_required()
@limiter.limit("20 per minute")
def performance_overview():
    """
    Vue d'ensemble des performances de l'application
    Nécessite une authentification JWT
    """
    try:
        # Statistiques SQL
        sql_stats = get_query_stats()

        # Statistiques du cache
        cache_stats = cache_service.get_stats()

        # Configuration actuelle
        config = get_config()

        # Informations système
        import psutil

        system_info = {
            "cpu_percent": psutil.cpu_percent(),
            "memory": {
                "total": round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 2),
                "available": round(
                    psutil.virtual_memory().available / 1024 / 1024 / 1024, 2
                ),
                "percent": psutil.virtual_memory().percent,
            },
            "disk": {
                "total": round(psutil.disk_usage("/").total / 1024 / 1024 / 1024, 2),
                "free": round(psutil.disk_usage("/").free / 1024 / 1024 / 1024, 2),
                "percent": psutil.disk_usage("/").percent,
            },
        }

        return (
            jsonify(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "performance": {
                        "database": sql_stats,
                        "cache": cache_stats,
                        "system": system_info,
                    },
                    "configuration": {
                        "sql_profiling_enabled": config.ENABLE_SQL_PROFILING,
                        "metrics_enabled": config.ENABLE_METRICS,
                        "cache_timeout": config.CACHE_DEFAULT_TIMEOUT,
                        "environment": os.environ.get("FLASK_ENV", "unknown"),
                    },
                }
            ),
            200,
        )

    except Exception as e:
        logger.error("Erreur lors de la récupération des performances", error=str(e))
        return (
            jsonify(
                {
                    "error": "Erreur interne",
                    "message": "Impossible de récupérer les statistiques de performance",
                }
            ),
            500,
        )


@monitoring_bp.route("/database/stats", methods=["GET"])
@jwt_required()
@limiter.limit("10 per minute")
def database_stats():
    """
    Statistiques détaillées de la base de données
    """
    try:
        query_stats = get_query_stats()
        table_stats = analyze_table_performance()

        return (
            jsonify(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "query_statistics": query_stats,
                    "table_analysis": table_stats,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error("Erreur lors de l'analyse de la base de données", error=str(e))
        return jsonify({"error": "Erreur d'analyse", "message": str(e)}), 500


@monitoring_bp.route("/database/optimize", methods=["POST"])
@jwt_required()
@limiter.limit("5 per hour")
def optimize_database():
    """
    Optimise la base de données en créant les indices nécessaires
    """
    try:
        create_database_indices()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Indices de performance créés avec succès",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(
            "Erreur lors de l'optimisation de la base de données", error=str(e)
        )
        return jsonify({"error": "Erreur d'optimisation", "message": str(e)}), 500


@monitoring_bp.route("/cache/stats", methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def cache_stats():
    """
    Statistiques détaillées du cache
    """
    try:
        stats = cache_service.get_stats()
        return (
            jsonify(
                {"timestamp": datetime.utcnow().isoformat(), "cache_statistics": stats}
            ),
            200,
        )

    except Exception as e:
        logger.error("Erreur lors de la récupération des stats cache", error=str(e))
        return jsonify({"error": "Erreur cache", "message": str(e)}), 500


@monitoring_bp.route("/cache/clear", methods=["POST"])
@jwt_required()
@limiter.limit("5 per hour")
def clear_cache():
    """
    Vide complètement le cache
    """
    try:
        result = cache_service.clear()

        return jsonify(
            {
                "success": result,
                "message": (
                    "Cache vidé avec succès" if result else "Échec du vidage du cache"
                ),
                "timestamp": datetime.utcnow().isoformat(),
            }
        ), (200 if result else 500)

    except Exception as e:
        logger.error("Erreur lors du vidage du cache", error=str(e))
        return jsonify({"error": "Erreur de vidage", "message": str(e)}), 500


@monitoring_bp.route("/cache/invalidate", methods=["POST"])
@jwt_required()
@limiter.limit("10 per hour")
def invalidate_cache_pattern():
    """
    Invalide les clés de cache correspondant à un pattern
    """
    try:
        pattern = request.json.get("pattern", "")
        if not pattern:
            return (
                jsonify(
                    {
                        "error": "Pattern requis",
                        "message": "Veuillez fournir un pattern à invalider",
                    }
                ),
                400,
            )

        deleted_count = cache_service.invalidate_pattern(pattern)

        return (
            jsonify(
                {
                    "success": True,
                    "pattern": pattern,
                    "deleted_keys": deleted_count,
                    "message": f"{deleted_count} clés invalidées",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(
            "Erreur lors de l'invalidation du cache", error=str(e), pattern=pattern
        )
        return jsonify({"error": "Erreur d'invalidation", "message": str(e)}), 500


@monitoring_bp.route("/query-stats/reset", methods=["POST"])
@jwt_required()
@limiter.limit("3 per hour")
def reset_sql_stats():
    """
    Remet à zéro les statistiques de requêtes SQL
    """
    try:
        reset_query_stats()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Statistiques SQL réinitialisées",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error("Erreur lors de la réinitialisation des stats SQL", error=str(e))
        return jsonify({"error": "Erreur de réinitialisation", "message": str(e)}), 500


@monitoring_bp.route("/slow-queries", methods=["GET"])
@jwt_required()
@limiter.limit("20 per minute")
def get_slow_queries():
    """
    Récupère les requêtes SQL lentes
    """
    try:
        stats = get_query_stats()
        limit = request.args.get("limit", 20, type=int)

        slow_queries = stats.get("recent_slow_queries", [])[:limit]

        # Formatage pour une meilleure lisibilité
        formatted_queries = []
        for query in slow_queries:
            formatted_queries.append(
                {
                    "duration_ms": round(query["duration"] * 1000, 2),
                    "statement": (
                        query["statement"][:200] + "..."
                        if len(query["statement"]) > 200
                        else query["statement"]
                    ),
                    "timestamp": datetime.fromtimestamp(query["timestamp"]).isoformat(),
                    "context": query.get("context", "unknown"),
                }
            )

        return (
            jsonify(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "total_slow_queries": stats.get("slow_queries_count", 0),
                    "slowest_query_ms": (
                        round(
                            stats.get("slowest_query", {}).get("duration", 0) * 1000, 2
                        )
                        if stats.get("slowest_query")
                        else 0
                    ),
                    "recent_slow_queries": formatted_queries,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error("Erreur lors de la récupération des requêtes lentes", error=str(e))
        return jsonify({"error": "Erreur de récupération", "message": str(e)}), 500


@monitoring_bp.route("/health-detailed", methods=["GET"])
@limiter.limit("60 per minute")
def detailed_health():
    """
    Health check détaillé sans authentification (pour monitoring externe)
    """
    try:
        import threading

        from sqlalchemy import text

        from ..database import db

        health_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "healthy",
            "checks": {},
        }

        overall_healthy = True

        # Test base de données avec timing
        try:
            start_time = datetime.utcnow()
            db.session.execute(text("SELECT 1"))
            db_duration = (datetime.utcnow() - start_time).total_seconds() * 1000

            health_info["checks"]["database"] = {
                "status": "healthy",
                "response_time_ms": round(db_duration, 2),
            }
        except Exception as e:
            health_info["checks"]["database"] = {"status": "unhealthy", "error": str(e)}
            overall_healthy = False

        # Test cache
        try:
            cache_service.set("health_test", "ok", timeout=10)
            test_value = cache_service.get("health_test")
            cache_service.delete("health_test")

            health_info["checks"]["cache"] = {
                "status": "healthy" if test_value == "ok" else "degraded"
            }
        except Exception as e:
            health_info["checks"]["cache"] = {"status": "unhealthy", "error": str(e)}

        # Informations système légères
        try:
            health_info["checks"]["system"] = {
                "thread_count": threading.active_count(),
                "process_id": os.getpid(),
            }
        except Exception:
            pass

        health_info["status"] = "healthy" if overall_healthy else "unhealthy"
        status_code = 200 if overall_healthy else 503

        return jsonify(health_info), status_code

    except Exception as e:
        logger.error("Erreur lors du health check détaillé", error=str(e))
        return (
            jsonify(
                {
                    "status": "error",
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": str(e),
                }
            ),
            500,
        )


# Export du blueprint pour l'enregistrement dans l'app principale
__all__ = ["monitoring_bp"]
