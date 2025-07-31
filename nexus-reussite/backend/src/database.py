"""
Configuration centralisée de la base de données pour Nexus Réussite
Instance SQLAlchemy partagée entre tous les modules
"""

import logging
import time
from functools import wraps
from typing import Any, Dict

from flask import g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import InterfaceError, SQLAlchemyError

# Instance SQLAlchemy centralisée
db = SQLAlchemy()
migrate = Migrate()

logger = logging.getLogger(__name__)

# Query profiling storage
query_stats = {
    "slow_queries": [],
    "total_queries": 0,
    "total_time": 0.0,
    "slowest_query": None,
}


def init_app(app):
    """
    Point d'entrée unique pour l'initialisation de la base de données

    Args:
        app: Instance Flask
    """
    logger.info("🗄️  Initialisation de la base de données...")

    # Configuration des paramètres de performance pour SQLAlchemy
    _configure_database_performance(app)

    # Initialisation SQLAlchemy
    db.init_app(app)

    # Initialisation Flask-Migrate pour Alembic
    migrate.init_app(app, db)

    # Configuration du profiling SQL si activé
    if app.config.get("ENABLE_SQL_PROFILING", False):
        setup_sql_profiling()

    # Import de tous les modèles pour l'enregistrement
    _import_all_models()

    logger.info("✅ Base de données initialisée avec succès")


def _import_all_models():
    """
    Importe tous les modèles pour s'assurer qu'ils sont enregistrés
    auprès de SQLAlchemy
    """
    try:
        # Import de tous les modules de modèles
        import models.base  # Modèles de base
        import models.formulas  # Modèles formules et cours
        import models.student  # Modèles étudiant
        import models.user  # Modèles utilisateur

        logger.info("📁 Tous les modèles importés avec succès")
    except ImportError as import_error:
        logger.error("❌ Erreur lors de l'import des modèles: %s", import_error)
        # Ne pas faire crash l'application si les modèles ne peuvent pas être importés
        logger.warning("⚠️ Certains modèles n'ont pas pu être importés, continuons...")


def create_tables(app=None):
    """
    Crée toutes les tables de la base de données

    Args:
        app: Instance Flask (optionnel si dans un contexte d'application)
    """
    if app:
        with app.app_context():
            db.create_all()
            logger.info("✅ Tables créées avec succès")
    else:
        db.create_all()
        logger.info("✅ Tables créées avec succès")


def drop_tables(app=None):
    """
    Supprime toutes les tables de la base de données

    Args:
        app: Instance Flask (optionnel si dans un contexte d'application)
    """
    if app:
        with app.app_context():
            db.drop_all()
            logger.warning("⚠️  Tables supprimées")
    else:
        db.drop_all()
        logger.warning("⚠️  Tables supprimées")


def _configure_database_performance(app):
    """
    Configure les paramètres de performance pour SQLAlchemy
    """
    # Configuration du pool de connexions
    app.config.setdefault(
        "SQLALCHEMY_ENGINE_OPTIONS",
        {
            "pool_size": 10,
            "pool_timeout": 20,
            "pool_recycle": 3600,
            "max_overflow": 20,
            "pool_pre_ping": True,  # Vérifie les connexions avant utilisation
            "echo": app.config.get("SQLALCHEMY_ECHO", False),
            "echo_pool": app.config.get("SQLALCHEMY_ECHO_POOL", False),
        },
    )

    # Configuration pour SQLAlchemy (améliore les performances)
    app.config.setdefault("SQLALCHEMY_ENGINE_OPTIONS", {}).update(
        {
            "future": True,  # Active le mode SQLAlchemy 2.0
            # Removed deprecated options that are not supported
        }
    )


def setup_sql_profiling():
    """
    Configure le profiling des requêtes SQL
    """
    logger.info("🔍 Activation du profiling SQL...")

    @event.listens_for(Engine, "before_cursor_execute")
    def receive_before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        """Événement déclenché avant l'exécution d'une requête"""
        context._query_start_time = time.time()

    @event.listens_for(Engine, "after_cursor_execute")
    def receive_after_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        """Événement déclenché après l'exécution d'une requête"""
        total_time = time.time() - context._query_start_time

        # Mise à jour des statistiques globales
        query_stats["total_queries"] += 1
        query_stats["total_time"] += total_time

        # Seuil pour considérer une requête comme lente (configurable)
        slow_query_threshold = 0.5  # 500ms

        if total_time > slow_query_threshold:
            query_info = {
                "statement": statement,
                "parameters": parameters,
                "duration": total_time,
                "timestamp": time.time(),
                "context": (
                    getattr(g, "request_id", "unknown")
                    if hasattr(g, "request_id")
                    else "unknown"
                ),
            }

            query_stats["slow_queries"].append(query_info)

            # Garder seulement les 100 dernières requêtes lentes
            if len(query_stats["slow_queries"]) > 100:
                query_stats["slow_queries"] = query_stats["slow_queries"][-100:]

            # Mettre à jour la requête la plus lente
            if (
                not query_stats["slowest_query"]
                or total_time > query_stats["slowest_query"]["duration"]
            ):
                query_stats["slowest_query"] = query_info

            logger.warning(
                "🐌 Requête lente détectée (%.3fs): %s...",
                total_time,
                statement[:100],
            )


