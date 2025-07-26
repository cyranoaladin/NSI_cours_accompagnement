"""
Service de gestion de la blacklist JWT pour Nexus Réussite
"""

import json
import logging
import time
from datetime import datetime, timedelta
from threading import Thread
from typing import Optional

import redis
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
Base = declarative_base()


class JWTBlacklistToken(Base):
    """Modèle de base de données pour le fallback de la blacklist JWT"""

    __tablename__ = "jwt_blacklist_tokens"

    id = Column(Integer, primary_key=True)
    jti = Column(String(36), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    reason = Column(String(100), default="logout")
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<JWTBlacklistToken {self.jti}>"


class JWTBlacklistService:
    """Service amélioré de gestion de la blacklist des tokens JWT avec DB fallback et auto-pruning"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0", db_url: str = None):
        """
        Initialise le service de blacklist avec Redis et DB fallback

        Args:
            redis_url: URL de connexion Redis
            db_url: URL de la base de données pour fallback
        """
        # Configuration Redis
        self.redis_client = None
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            logger.info("Service JWT Blacklist initialisé avec Redis")
        except redis.RedisError as e:
            logger.warning(f"Erreur de connexion Redis: {e}")

        # Configuration DB fallback
        self.db_session = None
        self.db_engine = None
        if db_url:
            try:
                self.db_engine = create_engine(db_url)
                Base.metadata.create_all(self.db_engine)
                Session = sessionmaker(bind=self.db_engine)
                self.db_session = Session()
                logger.info("DB fallback configuré pour JWT Blacklist")
            except Exception as e:
                logger.error(f"Erreur configuration DB fallback: {e}")

        # Fallback mémoire en dernier recours
        if not self.redis_client and not self.db_session:
            self._memory_store = set()
            logger.warning("Utilisation du stockage en mémoire pour JWT Blacklist")

        # Démarrage du thread de nettoyage automatique
        self._auto_prune_enabled = True
        self._prune_thread = Thread(target=self._auto_prune_worker, daemon=True)
        self._prune_thread.start()

    def add_token_to_blacklist(
        self,
        jti: str,
        expires_at: Optional[datetime] = None,
        user_id: int = None,
        reason: str = "logout",
    ) -> bool:
        """
        Ajoute un token à la blacklist avec support multi-storage

        Args:
            jti: JWT ID (identifiant unique du token)
            expires_at: Date d'expiration du token
            user_id: ID de l'utilisateur (optionnel)
            reason: Raison de la blacklist

        Returns:
            bool: True si ajouté avec succès
        """
        success = False

        # Tentative Redis en premier
        if self.redis_client:
            try:
                if expires_at:
                    ttl = int((expires_at - datetime.utcnow()).total_seconds())
                    if ttl <= 0:
                        return True  # Token déjà expiré
                else:
                    ttl = 86400  # 24h par défaut

                token_data = {
                    "blacklisted_at": datetime.utcnow().isoformat(),
                    "expires_at": expires_at.isoformat() if expires_at else None,
                    "user_id": user_id,
                    "reason": reason,
                }

                self.redis_client.setex(f"blacklist:{jti}", ttl, json.dumps(token_data))
                success = True
                logger.info(f"Token {jti} ajouté à la blacklist Redis")
            except Exception as e:
                logger.error(f"Erreur Redis pour token {jti}: {e}")

        # Fallback vers la DB si Redis échoue
        if not success and self.db_session:
            try:
                # Vérifier si le token existe déjà
                existing = (
                    self.db_session.query(JWTBlacklistToken).filter_by(jti=jti).first()
                )
                if not existing:
                    token = JWTBlacklistToken(
                        jti=jti, user_id=user_id, expires_at=expires_at, reason=reason
                    )
                    self.db_session.add(token)
                    self.db_session.commit()
                success = True
                logger.info(f"Token {jti} ajouté à la blacklist DB")
            except SQLAlchemyError as e:
                logger.error(f"Erreur DB pour token {jti}: {e}")
                self.db_session.rollback()

        # Fallback mémoire en dernier recours
        if not success:
            if hasattr(self, "_memory_store"):
                self._memory_store.add(jti)
                success = True
                logger.warning(f"Token {jti} ajouté à la blacklist mémoire")

        return success

    def is_token_blacklisted(self, jti: str) -> bool:
        """
        Vérifie si un token est dans la blacklist avec support multi-storage

        Args:
            jti: JWT ID à vérifier

        Returns:
            bool: True si le token est blacklisté
        """
        try:
            # Vérifier d'abord dans Redis
            if self.redis_client:
                return self.redis_client.exists(f"blacklist:{jti}") > 0

            # Fallback vers la DB
            if self.db_session:
                token = (
                    self.db_session.query(JWTBlacklistToken)
                    .filter_by(jti=jti, is_active=True)
                    .first()
                )

                # Vérifier l'expiration
                if token and token.expires_at and token.expires_at <= datetime.utcnow():
                    # Token expiré, le désactiver
                    token.is_active = False
                    self.db_session.commit()
                    return False

                return token is not None

            # Fallback mémoire
            if hasattr(self, "_memory_store"):
                return jti in self._memory_store

            return False

        except Exception as e:
            logger.error(f"Erreur lors de la vérification du token {jti}: {e}")
            return False

    def remove_token_from_blacklist(self, jti: str) -> bool:
        """
        Retire un token de la blacklist (pour les cas d'urgence)

        Args:
            jti: JWT ID à retirer

        Returns:
            bool: True si retiré avec succès
        """
        try:
            if self.redis_client:
                result = self.redis_client.delete(f"blacklist:{jti}")
                logger.info(f"Token {jti} retiré de la blacklist")
                return result > 0
            else:
                # Fallback mémoire
                self._memory_store.discard(jti)
                return True

        except Exception as e:
            logger.error(f"Erreur lors de la suppression du token {jti}: {e}")
            return False

    def get_blacklist_stats(self) -> dict:
        """
        Retourne des statistiques sur la blacklist

        Returns:
            dict: Statistiques de la blacklist
        """
        try:
            if self.redis_client:
                # Compter les clés de blacklist
                keys = self.redis_client.keys("blacklist:*")
                total_tokens = len(keys)

                # Récupérer quelques exemples avec métadonnées
                sample_data = []
                for key in keys[:5]:  # Prendre les 5 premiers
                    data = self.redis_client.get(key)
                    if data:
                        try:
                            parsed_data = json.loads(data)
                            sample_data.append(
                                {
                                    "jti": key.replace("blacklist:", ""),
                                    "blacklisted_at": parsed_data.get("blacklisted_at"),
                                    "expires_at": parsed_data.get("expires_at"),
                                }
                            )
                        except json.JSONDecodeError:
                            continue

                return {
                    "total_blacklisted_tokens": total_tokens,
                    "storage_type": "redis",
                    "sample_tokens": sample_data,
                }
            else:
                return {
                    "total_blacklisted_tokens": len(self._memory_store),
                    "storage_type": "memory",
                    "sample_tokens": list(self._memory_store)[:5],
                }

        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {e}")
            return {
                "total_blacklisted_tokens": 0,
                "storage_type": "error",
                "error": str(e),
            }

    def cleanup_expired_tokens(self) -> int:
        """
        Nettoie les tokens expirés de la blacklist (Redis le fait automatiquement)

        Returns:
            int: Nombre de tokens supprimés
        """
        if not self.redis_client:
            # Pour le stockage mémoire, on ne peut pas vraiment nettoyer
            # sans connaître les dates d'expiration
            return 0

        try:
            # Redis gère automatiquement l'expiration via TTL
            # Cette méthode est principalement pour la compatibilité
            keys_before = len(self.redis_client.keys("blacklist:*"))

            # Forcer le nettoyage des clés expirées
            expired_keys = []
            for key in self.redis_client.keys("blacklist:*"):
                ttl = self.redis_client.ttl(key)
                if ttl == -2:  # Clé expirée
                    expired_keys.append(key)

            if expired_keys:
                self.redis_client.delete(*expired_keys)

            keys_after = len(self.redis_client.keys("blacklist:*"))
            cleaned = keys_before - keys_after

            if cleaned > 0:
                logger.info(f"Nettoyage de {cleaned} tokens expirés de la blacklist")

            return cleaned

        except Exception as e:
            logger.error(f"Erreur lors du nettoyage: {e}")
            return 0

    def _auto_prune_worker(self):
        """Worker thread pour le nettoyage automatique des tokens expirés"""
        while self._auto_prune_enabled:
            try:
                # Nettoyage toutes les heures
                time.sleep(3600)

                if not self._auto_prune_enabled:
                    break

                # Nettoyage Redis (automatique via TTL)
                redis_cleaned = 0
                if self.redis_client:
                    redis_cleaned = self.cleanup_expired_tokens()

                # Nettoyage DB
                db_cleaned = 0
                if self.db_session:
                    db_cleaned = self._cleanup_db_expired_tokens()

                total_cleaned = redis_cleaned + db_cleaned
                if total_cleaned > 0:
                    logger.info(
                        f"Auto-pruning: {total_cleaned} tokens expirés supprimés"
                    )

            except Exception as e:
                logger.error(f"Erreur dans auto-prune worker: {e}")
                time.sleep(300)  # Attendre 5 minutes en cas d'erreur

    def _cleanup_db_expired_tokens(self) -> int:
        """Nettoie les tokens expirés de la base de données"""
        if not self.db_session:
            return 0

        try:
            # Désactiver les tokens expirés
            now = datetime.utcnow()
            expired_tokens = (
                self.db_session.query(JWTBlacklistToken)
                .filter(
                    JWTBlacklistToken.expires_at <= now,
                    JWTBlacklistToken.is_active == True,
                )
                .all()
            )

            count = len(expired_tokens)
            if count > 0:
                for token in expired_tokens:
                    token.is_active = False

                self.db_session.commit()
                logger.info(f"DB: {count} tokens expirés désactivés")

            # Supprimer les anciens tokens (plus de 30 jours)
            old_date = now - timedelta(days=30)
            old_tokens = self.db_session.query(JWTBlacklistToken).filter(
                JWTBlacklistToken.blacklisted_at <= old_date
            )

            deleted_count = old_tokens.count()
            if deleted_count > 0:
                old_tokens.delete()
                self.db_session.commit()
                logger.info(f"DB: {deleted_count} anciens tokens supprimés")

            return count + deleted_count

        except SQLAlchemyError as e:
            logger.error(f"Erreur lors du nettoyage DB: {e}")
            self.db_session.rollback()
            return 0

    def stop_auto_prune(self):
        """Arrête le nettoyage automatique"""
        self._auto_prune_enabled = False
        logger.info("Auto-pruning JWT blacklist arrêté")

    def force_cleanup(self) -> dict:
        """Force un nettoyage complet immédiat"""
        results = {"redis_cleaned": 0, "db_cleaned": 0, "total_cleaned": 0}

        try:
            if self.redis_client:
                results["redis_cleaned"] = self.cleanup_expired_tokens()

            if self.db_session:
                results["db_cleaned"] = self._cleanup_db_expired_tokens()

            results["total_cleaned"] = results["redis_cleaned"] + results["db_cleaned"]

            logger.info(
                f"Nettoyage forcé terminé: {results['total_cleaned']} tokens supprimés"
            )

        except Exception as e:
            logger.error(f"Erreur lors du nettoyage forcé: {e}")
            results["error"] = str(e)

        return results


# Instance globale du service
jwt_blacklist_service = None


def get_jwt_blacklist_service(redis_url: str = None) -> JWTBlacklistService:
    """
    Factory pour récupérer l'instance du service de blacklist

    Args:
        redis_url: URL Redis (optionnel)

    Returns:
        JWTBlacklistService: Instance du service
    """
    global jwt_blacklist_service

    if jwt_blacklist_service is None:
        if redis_url is None:
            from ..config import get_config

            config = get_config()
            redis_url = getattr(config, "REDIS_URL", "redis://localhost:6379/0")

        jwt_blacklist_service = JWTBlacklistService(redis_url)

    return jwt_blacklist_service
