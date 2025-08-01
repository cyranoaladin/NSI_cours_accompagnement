"""
Module d'optimisation des performances pour Nexus Réussite
Gestion du cache, monitoring et optimisations automatiques
"""

import logging
import time
from functools import wraps
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta

try:
    import psutil
except ImportError:
    psutil = None

try:
    import redis
except ImportError:
    redis = None

try:
    from flask import current_app, g, request
except ImportError:
    current_app = g = request = None

try:
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
except ImportError:
    event = Engine = None

try:
    from services.cache_service import cache_service
except ImportError:
    cache_service = None

logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """Optimiseur de performances pour l'application"""

    def __init__(self):
        self.redis_client = None
        self.query_stats = {
            'total_queries': 0,
            'slow_queries': 0,
            'total_time': 0.0,
            'slowest_query': None,
            'query_history': []
        }
        self.performance_metrics = {}

    def init_app(self, app):
        """Initialise l'optimiseur avec l'application Flask"""
        self.redis_client = cache_service.redis_client

        # Configuration du monitoring des requêtes SQL
        self._setup_query_monitoring()

        # Configuration du monitoring des performances
        self._setup_performance_monitoring(app)

        logger.info("✅ Performance Optimizer initialisé")

    def _setup_query_monitoring(self):
        """Configure le monitoring des requêtes SQL"""

        if not event or not Engine:
            logger.warning("SQLAlchemy not available - query monitoring disabled")
            return

        @event.listens_for(Engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            context._query_start_time = time.time()

        @event.listens_for(Engine, "after_cursor_execute")
        def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total = time.time() - context._query_start_time

            self.query_stats['total_queries'] += 1
            self.query_stats['total_time'] += total

            # Détecter les requêtes lentes (> 100ms)
            if total > 0.1:
                self.query_stats['slow_queries'] += 1

                if not self.query_stats['slowest_query'] or total > self.query_stats['slowest_query']['time']:
                    self.query_stats['slowest_query'] = {
                        'statement': statement[:200] + "..." if len(statement) > 200 else statement,
                        'time': total,
                        'timestamp': datetime.utcnow()
                    }

                logger.warning(f"Requête SQL lente ({total:.3f}s): {statement[:100]}...")

            # Garder un historique des 100 dernières requêtes
            self.query_stats['query_history'].append({
                'statement': statement[:100] + "..." if len(statement) > 100 else statement,
                'time': total,
                'timestamp': datetime.utcnow()
            })

            # Limiter l'historique
            if len(self.query_stats['query_history']) > 100:
                self.query_stats['query_history'] = self.query_stats['query_history'][-100:]

    def _setup_performance_monitoring(self, app):
        """Configure le monitoring des performances système"""

        if not current_app or not g or not request:
            logger.warning("Flask not available - performance monitoring disabled")
            return

        @app.before_request
        def before_request():
            g.request_start_time = time.time()
            if psutil:
                g.request_cpu_start = psutil.cpu_percent()

        @app.after_request
        def after_request(response):
            if hasattr(g, 'request_start_time'):
                duration = time.time() - g.request_start_time

                # Log les requêtes lentes (> 1s)
                if duration > 1.0:
                    logger.warning(
                        f"Requête HTTP lente ({duration:.3f}s): {request.method} {request.path}"
                    )

                # Mettre à jour les métriques
                endpoint = request.endpoint or 'unknown'
                if endpoint not in self.performance_metrics:
                    self.performance_metrics[endpoint] = {
                        'total_requests': 0,
                        'total_time': 0.0,
                        'average_time': 0.0,
                        'slow_requests': 0
                    }

                metrics = self.performance_metrics[endpoint]
                metrics['total_requests'] += 1
                metrics['total_time'] += duration
                metrics['average_time'] = metrics['total_time'] / metrics['total_requests']

                if duration > 1.0:
                    metrics['slow_requests'] += 1

            return response

    def get_performance_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de performance"""
        if not psutil:
            return {"error": "psutil not available"}

        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent()

        return {
            'system': {
                'cpu_percent': cpu,
                'memory_percent': memory.percent,
                'memory_available_mb': round(memory.available / 1024 / 1024, 2),
                'timestamp': datetime.utcnow().isoformat()
            },
            'database': {
                'total_queries': self.query_stats['total_queries'],
                'slow_queries': self.query_stats['slow_queries'],
                'average_query_time': (
                    round(self.query_stats['total_time'] / self.query_stats['total_queries'], 4)
                    if self.query_stats['total_queries'] > 0 else 0
                ),
                'slowest_query': self.query_stats['slowest_query']
            },
            'endpoints': self.performance_metrics,
            'cache': cache_service.get_stats() if cache_service else {"status": "not_available"}
        }

    def optimize_query_cache(self, query_key: str, data: Any, ttl: int = 300):
        """Cache optimisé pour les requêtes"""
        if self.redis_client and cache_service:
            try:
                cache_service.set(f"query:{query_key}", data, ttl)
                logger.debug(f"Requête mise en cache: {query_key}")
            except Exception as e:
                logger.warning(f"Erreur cache requête {query_key}: {e}")

    def get_cached_query(self, query_key: str) -> Optional[Any]:
        """Récupère une requête depuis le cache"""
        if self.redis_client and cache_service:
            try:
                return cache_service.get(f"query:{query_key}")
            except Exception as e:
                logger.warning(f"Erreur récupération cache {query_key}: {e}")
        return None

    def clear_performance_stats(self):
        """Remet à zéro les statistiques de performance"""
        self.query_stats = {
            'total_queries': 0,
            'slow_queries': 0,
            'total_time': 0.0,
            'slowest_query': None,
            'query_history': []
        }
        self.performance_metrics = {}
        logger.info("Statistiques de performance remises à zéro")


def cache_result(ttl: int = 300, key_prefix: str = ""):
    """Décorateur pour mettre en cache les résultats de fonction"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Générer une clé de cache unique
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"

            # Essayer de récupérer depuis le cache
            cached_result = performance_optimizer.get_cached_query(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_result

            # Exécuter la fonction et mettre en cache
            result = func(*args, **kwargs)
            performance_optimizer.optimize_query_cache(cache_key, result, ttl)
            logger.debug(f"Cache miss: {cache_key}")

            return result
        return wrapper
    return decorator


def monitor_performance(func: Callable) -> Callable:
    """Décorateur pour monitorer les performances d'une fonction"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time

        if duration > 0.5:  # Log les fonctions lentes
            logger.warning(f"Fonction lente ({duration:.3f}s): {func.__name__}")

        return result
    return wrapper


# Instance globale
performance_optimizer = PerformanceOptimizer()
