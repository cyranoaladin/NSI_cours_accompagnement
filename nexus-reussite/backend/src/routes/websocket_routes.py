"""
Routes API pour la gestion des WebSockets et notifications
"""

from datetime import datetime

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from services.websocket_service import (
    Notification,
    NotificationType,
    UserRole,
    create_achievement_notification,
    create_parent_notification,
    create_student_progress_notification,
    create_system_alert,
    create_teacher_message_notification,
    websocket_service,
)

websocket_bp = Blueprint("websocket", __name__, url_prefix="/api/websocket")


@websocket_bp.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    """Récupère les notifications d'un utilisateur"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        limit = request.args.get("limit", 50, type=int)
        unread_only = request.args.get("unread_only", False, type=bool)

        notifications = websocket_service.get_user_notifications(user_id, limit)

        if unread_only:
            notifications = [n for n in notifications if not n["read"]]

        return jsonify(
            {
                "success": True,
                "notifications": notifications,
                "total": len(notifications),
            }
        )

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(
            f"Erreur lors de la récupération des notifications: {e}"
        )
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur lors de la récupération des notifications",
                }
            ),
            500,
        )


@websocket_bp.route("/notifications/<notification_id>/read", methods=["POST"])
@jwt_required()
def mark_notification_read(notification_id):
    """Marque une notification comme lue"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        success = websocket_service.mark_notification_as_read(notification_id, user_id)

        if success:
            return jsonify(
                {"success": True, "message": "Notification marquée comme lue"}
            )
        else:
            return jsonify({"success": False, "error": "Notification non trouvée"}), 404

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors du marquage de la notification: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur lors du marquage de la notification",
                }
            ),
            500,
        )


@websocket_bp.route("/notifications/mark-all-read", methods=["POST"])
@jwt_required()
def mark_all_notifications_read():
    """Marque toutes les notifications d'un utilisateur comme lues"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        # Marquer toutes les notifications non lues comme lues
        marked_count = 0
        for notification in websocket_service.notification_history:
            if notification.recipient_id == user_id and not notification.read:
                notification.read = True
                marked_count += 1

        return jsonify(
            {
                "success": True,
                "message": f"{marked_count} notifications marquées comme lues",
            }
        )

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors du marquage des notifications: {e}")
        return (
            jsonify(
                {"success": False, "error": "Erreur lors du marquage des notifications"}
            ),
            500,
        )


@websocket_bp.route("/send-notification", methods=["POST"])
@jwt_required()
async def send_notification():
    """Envoie une notification (pour les enseignants et admins)"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get("role")

        # Vérifier les permissions
        if user_role not in ["teacher", "admin"]:
            return jsonify({"success": False, "error": "Permission insuffisante"}), 403

        data = request.get_json()

        # Validation des données
        required_fields = ["recipient_id", "title", "message", "type"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify(
                        {"success": False, "error": f"Champ requis manquant: {field}"}
                    ),
                    400,
                )

        # Créer la notification
        notification = Notification(
            id=f"manual_{datetime.utcnow().timestamp()}",
            type=NotificationType(data["type"]),
            title=data["title"],
            message=data["message"],
            recipient_id=data["recipient_id"],
            recipient_role=UserRole(data.get("recipient_role", "student")),
            data=data.get("data", {}),
            priority=data.get("priority", "normal"),
        )

        # Envoyer la notification
        success = await websocket_service.send_notification(notification)

        if success:
            return jsonify(
                {
                    "success": True,
                    "message": "Notification envoyée avec succès",
                    "notification_id": notification.id,
                }
            )
        else:
            return (
                jsonify(
                    {"success": False, "error": "Échec de l'envoi de la notification"}
                ),
                500,
            )

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors de l'envoi de la notification: {e}")
        return (
            jsonify(
                {"success": False, "error": "Erreur lors de l'envoi de la notification"}
            ),
            500,
        )


