"""
Service de visioconférence intégré pour Nexus Réussite
Utilise Jitsi Meet pour les sessions de cours en ligne
"""

import base64
import hashlib
import hmac
import json
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import requests


class ConferenceStatus(Enum):
    """États d'une conférence"""

    SCHEDULED = "scheduled"
    ACTIVE = "active"
    ENDED = "ended"
    CANCELLED = "cancelled"


class ParticipantRole(Enum):
    """Rôles des participants"""

    MODERATOR = "moderator"
    PARTICIPANT = "participant"
    OBSERVER = "observer"


@dataclass
class ConferenceParticipant:
    """Participant à une conférence"""

    user_id: str
    name: str
    email: str
    role: ParticipantRole
    avatar_url: Optional[str] = None
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None
    duration: Optional[int] = None  # en secondes


@dataclass
class ConferenceRoom:
    """Salle de conférence"""

    room_id: str
    room_name: str
    subject: str
    teacher_id: str
    teacher_name: str
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    status: ConferenceStatus = ConferenceStatus.SCHEDULED
    participants: List[ConferenceParticipant] = None
    max_participants: int = 10
    recording_enabled: bool = False
    recording_url: Optional[str] = None
    meeting_password: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self):
        if self.participants is None:
            self.participants = []


class VideoConferenceService:
    """Service de gestion des visioconférences"""

    def __init__(
        self, jitsi_domain: str = "meet.jit.si", app_id: str = "nexus_reussite"
    ):
        self.jitsi_domain = jitsi_domain
        self.app_id = app_id
        self.jwt_secret = "nexus_jitsi_secret_key"  # À configurer en production
        self.active_rooms: Dict[str, ConferenceRoom] = {}
        self.room_history: List[ConferenceRoom] = []

    def generate_room_id(self, teacher_id: str, subject: str) -> str:
        """Génère un ID unique pour une salle"""
        timestamp = int(time.time())
        unique_string = f"{teacher_id}_{subject}_{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]

    def generate_jwt_token(
        self,
        room_name: str,
        user_id: str,
        user_name: str,
        role: ParticipantRole = ParticipantRole.PARTICIPANT,
        avatar_url: str = None,
    ) -> str:
        """Génère un token JWT pour l'authentification Jitsi"""

        # Header JWT
        header = {"alg": "HS256", "typ": "JWT"}

        # Payload JWT
        now = int(time.time())
        payload = {
            "iss": self.app_id,
            "aud": "jitsi",
            "exp": now + 3600,  # Expire dans 1 heure
            "nbf": now - 10,  # Valide depuis 10 secondes avant
            "sub": self.jitsi_domain,
            "room": room_name,
            "context": {
                "user": {
                    "id": user_id,
                    "name": user_name,
                    "email": f"{user_id}@nexusreussite.tn",
                    "avatar": avatar_url
                    or f"https://api.dicebear.com/7.x/initials/svg?seed={user_name}",
                },
                "features": {
                    "livestreaming": role == ParticipantRole.MODERATOR,
                    "recording": role == ParticipantRole.MODERATOR,
                    "transcription": True,
                    "outbound-call": False,
                },
            },
            "moderator": role == ParticipantRole.MODERATOR,
        }

        # Encoder le JWT
        header_encoded = (
            base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        )
        payload_encoded = (
            base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        )

        # Créer la signature
        message = f"{header_encoded}.{payload_encoded}"
        signature = hmac.new(
            self.jwt_secret.encode(), message.encode(), hashlib.sha256
        ).digest()
        signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")

        return f"{message}.{signature_encoded}"

    def create_conference_room(
        self,
        teacher_id: str,
        teacher_name: str,
        subject: str,
        scheduled_start: datetime,
        duration_minutes: int = 60,
        max_participants: int = 10,
        description: str = None,
    ) -> ConferenceRoom:
        """Crée une nouvelle salle de conférence"""

        room_id = self.generate_room_id(teacher_id, subject)
        room_name = f"nexus_{subject.lower().replace(' ', '_')}_{room_id}"

        scheduled_end = scheduled_start + timedelta(minutes=duration_minutes)

        room = ConferenceRoom(
            room_id=room_id,
            room_name=room_name,
            subject=subject,
            teacher_id=teacher_id,
            teacher_name=teacher_name,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            max_participants=max_participants,
            description=description or f"Cours de {subject} avec {teacher_name}",
        )

        self.active_rooms[room_id] = room
        return room

    def get_conference_url(
        self,
        room: ConferenceRoom,
        user_id: str,
        user_name: str,
        role: ParticipantRole = ParticipantRole.PARTICIPANT,
    ) -> str:
        """Génère l'URL de la conférence pour un utilisateur"""

        # Générer le token JWT
        jwt_token = self.generate_jwt_token(room.room_name, user_id, user_name, role)

        # Paramètres de configuration
        config_params = {
            "jwt": jwt_token,
            "config.startWithAudioMuted": (
                "true" if role != ParticipantRole.MODERATOR else "false"
            ),
            "config.startWithVideoMuted": "false",
            "config.requireDisplayName": "true",
            "config.enableWelcomePage": "false",
            "config.prejoinPageEnabled": "true",
            "config.disableInviteFunctions": (
                "true" if role != ParticipantRole.MODERATOR else "false"
            ),
            "config.toolbarButtons": (
                json.dumps(
                    [
                        "microphone",
                        "camera",
                        "closedcaptions",
                        "desktop",
                        "fullscreen",
                        "fodeviceselection",
                        "hangup",
                        "profile",
                        "chat",
                        "recording",
                        "livestreaming",
                        "etherpad",
                        "sharedvideo",
                        "settings",
                        "raisehand",
                        "videoquality",
                        "filmstrip",
                        "invite",
                        "feedback",
                        "stats",
                        "shortcuts",
                    ]
                )
                if role == ParticipantRole.MODERATOR
                else json.dumps(
                    [
                        "microphone",
                        "camera",
                        "closedcaptions",
                        "fullscreen",
                        "hangup",
                        "profile",
                        "chat",
                        "raisehand",
                        "filmstrip",
                    ]
                )
            ),
        }

        # Interface personnalisée
        interface_config = {
            "BRAND_WATERMARK_LINK": "https://nexusreussite.tn",
            "SHOW_BRAND_WATERMARK": True,
            "SHOW_JITSI_WATERMARK": False,
            "SHOW_POWERED_BY": False,
            "SHOW_PROMOTIONAL_CLOSE_PAGE": False,
            "TOOLBAR_BUTTONS": config_params["config.toolbarButtons"],
            "SETTINGS_SECTIONS": [
                "devices",
                "language",
                "moderator",
                "profile",
                "calendar",
            ],
            "VIDEO_LAYOUT_FIT": "both",
            "filmStripOnly": False,
            "VERTICAL_FILMSTRIP": True,
        }

        # Construire l'URL
        base_url = f"https://{self.jitsi_domain}/{room.room_name}"
        params = {**config_params, "interfaceConfig": json.dumps(interface_config)}

        return f"{base_url}#{urlencode(params)}"

    def join_conference(
        self,
        room_id: str,
        user_id: str,
        user_name: str,
        user_email: str,
        role: ParticipantRole = ParticipantRole.PARTICIPANT,
    ) -> Dict[str, Any]:
        """Fait rejoindre un utilisateur à une conférence"""

        if room_id not in self.active_rooms:
            return {"success": False, "error": "Salle de conférence non trouvée"}

        room = self.active_rooms[room_id]

        # Vérifier si la salle n'est pas pleine
        if len(room.participants) >= room.max_participants:
            return {"success": False, "error": "Salle de conférence pleine"}

        # Vérifier si l'utilisateur n'est pas déjà dans la salle
        existing_participant = next(
            (p for p in room.participants if p.user_id == user_id), None
        )

        if existing_participant:
            # Mettre à jour l'heure de connexion
            existing_participant.joined_at = datetime.utcnow()
        else:
            # Ajouter le nouveau participant
            participant = ConferenceParticipant(
                user_id=user_id,
                name=user_name,
                email=user_email,
                role=role,
                joined_at=datetime.utcnow(),
            )
            room.participants.append(participant)

        # Démarrer la conférence si c'est le premier participant
        if room.status == ConferenceStatus.SCHEDULED and len(room.participants) == 1:
            room.status = ConferenceStatus.ACTIVE
            room.actual_start = datetime.utcnow()

        # Générer l'URL de la conférence
        conference_url = self.get_conference_url(room, user_id, user_name, role)

        return {
            "success": True,
            "conference_url": conference_url,
            "room_info": {
                "room_id": room.room_id,
                "subject": room.subject,
                "teacher_name": room.teacher_name,
                "participants_count": len(room.participants),
                "max_participants": room.max_participants,
                "status": room.status.value,
            },
        }

    def leave_conference(self, room_id: str, user_id: str) -> Dict[str, Any]:
        """Fait quitter un utilisateur d'une conférence"""

        if room_id not in self.active_rooms:
            return {"success": False, "error": "Salle de conférence non trouvée"}

        room = self.active_rooms[room_id]

        # Trouver le participant
        participant = next((p for p in room.participants if p.user_id == user_id), None)

        if not participant:
            return {"success": False, "error": "Participant non trouvé dans la salle"}

        # Mettre à jour les informations de départ
        participant.left_at = datetime.utcnow()
        if participant.joined_at:
            participant.duration = int(
                (participant.left_at - participant.joined_at).total_seconds()
            )

        # Retirer le participant de la liste active
        room.participants = [p for p in room.participants if p.user_id != user_id]

        # Terminer la conférence si plus de participants
        if len(room.participants) == 0 and room.status == ConferenceStatus.ACTIVE:
            room.status = ConferenceStatus.ENDED
            room.actual_end = datetime.utcnow()

            # Déplacer vers l'historique
            self.room_history.append(room)
            del self.active_rooms[room_id]

        return {"success": True, "message": "Participant retiré de la conférence"}

    def end_conference(self, room_id: str, teacher_id: str) -> Dict[str, Any]:
        """Termine une conférence (enseignant seulement)"""

        if room_id not in self.active_rooms:
            return {"success": False, "error": "Salle de conférence non trouvée"}

        room = self.active_rooms[room_id]

        # Vérifier que c'est l'enseignant qui termine la conférence
        if room.teacher_id != teacher_id:
            return {
                "success": False,
                "error": "Seul l'enseignant peut terminer la conférence",
            }

        # Terminer la conférence
        room.status = ConferenceStatus.ENDED
        room.actual_end = datetime.utcnow()

        # Mettre à jour tous les participants encore connectés
        for participant in room.participants:
            if not participant.left_at:
                participant.left_at = room.actual_end
                if participant.joined_at:
                    participant.duration = int(
                        (participant.left_at - participant.joined_at).total_seconds()
                    )

        # Déplacer vers l'historique
        self.room_history.append(room)
        del self.active_rooms[room_id]

        return {
            "success": True,
            "message": "Conférence terminée",
            "duration": (
                int((room.actual_end - room.actual_start).total_seconds())
                if room.actual_start
                else 0
            ),
            "participants_count": len(room.participants),
        }

    def get_room_info(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Récupère les informations d'une salle"""

        room = self.active_rooms.get(room_id)
        if not room:
            # Chercher dans l'historique
            room = next((r for r in self.room_history if r.room_id == room_id), None)

        if not room:
            return None

        return {
            "room_id": room.room_id,
            "subject": room.subject,
            "teacher_id": room.teacher_id,
            "teacher_name": room.teacher_name,
            "scheduled_start": room.scheduled_start.isoformat(),
            "scheduled_end": room.scheduled_end.isoformat(),
            "actual_start": (
                room.actual_start.isoformat() if room.actual_start else None
            ),
            "actual_end": room.actual_end.isoformat() if room.actual_end else None,
            "status": room.status.value,
            "participants_count": len(room.participants),
            "max_participants": room.max_participants,
            "description": room.description,
            "recording_enabled": room.recording_enabled,
            "recording_url": room.recording_url,
            "participants": [
                {
                    "user_id": p.user_id,
                    "name": p.name,
                    "role": p.role.value,
                    "joined_at": p.joined_at.isoformat() if p.joined_at else None,
                    "left_at": p.left_at.isoformat() if p.left_at else None,
                    "duration": p.duration,
                }
                for p in room.participants
            ],
        }

    def get_teacher_rooms(
        self, teacher_id: str, include_history: bool = False
    ) -> List[Dict[str, Any]]:
        """Récupère les salles d'un enseignant"""

        rooms = []

        # Salles actives
        for room in self.active_rooms.values():
            if room.teacher_id == teacher_id:
                rooms.append(self.get_room_info(room.room_id))

        # Historique si demandé
        if include_history:
            for room in self.room_history:
                if room.teacher_id == teacher_id:
                    rooms.append(self.get_room_info(room.room_id))

        # Trier par date de début
        rooms.sort(key=lambda x: x["scheduled_start"], reverse=True)

        return rooms

    def get_student_rooms(self, student_id: str) -> List[Dict[str, Any]]:
        """Récupère les salles auxquelles un élève peut accéder"""

        rooms = []

        # Récupérer les salles auxquelles l'élève est inscrit
        try:
            from src.models.enrollment import Enrollment

            enrollments = Enrollment.query.filter_by(student_id=student_id).all()
            enrolled_subjects = [e.subject for e in enrollments]

            for room in self.active_rooms.values():
                # Vérifier si l'élève est inscrit à cette matière
                if room.subject.lower() in [s.lower() for s in enrolled_subjects]:
                    room_info = self.get_room_info(room.room_id)
                    # Masquer certaines informations sensibles pour les élèves
                    room_info.pop("recording_url", None)
                    rooms.append(room_info)
        except ImportError:
            # Fallback: retourner toutes les salles actives si le modèle n'existe pas
            current_app.logger.warning(
                "Modèle Enrollment non trouvé, retour de toutes les salles"
            )
            for room in self.active_rooms.values():
                room_info = self.get_room_info(room.room_id)
                room_info.pop("recording_url", None)
                rooms.append(room_info)

        return rooms

    def schedule_recurring_conference(
        self,
        teacher_id: str,
        teacher_name: str,
        subject: str,
        start_time: datetime,
        duration_minutes: int,
        recurrence_days: List[int],
        end_date: datetime,
    ) -> List[ConferenceRoom]:
        """Programme des conférences récurrentes"""

        scheduled_rooms = []
        current_date = start_time.date()

        while current_date <= end_date.date():
            if current_date.weekday() in recurrence_days:
                scheduled_start = datetime.combine(current_date, start_time.time())

                room = self.create_conference_room(
                    teacher_id=teacher_id,
                    teacher_name=teacher_name,
                    subject=subject,
                    scheduled_start=scheduled_start,
                    duration_minutes=duration_minutes,
                    description=f"Cours récurrent de {subject} avec {teacher_name}",
                )

                scheduled_rooms.append(room)

            current_date += timedelta(days=1)

        return scheduled_rooms

    def get_conference_statistics(self, teacher_id: str = None) -> Dict[str, Any]:
        """Récupère les statistiques des conférences"""

        stats = {
            "total_conferences": len(self.room_history),
            "active_conferences": len(self.active_rooms),
            "total_participants": 0,
            "average_duration": 0,
            "conferences_by_subject": {},
            "participants_by_role": {"moderator": 0, "participant": 0, "observer": 0},
        }

        # Filtrer par enseignant si spécifié
        rooms_to_analyze = self.room_history
        if teacher_id:
            rooms_to_analyze = [
                r for r in self.room_history if r.teacher_id == teacher_id
            ]
            stats["total_conferences"] = len(rooms_to_analyze)

        total_duration = 0
        conference_count = 0

        for room in rooms_to_analyze:
            # Compter les participants
            stats["total_participants"] += len(room.participants)

            # Durée moyenne
            if room.actual_start and room.actual_end:
                duration = (room.actual_end - room.actual_start).total_seconds()
                total_duration += duration
                conference_count += 1

            # Par matière
            subject = room.subject
            if subject not in stats["conferences_by_subject"]:
                stats["conferences_by_subject"][subject] = 0
            stats["conferences_by_subject"][subject] += 1

            # Par rôle
            for participant in room.participants:
                role = participant.role.value
                stats["participants_by_role"][role] += 1

        # Calculer la durée moyenne
        if conference_count > 0:
            stats["average_duration"] = int(total_duration / conference_count)

        return stats


# Instance globale du service
video_conference_service = VideoConferenceService()

# Fonctions utilitaires


def create_instant_meeting(
    teacher_id: str, teacher_name: str, subject: str
) -> Dict[str, Any]:
    """Crée une réunion instantanée"""

    start_time = datetime.utcnow()
    room = video_conference_service.create_conference_room(
        teacher_id=teacher_id,
        teacher_name=teacher_name,
        subject=subject,
        scheduled_start=start_time,
        duration_minutes=120,  # 2 heures par défaut
        description=f"Réunion instantanée - {subject}",
    )

    return {
        "success": True,
        "room_id": room.room_id,
        "room_info": video_conference_service.get_room_info(room.room_id),
    }


def get_meeting_link(
    room_id: str, user_id: str, user_name: str, is_teacher: bool = False
) -> str:
    """Génère un lien de réunion pour un utilisateur"""

    role = ParticipantRole.MODERATOR if is_teacher else ParticipantRole.PARTICIPANT
    result = video_conference_service.join_conference(
        room_id, user_id, user_name, f"{user_id}@nexusreussite.tn", role
    )

    if result["success"]:
        return result["conference_url"]
    else:
        return None
