"""
Modèles de données pour Nexus Réussite
Architecture SQLAlchemy optimisée pour production
"""

# Classes de base
from .base import AuditMixin, BaseModel, SoftDeleteMixin, TimestampMixin

# Modèles système de contenu
from .content_system import (
    BrickType,
    ContentBrick,
    ContentBrickRating,
    ContentTemplate,
    DocumentBrick,
    DocumentInteraction,
    DocumentRequest,
    GeneratedDocument,
    LearningStep,
    Subject,
    TargetProfile,
)

# Modèles formules et cours
from .formulas import (
    Availability,
    Booking,
    BookingStatus,
    Enrollment,
    Formula,
    FormulaLevel,
    FormulaType,
    Group,
    GroupSession,
    IndividualSession,
    Location,
    ParentCommunication,
    SessionAttendance,
    SessionFormat,
    SessionReport,
    StudentObjective,
    Teacher,
    WeeklyReport,
)

# Modèles étudiant
from .student import ARIAInteraction, Assessment, LearningSession, Student

# Modèles utilisateur
from .user import (
    AcademicLevel,
    AdminProfile,
    LearningStyle,
    ParentChildRelation,
    ParentProfile,
    StudentProfile,
    TeacherProfile,
    User,
    UserRole,
    UserSession,
    UserStatus,
    create_user_with_profile,
)

# Exports principaux
__all__ = [
    # Classes de base
    "BaseModel",
    "TimestampMixin",
    "SoftDeleteMixin",
    "AuditMixin",
    # Modèles utilisateur
    "User",
    "UserRole",
    "UserStatus",
    "LearningStyle",
    "AcademicLevel",
    "StudentProfile",
    "ParentProfile",
    "TeacherProfile",
    "AdminProfile",
    "UserSession",
    "ParentChildRelation",
    "create_user_with_profile",
    # Modèles étudiant
    "Student",
    "LearningSession",
    "Assessment",
    "ARIAInteraction",
    # Modèles formules et cours
    "Formula",
    "FormulaType",
    "FormulaLevel",
    "SessionFormat",
    "BookingStatus",
    "Location",
    "Availability",
    "Booking",
    "SessionReport",
    "Group",
    "Teacher",
    "Enrollment",
    "IndividualSession",
    "GroupSession",
    "SessionAttendance",
    "WeeklyReport",
    "ParentCommunication",
    "StudentObjective",
    # Modèles système de contenu
    "ContentBrick",
    "DocumentRequest",
    "GeneratedDocument",
    "DocumentBrick",
    "ContentBrickRating",
    "DocumentInteraction",
    "ContentTemplate",
    "BrickType",
    "Subject",
    "TargetProfile",
    "LearningStep",
]
