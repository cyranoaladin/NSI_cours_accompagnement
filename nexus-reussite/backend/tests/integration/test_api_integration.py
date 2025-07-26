#!/usr/bin/env python3
"""
Tests d'intégration pour l'API Flask de Nexus Réussite
"""
# pylint: disable=import-error,unused-import,unused-argument,unused-variable
# pylint: disable=too-few-public-methods,too-many-locals

import json
from io import BytesIO

from src.models.user import User


class TestUserAPIIntegration:
    """Tests d'intégration pour l'API utilisateurs"""

    def test_complete_user_registration_flow(self, client):
        """Test du flow complet d'inscription utilisateur"""
        # Données d'inscription
        user_data = {
            "email": "integration@test.com",
            "password": "TestPassword123!",
            "name": "Integration Test",
            "role": "student",
        }

        # 1. Inscription
        response = client.post(
            "/api/auth/register",
            data=json.dumps(user_data),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert "user_id" in data
        assert "token" in data
        user_id = data["user_id"]
        token = data["token"]

        # 2. Vérification que l'utilisateur existe en DB
        user = User.query.get(user_id)
        assert user is not None
        assert user.email == user_data["email"]
        assert user.name == user_data["name"]
        assert user.role == user_data["role"]

        # 3. Connexion avec les mêmes credentials
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json",
        )
        assert response.status_code == 200

        # 4. Accès au profil avec le token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get(f"/api/users/{user_id}", headers=headers)
        assert response.status_code == 200
        profile_data = json.loads(response.data)
        assert profile_data["email"] == user_data["email"]

    def test_user_profile_update_flow(self, client, test_user, auth_headers):
        """Test du flow de mise à jour du profil"""
        # 1. Récupération du profil initial
        response = client.get(f"/api/users/{test_user.id}", headers=auth_headers)
        assert response.status_code == 200
        initial_data = json.loads(response.data)

        # 2. Mise à jour du profil
        update_data = {"name": "Updated Name", "bio": "Updated bio description"}
        response = client.put(
            f"/api/users/{test_user.id}",
            data=json.dumps(update_data),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 200

        # 3. Vérification des changements
        response = client.get(f"/api/users/{test_user.id}", headers=auth_headers)
        assert response.status_code == 200
        updated_data = json.loads(response.data)
        assert updated_data["name"] == update_data["name"]
        assert updated_data["bio"] == update_data["bio"]
        assert updated_data["email"] == initial_data["email"]  # Unchanged


class TestStudentAPIIntegration:
    """Tests d'intégration pour l'API étudiants"""

    def test_student_enrollment_and_progress_flow(
        self, client, test_student, auth_headers
    ):
        """Test du flow d'inscription et de progression étudiant"""
        # 1. Inscription à un cours
        course_data = {
            "course_name": "Python Avancé",
            "course_code": "PY301",
            "semester": "2024-1",
        }
        response = client.post(
            f"/api/students/{test_student.id}/enroll",
            data=json.dumps(course_data),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 201
        enrollment_data = json.loads(response.data)
        _ = enrollment_data[
            "enrollment_id"
        ]  # enrollment_id stored but not used in this test

        # 2. Enregistrement de progression
        progress_data = {
            "lesson_id": "lesson_001",
            "completion_percentage": 75,
            "time_spent": 120,  # minutes
            "quiz_score": 85,
        }
        response = client.post(
            f"/api/students/{test_student.id}/progress",
            data=json.dumps(progress_data),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 201

        # 3. Récupération des statistiques de progression
        response = client.get(
            f"/api/students/{test_student.id}/stats", headers=auth_headers
        )
        assert response.status_code == 200
        stats_data = json.loads(response.data)
        assert "total_courses" in stats_data
        assert "average_score" in stats_data
        assert "time_spent" in stats_data
        assert stats_data["total_courses"] >= 1

        # 4. Génération de rapport de progression
        response = client.get(
            f"/api/students/{test_student.id}/report", headers=auth_headers
        )
        assert response.status_code == 200
        report_data = json.loads(response.data)
        assert "courses" in report_data
        assert "overall_progress" in report_data


class TestDocumentAPIIntegration:
    """Tests d'intégration pour l'API documents"""

    def test_document_upload_and_processing_flow(
        self, client, test_user, auth_headers
    ):  # pylint: disable=unused-argument
        """Test du flow complet de gestion des documents"""
        # 1. Upload d'un document
        file_data = BytesIO(b"Contenu du document de test pour l'analyse")
        file_data.name = "test_document.txt"

        response = client.post(
            "/api/documents/upload",
            data={
                "file": (file_data, "test_document.txt"),
                "document_type": "homework",
                "subject": "NSI",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        upload_data = json.loads(response.data)
        document_id = upload_data["document_id"]

        # 2. Vérification du document uploadé
        response = client.get(f"/api/documents/{document_id}", headers=auth_headers)
        assert response.status_code == 200
        doc_data = json.loads(response.data)
        assert doc_data["filename"] == "test_document.txt"
        assert doc_data["document_type"] == "homework"

        # 3. Demande d'analyse ARIA
        analysis_request = {
            "analysis_type": "grammar_check",
            "language": "fr",
            "detailed": True,
        }
        response = client.post(
            f"/api/documents/{document_id}/analyze",
            data=json.dumps(analysis_request),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 202  # Accepted for processing

        # 4. Récupération du résultat d'analyse (simulation)
        response = client.get(
            f"/api/documents/{document_id}/analysis", headers=auth_headers
        )
        # Peut être 200 (completed) ou 202 (processing)
        assert response.status_code in [200, 202]

        # 5. Suppression du document
        response = client.delete(f"/api/documents/{document_id}", headers=auth_headers)
        assert response.status_code == 204

        # 6. Vérification de la suppression
        response = client.get(f"/api/documents/{document_id}", headers=auth_headers)
        assert response.status_code == 404


class TestARIAIntegration:
    """Tests d'intégration pour l'API ARIA"""

    def test_aria_conversation_flow(
        self, client, test_user, auth_headers
    ):  # pylint: disable=unused-argument
        """Test du flow complet de conversation avec ARIA"""
        # 1. Initiation d'une nouvelle conversation
        conversation_data = {"subject": "NSI", "context": "Aide aux devoirs"}
        response = client.post(
            "/api/aria/conversations",
            data=json.dumps(conversation_data),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 201
        conv_data = json.loads(response.data)
        conversation_id = conv_data["conversation_id"]

        # 2. Envoi d'un message à ARIA
        message_data = {
            "message": "Peux-tu m'aider avec les algorithmes de tri en Python?",
            "conversation_id": conversation_id,
        }
        response = client.post(
            "/api/aria/chat",
            data=json.dumps(message_data),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 200
        chat_data = json.loads(response.data)
        assert "response" in chat_data
        assert "message_id" in chat_data

        # 3. Récupération de l'historique de conversation
        response = client.get(
            f"/api/aria/conversations/{conversation_id}", headers=auth_headers
        )
        assert response.status_code == 200
        history_data = json.loads(response.data)
        assert "messages" in history_data
        assert len(history_data["messages"]) >= 2  # User message + ARIA response

        # 4. Évaluation de la réponse ARIA
        evaluation_data = {
            "message_id": chat_data["message_id"],
            "rating": 5,
            "feedback": "Très utile!",
        }
        response = client.post(
            f"/api/aria/conversations/{conversation_id}/evaluate",
            data=json.dumps(evaluation_data),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 201


class TestAdminAPIIntegration:
    """Tests d'intégration pour l'API admin"""

    def test_admin_user_management_flow(
        self, client, admin_user, admin_headers
    ):  # pylint: disable=unused-argument
        """Test du flow de gestion des utilisateurs par l'admin"""
        # 1. Récupération des statistiques
        response = client.get("/api/admin/stats", headers=admin_headers)
        assert response.status_code == 200
        stats_data = json.loads(response.data)
        assert "total_users" in stats_data
        assert "total_students" in stats_data
        initial_user_count = stats_data["total_users"]

        # 2. Création d'un nouvel utilisateur par l'admin
        new_user_data = {
            "email": "admin_created@test.com",
            "password": "AdminCreated123!",
            "name": "Admin Created User",
            "role": "teacher",
        }
        response = client.post(
            "/api/admin/users",
            data=json.dumps(new_user_data),
            content_type="application/json",
            headers=admin_headers,
        )
        assert response.status_code == 201
        created_user_data = json.loads(response.data)
        created_user_id = created_user_data["user_id"]

        # 3. Vérification de l'augmentation du nombre d'utilisateurs
        response = client.get("/api/admin/stats", headers=admin_headers)
        assert response.status_code == 200
        updated_stats = json.loads(response.data)
        assert updated_stats["total_users"] == initial_user_count + 1

        # 4. Modification de l'utilisateur créé
        update_data = {"name": "Updated Admin Created User", "is_active": False}
        response = client.put(
            f"/api/admin/users/{created_user_id}",
            data=json.dumps(update_data),
            content_type="application/json",
            headers=admin_headers,
        )
        assert response.status_code == 200

        # 5. Suppression de l'utilisateur
        response = client.delete(
            f"/api/admin/users/{created_user_id}", headers=admin_headers
        )
        assert response.status_code == 204

        # 6. Vérification du retour au nombre initial d'utilisateurs
        response = client.get("/api/admin/stats", headers=admin_headers)
        assert response.status_code == 200
        final_stats = json.loads(response.data)
        assert final_stats["total_users"] == initial_user_count


class TestEndToEndWorkflow:
    """Tests end-to-end complets"""

    def test_complete_student_learning_journey(self, client):
        """Test d'un parcours complet d'apprentissage étudiant"""
        # 1. Inscription de l'étudiant
        registration_data = {
            "email": "journey@student.com",
            "password": "Journey123!",
            "name": "Journey Student",
            "role": "student",
        }
        response = client.post(
            "/api/auth/register",
            data=json.dumps(registration_data),
            content_type="application/json",
        )
        assert response.status_code == 201
        auth_data = json.loads(response.data)
        student_id = auth_data["user_id"]
        token = auth_data["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Création du profil étudiant
        student_data = {
            "class_level": "Première",
            "specialization": "NSI",
            "academic_year": "2024-2025",
        }
        response = client.post(
            "/api/students",
            data=json.dumps(student_data),
            content_type="application/json",
            headers=headers,
        )
        assert response.status_code == 201

        # 3. Upload d'un devoir
        file_data = BytesIO(b"Mon algorithme de tri par insertion en Python")
        response = client.post(
            "/api/documents/upload",
            data={
                "file": (file_data, "devoir_tri.py"),
                "document_type": "homework",
                "subject": "NSI",
            },
            headers=headers,
        )
        assert response.status_code == 201
        doc_data = json.loads(response.data)
        document_id = doc_data["document_id"]

        # 4. Demande d'aide à ARIA pour le devoir
        conversation_data = {
            "subject": "NSI",
            "context": "Correction de devoir",
            "document_id": document_id,
        }
        response = client.post(
            "/api/aria/conversations",
            data=json.dumps(conversation_data),
            content_type="application/json",
            headers=headers,
        )
        assert response.status_code == 201
        conv_data = json.loads(response.data)
        conversation_id = conv_data["conversation_id"]

        # 5. Chat avec ARIA
        message_data = {
            "message": "Peux-tu analyser mon code et me donner des suggestions?",
            "conversation_id": conversation_id,
        }
        response = client.post(
            "/api/aria/chat",
            data=json.dumps(message_data),
            content_type="application/json",
            headers=headers,
        )
        assert response.status_code == 200

        # 6. Enregistrement de la progression
        progress_data = {
            "lesson_id": "algorithms_sorting",
            "completion_percentage": 85,
            "time_spent": 60,
            "quiz_score": 78,
        }
        response = client.post(
            f"/api/students/{student_id}/progress",
            data=json.dumps(progress_data),
            content_type="application/json",
            headers=headers,
        )
        assert response.status_code == 201

        # 7. Consultation des statistiques personnelles
        response = client.get(f"/api/students/{student_id}/stats", headers=headers)
        assert response.status_code == 200
        stats_data = json.loads(response.data)
        assert stats_data["time_spent"] >= 60
        assert stats_data["average_score"] == 78

        # 8. Génération du rapport de progression
        response = client.get(f"/api/students/{student_id}/report", headers=headers)
        assert response.status_code == 200
        report_data = json.loads(response.data)
        assert "overall_progress" in report_data
        assert report_data["overall_progress"] >= 85
