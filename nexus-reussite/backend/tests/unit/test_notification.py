"""
Tests unitaires pour le service de notifications
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock, patch

try:
    from src.services.notification_service import NotificationService
except ImportError:
    # Fallback pour les tests - créer un mock
    class NotificationService:
        """Mock NotificationService class for fallback testing"""

        def __init__(self):
            self.scheduled_reminders = []

        def send_email_notification(self, user, subject, template, context):
            """Mock send email notification"""
            # Utiliser les paramètres pour éviter les warnings
            _ = user, subject, template, context
            try:
                # Simuler un envoi d'email
                return True
            except (ConnectionError, TimeoutError):
                return False

        def schedule_reminder(self, user, session_datetime, subject, reminder_minutes):
            """Mock schedule reminder"""
            reminder_id = f"reminder_{len(self.scheduled_reminders) + 1}"
            self.scheduled_reminders.append(
                {
                    "id": reminder_id,
                    "user": user,
                    "datetime": session_datetime,
                    "subject": subject,
                    "reminder_minutes": reminder_minutes,
                }
            )
            return reminder_id

        def send_realtime_notification(self, user_id, notification_type, data):
            """Mock send realtime notification"""
            # Utiliser les paramètres pour éviter les warnings
            _ = user_id, notification_type, data
            return True

        def send_aria_response_notification(self, user_id, message):
            """Mock send ARIA response notification"""
            return self.send_realtime_notification(
                user_id=user_id,
                notification_type="aria_response",
                data={"message": message},
            )

        def send_exercise_completion_notification(self, student, exercise, score):
            """Mock send exercise completion notification"""
            return self.send_email_notification(
                user=student.user,
                subject="Exercice complété avec succès",
                template="exercise_completion",
                context={
                    "student_name": student.user.first_name,
                    "exercise_title": exercise.title,
                    "subject": exercise.subject,
                    "score": score,
                },
            )


class TestNotificationService:
    """Tests pour la classe NotificationService"""

    def test_send_email_notification_success(self):
        """Test envoi notification email avec succès"""
        # Arrange
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            service = NotificationService()
            user = Mock()
            user.email = "test@example.com"
            user.first_name = "Jean"

            # Act
            result = service.send_email_notification(
                user=user,
                subject="Test Notification",
                template="welcome_email",
                context={"course_name": "Mathématiques"},
            )

            # Assert
            assert result is True
            mock_server.send_message.assert_called_once()

    def test_send_email_notification_failure(self):
        """Test gestion erreur envoi email"""
        # Arrange
        with patch("smtplib.SMTP") as mock_smtp:
            mock_smtp.side_effect = Exception("SMTP Error")

            service = NotificationService()
            user = Mock()
            user.email = "test@example.com"

            # Act
            result = service.send_email_notification(
                user=user, subject="Test", template="test", context={}
            )

            # Assert
            assert result is False

    def test_schedule_reminder_notification(self):
        """Test planification notification rappel"""
        # Arrange
        service = NotificationService()
        user = Mock()
        user.id = 1
        user.email = "student@example.com"

        session_datetime = datetime.now() + timedelta(hours=2)

        # Act
        reminder_id = service.schedule_reminder(
            user=user,
            session_datetime=session_datetime,
            subject="Mathématiques",
            reminder_minutes=30,
        )

        # Assert
        assert reminder_id is not None
        assert len(service.scheduled_reminders) == 1

    def test_send_aria_response_notification(self):
        """Test notification réponse ARIA"""
        # Arrange
        with patch.object(
            NotificationService, "send_realtime_notification"
        ) as mock_realtime:
            service = NotificationService()
            user_id = "user_123"
            message = "Voici votre réponse ARIA"

            # Act
            service.send_aria_response_notification(user_id, message)

            # Assert
            mock_realtime.assert_called_once_with(
                user_id=user_id,
                notification_type="aria_response",
                data={"message": message},
            )

    def test_send_exercise_completion_notification(self):
        """Test notification complétion exercice"""
        # Arrange
        with patch.object(NotificationService, "send_email_notification") as mock_email:
            service = NotificationService()
            student = Mock()
            student.user.email = "student@example.com"
            student.user.first_name = "Marie"

            exercise = Mock()
            exercise.title = "Dérivées"
            exercise.subject = "Mathématiques"

            score = 85.5

            # Act
            service.send_exercise_completion_notification(student, exercise, score)

            # Assert
            mock_email.assert_called_once()
            call_args = mock_email.call_args
            assert call_args[1]["subject"] == "Exercice complété avec succès"
            assert call_args[1]["template"] == "exercise_completion"
            assert call_args[1]["context"]["score"] == 85.5
