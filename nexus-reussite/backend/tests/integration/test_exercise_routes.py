"""
Tests d'intégration pour les routes d'exercices.

Ce module contient les tests pour les endpoints liés aux exercices,
incluant la création, récupération, soumission et gestion des exercices.
"""

# pylint: disable=import-error
import pytest

from tests.integration.test_auth_routes import TestAuthRoutes


class TestExerciseRoutes(TestAuthRoutes):
    """Classe de tests pour les routes d'exercices."""

    @pytest.fixture
    def auth_student_client(self, client):
        """Fixture client avec étudiant authentifié"""
        # Créer et connecter un étudiant
        student_data = {
            "email": "etudiant@test.com",
            "password": "Password123!",
            "first_name": "Marie",
            "last_name": "Student",
            "role": "student",
        }
        client.post("/api/auth/register", json=student_data)

        login_response = client.post(
            "/api/auth/login",
            json={"email": "etudiant@test.com", "password": "Password123!"},
        )
        token = login_response.get_json()["token"]

        return client, {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def auth_teacher_client(self, client):
        """Fixture client avec professeur authentifié"""
        # Créer et connecter un professeur
        teacher_data = {
            "email": "professeur@test.com",
            "password": "Password123!",
            "first_name": "Jean",
            "last_name": "Teacher",
            "role": "teacher",
        }
        client.post("/api/auth/register", json=teacher_data)

        login_response = client.post(
            "/api/auth/login",
            json={"email": "professeur@test.com", "password": "Password123!"},
        )
        token = login_response.get_json()["token"]

        return client, {"Authorization": f"Bearer {token}"}

    def test_get_exercises_list_student(self, auth_student_client):
        """Test récupération liste exercices pour étudiant"""
        # Arrange
        client, headers = auth_student_client

        # Act
        response = client.get("/api/exercises/", headers=headers)

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert "exercises" in data
        assert isinstance(data["exercises"], list)

    def test_get_exercises_with_filters(self, auth_student_client):
        """Test récupération exercices avec filtres"""
        # Arrange
        client, headers = auth_student_client

        # Act
        response = client.get(
            "/api/exercises/?subject=Mathématiques&level=Terminale", headers=headers
        )

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert "exercises" in data

        # Vérifier que les filtres sont appliqués
        for exercise in data["exercises"]:
            if exercise["subject"]:
                assert exercise["subject"] == "Mathématiques"
            if exercise["level"]:
                assert exercise["level"] == "Terminale"

    def test_get_exercise_by_id(self, auth_student_client):
        """Test récupération exercice par ID"""
        # Arrange
        client, headers = auth_student_client

        # Act
        response = client.get("/api/exercises/1", headers=headers)

        # Assert
        if response.status_code == 200:
            data = response.get_json()
            assert "id" in data
            assert "title" in data
            assert "description" in data
        else:
            # Si aucun exercice n'existe, doit retourner 404
            assert response.status_code == 404

    def test_submit_exercise_solution_student(self, auth_student_client):
        """Test soumission solution exercice par étudiant"""
        # Arrange
        client, headers = auth_student_client

        solution_data = {
            "exercise_id": 1,
            "solution": "f'(x) = 2x + 3",
            "reasoning": "Dérivée d'une fonction polynomiale du premier degré",
            "time_spent": 15,  # minutes
        }

        # Act
        response = client.post(
            "/api/exercises/submit", json=solution_data, headers=headers
        )

        # Assert
        # Peut retourner 201 (créé) ou 404 (exercice inexistant)
        assert response.status_code in [201, 404]

        if response.status_code == 201:
            data = response.get_json()
            assert "score" in data
            assert "feedback" in data
            assert data["score"] >= 0
            assert data["score"] <= 100

    def test_submit_exercise_solution_invalid_data(self, auth_student_client):
        """Test soumission solution avec données invalides"""
        # Arrange
        client, headers = auth_student_client

        invalid_data = {
            "exercise_id": "invalid",  # ID invalide
            "solution": "",  # Solution vide
        }

        # Act
        response = client.post(
            "/api/exercises/submit", json=invalid_data, headers=headers
        )

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_exercise_teacher_authorized(self, auth_teacher_client):
        """Test création exercice par professeur autorisé"""
        # Arrange
        client, headers = auth_teacher_client

        exercise_data = {
            "title": "Calcul de limites",
            "description": "Calculer les limites des fonctions suivantes",
            "subject": "Mathématiques",
            "level": "Terminale",
            "difficulty": 3,
            "points": 10,
            "questions": [
                {
                    "text": "Calculer lim(x→0) sin(x)/x",
                    "points": 5,
                    "type": "calculation",
                }
            ],
        }

        # Act
        response = client.post("/api/exercises/", json=exercise_data, headers=headers)

        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert "id" in data
        assert data["title"] == "Calcul de limites"
        assert data["subject"] == "Mathématiques"

    def test_create_exercise_student_unauthorized(self, auth_student_client):
        """Test création exercice par étudiant non autorisé"""
        # Arrange
        client, headers = auth_student_client

        exercise_data = {
            "title": "Test Exercise",
            "description": "Test Description",
            "subject": "Mathématiques",
            "level": "Terminale",
        }

        # Act
        response = client.post("/api/exercises/", json=exercise_data, headers=headers)

        # Assert
        assert response.status_code == 403  # Forbidden
        data = response.get_json()
        assert "error" in data
        assert "autorisé" in data["error"].lower()

    def test_update_exercise_teacher(self, auth_teacher_client):
        """Test mise à jour exercice par professeur"""
        # Arrange
        client, headers = auth_teacher_client

        update_data = {
            "title": "Titre mis à jour",
            "description": "Description mise à jour",
            "difficulty": 4,
        }

        # Act
        response = client.put("/api/exercises/1", json=update_data, headers=headers)

        # Assert
        # Peut retourner 200 (mis à jour) ou 404 (exercice inexistant)
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.get_json()
            assert data["title"] == "Titre mis à jour"
            assert data["difficulty"] == 4

    def test_delete_exercise_teacher(self, auth_teacher_client):
        """Test suppression exercice par professeur"""
        # Arrange
        client, headers = auth_teacher_client

        # Act
        response = client.delete("/api/exercises/1", headers=headers)

        # Assert
        # Peut retourner 200 (supprimé) ou 404 (exercice inexistant)
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.get_json()
            assert "supprimé" in data["message"].lower()

    def test_get_student_exercise_history(self, auth_student_client):
        """Test récupération historique exercices étudiant"""
        # Arrange
        client, headers = auth_student_client

        # Act
        response = client.get("/api/exercises/history", headers=headers)

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert "history" in data
        assert isinstance(data["history"], list)

    def test_get_exercise_statistics_teacher(self, auth_teacher_client):
        """Test récupération statistiques exercice pour professeur"""
        # Arrange
        client, headers = auth_teacher_client

        # Act
        response = client.get("/api/exercises/1/statistics", headers=headers)

        # Assert
        # Peut retourner 200 (stats) ou 404 (exercice inexistant)
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.get_json()
            assert "completion_rate" in data
            assert "average_score" in data
            assert "attempt_count" in data

    def test_get_exercise_unauthenticated(self, client):
        """Test accès exercice sans authentification"""
        # Act
        response = client.get("/api/exercises/")

        # Assert
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert "token" in data["error"].lower()

    def test_bulk_import_exercises_teacher(self, auth_teacher_client):
        """Test import en lot d'exercices par professeur"""
        # Arrange
        client, headers = auth_teacher_client

        exercises_data = {
            "exercises": [
                {
                    "title": "Exercice 1",
                    "description": "Description 1",
                    "subject": "Mathématiques",
                    "level": "Première",
                    "difficulty": 2,
                },
                {
                    "title": "Exercice 2",
                    "description": "Description 2",
                    "subject": "NSI",
                    "level": "Terminale",
                    "difficulty": 3,
                },
            ]
        }

        # Act
        response = client.post(
            "/api/exercises/bulk-import", json=exercises_data, headers=headers
        )

        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert "imported_count" in data
        assert data["imported_count"] == 2
