# Nexus Réussite Backend

Nexus Réussite is an intelligent educational platform leveraging adaptive AI technology. This backend repository provides the necessary services for data management, user authentication, video conferencing, AI tutoring capabilities, and more.

## Requirements

- Python 3.9+
- PostgreSQL 13+
- Redis

[![CI/CD Status](https://github.com/nexus-reussite/backend/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/nexus-reussite/backend/actions?query=workflow%3ACI%2FCD+Pipeline)

## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/nexus-reussite/backend.git
cd backend
```

### Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

For standard installs, use:

```bash
pip install -r requirements.txt
```

For deterministic installs using the lock file, you can run:

```bash
pip install -r requirements.lock
```

### Local Environment Setup

Create a `.env` file in the root directory with the following variables:

```dotenv
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

## Configuration

Environment variables are used to configure the application:

- `FLASK_ENV`: `development`, `production`, etc.
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis server URL
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT secret key

## Running the Application

### Development Mode

```bash
flask run
```

Ensure that the `FLASK_ENV` is set to `development`.

## Troubleshooting

- Ensure PostgreSQL and Redis are running and properly configured.
- Check environment variables for misconfigurations.
- Verify required ports are available.

## CI/CD Pipeline

The project implements a comprehensive CI/CD pipeline documented in `CI_CD_DOCUMENTATION.md`. The pipeline includes automated testing, security scanning, dockerization, and deployments.

- **Builds**: Automated via GitHub Actions
- **Status**: ![CI/CD Pipeline](https://github.com/nexus-reussite/backend/workflows/CI%2FCD%20Pipeline/badge.svg)

## Dependency Management

### Lock File for Deterministic Builds

This project uses a lock file (`requirements.lock`) to ensure deterministic builds across different environments. The lock file contains exact versions of all dependencies.

#### Updating Dependencies

1. Update dependencies in `requirements.txt`
2. Use the provided script to update the lock file:
   ```bash
   ./scripts/update-requirements-lock.sh
   ```
   
   Or manually:
   - Install the new dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Generate the new lock file:
     ```bash
     pip freeze > requirements.lock
     ```
3. Commit both `requirements.txt` and `requirements.lock`

#### Checking for Dependency Conflicts

To manually check for dependency conflicts, run:

```bash
pip check
```

This command is automatically executed in our CI pipeline to detect version conflicts early.

### Automated CI Dependency Verification

Our CI pipeline automatically:
- Checks for dependency conflicts using `pip check`
- Validates that all dependencies can be installed successfully
- Ensures consistent environments across development and production

## Environment Variables Reference

### Required Environment Variables

| Variable | Description | Example | Default |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Application environment | `development`, `production` | `development` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost/db` | - |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` | - |
| `SECRET_KEY` | Flask application secret key | `your-random-secret-key` | - |
| `JWT_SECRET_KEY` | JWT token signing key | `your-jwt-secret-key` | - |

### Optional Environment Variables

| Variable | Description | Example | Default |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | `sk-...` | `demo-key-for-testing` |
| `SENTRY_DSN` | Sentry error tracking DSN | `https://...@sentry.io/...` | - |
| `ENABLE_METRICS` | Enable Prometheus metrics | `true`, `false` | `true` |
| `CACHE_TTL_SHORT` | Short cache TTL (seconds) | `300` | `300` (dev) / `600` (prod) |
| `COMPRESS_LEVEL` | Response compression level | `1-9` | `6` |

## API Documentation

The API documentation is available via Swagger UI:

- **Development**: http://localhost:5000/api/docs/
- **Production**: https://api.nexus-reussite.com/api/docs/

### API Endpoints Overview

- **Authentication**: `/api/auth/` - User login, registration, JWT management
- **Students**: `/api/students/` - Student profile and progress management
- **Documents**: `/api/documents/` - AI-powered document generation
- **Formulas**: `/api/formulas/` - Mathematical formulas database
- **Health**: `/api/health` - System health monitoring
- **Metrics**: `/metrics` - Prometheus metrics (production)

## Development Workflow

### Setting up Development Environment

1. **Install System Dependencies**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3.12 python3.12-venv python3-pip postgresql-13 redis-server
   
   # macOS (using Homebrew)
   brew install python@3.12 postgresql@13 redis
   ```

2. **Start Required Services**:
   ```bash
   # Start PostgreSQL
   sudo systemctl start postgresql  # Linux
   brew services start postgresql@13  # macOS
   
   # Start Redis
   sudo systemctl start redis  # Linux
   brew services start redis  # macOS
   ```

3. **Create Database**:
   ```bash
   sudo -u postgres createdb nexus_reussite_dev
   ```

4. **Run Database Migrations**:
   ```bash
   flask db upgrade
   ```

5. **Run the Application**:
   ```bash
   python src/main.py
   # or
   flask run
   ```

### Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

## Docker Development

### Using Docker Compose

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up

# Start in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f backend

# Stop services
docker-compose -f docker-compose.dev.yml down
```

### Building Production Image

```bash
# Build the image
docker build -f Dockerfile.production -t nexus-reussite-backend:latest .

# Run the container
docker run -d --name nexus-backend \
  --env-file .env.production \
  -p 5000:5000 \
  nexus-reussite-backend:latest
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Issues

**Problem**: `sqlalchemy.exc.OperationalError: connection to server`

**Solutions**:
- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Check database URL format: `postgresql://user:password@host:port/database`
- Verify database exists: `psql -l`

#### 2. Redis Connection Issues

**Problem**: `redis.exceptions.ConnectionError`

**Solutions**:
- Ensure Redis is running: `sudo systemctl status redis`
- Check Redis URL format: `redis://host:port/database`
- Test connection: `redis-cli ping`

#### 3. Import Errors

**Problem**: `ModuleNotFoundError` or circular imports

**Solutions**:
- Ensure virtual environment is activated
- Check PYTHONPATH includes the project root
- Run the import detection script: `python detect_circular_imports.py`

#### 4. Permission Errors

**Problem**: File or directory permission denied

**Solutions**:
- Check file permissions: `ls -la`
- Ensure proper ownership: `chown -R user:group directory`
- For Docker: check user in container matches host user

### Diagnostic Commands

```bash
# Check application health
curl http://localhost:5000/health

# Run built-in diagnostics
flask diagnose

# Check dependency conflicts
pip check

# View application logs
tail -f logs/app.log

# Check database connectivity
psql $DATABASE_URL -c "SELECT 1;"

# Check Redis connectivity
redis-cli -u $REDIS_URL ping
```

## Performance Optimization

### Development Performance

- **Hot Reloading**: Flask automatically reloads on code changes
- **Debug Mode**: Detailed error pages and debugging tools
- **SQL Logging**: Set `SQLALCHEMY_ECHO=True` to log all SQL queries

### Production Performance

- **Gunicorn**: Multi-worker WSGI server with gevent workers
- **Compression**: Automatic response compression via Flask-Compress
- **Caching**: Redis-backed caching with optimized TTLs
- **Connection Pooling**: SQLAlchemy connection pool (20 connections)
- **Rate Limiting**: Protective rate limiting with configurable rules

## Security Features

### Authentication & Authorization
- JWT-based authentication with configurable expiration
- Password hashing using bcrypt
- Session management with secure cookies

### Security Headers
- HTTPS enforcement in production (Flask-Talisman)
- HSTS (HTTP Strict Transport Security)
- Content Security Policy (CSP)
- Referrer Policy and Feature Policy

### Data Protection
- SQL injection protection via SQLAlchemy ORM
- XSS protection through template escaping
- CSRF protection with Flask-WTF
- Input validation and sanitization

## Code Quality

### Linting and Formatting

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check style guide compliance
flake8 src/ tests/

# Static analysis
pylint src/

# Type checking
mypy src/ --ignore-missing-imports
```

### Security Scanning

```bash
# Security linting
bandit -r src/

# Dependency vulnerability scanning
safety check

# License compliance
pip-licenses
```

## Monitoring and Observability

### Health Endpoints

- **Health Check**: `GET /health` - Comprehensive system status
- **Readiness Probe**: `GET /ready` - Kubernetes readiness check
- **Liveness Probe**: `GET /live` - Kubernetes liveness check

### Metrics

- **Prometheus Metrics**: Available at `/metrics` endpoint
- **Application Metrics**: Request count, duration, error rates
- **System Metrics**: Memory usage, CPU utilization, database connections

### Logging

- **Structured Logging**: JSON-formatted logs for better parsing
- **Log Levels**: Configurable logging levels (DEBUG, INFO, WARNING, ERROR)
- **Request Logging**: Automatic logging of HTTP requests and responses

## Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 and use provided linting tools
2. **Testing**: Maintain test coverage above 90%
3. **Documentation**: Update documentation for new features
4. **Security**: Run security scans before submitting PRs

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and add tests
4. Run the full test suite: `pytest`
5. Format code: `black src/ tests/`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Create a Pull Request

### Development Resources

- **API Documentation**: http://localhost:5000/api/docs/
- **Development Guide**: `docs/development.md`
- **CI/CD Documentation**: `CI_CD_DOCUMENTATION.md`
- **Production Deployment**: `PRODUCTION_DEPLOYMENT.md`

## License

MIT License. See `LICENSE` file for more information.

## Support

For questions, issues, or contributions:

- **GitHub Issues**: [Create an issue](https://github.com/nexus-reussite/backend/issues)
- **Documentation**: Check the `docs/` directory
- **API Reference**: Visit `/api/docs/` when running the application

---

**Project Status**: [![CI/CD Pipeline](https://github.com/nexus-reussite/backend/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/nexus-reussite/backend/actions)