def get_query_stats() -> Dict[str, Any]:
    """
    Retourne les statistiques des requêtes SQL
    """
    avg_time = (
        query_stats["total_time"] / query_stats["total_queries"]
        if query_stats["total_queries"] > 0
        else 0
    )

    return {
        "total_queries": query_stats["total_queries"],
        "total_time": query_stats["total_time"],
        "average_time": avg_time,
        "slow_queries_count": len(query_stats["slow_queries"]),
        "slowest_query": query_stats["slowest_query"],
        "recent_slow_queries": query_stats["slow_queries"][
            -10:
        ],  # 10 dernières requêtes lentes
    }


def reset_query_stats():
    """
    Remet à zéro les statistiques des requêtes
    """
    global query_stats
    query_stats = {
        "slow_queries": [],
        "total_queries": 0,
        "total_time": 0.0,
        "slowest_query": None,
    }
    logger.info("📊 Statistiques des requêtes réinitialisées")


def profile_query(func):
    """
    Décorateur pour profiler une fonction qui exécute des requêtes
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info("⚡ %s exécuté en %.3fs", func.__name__, duration)
            return result
        except (RuntimeError, OSError, ValueError) as exception:
            duration = time.time() - start_time
            logger.error(
                "❌ %s a échoué après %.3fs: %s", func.__name__, duration, exception
            )
            raise

    return wrapper


def create_database_indices():
    """
    Crée les indices de base de données pour optimiser les performances
    Cette fonction doit être appelée après la création des tables
    """
    try:
        with db.engine.connect() as conn:
            # Indices pour la table users (si elle existe)
            indices_sql = [
                "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
                "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",
                "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);",
                "CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login);",
                # Indices pour la table students (si elle existe)
                "CREATE INDEX IF NOT EXISTS idx_students_user_id ON students(user_id);",
                "CREATE INDEX IF NOT EXISTS idx_students_level ON students(level);",
                "CREATE INDEX IF NOT EXISTS idx_students_created_at ON "
                + "students(created_at);",
                # Indices pour les tables de contenu (si elles existent)
                "CREATE INDEX IF NOT EXISTS idx_content_created_at ON "
                + "content_items(created_at);",
                "CREATE INDEX IF NOT EXISTS idx_content_type ON "
                + "content_items(content_type);",
                "CREATE INDEX IF NOT EXISTS idx_content_status ON "
                + "content_items(status);",
                # Indices pour les formules (si la table existe)
                "CREATE INDEX IF NOT EXISTS idx_formulas_subject ON "
                + "formulas(subject);",
                "CREATE INDEX IF NOT EXISTS idx_formulas_level ON formulas(level);",
                "CREATE INDEX IF NOT EXISTS idx_formulas_created_at ON "
                + "formulas(created_at);",
            ]

            created_indices = 0
            for sql in indices_sql:
                try:
                    conn.execute(db.text(sql))
                    created_indices += 1
                except (SQLAlchemyError, InterfaceError) as exception:
                    # L'indice existe déjà ou la table n'existe pas
                    logger.debug("Indice non créé: %s", exception)

            conn.commit()
            logger.info("📈 %s indices de performance créés/vérifiés", created_indices)

    except (ValueError, TypeError, RuntimeError) as exception:
        logger.error("❌ Erreur lors de la création des indices: %s", exception)


def analyze_table_performance() -> Dict[str, Any]:
    """
    Analyse les performances des tables de la base de données
    """
    try:
        with db.engine.connect() as conn:
            # Requête pour obtenir des statistiques sur les tables (PostgreSQL)
            if "postgresql" in str(db.engine.url):
                stats_query = """
                SELECT 
                    schemaname,
                    tablename,
                    attname,
                    n_distinct,
                    correlation
                FROM pg_stats 
                WHERE schemaname = 'public'
                ORDER BY tablename, attname;
                """
            else:
                # Pour SQLite, requête simplifiée
                stats_query = """
                SELECT name as tablename, sql 
                FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%';
                """

            result = conn.execute(db.text(stats_query))
            return {
                "database_type": str(db.engine.url).split(":")[0],
                "tables_stats": [dict(row._mapping) for row in result],
            }
    except (ValueError, TypeError, RuntimeError) as exception:
        logger.error("❌ Erreur lors de l'analyse des performances: %s", exception)
        return {"error": str(exception)}


# Fonction de compatibilité avec l'ancien nom
init_database = init_app

__all__ = [
    "db",
    "migrate",
    "init_app",
    "init_database",
    "create_tables",
    "drop_tables",
    "get_query_stats",
    "reset_query_stats",
    "profile_query",
    "create_database_indices",
    "analyze_table_performance",
    "setup_sql_profiling",
]
