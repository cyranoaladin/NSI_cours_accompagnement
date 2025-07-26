"""
Tests unitaires pour le modèle Teacher
"""

import pytest

# Import avec gestion d'erreur pour les tests
try:
    from src.models.teacher import Teacher  # pylint: disable=import-error
    from src.models.user import User  # pylint: disable=import-error
except ImportError:
    # Fallback pour les tests sans les modules réels
    class Teacher:  # pylint: disable=too-few-public-methods
        """Mock Teacher class for testing"""

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class User:  # pylint: disable=too-few-public-methods
        """Mock User class for testing"""

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


class TestTeacher:
    """Tests unitaires pour le modèle Teacher"""

    def test_create_teacher(self, test_db):
        """Test de création d'un enseignant"""
        # Arrange
        teacher_data = {
            "speciality": "Mathématiques",
            "experience_years": 5,
            "certification": "Agrégation",
        }

        # Act
        teacher = Teacher(**teacher_data)
        test_db.session.add(teacher)
        test_db.session.commit()

        # Assert
        assert teacher.id is not None
        assert teacher.speciality == "Mathématiques"
        assert teacher.experience_years == 5
        assert teacher.certification == "Agrégation"
        assert teacher.created_at is not None

    def test_teacher_with_user_relationship(self, test_db, sample_user):
        """Test de la relation Teacher-User"""
        # Arrange
        teacher = Teacher(
            user_id=sample_user.id, speciality="Physique", experience_years=10
        )

        # Act
        test_db.session.add(teacher)
        test_db.session.commit()

        # Assert
        assert teacher.user == sample_user
        assert teacher.user.username == "test_user"
        assert teacher.user.email == "test@example.com"

    def test_teacher_string_representation(self, test_db, sample_user):
        """Test de la représentation string du teacher"""
        # Arrange
        teacher = Teacher(
            user_id=sample_user.id, speciality="Chimie", experience_years=3
        )
        test_db.session.add(teacher)
        test_db.session.commit()

        # Act
        teacher_str = str(teacher)

        # Assert
        assert "Teacher" in teacher_str
        assert "Chimie" in teacher_str

    def test_teacher_to_dict(self, test_db, sample_user):
        """Test de sérialisation du teacher en dictionnaire"""
        # Arrange
        teacher = Teacher(
            user_id=sample_user.id,
            speciality="Histoire",
            experience_years=8,
            certification="CAPES",
        )
        test_db.session.add(teacher)
        test_db.session.commit()

        # Act
        teacher_dict = teacher.to_dict()

        # Assert
        assert isinstance(teacher_dict, dict)
        assert teacher_dict["id"] == teacher.id
        assert teacher_dict["speciality"] == "Histoire"
        assert teacher_dict["experience_years"] == 8
        assert teacher_dict["certification"] == "CAPES"
        assert "created_at" in teacher_dict

    def test_teacher_validation_speciality_required(
        self, test_db
    ):  # pylint: disable=unused-argument
        """Test de validation - spécialité requise"""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="La spécialité est requise"):
            Teacher(speciality=None)  # pylint: disable=unused-variable

    def test_teacher_validation_experience_years_positive(
        self, test_db
    ):  # pylint: disable=unused-argument
        """Test de validation - années d'expérience positives"""
        # Arrange & Act & Assert
        with pytest.raises(
            ValueError, match="Les années d'expérience doivent être positives"
        ):
            Teacher(  # pylint: disable=unused-variable
                speciality="Mathématiques", experience_years=-1
            )

    def test_teacher_validation_experience_years_reasonable(
        self, test_db
    ):  # pylint: disable=unused-argument
        """Test de validation - années d'expérience raisonnables"""
        # Arrange & Act & Assert
        with pytest.raises(
            ValueError, match="Les années d'expérience ne peuvent pas dépasser 50"
        ):
            Teacher(  # pylint: disable=unused-variable
                speciality="Mathématiques", experience_years=51
            )

    def test_find_teachers_by_speciality(
        self, test_db, sample_user
    ):  # pylint: disable=unused-argument
        """Test de recherche d'enseignants par spécialité"""
        # Arrange
        # Créer un autre utilisateur pour le deuxième enseignant
        user2 = User(
            username="teacher2",
            email="teacher2@example.com",
            password_hash="hashed_password",
        )
        test_db.session.add(user2)
        test_db.session.commit()

        teacher1 = Teacher(
            user_id=sample_user.id, speciality="Mathématiques", experience_years=5
        )
        teacher2 = Teacher(
            user_id=user2.id, speciality="Mathématiques", experience_years=8
        )
        teacher3 = Teacher(
            user_id=sample_user.id, speciality="Physique", experience_years=3
        )

        test_db.session.add_all([teacher1, teacher2, teacher3])
        test_db.session.commit()

        # Act
        math_teachers = Teacher.query.filter_by(speciality="Mathématiques").all()

        # Assert
        assert len(math_teachers) == 2
        assert all(t.speciality == "Mathématiques" for t in math_teachers)

    def test_teacher_update_speciality(
        self, test_db, sample_user
    ):  # pylint: disable=unused-argument
        """Test de mise à jour de la spécialité"""
        # Arrange
        teacher = Teacher(
            user_id=sample_user.id, speciality="Biologie", experience_years=4
        )
        test_db.session.add(teacher)
        test_db.session.commit()

        # Act
        teacher.speciality = (
            "Géologie"  # pylint: disable=attribute-defined-outside-init
        )
        test_db.session.commit()

        # Assert
        updated_teacher = Teacher.query.get(teacher.id)
        assert updated_teacher.speciality == "Géologie"

    def test_teacher_increment_experience(
        self, test_db, sample_user
    ):  # pylint: disable=unused-argument
        """Test d'incrémentation de l'expérience"""
        # Arrange
        teacher = Teacher(
            user_id=sample_user.id, speciality="Anglais", experience_years=2
        )
        test_db.session.add(teacher)
        test_db.session.commit()

        # Act
        teacher.experience_years += 1
        test_db.session.commit()

        # Assert
        updated_teacher = Teacher.query.get(teacher.id)
        assert updated_teacher.experience_years == 3

    def test_teacher_delete_cascade(
        self, test_db, sample_user
    ):  # pylint: disable=unused-argument
        """Test de suppression en cascade"""
        # Arrange
        teacher = Teacher(
            user_id=sample_user.id, speciality="Espagnol", experience_years=6
        )
        test_db.session.add(teacher)
        test_db.session.commit()
        teacher_id = teacher.id

        # Act
        test_db.session.delete(teacher)
        test_db.session.commit()

        # Assert
        deleted_teacher = Teacher.query.get(teacher_id)
        assert deleted_teacher is None

    def test_teacher_query_by_experience_range(
        self, test_db, sample_user
    ):  # pylint: disable=unused-argument
        """Test de requête par plage d'expérience"""
        # Arrange
        teachers_data = [
            {"speciality": "Math", "experience_years": 2},
            {"speciality": "Physics", "experience_years": 5},
            {"speciality": "Chemistry", "experience_years": 8},
            {"speciality": "Biology", "experience_years": 12},
        ]

        for i, data in enumerate(teachers_data):
            user = User(
                username=f"teacher_{i}",
                email=f"teacher_{i}@example.com",
                password_hash="hashed_password",
            )
            test_db.session.add(user)
            test_db.session.commit()

            teacher = Teacher(user_id=user.id, **data)
            test_db.session.add(teacher)

        test_db.session.commit()

        # Act
        experienced_teachers = Teacher.query.filter(
            Teacher.experience_years >= 5, Teacher.experience_years <= 10
        ).all()

        # Assert
        assert len(experienced_teachers) == 2
        experience_years = [t.experience_years for t in experienced_teachers]
        assert 5 in experience_years
        assert 8 in experience_years

    def test_teacher_with_certification(
        self, test_db, sample_user
    ):  # pylint: disable=unused-argument
        """Test d'enseignant avec certification"""
        # Arrange
        teacher = Teacher(
            user_id=sample_user.id,
            speciality="Informatique",
            experience_years=7,
            certification="Doctorat",
        )

        # Act
        test_db.session.add(teacher)
        test_db.session.commit()

        # Assert
        assert teacher.certification == "Doctorat"
        assert "Doctorat" in teacher.to_dict()["certification"]

    def test_teacher_without_certification(
        self, test_db, sample_user
    ):  # pylint: disable=unused-argument
        """Test d'enseignant sans certification"""
        # Arrange
        teacher = Teacher(user_id=sample_user.id, speciality="Art", experience_years=3)

        # Act
        test_db.session.add(teacher)
        test_db.session.commit()

        # Assert
        assert teacher.certification is None
        teacher_dict = teacher.to_dict()
        assert teacher_dict.get("certification") is None