@websocket_bp.route("/broadcast", methods=["POST"])
@jwt_required()
async def broadcast_notification():
    """Diffuse une notification à tous les utilisateurs d'un rôle (admin seulement)"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get("role")

        # Vérifier les permissions admin
        if user_role != "admin":
            return (
                jsonify(
                    {"success": False, "error": "Permission administrateur requise"}
                ),
                403,
            )

        data = request.get_json()

        # Validation des données
        required_fields = ["target_role", "title", "message"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify(
                        {"success": False, "error": f"Champ requis manquant: {field}"}
                    ),
                    400,
                )

        target_role = UserRole(data["target_role"])

        # Créer le message de diffusion
        broadcast_message = {
            "type": "broadcast_notification",
            "data": {
                "id": f"broadcast_{datetime.utcnow().timestamp()}",
                "type": data.get("type", "system_alert"),
                "title": data["title"],
                "message": data["message"],
                "priority": data.get("priority", "normal"),
                "timestamp": datetime.utcnow().isoformat(),
                "data": data.get("data", {}),
            },
        }

        # Diffuser le message
        sent_count = await websocket_service.broadcast_to_role(
            target_role, broadcast_message
        )

        return jsonify(
            {
                "success": True,
                "message": f"Notification diffusée à {sent_count} utilisateurs",
                "sent_count": sent_count,
            }
        )

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors de la diffusion: {e}")
        return jsonify({"success": False, "error": "Erreur lors de la diffusion"}), 500


@websocket_bp.route("/connections", methods=["GET"])
@jwt_required()
def get_active_connections():
    """Récupère les connexions actives (admin seulement)"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get("role")

        # Vérifier les permissions admin
        if user_role != "admin":
            return (
                jsonify(
                    {"success": False, "error": "Permission administrateur requise"}
                ),
                403,
            )

        # Statistiques des connexions
        connections_stats = {
            "total_connections": len(websocket_service.connections),
            "unique_users": len(websocket_service.user_connections),
            "connections_by_role": {},
            "recent_connections": [],
        }

        # Compter par rôle
        for connection in websocket_service.connections.values():
            role = connection.user_role.value
            if role not in connections_stats["connections_by_role"]:
                connections_stats["connections_by_role"][role] = 0
            connections_stats["connections_by_role"][role] += 1

        # Connexions récentes (dernières 10)
        recent_connections = sorted(
            websocket_service.connections.values(),
            key=lambda x: x.connected_at,
            reverse=True,
        )[:10]

        for connection in recent_connections:
            connections_stats["recent_connections"].append(
                {
                    "user_id": connection.user_id,
                    "role": connection.user_role.value,
                    "connected_at": connection.connected_at.isoformat(),
                    "last_ping": connection.last_ping.isoformat(),
                }
            )

        return jsonify({"success": True, "data": connections_stats})

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors de la récupération des connexions: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur lors de la récupération des connexions",
                }
            ),
            500,
        )


@websocket_bp.route("/test-notification", methods=["POST"])
@jwt_required()
async def test_notification():
    """Envoie une notification de test (développement seulement)"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")

        # Créer une notification de test
        test_notification = Notification(
            id=f"test_{datetime.utcnow().timestamp()}",
            type=NotificationType.SYSTEM_ALERT,
            title="Notification de test",
            message="Ceci est une notification de test pour vérifier le système WebSocket",
            recipient_id=user_id,
            recipient_role=UserRole(current_user.get("role", "student")),
            data={"test": True},
            priority="normal",
        )

        # Envoyer la notification
        success = await websocket_service.send_notification(test_notification)

        return jsonify(
            {
                "success": success,
                "message": (
                    "Notification de test envoyée" if success else "Échec de l'envoi"
                ),
                "notification_id": test_notification.id,
            }
        )

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors du test de notification: {e}")
        return (
            jsonify({"success": False, "error": "Erreur lors du test de notification"}),
            500,
        )


# Routes pour les notifications spécialisées


@websocket_bp.route("/student-progress", methods=["POST"])
@jwt_required()
async def notify_student_progress():
    """Notifie la progression d'un élève"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get("role")

        # Vérifier les permissions
        if user_role not in ["teacher", "admin"]:
            return jsonify({"success": False, "error": "Permission insuffisante"}), 403

        data = request.get_json()
        student_id = data.get("student_id")
        subject = data.get("subject")
        progress = data.get("progress")

        if not all([student_id, subject, progress is not None]):
            return jsonify({"success": False, "error": "Données manquantes"}), 400

        # Créer et envoyer la notification
        notification = create_student_progress_notification(
            student_id, subject, progress
        )
        success = await websocket_service.send_notification(notification)

        # Notifier aussi les parents si applicable
        try:
            from src.models.user import User

            student = User.query.get(student_id)
            if student and student.parent_id:
                parent_notification = create_parent_notification(
                    student.parent_id,
                    student.first_name,
                    f"Progression mise à jour en {subject}: {progress}%",
                    {
                        "subject": subject,
                        "progress": progress,
                        "student_id": student_id,
                    },
                )
                await websocket_service.send_notification(parent_notification)
        except (RuntimeError, OSError, ValueError) as e:
            current_app.logger.warning(f"Impossible de notifier le parent: {e}")

        return jsonify(
            {"success": success, "message": "Notification de progression envoyée"}
        )

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors de la notification de progression: {e}")
        return (
            jsonify({"success": False, "error": "Erreur lors de la notification"}),
            500,
        )


