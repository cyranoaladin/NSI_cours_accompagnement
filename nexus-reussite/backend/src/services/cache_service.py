#!/usr/bin/env python3
"""Cache Service with Redis for Production"""

import redis
from flask import current_app

# Instance Redis globale
redis_client = None

# Cache mémoire local de fallback
cache_store = {}

def init_cache(app):
    """Initialise le cache Redis"""
    global redis_client
    try:
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        redis_client = redis.from_url(redis_url)
        redis_client.ping()  # Test de connexion
        app.logger.info("✅ Cache Redis initialisé avec succès")
    except Exception as e:
        app.logger.warning(f"⚠️ Redis non disponible, utilisation du cache mémoire: {e}")
        redis_client = None

    return app

def get_cache():
    """Retourne l'instance cache"""
    return redis_client

def get(key):
    """Récupère une valeur du cache"""
    if redis_client:
        try:
            value = redis_client.get(key)
            return value.decode('utf-8') if value else None
        except:
            pass
    return cache_store.get(key)

def set(key, value, timeout=300):
    """Stocke une valeur dans le cache"""
    if redis_client:
        try:
            return redis_client.setex(key, timeout, value)
        except:
            pass
    cache_store[key] = value
    return True

def clear(key):
    """Supprime une clé du cache"""
    if redis_client:
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Erreur Redis clear: {e}")
            return False
    else:
        # Cache mémoire local
        cache_store.pop(key, None)
        return True

def setup_cache(app):
    """Alias pour compatibilité"""
    return init_cache(app)

# Instance globale du service de cache
cache_service = {
    'get': get,
    'set': set,
    'clear': clear,
    'get_cache': get_cache,
    'init_cache': init_cache
}
