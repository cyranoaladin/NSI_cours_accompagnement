"""
Initialisation de la base de données Nexus Réussite
Script d'initialisation avec données de démonstration
"""
import os
import sys
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main_production import create_app, db
from src.models.user import User, UserRole, UserStatus
from src.models.student import StudentProfile, LearningStyle, AcademicLevel
from src.models.content_system import Course, Module, Exercise, Quiz, QuizQuestion
from src.models.formulas import Formula, FormulaType


def init_database():
    """Initialise la base de données avec la structure et les données de démonstration"""

    print("🚀 Initialisation de la base de données Nexus Réussite...")

    # Créer les tables
    print("📋 Création des tables...")
    db.drop_all()
    db.create_all()

    # Créer les données de démonstration
    create_demo_data()

    print("✅ Base de données initialisée avec succès!")


def create_demo_data():
    """Crée les données de démonstration"""

    print("👥 Création des utilisateurs de démonstration...")

    # === ADMINISTRATEURS ===
    admin = User(
        email='admin@nexus-reussite.com',
        password='admin123',
        first_name='Admin',
        last_name='Nexus',
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        email_verified=True
    )
    db.session.add(admin)

    # === ENSEIGNANTS ===
    teachers_data = [
        {
            'email': 'marc.dubois@nexus-reussite.com',
            'password': 'teacher123',
            'first_name': 'Marc',
            'last_name': 'Dubois',
            'phone': '+216 20 123 456',
            'specialties': ['Mathématiques', 'Physique'],
            'experience': 15,
            'qualification': 'Agrégé de Mathématiques',
            'rating': 4.9,
            'description': 'Professeur agrégé avec 15 ans d\'expérience dans les établissements AEFE'
        },
        {
            'email': 'sophie.martin@nexus-reussite.com',
            'password': 'teacher123',
            'first_name': 'Sophie',
            'last_name': 'Martin',
            'phone': '+216 20 234 567',
            'specialties': ['NSI', 'Mathématiques'],
            'experience': 8,
            'qualification': 'Certifiée NSI, DIU',
            'rating': 4.8,
            'description': 'Spécialiste NSI passionnée de programmation et d\'algorithmique'
        },
        {
            'email': 'david.rousseau@nexus-reussite.com',
            'password': 'teacher123',
            'first_name': 'David',
            'last_name': 'Rousseau',
            'phone': '+216 20 345 678',
            'specialties': ['Physique-Chimie'],
            'experience': 12,
            'qualification': 'Docteur en Physique',
            'rating': 4.9,
            'description': 'Docteur en Physique avec expertise en sciences expérimentales'
        }
    ]

    for teacher_data in teachers_data:
        teacher = User(
            email=teacher_data['email'],
            password=teacher_data['password'],
            first_name=teacher_data['first_name'],
            last_name=teacher_data['last_name'],
            phone=teacher_data.get('phone'),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE,
            email_verified=True
        )
        db.session.add(teacher)

    # === ÉTUDIANTS ===
    students_data = [
        {
            'email': 'sarah.martin@email.com',
            'password': 'demo123',
            'first_name': 'Sarah',
            'last_name': 'Martin',
            'academic_level': AcademicLevel.TERMINALE,
            'specialties': ['Mathématiques', 'NSI', 'Physique-Chimie'],
            'learning_style': LearningStyle.VISUAL,
            'learning_style_percentage': 85,
            'current_grade': 16.5,
            'target_grade': 18.0,
            'bio': 'Élève sérieuse et motivée, vise une école d\'ingénieur'
        },
        {
            'email': 'ahmed.ben.ali@email.com',
            'password': 'demo123',
            'first_name': 'Ahmed',
            'last_name': 'Ben Ali',
            'academic_level': AcademicLevel.PREMIERE,
            'specialties': ['Mathématiques', 'Physique-Chimie'],
            'learning_style': LearningStyle.AUDITORY,
            'learning_style_percentage': 70,
            'current_grade': 13.2,
            'target_grade': 15.0,
            'bio': 'Élève appliqué qui souhaite progresser en sciences'
        },
        {
            'email': 'lea.dubois@email.com',
            'password': 'demo123',
            'first_name': 'Léa',
            'last_name': 'Dubois',
            'academic_level': AcademicLevel.TERMINALE,
            'specialties': ['Français', 'Philosophie', 'Histoire-Géographie'],
            'learning_style': LearningStyle.KINESTHETIC,
            'learning_style_percentage': 80,
            'current_grade': 15.8,
            'target_grade': 17.0,
            'bio': 'Passionnée de littérature et de philosophie'
        },
        {
            'email': 'youssef.trabelsi@email.com',
            'password': 'demo123',
            'first_name': 'Youssef',
            'last_name': 'Trabelsi',
            'academic_level': AcademicLevel.TERMINALE,
            'specialties': ['Mathématiques', 'NSI'],
            'learning_style': LearningStyle.LOGICAL,
            'learning_style_percentage': 90,
            'current_grade': 17.2,
            'target_grade': 18.5,
            'bio': 'Futur ingénieur en informatique, passionné de programmation'
        },
        {
            'email': 'nour.ben.salem@email.com',
            'password': 'demo123',
            'first_name': 'Nour',
            'last_name': 'Ben Salem',
            'academic_level': AcademicLevel.PREMIERE,
            'specialties': ['Physique-Chimie', 'Mathématiques', 'SVT'],
            'learning_style': LearningStyle.VISUAL,
            'learning_style_percentage': 75,
            'current_grade': 14.5,
            'target_grade': 16.0,
            'bio': 'Intéressée par la médecine et les sciences de la vie'
        }
    ]

    for student_data in students_data:
        # Créer l'utilisateur
        student = User(
            email=student_data['email'],
            password=student_data['password'],
            first_name=student_data['first_name'],
            last_name=student_data['last_name'],
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE,
            email_verified=True
        )
        db.session.add(student)
        db.session.flush()  # Pour obtenir l'ID

        # Créer le profil étudiant
        student_profile = StudentProfile(
            user_id=student.id,
            academic_level=student_data['academic_level'],
            specialties=student_data['specialties'],
            learning_style=student_data['learning_style'],
            learning_style_percentage=student_data['learning_style_percentage'],
            current_grade=student_data['current_grade'],
            target_grade=student_data['target_grade'],
            bio=student_data['bio']
        )
        db.session.add(student_profile)

    # === PARENTS ===
    parents_data = [
        {
            'email': 'parent.martin@email.com',
            'password': 'demo123',
            'first_name': 'Pierre',
            'last_name': 'Martin',
            'phone': '+216 20 111 222',
            'children_emails': ['sarah.martin@email.com']
        },
        {
            'email': 'parent.benali@email.com',
            'password': 'demo123',
            'first_name': 'Fatma',
            'last_name': 'Ben Ali',
            'phone': '+216 20 333 444',
            'children_emails': ['ahmed.ben.ali@email.com']
        },
        {
            'email': 'parent.dubois@email.com',
            'password': 'demo123',
            'first_name': 'Marie',
            'last_name': 'Dubois',
            'phone': '+216 20 555 666',
            'children_emails': ['lea.dubois@email.com']
        }
    ]

    for parent_data in parents_data:
        parent = User(
            email=parent_data['email'],
            password=parent_data['password'],
            first_name=parent_data['first_name'],
            last_name=parent_data['last_name'],
            phone=parent_data.get('phone'),
            role=UserRole.PARENT,
            status=UserStatus.ACTIVE,
            email_verified=True
        )
        db.session.add(parent)

    # Commit des utilisateurs
    print("💾 Sauvegarde des utilisateurs...")
    db.session.commit()

    # === FORMULES D'ACCOMPAGNEMENT ===
    print("📋 Création des formules d'accompagnement...")

    formulas_data = [
        {
            'name': 'Coaching Premium',
            'type': FormulaType.INDIVIDUAL,
            'price': 320.0,
            'currency': 'TND',
            'duration_weeks': 4,
            'hours_per_week': 1,
            'description': 'Accompagnement individuel premium avec suivi personnalisé',
            'features': [
                '4h de cours particuliers par mois',
                'Accès complet à la plateforme',
                'Reporting hebdomadaire détaillé',
                'Support ARIA 24/7',
                'Fiches personnalisées'
            ],
            'target_audience': 'Élèves souhaitant un accompagnement sur mesure'
        },
        {
            'name': 'Excellence Bac',
            'type': FormulaType.INDIVIDUAL,
            'price': 420.0,
            'currency': 'TND',
            'duration_weeks': 4,
            'hours_per_week': 1.5,
            'description': 'Préparation intensive au Baccalauréat français',
            'features': [
                '6h de cours particuliers par mois',
                'Simulations de Bac personnalisées',
                'Objectifs ciblés par matière',
                'Grand Oral inclus',
                'Correction de copies'
            ],
            'target_audience': 'Terminales visant l\'excellence au Bac'
        },
        {
            'name': 'Groupe Réussite',
            'type': FormulaType.GROUP,
            'price': 180.0,
            'currency': 'TND',
            'duration_weeks': 4,
            'hours_per_week': 0.5,
            'description': 'Mini-groupe de 3-5 élèves de niveau homogène',
            'features': [
                '2h de cours en groupe par semaine',
                'Module en ligne personnalisé',
                'Émulation collective',
                'Tarif avantageux',
                'Suivi individuel dans le groupe'
            ],
            'target_audience': 'Élèves appréciant l\'apprentissage en groupe'
        },
        {
            'name': 'Combo Révision',
            'type': FormulaType.GROUP,
            'price': 290.0,
            'currency': 'TND',
            'duration_weeks': 4,
            'hours_per_week': 1,
            'description': 'Révision intensive en groupe sur 2 matières',
            'features': [
                '2 matières au choix',
                '4h de cours par semaine',
                'Groupes de 3-4 élèves',
                'Méthodes collaboratives',
                'Contrôles réguliers'
            ],
            'target_audience': 'Élèves souhaitant réviser efficacement'
        },
        {
            'name': 'Duo Sciences',
            'type': FormulaType.SPECIALIZED,
            'price': 400.0,
            'currency': 'TND',
            'duration_weeks': 4,
            'hours_per_week': 1,
            'description': 'Maths + NSI en formule hybride optimisée',
            'features': [
                'Maths et NSI combinées',
                'Approche transversale',
                'Projets pratiques',
                'Préparation études supérieures',
                'Portfolio de projets'
            ],
            'target_audience': 'Futurs ingénieurs et développeurs'
        },
        {
            'name': 'Grand Oral',
            'type': FormulaType.SPECIALIZED,
            'price': 390.0,
            'currency': 'TND',
            'duration_weeks': 8,
            'hours_per_week': 0.5,
            'description': 'Préparation complète au Grand Oral du Bac',
            'features': [
                'Méthodologie complète',
                'Entraînements filmés',
                'Feedback détaillé',
                'Gestion du stress',
                'Simulations réelles'
            ],
            'target_audience': 'Terminales préparant le Grand Oral'
        }
    ]

    for formula_data in formulas_data:
        formula = Formula(
            name=formula_data['name'],
            type=formula_data['type'],
            price=formula_data['price'],
            currency=formula_data['currency'],
            duration_weeks=formula_data['duration_weeks'],
            hours_per_week=formula_data['hours_per_week'],
            description=formula_data['description'],
            features=formula_data['features'],
            target_audience=formula_data['target_audience'],
            is_active=True
        )
        db.session.add(formula)

    # === CONTENU PÉDAGOGIQUE ===
    print("📚 Création du contenu pédagogique...")

    # Cours de Mathématiques Terminale
    math_course = Course(
        title='Mathématiques Terminale',
        description='Cours complet de mathématiques pour la classe de Terminale',
        subject='Mathématiques',
        level='Terminale',
        duration_hours=120,
        difficulty_level=8,
        is_published=True
    )
    db.session.add(math_course)
    db.session.flush()

    # Modules du cours de maths
    math_modules = [
        {
            'title': 'Fonctions et Dérivation',
            'description': 'Étude complète des fonctions et de la dérivation',
            'content': 'Module couvrant les fonctions, limites, dérivées et applications',
            'order_index': 1,
            'estimated_duration': 20
        },
        {
            'title': 'Intégration',
            'description': 'Calcul intégral et applications',
            'content': 'Primitives, intégrales définies et applications géométriques',
            'order_index': 2,
            'estimated_duration': 15
        },
        {
            'title': 'Probabilités',
            'description': 'Probabilités et statistiques',
            'content': 'Variables aléatoires, lois de probabilité, statistiques',
            'order_index': 3,
            'estimated_duration': 18
        }
    ]

    for module_data in math_modules:
        module = Module(
            course_id=math_course.id,
            title=module_data['title'],
            description=module_data['description'],
            content=module_data['content'],
            order_index=module_data['order_index'],
            estimated_duration=module_data['estimated_duration'],
            is_published=True
        )
        db.session.add(module)

    # Commit final
    print("💾 Sauvegarde finale...")
    db.session.commit()

    print("✨ Données de démonstration créées avec succès!")
    print("\n📋 Comptes créés:")
    print("👨‍💼 Admin: admin@nexus-reussite.com / admin123")
    print("👨‍🏫 Enseignants: marc.dubois@nexus-reussite.com / teacher123")
    print("👨‍🎓 Étudiants: sarah.martin@email.com / demo123")
    print("👨‍👩‍👧‍👦 Parents: parent.martin@email.com / demo123")


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        init_database()
