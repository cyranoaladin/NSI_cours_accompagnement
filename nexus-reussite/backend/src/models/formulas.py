from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from ..database import db
from .base import BaseModel, SoftDeleteMixin


class FormulaType(Enum):
    INDIVIDUAL = "individual"
    GROUP = "group"
    WORKSHOP = "workshop"
    INTENSIVE = "intensive"


class FormulaLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class SessionFormat(Enum):
    ONLINE = "online"
    IN_PERSON = "in_person"
    HYBRID = "hybrid"


class BookingStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


# ================================
# MODÈLES EXISTANTS AMÉLIORÉS
# ================================


class Formula(db.Model):
    __tablename__ = "formulas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(FormulaType), nullable=False)
    level = db.Column(db.Enum(FormulaLevel), nullable=False)
    price_dt = db.Column(db.Float, nullable=False)
    hours_per_month = db.Column(db.Integer, nullable=False)
    max_students = db.Column(db.Integer, nullable=True)  # Pour les groupes
    description = db.Column(db.Text)
    features = db.Column(db.JSON)  # Liste des fonctionnalités
    supports_online = db.Column(db.Boolean, default=True)
    supports_in_person = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relations
    enrollments = db.relationship("Enrollment", backref="formula", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "level": self.level.value,
            "price_dt": self.price_dt,
            "hours_per_month": self.hours_per_month,
            "max_students": self.max_students,
            "description": self.description,
            "features": self.features,
            "supports_online": self.supports_online,
            "supports_in_person": self.supports_in_person,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# ================================
# NOUVEAUX MODÈLES POUR LE SYSTÈME HYBRIDE
# ================================


class Location(db.Model):
    """Modèle pour les salles/lieux de cours en présentiel"""

    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100), nullable=False
    )  # Ex: "Salle Alpha", "Laboratoire NSI"
    capacity = db.Column(db.Integer, nullable=False, default=1)  # Nombre max d'élèves
    address = db.Column(
        db.String(200), nullable=True
    )  # Adresse si différente du centre principal
    equipment = db.Column(db.JSON, nullable=True)  # Équipements disponibles
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relations
    bookings = db.relationship("Booking", backref="location", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "address": self.address,
            "equipment": self.equipment,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Availability(db.Model):
    """Modèle pour les disponibilités des enseignants"""

    __tablename__ = "availabilities"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_for_in_person = db.Column(
        db.Boolean, nullable=False
    )  # True = présentiel, False = en ligne
    is_recurring = db.Column(
        db.Boolean, default=False
    )  # Si c'est une récurrence hebdomadaire
    recurring_pattern = db.Column(db.JSON, nullable=True)  # Pattern de récurrence
    is_booked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "is_for_in_person": self.is_for_in_person,
            "is_recurring": self.is_recurring,
            "recurring_pattern": self.recurring_pattern,
            "is_booked": self.is_booked,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Booking(db.Model):
    """Modèle pour les réservations de cours (hybrides)"""

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    availability_id = db.Column(
        db.Integer, db.ForeignKey("availabilities.id"), nullable=True
    )

    # Informations de la session
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    format = db.Column(
        db.Enum(SessionFormat), nullable=False
    )  # ONLINE, IN_PERSON, HYBRID
    location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=True
    )  # Obligatoire si IN_PERSON

    # Détails du cours
    subject = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    duration_minutes = db.Column(db.Integer, default=60)

    # Statut et suivi
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.PENDING)
    booking_notes = db.Column(db.Text, nullable=True)  # Notes lors de la réservation
    cancellation_reason = db.Column(db.String(200), nullable=True)

    # URLs pour les cours en ligne
    meeting_url = db.Column(db.String(500), nullable=True)  # Lien Zoom/Meet
    meeting_password = db.Column(db.String(50), nullable=True)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_by = db.Column(db.String(50), default="student")  # student, teacher, admin

    # Relations
    session_report = db.relationship(
        "SessionReport", backref="booking", uselist=False, lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "teacher_id": self.teacher_id,
            "availability_id": self.availability_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "format": self.format.value,
            "location_id": self.location_id,
            "subject": self.subject,
            "topic": self.topic,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "status": self.status.value,
            "booking_notes": self.booking_notes,
            "cancellation_reason": self.cancellation_reason,
            "meeting_url": self.meeting_url,
            "meeting_password": self.meeting_password,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
        }


class SessionReport(db.Model):
    """Rapport de session après un cours"""

    __tablename__ = "session_reports"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)

    # Contenu du rapport
    topics_covered = db.Column(db.JSON)  # Liste des sujets abordés
    student_performance = db.Column(db.Integer)  # Note sur 20
    participation_level = db.Column(db.String(20))  # high, medium, low
    comprehension_level = db.Column(db.String(20))  # excellent, good, needs_work

    # Notes et recommandations
    teacher_notes = db.Column(db.Text)
    homework_assigned = db.Column(db.Text)
    next_session_recommendations = db.Column(db.Text)
    parent_feedback_requested = db.Column(db.Boolean, default=False)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "topics_covered": self.topics_covered,
            "student_performance": self.student_performance,
            "participation_level": self.participation_level,
            "comprehension_level": self.comprehension_level,
            "teacher_notes": self.teacher_notes,
            "homework_assigned": self.homework_assigned,
            "next_session_recommendations": self.next_session_recommendations,
            "parent_feedback_requested": self.parent_feedback_requested,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "teacher_id": self.teacher_id,
        }


