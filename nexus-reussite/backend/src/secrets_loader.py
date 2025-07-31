"""
Gestionnaire sécurisé des secrets pour Nexus Réussite
Version production-ready avec support Vault et variables d'environnement
"""

import logging
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Support optionnel pour HashiCorp Vault
try:
    import hvac  # noqa: F401

    VAULT_AVAILABLE = True
except ImportError:
    VAULT_AVAILABLE = False

# Support optionnel pour AWS Secrets Manager
try:
    import boto3  # noqa: F401
    from botocore.exceptions import ClientError  # noqa: F401

    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

logger = logging.getLogger(__name__)


class SecretsLoader:
    """
    Gestionnaire centralisé des secrets avec support multi-backend
    Priorité : Vault > AWS Secrets Manager > Variables d'environnement
    """

    def __init__(self):
        self.vault_client = None
        self.aws_secrets_client = None
        self.is_production = os.environ.get("FLASK_ENV") == "production"
        self.secrets_cache: Dict[str, str] = {}

        # Initialiser les clients selon la disponibilité
        self._init_vault_client()
        self._init_aws_client()
        self._load_secrets()

        logger.info("SecretsLoader initialized - Production: %s", self.is_production)

    def _init_vault_client(self):
        """Initialise le client HashiCorp Vault si configuré"""
        if not VAULT_AVAILABLE:
            return

        vault_url = os.environ.get("VAULT_ADDR", os.environ.get("VAULT_URL"))
        vault_token = os.environ.get("VAULT_TOKEN")
        vault_role_id = os.environ.get("VAULT_ROLE_ID")
        vault_secret_id = os.environ.get("VAULT_SECRET_ID")

        if vault_url and (vault_token or (vault_role_id and vault_secret_id)):
            try:
                import hvac as vault_lib

                self.vault_client = vault_lib.Client(url=vault_url)

                if vault_token:
                    self.vault_client.token = vault_token
                elif vault_role_id and vault_secret_id:
                    # Authentification AppRole
                    auth_response = self.vault_client.auth.approle.login(
                        role_id=vault_role_id, secret_id=vault_secret_id
                    )
                    self.vault_client.token = auth_response["auth"]["client_token"]

                if self.vault_client.is_authenticated():
                    logger.info("HashiCorp Vault client initialized successfully")
                else:
                    logger.error("Vault authentication failed")
                    self.vault_client = None

            except (ImportError, ValueError, RuntimeError) as e:
                logger.error("Failed to initialize Vault client: %s", e)
                self.vault_client = None

    def _init_aws_client(self):
        """Initialise le client AWS Secrets Manager si configuré"""
        if not AWS_AVAILABLE:
            return

        aws_region = os.environ.get("AWS_REGION", "us-east-1")

        try:
            import boto3 as aws_boto3

            self.aws_secrets_client = aws_boto3.client(
                "secretsmanager", region_name=aws_region
            )
            logger.info("AWS Secrets Manager client initialized successfully")
        except (ImportError, ValueError, RuntimeError) as e:
            logger.error("Failed to initialize AWS Secrets Manager: %s", e)
            self.aws_secrets_client = None

    def _load_secrets(self):
        """Load secrets from appropriate source based on environment"""
        # Load from .env files first
        self._load_from_dotenv()

        # Then try to load additional secrets from external sources
        if self.vault_client:
            logger.info("Loading additional secrets from Vault")
            self._load_from_vault()
        elif self.aws_secrets_client:
            logger.info("Loading additional secrets from AWS Secrets Manager")
            self._load_from_aws()

    def _load_from_vault(self):
        """Load secrets from HashiCorp Vault"""
        if not self.vault_client:
            return

        vault_path = os.environ.get("VAULT_SECRET_PATH", "secret/nexus-reussite")

        try:
            response = self.vault_client.secrets.kv.v2.read_secret_version(
                path=vault_path
            )
            if response and "data" in response:
                vault_secrets = response["data"]["data"]
                self.secrets_cache.update(vault_secrets)

                # Set environment variables from Vault
                for key, value in vault_secrets.items():
                    os.environ[key] = str(value)

                logger.info("Loaded %d secrets from Vault", len(vault_secrets))
        except (ValueError, RuntimeError) as e:
            logger.warning("Failed to load secrets from Vault: %s", e)

    def _load_from_aws(self):
        """Load secrets from AWS Secrets Manager"""
        if not self.aws_secrets_client:
            return

        secret_name = os.environ.get("AWS_SECRET_NAME", "nexus-reussite/production")

        try:
            if AWS_AVAILABLE:
                pass
            response = self.aws_secrets_client.get_secret_value(SecretId=secret_name)
            secrets_json = response.get("SecretString", "{}")

            import json

            aws_secrets = json.loads(secrets_json)
            self.secrets_cache.update(aws_secrets)

            # Set environment variables from AWS
            for key, value in aws_secrets.items():
                os.environ[key] = str(value)

            logger.info("Loaded %d secrets from AWS Secrets Manager", len(aws_secrets))
        except (RuntimeError, OSError, ValueError) as e:  # Keep generic for AWS imports issues
            if "ClientError" in str(type(e)):
                logger.warning("Failed to load secrets from AWS: %s", e)
            else:
                logger.warning("Unexpected error loading secrets from AWS: %s", e)

    def _load_from_dotenv(self):
        """Load secrets from .env files"""
        try:
            # Load environment-specific .env file first
            env = os.getenv("FLASK_ENV", "development")
            env_file = f".env.{env}"

            if os.path.exists(env_file):
                load_dotenv(env_file, override=True)
                logger.info("Loaded environment file: %s", env_file)

            # Load main .env file
            if os.path.exists(".env"):
                load_dotenv(".env")
                logger.info("Loaded .env file")

            # In production, ensure critical secrets are set
            if env == "production":
                self._validate_production_secrets()

        except (ValueError, TypeError, RuntimeError) as e:
            logger.error("Failed to load secrets from .env: %s", e)
            raise

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Récupère un secret avec la stratégie de fallback
        1. Cache mémoire
        2. Variables d'environnement
        3. Valeur par défaut
        """
        # Vérifier le cache d'abord
        if key in self.secrets_cache:
            return self.secrets_cache[key]

        # Fallback vers variables d'environnement
        secret_value = os.environ.get(key)

        # Utiliser la valeur par défaut si rien trouvé
        if secret_value is None:
            secret_value = default

        # Mettre en cache si trouvé
        if secret_value is not None:
            self.secrets_cache[key] = secret_value

        return secret_value

    def validate_critical_secrets(self) -> Dict[str, Any]:
        """Valide que tous les secrets critiques sont présents"""
        critical_secrets = [
            "SECRET_KEY",
            "JWT_SECRET_KEY",
            "DATABASE_URL",
            "CSRF_SECRET_KEY",
        ]

        if self.is_production:
            critical_secrets.extend(["OPENAI_API_KEY", "CORS_ORIGINS"])

        validation_result = {
            "valid": True,
            "missing_secrets": [],
            "weak_secrets": [],
            "recommendations": [],
        }

        for secret_key in critical_secrets:
            value = self.get_secret(secret_key)

            if not value:
                validation_result["missing_secrets"].append(secret_key)
                validation_result["valid"] = False
            elif len(str(value)) < 32 and "KEY" in secret_key:
                validation_result["weak_secrets"].append(secret_key)

        # Recommendations
        if validation_result["missing_secrets"]:
            validation_result["recommendations"].append(
                f"Set missing secrets: {', '.join(validation_result['missing_secrets'])}"
            )

        if validation_result["weak_secrets"]:
            validation_result["recommendations"].append(
                f"Strengthen weak secrets: {', '.join(validation_result['weak_secrets'])}"
            )

        if not self.vault_client and not self.aws_secrets_client and self.is_production:
            validation_result["recommendations"].append(
                "Consider using Vault or AWS Secrets Manager for production"
            )

        return validation_result

    def _validate_production_secrets(self):
        """Validate that required secrets are set in production"""
        secret_validation = self.validate_critical_secrets()

        if not secret_validation["valid"]:
            error_msg = f"Missing required secrets in production: {', '.join(secret_validation['missing_secrets'])}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def reload_secrets(self):
        """Recharge tous les secrets (vide le cache)"""
        self.secrets_cache.clear()
        self._load_secrets()
        logger.info("Secrets cache cleared and reloaded")

    def get_secret_sources(self) -> Dict[str, bool]:
        """Retourne les sources de secrets disponibles"""
        return {
            "environment_variables": True,
            "hashicorp_vault": self.vault_client is not None,
            "aws_secrets_manager": self.aws_secrets_client is not None,
            "vault_available": VAULT_AVAILABLE,
            "aws_available": AWS_AVAILABLE,
        }

    def is_vault_enabled(self) -> bool:
        """Check if Vault is enabled"""
        return self.vault_client is not None

    def refresh_secrets(self):
        """Refresh secrets from source (alias for reload_secrets)"""
        self.reload_secrets()


def generate_secret_key(length: int = 32) -> str:
    """Génère une cl secrète sécurisée"""
    import secrets
    import string

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_env_template() -> str:
    """Crée un template .env sécurisé avec des clés générées"""
    import datetime

    template = f"""# NEXUS RÉUSSITE - ENVIRONMENT CONFIGURATION
# Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# CRITICAL: Review and customize all values before use!

# ===========================================
# FLASK CONFIGURATION
# ===========================================
FLASK_ENV=production
SECRET_KEY={generate_secret_key(32)}
JWT_SECRET_KEY={generate_secret_key(32)}
CSRF_SECRET_KEY={generate_secret_key(32)}

# ===========================================
# DATABASE CONFIGURATION (PostgreSQL Managed)
# ===========================================
DATABASE_URL=postgresql://username:password@your-db-host:5432/nexus_reussite_prod

# Database Pool Settings
DB_POOL_SIZE=50
DB_POOL_TIMEOUT=60
DB_MAX_OVERFLOW=100
DB_POOL_RECYCLE=3600

# ===========================================
# REDIS CONFIGURATION (Managed Redis)
# ===========================================
REDIS_URL=redis://:password@your-redis-host:6379/0
CACHE_TTL_SHORT=300
CACHE_TTL_MEDIUM=3600
CACHE_TTL_LONG=86400

# ===========================================
# SECURITY CONFIGURATION
# ===========================================
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_TRUSTED_DOMAINS=yourdomain.com,www.yourdomain.com

# Force HTTPS
SECURITY_ENFORCE_HTTPS=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# ===========================================
# AI CONFIGURATION
# ===========================================
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000

