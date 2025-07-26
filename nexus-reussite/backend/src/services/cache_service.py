"""
Service de cache avancé pour Nexus Réussite
Support Redis et cache mémoire avec invalidation intelligente
"""

import hashlib
import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, List, Optional, Union

import redis
from flask import current_app, g, request
from flask_caching import Cache
from redis.exceptions import ConnectionError as RedisConnectionError

logger = logging.getLogger(__name__)


class CacheService:
    """Service de cache avec support Redis et fallback mémoire"""

    def __init__(self, app=None):
        self.cache = None
        self.redis_client = None
        self.is_redis_available = False

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialise le service de cache avec l'application Flask"""
        logger.info("🚀 Initialisation du service de cache...")

        # Configuration du cache principal (Flask-Caching)
        cache_config = {
            "CACHE_TYPE": "redis" if self._check_redis_availability(app) else "simple",
            "CACHE_DEFAULT_TIMEOUT": app.config.get(
                "CACHE_DEFAULT_TIMEOUT", 300
            ),  # 5 minutes
            "CACHE_KEY_PREFIX": app.config.get("CACHE_KEY_PREFIX", "nexus_"),
        }

        # Configuration Redis spécifique
        if cache_config["CACHE_TYPE"] == "redis":
            redis_url = app.config.get("REDIS_URL", "redis://localhost:6379/0")
            cache_config.update(
                {
                    "CACHE_REDIS_URL": redis_url,
                    "CACHE_REDIS_DB": app.config.get("CACHE_REDIS_DB", 0),
                    "CACHE_REDIS_SOCKET_TIMEOUT": 5,
                    "CACHE_REDIS_SOCKET_CONNECT_TIMEOUT": 5,
                }
            )
            self.is_redis_available = True
            logger.info("✅ Cache Redis configuré")
        else:
            logger.warning("⚠️ Redis non disponible, utilisation du cache mémoire")

        # Initialisation Flask-Caching
        self.cache = Cache()
        self.cache.init_app(app, config=cache_config)

        # Client Redis direct pour opérations avancées
        if self.is_redis_available:
            try:
                self.redis_client = redis.from_url(
                    app.config.get("REDIS_URL", "redis://localhost:6379/0"),
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5,
                )
                # Test de connexion
                self.redis_client.ping()
                logger.info("✅ Connexion Redis établie")
            except Exception as e:
                logger.error(f"❌ Échec connexion Redis: {e}")
                self.redis_client = None
                self.is_redis_available = False

    def _check_redis_availability(self, app) -> bool:
        """Vérifie si Redis est disponible"""
        try:
            redis_url = app.config.get("REDIS_URL", "redis://localhost:6379/0")
            test_client = redis.from_url(redis_url, socket_timeout=2)
            test_client.ping()
            return True
        except Exception:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur du cache"""
        try:
            value = self.cache.get(key)
            if value is not None:
                logger.debug(f"🎯 Cache HIT pour la clé: {key}")
                return value
            else:
                logger.debug(f"❌ Cache MISS pour la clé: {key}")
                return default
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération du cache {key}: {e}")
            return default

    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """Stocke une valeur dans le cache"""
        try:
            result = self.cache.set(key, value, timeout=timeout)
            if result:
                logger.debug(f"✅ Valeur mise en cache: {key}")
            return result
        except Exception as e:
            logger.error(f"❌ Erreur lors de la mise en cache {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Supprime une clé du cache"""
        try:
            result = self.cache.delete(key)
            if result:
                logger.debug(f"🗑️ Clé supprimée du cache: {key}")
            return result
        except Exception as e:
            logger.error(f"❌ Erreur lors de la suppression du cache {key}: {e}")
            return False

    def clear(self) -> bool:
        """Vide tout le cache"""
        try:
            result = self.cache.clear()
            logger.info("🧹 Cache vidé complètement")
            return result
        except Exception as e:
            logger.error(f"❌ Erreur lors du vidage du cache: {e}")
            return False

    def cached(self, timeout: int = 300, key_prefix: str = "", unless: callable = None):
        """Décorateur de mise en cache pour les fonctions"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Génération de la clé de cache
                cache_key = self._generate_cache_key(func, key_prefix, *args, **kwargs)

                # Vérification de la condition unless
                if unless and unless():
                    return func(*args, **kwargs)

                # Tentative de récupération du cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result

                # Exécution de la fonction et mise en cache
                result = func(*args, **kwargs)
                self.set(cache_key, result, timeout=timeout)

                return result

            return wrapper

        return decorator

    def _generate_cache_key(self, func, prefix: str, *args, **kwargs) -> str:
        """Génère une clé de cache unique pour une fonction"""
        # Création d'un hash des arguments
        args_str = str(args) + str(sorted(kwargs.items()))
        args_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]

        # Inclusion de l'utilisateur si disponible
        user_id = getattr(g, "current_user_id", "anonymous")

        return f"{prefix}{func.__module__}.{func.__name__}_{user_id}_{args_hash}"

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalide toutes les clés correspondant à un pattern (Redis uniquement)"""
        if not self.redis_client:
            logger.warning("Pattern invalidation non disponible sans Redis")
            return 0

        try:
            keys = self.redis_client.keys(f"*{pattern}*")
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"🗑️ {deleted} clés invalidées avec le pattern: {pattern}")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'invalidation du pattern {pattern}: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        stats = {
            "cache_type": "redis" if self.is_redis_available else "memory",
            "redis_available": self.is_redis_available,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if self.redis_client:
            try:
                info = self.redis_client.info()
                stats.update(
                    {
                        "redis_info": {
                            "used_memory": info.get("used_memory_human"),
                            "connected_clients": info.get("connected_clients"),
                            "total_commands_processed": info.get(
                                "total_commands_processed"
                            ),
                            "keyspace_hits": info.get("keyspace_hits"),
                            "keyspace_misses": info.get("keyspace_misses"),
                            "uptime_in_seconds": info.get("uptime_in_seconds"),
                        }
                    }
                )

                # Calcul du hit rate
                hits = info.get("keyspace_hits", 0)
                misses = info.get("keyspace_misses", 0)
                total = hits + misses
                hit_rate = (hits / total * 100) if total > 0 else 0
                stats["hit_rate"] = f"{hit_rate:.2f}%"

            except Exception as e:
                logger.error(f"❌ Erreur lors de la récupération des stats Redis: {e}")
                stats["redis_error"] = str(e)

        return stats

    def warmup_cache(self, warmup_functions: List[callable]):
        """Préchauffe le cache avec des fonctions spécifiées"""
        logger.info("🔥 Préchauffage du cache en cours...")
        warmed_count = 0

        for func in warmup_functions:
            try:
                func()
                warmed_count += 1
                logger.debug(f"✅ Cache préchauffé: {func.__name__}")
            except Exception as e:
                logger.error(f"❌ Échec préchauffage {func.__name__}: {e}")

        logger.info(
            f"🔥 Préchauffage terminé: {warmed_count}/{len(warmup_functions)} fonctions"
        )
        return warmed_count