@websocket_bp.route("/achievement", methods=["POST"])
@jwt_required()
async def notify_achievement():
    """Notifie qu'un élève a débloqué une réussite"""
    try:
        data = request.get_json()
        student_id = data.get("student_id")
        achievement_name = data.get("achievement_name")
        description = data.get("description", "")

        if not all([student_id, achievement_name]):
            return jsonify({"success": False, "error": "Données manquantes"}), 400

        # Créer et envoyer la notification
        notification = create_achievement_notification(
            student_id, achievement_name, description
        )
        success = await websocket_service.send_notification(notification)

        return jsonify(
            {"success": success, "message": "Notification de réussite envoyée"}
        )

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors de la notification de réussite: {e}")
        return (
            jsonify({"success": False, "error": "Erreur lors de la notification"}),
            500,
        )


@websocket_bp.route("/teacher-message", methods=["POST"])
@jwt_required()
async def send_teacher_message():
    """Envoie un message d'enseignant à un élève"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get("role")

        # Vérifier les permissions
        if user_role != "teacher":
            return (
                jsonify({"success": False, "error": "Permission enseignant requise"}),
                403,
            )

        data = request.get_json()
        student_id = data.get("student_id")
        message = data.get("message")
        teacher_name = current_user.get("name", "Votre enseignant")

        if not all([student_id, message]):
            return jsonify({"success": False, "error": "Données manquantes"}), 400

        # Créer et envoyer la notification
        notification = create_teacher_message_notification(
            student_id, teacher_name, message
        )
        success = await websocket_service.send_notification(notification)

        return jsonify({"success": success, "message": "Message envoyé à l'élève"})

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors de l'envoi du message: {e}")
        return (
            jsonify({"success": False, "error": "Erreur lors de l'envoi du message"}),
            500,
        )


@websocket_bp.route("/system-alert", methods=["POST"])
@jwt_required()
async def send_system_alert():
    """Envoie une alerte système (admin seulement)"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get("role")

        # Vérifier les permissions admin
        if user_role != "admin":
            return (
                jsonify(
                    {"success": False, "error": "Permission administrateur requise"}
                ),
                403,
            )

        data = request.get_json()
        title = data.get("title")
        message = data.get("message")
        priority = data.get("priority", "normal")
        target_admins = data.get("target_admins", ["admin"])  # Liste des IDs admin

        if not all([title, message]):
            return jsonify({"success": False, "error": "Titre et message requis"}), 400

        # Envoyer l'alerte à tous les admins ciblés
        sent_count = 0
        for admin_id in target_admins:
            alert = create_system_alert(admin_id, title, message, priority)
            if await websocket_service.send_notification(alert):
                sent_count += 1

        return jsonify(
            {
                "success": sent_count > 0,
                "message": f"Alerte envoyée à {sent_count} administrateurs",
            }
        )

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(f"Erreur lors de l'envoi de l'alerte: {e}")
        return (
            jsonify({"success": False, "error": "Erreur lors de l'envoi de l'alerte"}),
            500,
        )


@websocket_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_notification_stats():
    """Récupère les statistiques des notifications"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get("role")

        # Statistiques de base pour tous les utilisateurs
        user_id = current_user.get("user_id")
        user_notifications = [
            n
            for n in websocket_service.notification_history
            if n.recipient_id == user_id
        ]

        stats = {
            "total_notifications": len(user_notifications),
            "unread_notifications": len([n for n in user_notifications if not n.read]),
            "notifications_by_type": {},
            "notifications_by_priority": {},
        }

        # Compter par type et priorité
        for notification in user_notifications:
            # Par type
            notif_type = notification.type.value
            if notif_type not in stats["notifications_by_type"]:
                stats["notifications_by_type"][notif_type] = 0
            stats["notifications_by_type"][notif_type] += 1

            # Par priorité
            priority = notification.priority
            if priority not in stats["notifications_by_priority"]:
                stats["notifications_by_priority"][priority] = 0
            stats["notifications_by_priority"][priority] += 1

        # Statistiques globales pour les admins
        if user_role == "admin":
            stats["global"] = {
                "total_notifications": len(websocket_service.notification_history),
                "active_connections": len(websocket_service.connections),
                "unique_users": len(websocket_service.user_connections),
            }

        return jsonify({"success": True, "stats": stats})

    except (RuntimeError, OSError, ValueError) as e:
        current_app.logger.error(
            f"Erreur lors de la récupération des statistiques: {e}"
        )
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur lors de la récupération des statistiques",
                }
            ),
            500,
        )
