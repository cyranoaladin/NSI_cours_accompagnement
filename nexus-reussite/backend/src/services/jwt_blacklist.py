#!/usr/bin/env python3
"""JWT Blacklist Service for Production"""

import time
from typing import Set

# Set global pour stocker les tokens révoqués
_blacklisted_tokens: Set[str] = set()

class JWTBlacklistService:
    """Service de gestion de la blacklist JWT"""

    def __init__(self):
        self.blacklisted_tokens = _blacklisted_tokens

    def is_token_revoked(self, jti: str) -> bool:
        """Vérifie si un token est révoqué"""
        return jti in self.blacklisted_tokens

    def revoke_token(self, jti: str) -> None:
        """Révoque un token"""
        self.blacklisted_tokens.add(jti)

    def cleanup_expired_tokens(self) -> None:
        """Nettoie les tokens expirés (à implémenter avec Redis)"""
        # Pour une version production, utiliser Redis avec TTL
        pass

# Instance globale du service
_jwt_blacklist_service = JWTBlacklistService()

def get_jwt_blacklist_service() -> JWTBlacklistService:
    """Retourne l'instance du service de blacklist JWT"""
    return _jwt_blacklist_service