# ===========================================
# EMAIL CONFIGURATION
# ===========================================
MAIL_SERVER=smtp.yourdomain.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=notifications@yourdomain.com
MAIL_PASSWORD=your-smtp-password

# ===========================================
# MONITORING & OBSERVABILITY
# ===========================================
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1

# ===========================================
# VAULT CONFIGURATION (Optional)
# ===========================================
# VAULT_URL=https://vault.yourdomain.com:8200
# VAULT_TOKEN=your-vault-token
# VAULT_SECRET_PATH=secret/nexus-reussite

# ===========================================
# AWS SECRETS MANAGER (Optional)
# ===========================================
# AWS_REGION=us-east-1
# AWS_SECRET_NAME=nexus-reussite/production

# ===========================================
# PERFORMANCE TUNING
# ===========================================
COMPRESS_LEVEL=6
COMPRESS_MIN_SIZE=500
ENABLE_METRICS=True
LOG_LEVEL=WARNING
"""
    return template


# Global secrets loader instance
loader = SecretsLoader()


if __name__ == "__main__":
    # Test et validation des secrets
    print("🔐 Nexus Réussite - Secrets Loader Test")
    print("=" * 50)

    # Afficher les sources disponibles
    sources = loader.get_secret_sources()
    print("\n📊 Available Secret Sources:")
    for source, available in sources.items():
        status = "✅" if available else "❌"
        print(f"  {status} {source.replace('_', ' ').title()}")

    # Valider les secrets critiques
    print("\n🔍 Critical Secrets Validation:")
    validation = loader.validate_critical_secrets()

    if validation["valid"]:
        print("  ✅ All critical secrets are present")
    else:
        print("  ❌ Missing critical secrets:")
        for secret in validation["missing_secrets"]:
            print(f"    - {secret}")

    if validation["weak_secrets"]:
        print("  ⚠️ Weak secrets detected:")
        for secret in validation["weak_secrets"]:
            print(f"    - {secret}")

    # Recommandations
    if validation["recommendations"]:
        print("\n💡 Recommendations:")
        for rec in validation["recommendations"]:
            print(f"  - {rec}")

    # Générer template si demandé
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "--generate-template":
        template = create_env_template()
        with open(".env.template", "w", encoding="utf-8") as f:
            f.write(template)
        print("\n📝 Template .env.template generated successfully!")
        print("   Review and customize before using in production.")
