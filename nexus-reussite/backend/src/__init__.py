"""
Nexus Réussite Backend Package
Plateforme éducative intelligente avec IA adaptative
"""

__version__ = "1.0.0"
__author__ = "Nexus Réussite Team"

# Imports principaux pour faciliter l'utilisation
# imports retardés pour éviter les problèmes circulaires
from .config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
)


def get_app():
    """Factory function pour créer l'application"""
    from .main_production import create_app

    return create_app()


__all__ = [
    "Config",
    "DevelopmentConfig",
    "TestingConfig",
    "ProductionConfig",
    "get_app",
]
