"""
Application factory for Nexus Réussite Backend
Production-ready entrypoint with factory pattern
"""

import logging
import os
from typing import Optional

from .main_production import create_app as _create_app

# Configure logging for production
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def create_app(config_name: Optional[str] = None):
    """
    Application factory function for production deployment
    This is the main entry point used by gunicorn
    """
    try:
        # Use the existing factory from main_production
        app = _create_app(config_name)

        logger.info("✅ Nexus Réussite Backend initialized successfully")
        logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'unknown')}")
        logger.info(f"Debug mode: {app.debug}")

        return app

    except Exception as e:
        logger.error(f"❌ Failed to initialize application: {str(e)}")
        raise


# Create default app instance for gunicorn
app = create_app()

if __name__ == "__main__":
    # This should not be used in production, but kept for compatibility
    app.run()