# ================================
# MODÈLES EXISTANTS (inchangés mais ajout des relations)
# ================================


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)  # Seconde, Première, Terminale
    max_students = db.Column(db.Integer, default=6)
    current_students = db.Column(db.Integer, default=0)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    default_location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=True
    )
    supports_online = db.Column(db.Boolean, default=True)
    schedule = db.Column(db.JSON)  # Horaires des cours
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    enrollments = db.relationship("Enrollment", backref="group", lazy=True)
    sessions = db.relationship("GroupSession", backref="group", lazy=True)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    subjects = db.Column(db.JSON)  # Liste des matières enseignées
    qualifications = db.Column(db.JSON)  # Certifications, diplômes
    experience_years = db.Column(db.Integer)
    is_aefe_certified = db.Column(db.Boolean, default=False)
    is_nsi_diu = db.Column(db.Boolean, default=False)
    can_teach_online = db.Column(db.Boolean, default=True)
    can_teach_in_person = db.Column(db.Boolean, default=True)
    hourly_rate_online = db.Column(db.Float, nullable=True)
    hourly_rate_in_person = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    groups = db.relationship("Group", backref="teacher", lazy=True)
    individual_sessions = db.relationship(
        "IndividualSession", backref="teacher", lazy=True
    )
    availabilities = db.relationship("Availability", backref="teacher", lazy=True)
    bookings = db.relationship("Booking", backref="teacher", lazy=True)
    session_reports = db.relationship("SessionReport", backref="teacher", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": f"{self.first_name} {self.last_name}",
            "email": self.email,
            "phone": self.phone,
            "subjects": self.subjects,
            "qualifications": self.qualifications,
            "experience_years": self.experience_years,
            "is_aefe_certified": self.is_aefe_certified,
            "is_nsi_diu": self.is_nsi_diu,
            "can_teach_online": self.can_teach_online,
            "can_teach_in_person": self.can_teach_in_person,
            "hourly_rate_online": self.hourly_rate_online,
            "hourly_rate_in_person": self.hourly_rate_in_person,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    formula_id = db.Column(db.Integer, db.ForeignKey("formulas.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    preferred_format = db.Column(db.Enum(SessionFormat), default=SessionFormat.HYBRID)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class IndividualSession(db.Model):
    __tablename__ = "individual_sessions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    format = db.Column(db.Enum(SessionFormat), default=SessionFormat.ONLINE)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=True)
    status = db.Column(
        db.String(20), default="scheduled"
    )  # scheduled, completed, cancelled
    topics_covered = db.Column(db.JSON)
    homework_assigned = db.Column(db.Text)
    teacher_notes = db.Column(db.Text)
    student_performance = db.Column(db.Integer)  # Note sur 20
    meeting_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GroupSession(db.Model):
    __tablename__ = "group_sessions"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=90)
    format = db.Column(db.Enum(SessionFormat), default=SessionFormat.IN_PERSON)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=True)
    status = db.Column(db.String(20), default="scheduled")
    topics_covered = db.Column(db.JSON)
    homework_assigned = db.Column(db.Text)
    teacher_notes = db.Column(db.Text)
    meeting_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    attendances = db.relationship("SessionAttendance", backref="session", lazy=True)


class SessionAttendance(db.Model):
    __tablename__ = "session_attendances"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer, db.ForeignKey("group_sessions.id"), nullable=False
    )
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    is_present = db.Column(db.Boolean, default=True)
    participation_score = db.Column(db.Integer)  # Note de participation sur 20
    individual_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WeeklyReport(db.Model):
    __tablename__ = "weekly_reports"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)
    week_end_date = db.Column(db.Date, nullable=False)
    subjects_progress = db.Column(db.JSON)  # Progression par matière
    aria_insights = db.Column(db.Text)
    teacher_comments = db.Column(db.JSON)  # Commentaires par enseignant
    next_week_objectives = db.Column(db.JSON)
    parent_feedback = db.Column(db.Text)
    is_sent_to_parents = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ParentCommunication(db.Model):
    __tablename__ = "parent_communications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    sender_type = db.Column(db.String(20), nullable=False)  # teacher, parent, admin
    sender_id = db.Column(db.Integer, nullable=False)
    recipient_type = db.Column(db.String(20), nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default="normal")  # low, normal, high, urgent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentObjective(db.Model):
    __tablename__ = "student_objectives"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    objective_text = db.Column(db.Text, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    is_achieved = db.Column(db.Boolean, default=False)
    achievement_date = db.Column(db.Date, nullable=True)
    progress_percentage = db.Column(db.Integer, default=0)
    created_by = db.Column(db.String(50), nullable=False)  # teacher, aria, parent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
