"""
Service WebSocket pour les notifications en temps réel
Gère les connexions WebSocket et la diffusion de notifications
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import websockets
from websockets.server import WebSocketServerProtocol
import jwt
from functools import wraps

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationType(Enum):
    """Types de notifications supportées"""
    STUDENT_PROGRESS = "student_progress"
    TEACHER_MESSAGE = "teacher_message"
    COURSE_UPDATE = "course_update"
    ARIA_RESPONSE = "aria_response"
    SYSTEM_ALERT = "system_alert"
    PAYMENT_UPDATE = "payment_update"
    SCHEDULE_CHANGE = "schedule_change"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    REMINDER = "reminder"
    EMERGENCY = "emergency"

class UserRole(Enum):
    """Rôles utilisateur pour les notifications"""
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"

@dataclass
class Notification:
    """Structure d'une notification"""
    id: str
    type: NotificationType
    title: str
    message: str
    recipient_id: str
    recipient_role: UserRole
    data: Optional[Dict[str, Any]] = None
    priority: str = "normal"  # low, normal, high, urgent
    timestamp: str = None
    read: bool = False
    expires_at: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la notification en dictionnaire"""
        result = asdict(self)
        result['type'] = self.type.value
        result['recipient_role'] = self.recipient_role.value
        return result

@dataclass
class WebSocketConnection:
    """Représente une connexion WebSocket active"""
    websocket: WebSocketServerProtocol
    user_id: str
    user_role: UserRole
    connected_at: datetime
    last_ping: datetime

class WebSocketService:
    """Service de gestion des WebSockets et notifications"""

    def __init__(self, jwt_secret: str = "nexus_secret_key"):
        self.jwt_secret = jwt_secret
        self.connections: Dict[str, WebSocketConnection] = {}
        self.user_connections: Dict[str, Set[str]] = {}  # user_id -> set of connection_ids
        self.notification_history: List[Notification] = []
        self.running = False

    def authenticate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Authentifie un token JWT"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return payload
        except jwt.InvalidTokenError:
            logger.warning(f"Token JWT invalide: {token}")
            return None

    def generate_connection_id(self, user_id: str) -> str:
        """Génère un ID unique pour une connexion"""
        timestamp = datetime.utcnow().timestamp()
        return f"{user_id}_{int(timestamp * 1000)}"

    async def register_connection(self, websocket: WebSocketServerProtocol, user_id: str, user_role: UserRole) -> str:
        """Enregistre une nouvelle connexion WebSocket"""
        connection_id = self.generate_connection_id(user_id)

        connection = WebSocketConnection(
            websocket=websocket,
            user_id=user_id,
            user_role=user_role,
            connected_at=datetime.utcnow(),
            last_ping=datetime.utcnow()
        )

        self.connections[connection_id] = connection

        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(connection_id)

        logger.info(f"Nouvelle connexion WebSocket: {connection_id} pour {user_id} ({user_role.value})")

        # Envoyer les notifications non lues
        await self.send_unread_notifications(user_id, user_role)

        return connection_id

    async def unregister_connection(self, connection_id: str):
        """Désenregistre une connexion WebSocket"""
        if connection_id in self.connections:
            connection = self.connections[connection_id]
            user_id = connection.user_id

            del self.connections[connection_id]

            if user_id in self.user_connections:
                self.user_connections[user_id].discard(connection_id)
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]

            logger.info(f"Connexion WebSocket fermée: {connection_id}")

    async def send_to_connection(self, connection_id: str, message: Dict[str, Any]) -> bool:
        """Envoie un message à une connexion spécifique"""
        if connection_id not in self.connections:
            return False

        connection = self.connections[connection_id]
        try:
            await connection.websocket.send(json.dumps(message))
            return True
        except websockets.exceptions.ConnectionClosed:
            await self.unregister_connection(connection_id)
            return False
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message: {e}")
            return False

    async def send_to_user(self, user_id: str, message: Dict[str, Any]) -> int:
        """Envoie un message à toutes les connexions d'un utilisateur"""
        if user_id not in self.user_connections:
            return 0

        sent_count = 0
        connection_ids = list(self.user_connections[user_id])

        for connection_id in connection_ids:
            if await self.send_to_connection(connection_id, message):
                sent_count += 1

        return sent_count

    async def broadcast_to_role(self, role: UserRole, message: Dict[str, Any]) -> int:
        """Diffuse un message à tous les utilisateurs d'un rôle"""
        sent_count = 0

        for connection in self.connections.values():
            if connection.user_role == role:
                try:
                    await connection.websocket.send(json.dumps(message))
                    sent_count += 1
                except websockets.exceptions.ConnectionClosed:
                    await self.unregister_connection(self.get_connection_id(connection))
                except Exception as e:
                    logger.error(f"Erreur lors de la diffusion: {e}")

        return sent_count

    def get_connection_id(self, connection: WebSocketConnection) -> Optional[str]:
        """Trouve l'ID d'une connexion"""
        for conn_id, conn in self.connections.items():
            if conn == connection:
                return conn_id
        return None

    async def send_notification(self, notification: Notification) -> bool:
        """Envoie une notification à un utilisateur"""
        # Ajouter à l'historique
        self.notification_history.append(notification)

        # Préparer le message
        message = {
            "type": "notification",
            "data": notification.to_dict()
        }

        # Envoyer à l'utilisateur
        sent_count = await self.send_to_user(notification.recipient_id, message)

        if sent_count > 0:
            logger.info(f"Notification envoyée à {notification.recipient_id}: {notification.title}")
            return True
        else:
            logger.warning(f"Impossible d'envoyer la notification à {notification.recipient_id}")
            return False

    async def send_unread_notifications(self, user_id: str, user_role: UserRole):
        """Envoie les notifications non lues à un utilisateur"""
        unread_notifications = [
            notif for notif in self.notification_history
            if notif.recipient_id == user_id and not notif.read
        ]

        for notification in unread_notifications:
            message = {
                "type": "notification",
                "data": notification.to_dict()
            }
            await self.send_to_user(user_id, message)

    def mark_notification_as_read(self, notification_id: str, user_id: str) -> bool:
        """Marque une notification comme lue"""
        for notification in self.notification_history:
            if notification.id == notification_id and notification.recipient_id == user_id:
                notification.read = True
                return True
        return False

    def get_user_notifications(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupère les notifications d'un utilisateur"""
        user_notifications = [
            notif.to_dict() for notif in self.notification_history
            if notif.recipient_id == user_id
        ]

        # Trier par timestamp décroissant
        user_notifications.sort(key=lambda x: x['timestamp'], reverse=True)

        return user_notifications[:limit]

    async def ping_connections(self):
        """Envoie un ping à toutes les connexions pour vérifier leur état"""
        current_time = datetime.utcnow()
        dead_connections = []

        for connection_id, connection in self.connections.items():
            try:
                ping_message = {
                    "type": "ping",
                    "timestamp": current_time.isoformat()
                }
                await connection.websocket.send(json.dumps(ping_message))
                connection.last_ping = current_time
            except websockets.exceptions.ConnectionClosed:
                dead_connections.append(connection_id)
            except Exception as e:
                logger.error(f"Erreur lors du ping: {e}")
                dead_connections.append(connection_id)

        # Nettoyer les connexions mortes
        for connection_id in dead_connections:
            await self.unregister_connection(connection_id)

    async def handle_websocket(self, websocket: WebSocketServerProtocol, path: str):
        """Gestionnaire principal des connexions WebSocket"""
        connection_id = None

        try:
            # Attendre le message d'authentification
            auth_message = await websocket.recv()
            auth_data = json.loads(auth_message)

            if auth_data.get("type") != "auth":
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Message d'authentification requis"
                }))
                return

            # Vérifier le token
            token = auth_data.get("token")
            if not token:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Token manquant"
                }))
                return

            user_data = self.authenticate_token(token)
            if not user_data:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Token invalide"
                }))
                return

            user_id = user_data.get("user_id")
            user_role = UserRole(user_data.get("role", "student"))

            # Enregistrer la connexion
            connection_id = await self.register_connection(websocket, user_id, user_role)

            # Confirmer l'authentification
            await websocket.send(json.dumps({
                "type": "auth_success",
                "connection_id": connection_id,
                "user_id": user_id,
                "role": user_role.value
            }))

            # Boucle de traitement des messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(connection_id, data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Format JSON invalide"
                    }))
                except Exception as e:
                    logger.error(f"Erreur lors du traitement du message: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.info("Connexion WebSocket fermée")
        except Exception as e:
            logger.error(f"Erreur dans handle_websocket: {e}")
        finally:
            if connection_id:
                await self.unregister_connection(connection_id)

    async def handle_message(self, connection_id: str, data: Dict[str, Any]):
        """Traite un message reçu d'un client"""
        message_type = data.get("type")

        if message_type == "pong":
            # Réponse au ping
            if connection_id in self.connections:
                self.connections[connection_id].last_ping = datetime.utcnow()

        elif message_type == "mark_read":
            # Marquer une notification comme lue
            notification_id = data.get("notification_id")
            if connection_id in self.connections:
                user_id = self.connections[connection_id].user_id
                success = self.mark_notification_as_read(notification_id, user_id)

                response = {
                    "type": "mark_read_response",
                    "notification_id": notification_id,
                    "success": success
                }
                await self.send_to_connection(connection_id, response)

        elif message_type == "get_notifications":
            # Récupérer les notifications
            if connection_id in self.connections:
                user_id = self.connections[connection_id].user_id
                limit = data.get("limit", 50)
                notifications = self.get_user_notifications(user_id, limit)

                response = {
                    "type": "notifications_list",
                    "notifications": notifications
                }
                await self.send_to_connection(connection_id, response)

    async def start_ping_task(self):
        """Démarre la tâche de ping périodique"""
        while self.running:
            await self.ping_connections()
            await asyncio.sleep(30)  # Ping toutes les 30 secondes

    def start_server(self, host: str = "localhost", port: int = 8765):
        """Démarre le serveur WebSocket"""
        self.running = True

        # Créer le serveur WebSocket
        start_server = websockets.serve(self.handle_websocket, host, port)

        # Démarrer les tâches
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        loop.create_task(self.start_ping_task())

        logger.info(f"Serveur WebSocket démarré sur ws://{host}:{port}")

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("Arrêt du serveur WebSocket")
        finally:
            self.running = False

# Fonctions utilitaires pour créer des notifications

def create_student_progress_notification(student_id: str, subject: str, progress: float) -> Notification:
    """Crée une notification de progression d'élève"""
    return Notification(
        id=f"progress_{student_id}_{datetime.utcnow().timestamp()}",
        type=NotificationType.STUDENT_PROGRESS,
        title="Progression mise à jour",
        message=f"Votre progression en {subject} est maintenant de {progress}%",
        recipient_id=student_id,
        recipient_role=UserRole.STUDENT,
        data={"subject": subject, "progress": progress}
    )

def create_teacher_message_notification(student_id: str, teacher_name: str, message: str) -> Notification:
    """Crée une notification de message d'enseignant"""
    return Notification(
        id=f"teacher_msg_{student_id}_{datetime.utcnow().timestamp()}",
        type=NotificationType.TEACHER_MESSAGE,
        title=f"Message de {teacher_name}",
        message=message,
        recipient_id=student_id,
        recipient_role=UserRole.STUDENT,
        data={"teacher_name": teacher_name},
        priority="high"
    )

def create_achievement_notification(student_id: str, achievement_name: str, description: str) -> Notification:
    """Crée une notification de réussite débloquée"""
    return Notification(
        id=f"achievement_{student_id}_{datetime.utcnow().timestamp()}",
        type=NotificationType.ACHIEVEMENT_UNLOCKED,
        title="Nouvelle réussite débloquée !",
        message=f"Félicitations ! Vous avez débloqué : {achievement_name}",
        recipient_id=student_id,
        recipient_role=UserRole.STUDENT,
        data={"achievement_name": achievement_name, "description": description},
        priority="high"
    )

def create_parent_notification(parent_id: str, student_name: str, message: str, data: Dict[str, Any] = None) -> Notification:
    """Crée une notification pour un parent"""
    return Notification(
        id=f"parent_{parent_id}_{datetime.utcnow().timestamp()}",
        type=NotificationType.STUDENT_PROGRESS,
        title=f"Mise à jour - {student_name}",
        message=message,
        recipient_id=parent_id,
        recipient_role=UserRole.PARENT,
        data=data or {}
    )

def create_system_alert(admin_id: str, title: str, message: str, priority: str = "normal") -> Notification:
    """Crée une alerte système pour un administrateur"""
    return Notification(
        id=f"system_{admin_id}_{datetime.utcnow().timestamp()}",
        type=NotificationType.SYSTEM_ALERT,
        title=title,
        message=message,
        recipient_id=admin_id,
        recipient_role=UserRole.ADMIN,
        priority=priority
    )

# Instance globale du service
websocket_service = WebSocketService()

if __name__ == "__main__":
    # Test du serveur WebSocket
    service = WebSocketService()
    service.start_server("0.0.0.0", 8765)

