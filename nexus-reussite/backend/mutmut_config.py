"""
Mutation testing configuration for Nexus Réussite Backend.
"""

import os


def pre_mutation(context):
    """
    Pre-mutation hook to prepare test environment.
    """
    # Set test environment variables
    os.environ["TESTING"] = "True"
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["JWT_SECRET_KEY"] = "test-jwt-secret"
    os.environ["OPENAI_API_KEY"] = "test-openai-key"


def post_mutation(context, result):
    """
    Post-mutation hook to clean up after testing.
    """
    # Clean up any test artifacts if needed
    pass


# Configuration for mutmut
MUTMUT_CONFIG = {
    "paths_to_mutate": [
        "src/services/",
        "src/models/",
        "src/utils/",
        "src/routes/",
    ],
    "paths_to_exclude": [
        "src/migrations/",
        "tests/",
        "conftest.py",
        "__pycache__/",
        ".venv/",
    ],
    "backup": False,
    "runner": "python -m pytest tests/ -x --tb=no -q",
    "tests_dir": "tests/",
    "coverage_threshold": 90,
    "timeout": 120,  # 2 minutes per test
}
