"""
Base models and mixins for Nexus Réussite
Common functionality shared across all models
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy.ext.declarative import declared_attr

from database import db


class TimestampMixin:
    """Mixin pour ajouter les timestamps created_at et updated_at"""

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(cls):
        return db.Column(
            db.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )


class BaseModel(db.Model, TimestampMixin):
    """Modèle de base avec fonctionnalités communes"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self, include_relations=False) -> Dict[str, Any]:
        """
        Convertit le modèle en dictionnaire

        Args:
            include_relations: Si True, inclut les relations
        """
        result = {}

        # Colonnes de base
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value

        # Relations si demandées
        if include_relations:
            for relation in self.__mapper__.relationships:
                value = getattr(self, relation.key)
                if value is not None:
                    if hasattr(value, "__iter__") and not isinstance(value, str):
                        # Collection
                        result[relation.key] = [
                            item.to_dict() if hasattr(item, "to_dict") else str(item)
                            for item in value
                        ]
                    else:
                        # Single object
                        result[relation.key] = (
                            value.to_dict() if hasattr(value, "to_dict") else str(value)
                        )
                else:
                    result[relation.key] = None

        return result

    def update_from_dict(self, data: Dict[str, Any], exclude_fields=None):
        """
        Met à jour le modèle à partir d'un dictionnaire

        Args:
            data: Dictionnaire avec les nouvelles valeurs
            exclude_fields: Liste des champs à exclure
        """
        if exclude_fields is None:
            exclude_fields = ["id", "created_at"]

        for key, value in data.items():
            if key not in exclude_fields and hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = datetime.utcnow()

    @classmethod
    def get_by_id(cls, model_id: int):
        """Récupère un objet par son ID"""
        return cls.query.get(model_id)

    @classmethod
    def get_or_404(cls, model_id: int):
        """Récupère un objet par son ID ou lève une erreur 404"""
        return cls.query.get_or_404(model_id)

    def save(self):
        """Sauvegarde l'objet dans la base de données"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Supprime l'objet de la base de données"""
        db.session.delete(self)
        db.session.commit()


class SoftDeleteMixin:
    """Mixin pour la suppression logique"""

    @declared_attr
    def is_deleted(cls):
        return db.Column(db.Boolean, default=False, nullable=False)

    @declared_attr
    def deleted_at(cls):
        return db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        """Suppression logique"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def restore(self):
        """Restauration après suppression logique"""
        self.is_deleted = False
        self.deleted_at = None
        db.session.commit()


class AuditMixin:
    """Mixin pour l'audit des modifications"""

    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, nullable=True)

    @declared_attr
    def updated_by(cls):
        return db.Column(db.Integer, nullable=True)

    def set_audit_fields(self, user_id: int, is_creation=False):
        """Définit les champs d'audit"""
        if is_creation:
            self.created_by = user_id
        self.updated_by = user_id
