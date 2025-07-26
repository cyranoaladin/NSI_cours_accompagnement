"""
API Documentation Module for Nexus Réussite Backend
Provides Swagger/OpenAPI documentation generation using Flask-RestX
"""

from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

# API Documentation Configuration
API_VERSION = "1.0.0"
API_TITLE = "Nexus Réussite Backend API"
API_DESCRIPTION = """
🎓 **Nexus Réussite Backend API Documentation**

## Overview
Nexus Réussite is an intelligent educational platform leveraging adaptive AI technology. 
This API provides comprehensive services for:
- Student management and authentication
- AI-powered tutoring and content generation  
- Document generation (revision sheets, exercises, reports)
- Video conferencing and real-time collaboration
- Formula and concept management
- Progress tracking and analytics

## Authentication
The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:
```
Authorization: Bearer your_jwt_token_here
```

## Rate Limiting
All endpoints are rate limited:
- **Development**: 200/day, 50/hour, 1/second
- **Production**: 1000/day, 100/hour, 2/second

## Error Handling
The API returns consistent error responses in JSON format:
```json
{
    "error": "Error Type",
    "message": "Human readable error message",
    "code": "ERROR_CODE"
}
```

## Versioning
Current API version: v1.0.0
Base URL: `/api/`

---
*Generated from Flask-RestX Documentation*
"""


def init_api_docs(app: Flask) -> Api:
    """
    Initialize Flask-RestX API documentation

    Args:
        app: Flask application instance

    Returns:
        Api: Configured Flask-RestX API instance
    """

    # Fix for reverse proxy (if behind load balancer)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Configure API documentation
    api = Api(
        app,
        version=API_VERSION,
        title=API_TITLE,
        description=API_DESCRIPTION,
        doc="/api/docs/",  # Swagger UI endpoint
        prefix="/api",  # API prefix
        validate=True,  # Enable request validation
        ordered=True,  # Maintain endpoint order
        catch_all_404s=True,
        # Security definitions
        security="Bearer",
        authorizations={
            "Bearer": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'",
            }
        },
    )

    # Add global tags for organization
    api.add_namespace(create_auth_namespace(), path="/auth")
    api.add_namespace(create_students_namespace(), path="/students")
    api.add_namespace(create_documents_namespace(), path="/documents")
    api.add_namespace(create_formulas_namespace(), path="/formulas")
    api.add_namespace(create_health_namespace(), path="/health")

    return api


def create_auth_namespace():
    """Create authentication endpoints namespace"""
    from flask_restx import Namespace

    auth_ns = Namespace(
        "auth", description="Authentication and user management operations"
    )

    # Define models for documentation
    login_model = auth_ns.model(
        "Login",
        {
            "email": fields.String(
                required=True,
                description="User email address",
                example="student@example.com",
            ),
            "password": fields.String(
                required=True, description="User password", example="password123"
            ),
        },
    )

    token_response = auth_ns.model(
        "TokenResponse",
        {
            "access_token": fields.String(description="JWT access token"),
            "user": fields.Raw(description="User information object"),
            "expires_in": fields.Integer(
                description="Token expiration time in seconds"
            ),
        },
    )

    return auth_ns


def create_students_namespace():
    """Create students management namespace"""
    from flask_restx import Namespace

    students_ns = Namespace(
        "students", description="Student profile and progress management"
    )

    student_model = students_ns.model(
        "Student",
        {
            "id": fields.String(description="Student unique identifier"),
            "name": fields.String(required=True, description="Student full name"),
            "email": fields.String(required=True, description="Student email address"),
            "level": fields.String(
                description="Academic level",
                enum=["6ème", "5ème", "4ème", "3ème", "2nde", "1ère", "Terminale"],
            ),
            "specialties": fields.List(
                fields.String, description="Academic specialties"
            ),
            "created_at": fields.DateTime(description="Account creation date"),
        },
    )

    return students_ns


def create_documents_namespace():
    """Create document generation namespace"""
    from flask_restx import Namespace

    docs_ns = Namespace(
        "documents", description="AI-powered document generation services"
    )

    revision_request = docs_ns.model(
        "RevisionSheetRequest",
        {
            "subject": fields.String(
                required=True, description="Academic subject", example="Mathématiques"
            ),
            "topic": fields.String(
                required=True, description="Specific topic", example="Dérivées"
            ),
            "student_name": fields.String(
                required=True, description="Student name", example="Jean Dupont"
            ),
            "student_level": fields.String(
                description="Academic level", example="Terminale"
            ),
            "learning_style": fields.String(
                description="Learning style preference",
                enum=["visual", "auditory", "kinesthetic", "mixed"],
            ),
        },
    )

    return docs_ns


def create_formulas_namespace():
    """Create formulas management namespace"""
    from flask_restx import Namespace

    formulas_ns = Namespace(
        "formulas", description="Mathematical formulas and concepts database"
    )

    formula_model = formulas_ns.model(
        "Formula",
        {
            "id": fields.String(description="Formula unique identifier"),
            "name": fields.String(required=True, description="Formula name"),
            "latex": fields.String(required=True, description="LaTeX representation"),
            "description": fields.String(description="Formula description"),
            "subject": fields.String(description="Academic subject"),
            "level": fields.String(description="Academic level"),
            "tags": fields.List(fields.String, description="Formula tags"),
        },
    )

    return formulas_ns


def create_health_namespace():
    """Create health monitoring namespace"""
    from flask_restx import Namespace

    health_ns = Namespace(
        "health", description="System health and monitoring endpoints"
    )

    health_response = health_ns.model(
        "HealthResponse",
        {
            "status": fields.String(
                description="Overall system status",
                enum=["healthy", "unhealthy", "degraded"],
            ),
            "timestamp": fields.String(description="Health check timestamp"),
            "version": fields.String(description="Application version"),
            "environment": fields.String(description="Deployment environment"),
            "services": fields.Raw(description="Individual service statuses"),
            "performance": fields.Raw(description="Performance metrics"),
            "resources": fields.Raw(description="System resource usage"),
        },
    )

    return health_ns
