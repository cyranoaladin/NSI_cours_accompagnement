"""
Modèle utilisateur pour la plateforme NSI
"""
from datetime import datetime
from enum import Enum

from werkzeug.security import generate_password_hash, check_password_hash

from ..database import db


class UserRole(Enum):
    """Énumération des rôles utilisateur"""
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"


class UserStatus(Enum):
    """Énumération des statuts utilisateur"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"

class User(db.Model):
    """Modèle utilisateur unifié pour tous les types d'utilisateurs"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Informations personnelles
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)

    # Rôle et statut
    role = db.Column(db.Enum(UserRole), nullable=False)
    status = db.Column(db.Enum(UserStatus), default=UserStatus.ACTIVE)

    # Métadonnées
    last_login = db.Column(db.DateTime, nullable=True)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100), nullable=True)
    password_reset_token = db.Column(db.String(100), nullable=True)
    password_reset_expires = db.Column(db.DateTime, nullable=True)

    # Préférences utilisateur
    preferences = db.Column(db.JSON, nullable=True)  # Préférences UI, notifications, etc.
    timezone = db.Column(db.String(50), default='Africa/Tunis')
    language = db.Column(db.String(5), default='fr')

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations selon le rôle
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, lazy=True,
                                    cascade='all, delete-orphan')
    parent_profile = db.relationship('ParentProfile', backref='user', uselist=False, lazy=True,
                                   cascade='all, delete-orphan')
    teacher_profile = db.relationship('TeacherProfile', backref='user', uselist=False, lazy=True,
                                    cascade='all, delete-orphan')
    admin_profile = db.relationship('AdminProfile', backref='user', uselist=False, lazy=True,
                                  cascade='all, delete-orphan')

    # Sessions et tokens
    user_sessions = db.relationship('UserSession', backref='user', lazy=True,
                                  cascade='all, delete-orphan')

    def __init__(self, email, password, first_name, last_name, role, **kwargs):
        self.email = email.lower().strip()
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role if isinstance(role, UserRole) else UserRole(role)

        # Champs optionnels
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_password(self, password):
        """Définit le mot de passe haché"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        """Retourne le nom complet"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        """Vérifie si l'utilisateur est actif"""
        return self.status == UserStatus.ACTIVE

    def to_dict(self, include_sensitive=False):  # pylint: disable=unused-argument
        """Convertit l'utilisateur en dictionnaire"""
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'avatar_url': self.avatar_url,
            'role': self.role.value,
            'status': self.status.value if self.status else 'active',
            'email_verified': self.email_verified,
            'preferences': self.preferences,
            'timezone': self.timezone,
            'language': self.language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

        # Ajouter le profil spécifique selon le rôle
        if self.role == UserRole.STUDENT and self.student_profile:
            data['profile'] = self.student_profile.to_dict()
        elif self.role == UserRole.PARENT and self.parent_profile:
            data['profile'] = self.parent_profile.to_dict()
        elif self.role == UserRole.TEACHER and self.teacher_profile:
            data['profile'] = self.teacher_profile.to_dict()
        elif self.role == UserRole.ADMIN and self.admin_profile:
            data['profile'] = self.admin_profile.to_dict()

        return data

