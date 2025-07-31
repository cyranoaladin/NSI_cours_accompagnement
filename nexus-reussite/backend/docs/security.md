# Security Documentation - Nexus Réussite Backend

## Secrets Management

### Overview
The Nexus Réussite backend implements a centralized secrets management system that supports both development (dotenv) and production (Vault) environments. This ensures secure handling of sensitive information while maintaining development convenience.

### Architecture

The secrets management is handled by the `src/secrets_loader.py` module, which automatically:
- Loads secrets from HashiCorp Vault in production when `VAULT_ADDR` is set
- Falls back to `.env` files for local development
- Validates required secrets in production environments
- Provides a uniform interface for secret access

### Environment-specific Configuration

#### Development Environment
- Uses `.env` files for secret storage
- Supports environment-specific files (`.env.development`, `.env.testing`)
- Provides sensible defaults for non-critical settings
- Allows hardcoded fallbacks for development convenience

#### Production Environment
- **Requires** all critical secrets to be set via environment variables or Vault
- Raises exceptions if required secrets are missing
- Supports HashiCorp Vault integration
- Enforces HTTPS and secure cookie settings

### Required Secrets

#### Critical (Production-mandatory)
- `SECRET_KEY`: Flask application secret key
- `JWT_SECRET_KEY`: JWT token signing key  
- `DATABASE_URL`: Database connection string

#### Optional (with defaults)
- `OPENAI_API_KEY`: OpenAI API access key
- `MAIL_USERNAME`: SMTP authentication username
- `MAIL_PASSWORD`: SMTP authentication password
- `REDIS_URL`: Redis connection string
- `SENTRY_DSN`: Error tracking DSN

### Vault Configuration

When using HashiCorp Vault in production:

```bash
# Required environment variables
VAULT_ADDR=https://vault.example.com:8200
VAULT_TOKEN=your-vault-token
VAULT_PATH=secret/nexus-reussite  # optional, defaults to secret/nexus-reussite
```

### Usage Examples

#### Loading Secrets in Code
```python
from src.secrets_loader import loader

# Get a secret with optional default
api_key = loader.get_secret('OPENAI_API_KEY', 'default-value')

# Check if Vault is enabled
if loader.is_vault_enabled():
    print("Using Vault for secrets")

# Refresh secrets (useful for secret rotation)
loader.refresh_secrets()
```

#### Environment File Structure
```bash
# .env.production (template)
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-jwt-production-key
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=your-openai-key
```

### Security Best Practices

1. **Never commit secrets to version control**
   - Use `.env.example` for documentation
   - Add `.env*` to `.gitignore`
   - Use environment variables in CI/CD

2. **Rotate secrets regularly**
   - Use Vault's secret rotation features
   - Update secrets in coordinated deployment

3. **Principle of least privilege**
   - Grant minimal required permissions
   - Use service-specific credentials

4. **Monitor secret access**
   - Enable Vault audit logging
   - Monitor for unauthorized access

### Migration from Hardcoded Secrets

All previously hardcoded secrets have been externalized:

1. **Database initialization scripts**: Now use `ADMIN_PASSWORD` env var
2. **Test configuration**: Uses `TEST_*` prefixed environment variables
3. **Configuration defaults**: Removed hardcoded fallbacks in production

### Troubleshooting

#### Common Issues

**Error: "Missing required secrets in production"**
- Ensure all required environment variables are set
- Verify Vault connectivity and authentication
- Check secret paths and permissions

**Error: "Vault loading not implemented"**
- Install hvac library: `pip install hvac`
- Verify VAULT_ADDR and VAULT_TOKEN are set
- Test Vault connectivity manually

**Error: "Failed to authenticate with Vault"**
- Check VAULT_TOKEN validity
- Verify network connectivity to Vault
- Ensure proper Vault policies are applied

### Dependencies

- `python-dotenv`: For .env file loading
- `hvac`: For HashiCorp Vault integration (production)

### Future Enhancements

- Support for additional secret backends (AWS Secrets Manager, Azure Key Vault)
- Automatic secret rotation
- Secret versioning and rollback capabilities
- Integration with Kubernetes secrets
