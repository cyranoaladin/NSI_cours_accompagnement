"""
Modèles de données pour Nexus Réussite
Architecture SQLAlchemy optimisée pour production
"""

from .user import User, UserRole
from .student import Student, LearningSession, Assessment, ARIAInteraction
from .formulas import Formula, Enrollment, Teacher, Group, Booking
from .content_system import ContentBrick, DocumentRequest, GeneratedDocument, BrickType, Subject

# Exports principaux
__all__ = [
    "User",
    "UserRole",
    "Student",
    "LearningSession",
    "Assessment",
    "ARIAInteraction",
    "Formula",
    "Enrollment",
    "Teacher",
    "Group",
    "Booking",
    "ContentBrick",
    "DocumentRequest",
    "GeneratedDocument",
    "BrickType",
    "Subject"
]