# Instance globale du service de cache
cache_service = CacheService()


def init_cache(app):
    """Initialise le service de cache avec l'application"""
    cache_service.init_app(app)
    return cache_service


# Décorateurs de convenance
def cached(timeout=300, key_prefix="", unless=None):
    """Décorateur de mise en cache"""
    return cache_service.cached(timeout=timeout, key_prefix=key_prefix, unless=unless)


def cache_user_data(timeout=600):
    """Décorateur spécifique pour les données utilisateur"""
    return cached(timeout=timeout, key_prefix="user_data_")


def cache_content(timeout=1800):
    """Décorateur spécifique pour le contenu (30 minutes)"""
    return cached(timeout=timeout, key_prefix="content_")


def cache_formulas(timeout=3600):
    """Décorateur spécifique pour les formules (1 heure)"""
    return cached(timeout=timeout, key_prefix="formulas_")


# Fonctions d'invalidation de cache intelligente
def invalidate_user_cache(user_id: int):
    """Invalide le cache pour un utilisateur spécifique"""
    cache_service.invalidate_pattern(f"user_data_{user_id}")
    cache_service.invalidate_pattern(f"user_{user_id}")


def invalidate_content_cache():
    """Invalide le cache de contenu"""
    cache_service.invalidate_pattern("content_")


def invalidate_formulas_cache():
    """Invalide le cache des formules"""
    cache_service.invalidate_pattern("formulas_")


__all__ = [
    "CacheService",
    "cache_service",
    "init_cache",
    "cached",
    "cache_user_data",
    "cache_content",
    "cache_formulas",
    "invalidate_user_cache",
    "invalidate_content_cache",
    "invalidate_formulas_cache",
]
