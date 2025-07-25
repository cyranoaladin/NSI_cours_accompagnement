# Nexus Réussite Backend

Nexus Réussite is an intelligent educational platform leveraging adaptive AI technology. This backend repository provides the necessary services for data management, user authentication, video conferencing, AI tutoring capabilities, and more.

## Requirements

- Python 3.9+
- PostgreSQL 13+
- Redis

## Installation

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

## Configuration

Environment variables are used to configure the application. You can specify them in a `.env` file or export them manually:

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

## Code Quality

Uses `black`, `isort`, `flake8`, `pylint` for maintaining code quality.
Run the following command to apply formatting and linting:

```bash
black .
isort .
flake8
```

## Contributing

Contributions are welcome! Please check out the development documentation in `docs/development.md` for more information on contributing and testing.

## License

MIT License. See `LICENSE` file for more information.

---
