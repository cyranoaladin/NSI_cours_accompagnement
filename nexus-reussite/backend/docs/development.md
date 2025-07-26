# Development Documentation

## Architectural Overview

Nexus Réussite Backend consists of multiple microservices that handle different aspects of the platform - authentication, AI services, file management, and live tutoring. Each service is designed to be scalable and maintainable, adhering to best practices in microservice architecture.

### Key Components

- **Auth Service**: Handles user authentication using JWT.
- **AI Service**: Integrates with OpenAI's GPT-4 for adaptive tutoring.
- **File Service**: Manages content storage and delivery.
- **Real-Time Communication**: Leverages WebSockets and Jitsi for real-time video conferencing.

## ADRs (Architectural Decision Records)

The ADRs document significant architectural decisions made during the development of the Nexus Réussite Backend.

### Decision 1: Use of Flask Framework
- Date: YYYY-MM-DD
- Status: Accepted
- Context: Lightweight and flexible requirements for a high level of customization.
- Decision: Utilize Flask for the backend framework.
- Consequences: Increased speed of development, community support.

### Decision 2: PostgreSQL for Relational Database
- Date: YYYY-MM-DD
- Status: Accepted
- Context: Reliable data integrity and support for complex querying.
- Decision: Use PostgreSQL as the primary database.
- Consequences: Ensured data consistency and transactional integrity.

## Testing

Testing is conducted with `pytest` for unit tests and `pytest-asyncio` for asynchronous code testing. A comprehensive suite of tests is maintained in the `tests` directory.

### Running Tests

To run the test suite, execute:

```bash
pytest tests/
```

## Continuous Integration

CI/CD pipelines are set up using GitHub Actions. Refer to `.github/workflows/ci.yml` for configuration details.

## Setting Up Local Development

1. **Initialize Database**: Use `flask db init` and `flask db migrate` for database setup and migrations.
2. **Run Server Locally**: Start the development server using `flask run` to host locally.
3. **Pre-Commit Hooks**: Ensure `pre-commit install` is run to set up hooks for code quality checks.