class StudentProfile(db.Model):
    """Profil spécifique pour les étudiants"""
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Informations académiques
    grade_level = db.Column(db.String(20), nullable=False)  # seconde, premiere, terminale
    school = db.Column(db.String(100), nullable=True)
    specialties = db.Column(db.JSON, nullable=True)  # Spécialités choisies

    # Profil d'apprentissage ARIA
    learning_style = db.Column(db.String(50), nullable=True)  # visual, auditory, kinesthetic, mixed
    cognitive_profile = db.Column(db.JSON, nullable=True)  # Profil cognitif détaillé
    performance_data = db.Column(db.JSON, nullable=True)  # Historique de performance

    # Objectifs et motivation
    goals = db.Column(db.JSON, nullable=True)  # Objectifs scolaires et de carrière
    interests = db.Column(db.JSON, nullable=True)  # Centres d'intérêt
    motivation_level = db.Column(db.String(20), default='medium')  # low, medium, high

    # Relations avec les parents
    parent_ids = db.Column(db.JSON, nullable=True)  # IDs des parents liés

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convertit le profil étudiant en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'grade_level': self.grade_level,
            'school': self.school,
            'specialties': self.specialties,
            'learning_style': self.learning_style,
            'cognitive_profile': self.cognitive_profile,
            'performance_data': self.performance_data,
            'goals': self.goals,
            'interests': self.interests,
            'motivation_level': self.motivation_level,
            'parent_ids': self.parent_ids,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ParentProfile(db.Model):
    """Profil spécifique pour les parents"""
    __tablename__ = 'parent_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Informations personnelles
    profession = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    emergency_contact = db.Column(db.String(20), nullable=True)

    # Relations avec les enfants
    children_ids = db.Column(db.JSON, nullable=True)  # IDs des enfants suivis

    # Préférences de communication
    preferred_contact_method = db.Column(db.String(20), default='email')  # email, phone, sms
    notification_preferences = db.Column(db.JSON, nullable=True)
    report_frequency = db.Column(db.String(20), default='weekly')  # daily, weekly, monthly

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convertit le profil parent en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'profession': self.profession,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'children_ids': self.children_ids,
            'preferred_contact_method': self.preferred_contact_method,
            'notification_preferences': self.notification_preferences,
            'report_frequency': self.report_frequency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TeacherProfile(db.Model):
    """Profil spécifique pour les enseignants"""
    __tablename__ = 'teacher_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Qualifications
    subjects = db.Column(db.JSON, nullable=False)  # Matières enseignées
    qualifications = db.Column(db.JSON, nullable=True)  # Diplômes, certifications
    experience_years = db.Column(db.Integer, nullable=True)
    is_aefe_certified = db.Column(db.Boolean, default=False)
    is_nsi_diu = db.Column(db.Boolean, default=False)

    # Modalités d'enseignement
    can_teach_online = db.Column(db.Boolean, default=True)
    can_teach_in_person = db.Column(db.Boolean, default=True)
    preferred_formats = db.Column(db.JSON, nullable=True)  # Préférences de format

    # Tarification
    hourly_rate_online = db.Column(db.Float, nullable=True)
    hourly_rate_in_person = db.Column(db.Float, nullable=True)
    hourly_rate_group = db.Column(db.Float, nullable=True)

    # Disponibilités par défaut
    default_availability = db.Column(db.JSON, nullable=True)  # Planning récurrent
    max_hours_per_week = db.Column(db.Integer, default=30)

    # Évaluations et statistiques
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    total_hours_taught = db.Column(db.Integer, default=0)

    # Bio et présentation
    bio = db.Column(db.Text, nullable=True)
    specialties_description = db.Column(db.Text, nullable=True)

    # Métadonnées
    hire_date = db.Column(db.Date, nullable=True)
    is_active_teacher = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convertit le profil enseignant en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subjects': self.subjects,
            'qualifications': self.qualifications,
            'experience_years': self.experience_years,
            'is_aefe_certified': self.is_aefe_certified,
            'is_nsi_diu': self.is_nsi_diu,
            'can_teach_online': self.can_teach_online,
            'can_teach_in_person': self.can_teach_in_person,
            'preferred_formats': self.preferred_formats,
            'hourly_rate_online': self.hourly_rate_online,
            'hourly_rate_in_person': self.hourly_rate_in_person,
            'hourly_rate_group': self.hourly_rate_group,
            'default_availability': self.default_availability,
            'max_hours_per_week': self.max_hours_per_week,
            'rating': self.rating,
            'total_reviews': self.total_reviews,
            'total_hours_taught': self.total_hours_taught,
            'bio': self.bio,
            'specialties_description': self.specialties_description,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'is_active_teacher': self.is_active_teacher,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AdminProfile(db.Model):
    """Profil spécifique pour les administrateurs"""
    __tablename__ = 'admin_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Permissions et rôles
    permissions = db.Column(db.JSON, nullable=True)  # Permissions spécifiques
    department = db.Column(db.String(50), nullable=True)  # Service de rattachement
    is_super_admin = db.Column(db.Boolean, default=False)

    # Accès et sécurité
    can_manage_users = db.Column(db.Boolean, default=False)
    can_manage_content = db.Column(db.Boolean, default=False)
    can_view_reports = db.Column(db.Boolean, default=True)
    can_manage_billing = db.Column(db.Boolean, default=False)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convertit le profil administrateur en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'permissions': self.permissions,
            'department': self.department,
            'is_super_admin': self.is_super_admin,
            'can_manage_users': self.can_manage_users,
            'can_manage_content': self.can_manage_content,
            'can_view_reports': self.can_view_reports,
            'can_manage_billing': self.can_manage_billing,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UserSession(db.Model):
    """Sessions utilisateur pour la gestion des tokens JWT"""
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Informations de session
    session_token = db.Column(db.String(255), nullable=False, unique=True)
    refresh_token = db.Column(db.String(255), nullable=True, unique=True)
    expires_at = db.Column(db.DateTime, nullable=False)

    # Informations de connexion
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 compatible
    user_agent = db.Column(db.String(500), nullable=True)
    device_type = db.Column(db.String(50), nullable=True)  # web, mobile, tablet
    location = db.Column(db.String(100), nullable=True)  # Ville/Pays approximatif

    # Statut
    is_active = db.Column(db.Boolean, default=True)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convertit la session utilisateur en dictionnaire"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'device_type': self.device_type,
            'location': self.location,
            'is_active': self.is_active,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ParentChildRelation(db.Model):
    """Table de liaison entre parents et enfants"""
    __tablename__ = 'parent_child_relations'

    id = db.Column(db.Integer, primary_key=True)
    parent_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    child_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Type de relation
    # parent, guardian, tutor
    relation_type = db.Column(db.String(20), default='parent')
    is_primary_contact = db.Column(db.Boolean, default=False)
    can_view_grades = db.Column(db.Boolean, default=True)
    can_book_sessions = db.Column(db.Boolean, default=True)
    can_receive_reports = db.Column(db.Boolean, default=True)

    # Métadonnées
    confirmed_at = db.Column(db.DateTime, nullable=True)  # Quand la relation a été confirmée
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Contrainte d'unicité
    __table_args__ = (db.UniqueConstraint('parent_user_id', 'child_user_id',
                                          name='unique_parent_child'),)

    def to_dict(self):
        """Convertit la relation parent-enfant en dictionnaire"""
        return {
            'id': self.id,
            'parent_user_id': self.parent_user_id,
            'child_user_id': self.child_user_id,
            'relation_type': self.relation_type,
            'is_primary_contact': self.is_primary_contact,
            'can_view_grades': self.can_view_grades,
            'can_book_sessions': self.can_book_sessions,
            'can_receive_reports': self.can_receive_reports,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Fonctions utilitaires
def create_user_with_profile(email, password, first_name, last_name, role, profile_data=None):
    """Crée un utilisateur avec son profil spécifique"""

    # Créer l'utilisateur principal
    user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role
    )

    db.session.add(user)
    db.session.flush()  # Pour obtenir l'ID

    # Créer le profil spécifique selon le rôle
    if profile_data is None:
        profile_data = {}

    if role == UserRole.STUDENT:
        profile = StudentProfile(
            user_id=user.id,
            grade_level=profile_data.get('grade_level', 'terminale'),
            school=profile_data.get('school'),
            specialties=profile_data.get('specialties', []),
            learning_style=profile_data.get('learning_style'),
            goals=profile_data.get('goals', []),
            interests=profile_data.get('interests', [])
        )
    elif role == UserRole.PARENT:
        profile = ParentProfile(
            user_id=user.id,
            profession=profile_data.get('profession'),
            address=profile_data.get('address'),
            emergency_contact=profile_data.get('emergency_contact'),
            children_ids=profile_data.get('children_ids', [])
        )
    elif role == UserRole.TEACHER:
        profile = TeacherProfile(
            user_id=user.id,
            subjects=profile_data.get('subjects', []),
            qualifications=profile_data.get('qualifications', []),
            experience_years=profile_data.get('experience_years'),
            is_aefe_certified=profile_data.get('is_aefe_certified', False),
            can_teach_online=profile_data.get('can_teach_online', True),
            can_teach_in_person=profile_data.get('can_teach_in_person', True),
            bio=profile_data.get('bio')
        )
    elif role == UserRole.ADMIN:
        profile = AdminProfile(
            user_id=user.id,
            permissions=profile_data.get('permissions', []),
            department=profile_data.get('department'),
            is_super_admin=profile_data.get('is_super_admin', False)
        )
    else:
        raise ValueError(f"Rôle non supporté: {role}")

    db.session.add(profile)
    return user, profile
