"""
Enhanced CORS Middleware pour Nexus Réussite
Implémente la vérification dynamique d'origine et le cache preflight
"""

import json
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse

import redis
from flask import current_app, g, request
from flask_cors import CORS

logger = logging.getLogger(__name__)


class EnhancedCORSMiddleware:
    """Middleware CORS amélioré avec vérification dynamique et cache"""

    def __init__(self, app=None):
        self.cors = None
        self.redis_client = None
        self.allowed_origins_cache = {}
        self.cache_timeout = 300  # 5 minutes

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialise le middleware CORS avec l'application Flask"""

        # Configuration Redis pour le cache preflight
        try:
            redis_url = app.config.get("REDIS_URL", "redis://localhost:6379/1")
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            logger.info("Cache Redis initialisé pour CORS preflight")
        except Exception as e:
            logger.warning(f"Redis non disponible pour CORS cache: {e}")
            self.redis_client = None

        # Configuration CORS simplifié pour éviter les erreurs
        # Utilise les origines de la configuration plutôt qu'une fonction
        cors_origins = app.config.get("CORS_ORIGINS", ["http://localhost:3000"])

        self.cors = CORS(
            app,
            resources={
                r"/api/*": {
                    "origins": cors_origins,
                    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                    "allow_headers": [
                        "Content-Type",
                        "Authorization",
                        "X-Requested-With",
                        "X-CSRFToken",
                        "Accept",
                        "Origin",
                        "User-Agent",
                    ],
                    "supports_credentials": True,
                    "max_age": 3600,  # Cache preflight pour 1 heure
                    "send_wildcard": False,
                }
            },
        )

        # Middleware pour gérer les requêtes OPTIONS avec cache
        app.before_request(self._handle_preflight_cache)
        app.after_request(self._add_cors_headers)

    def _validate_origin(self, origin: str) -> bool:
        """
        Valide dynamiquement l'origine de la requête

        Args:
            origin: L'origine à valider

        Returns:
            bool: True si l'origine est autorisée
        """
        if not origin:
            return False

        # Cache en mémoire pour éviter la validation répétée
        cache_key = f"origin_{origin}"
        if cache_key in self.allowed_origins_cache:
            cached_result = self.allowed_origins_cache[cache_key]
            if cached_result["expires"] > datetime.utcnow():
                return cached_result["allowed"]

        # Validation de l'origine
        is_allowed = self._check_origin_allowed(origin)

        # Mise en cache du résultat
        self.allowed_origins_cache[cache_key] = {
            "allowed": is_allowed,
            "expires": datetime.utcnow() + timedelta(seconds=self.cache_timeout),
        }

        # Nettoyage périodique du cache
        self._cleanup_origin_cache()

        if is_allowed:
            logger.info(f"Origine autorisée: {origin}")
        else:
            logger.warning(f"Origine rejetée: {origin}")

        return is_allowed

    def _check_origin_allowed(self, origin: str) -> bool:
        """
        Vérifie si une origine est autorisée selon différents critères

        Args:
            origin: L'origine à vérifier

        Returns:
            bool: True si autorisée
        """
        try:
            parsed = urlparse(origin)

            # Vérification de base du schéma
            if parsed.scheme not in ["http", "https"]:
                return False

            # Configuration des origines autorisées
            config_origins = current_app.config.get("CORS_ORIGINS", [])

            # 1. Vérification directe
            if origin in config_origins:
                return True

            # 2. Vérification avec wildcards
            for allowed_origin in config_origins:
                if self._match_origin_pattern(origin, allowed_origin):
                    return True

            # 3. Environnement de développement
            if current_app.config.get("ENV") == "development":
                if self._is_development_origin(parsed):
                    return True

            # 4. Domaines de confiance configurés
            trusted_domains = current_app.config.get("CORS_TRUSTED_DOMAINS", [])
            if self._is_trusted_domain(parsed.netloc, trusted_domains):
                return True

            return False

        except Exception as e:
            logger.error(f"Erreur lors de la validation d'origine {origin}: {e}")
            return False

    def _match_origin_pattern(self, origin: str, pattern: str) -> bool:
        """
        Vérifie si l'origine correspond au pattern (avec support wildcards)

        Args:
            origin: L'origine à vérifier
            pattern: Le pattern à matcher

        Returns:
            bool: True si match
        """
        if "*" not in pattern:
            return origin == pattern

        # Conversion du pattern en regex
        regex_pattern = pattern.replace("*", r"[^/]*")
        regex_pattern = f"^{regex_pattern}$"

        try:
            return bool(re.match(regex_pattern, origin))
        except re.error:
            return False

    def _is_development_origin(self, parsed_url) -> bool:
        """
        Vérifie si l'origine est autorisée en développement

        Args:
            parsed_url: URL parsée

        Returns:
            bool: True si origine de développement autorisée
        """
        # Localhost et 127.0.0.1
        if parsed_url.hostname in ["localhost", "127.0.0.1"]:
            return True

        # Adresses IP privées
        if parsed_url.hostname and self._is_private_ip(parsed_url.hostname):
            return True

        # Domaines de développement courants
        dev_domains = [".local", ".dev", ".test"]
        if any(parsed_url.hostname.endswith(domain) for domain in dev_domains):
            return True

        return False

    def _is_private_ip(self, ip: str) -> bool:
        """Vérifie si une IP est privée"""
        try:
            import ipaddress

            addr = ipaddress.ip_address(ip)
            return addr.is_private
        except ValueError:
            return False

    def _is_trusted_domain(self, hostname: str, trusted_domains: List[str]) -> bool:
        """
        Vérifie si le hostname appartient à un domaine de confiance

        Args:
            hostname: Le nom d'hôte à vérifier
            trusted_domains: Liste des domaines de confiance

        Returns:
            bool: True si domaine de confiance
        """
        for domain in trusted_domains:
            if hostname == domain or hostname.endswith(f".{domain}"):
                return True
        return False

    def _cleanup_origin_cache(self):
        """Nettoie le cache des origines expirées"""
        now = datetime.utcnow()
        expired_keys = [
            key
            for key, value in self.allowed_origins_cache.items()
            if value["expires"] <= now
        ]

        for key in expired_keys:
            del self.allowed_origins_cache[key]

    def _handle_preflight_cache(self):
        """Gère le cache des requêtes preflight OPTIONS"""
        if request.method != "OPTIONS":
            return

        if not self.redis_client:
            return

        # Clé de cache basée sur l'origine et la méthode demandée
        origin = request.headers.get("Origin")
        method = request.headers.get("Access-Control-Request-Method")

        if not origin or not method:
            return

        cache_key = f"preflight:{origin}:{method}"

        try:
            # Vérifier le cache
            cached_response = self.redis_client.get(cache_key)
            if cached_response:
                logger.debug(f"Cache hit pour preflight: {cache_key}")
                g.preflight_cached = True
                return

            # Marquer pour mise en cache après traitement
            g.preflight_cache_key = cache_key

        except Exception as e:
            logger.error(f"Erreur cache preflight: {e}")

    def _add_cors_headers(self, response):
        """Ajoute les en-têtes CORS et gère le cache preflight"""

        # Mise en cache des réponses preflight réussies
        if (
            request.method == "OPTIONS"
            and hasattr(g, "preflight_cache_key")
            and response.status_code == 200
            and self.redis_client
        ):

            try:
                cache_data = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "origin": request.headers.get("Origin"),
                    "method": request.headers.get("Access-Control-Request-Method"),
                }

                self.redis_client.setex(
                    g.preflight_cache_key, 3600, json.dumps(cache_data)  # 1 heure
                )

                logger.debug(f"Cache preflight mis à jour: {g.preflight_cache_key}")

            except Exception as e:
                logger.error(f"Erreur mise en cache preflight: {e}")

        # Ajout d'en-têtes de sécurité supplémentaires
        if request.headers.get("Origin"):
            response.headers["Vary"] = "Origin"
            response.headers["X-Content-Type-Options"] = "nosniff"

        return response

    def get_cors_stats(self) -> Dict:
        """Retourne les statistiques CORS"""
        stats = {
            "cache_size": len(self.allowed_origins_cache),
            "cache_enabled": self.redis_client is not None,
            "origins_cached": list(self.allowed_origins_cache.keys()),
        }

        if self.redis_client:
            try:
                preflight_keys = self.redis_client.keys("preflight:*")
                stats["preflight_cache_entries"] = len(preflight_keys)
            except Exception:
                stats["preflight_cache_entries"] = "error"

        return stats

    def clear_cache(self):
        """Vide le cache CORS"""
        self.allowed_origins_cache.clear()

        if self.redis_client:
            try:
                preflight_keys = self.redis_client.keys("preflight:*")
                if preflight_keys:
                    self.redis_client.delete(*preflight_keys)
                logger.info("Cache CORS Redis vidé")
            except Exception as e:
                logger.error(f"Erreur lors du vidage du cache CORS: {e}")


# Instance globale
enhanced_cors = EnhancedCORSMiddleware()
