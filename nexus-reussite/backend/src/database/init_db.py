#!/usr/bin/env python3
"""
Script d'initialisation de la base de données Nexus Réussite
Crée toutes les tables et insère les données de démonstration
"""

import os
import sys
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, db
from models.student import Student, Parent, Teacher, Admin, User
from models.content_system import ContentModule, LearningPath, Quiz, QuizQuestion, StudentProgress
from models.formulas import Formula, Enrollment

def create_demo_users():
    """Créer les utilisateurs de démonstration"""
    print("Création des utilisateurs de démonstration...")

    # Étudiants
    students_data = [
        {
            'email': 'sarah.martin@email.com',
            'password': 'demo123',
            'first_name': 'Sarah',
            'last_name': 'Martin',
            'grade': 'Terminale',
            'specialties': ['Mathématiques', 'NSI', 'Physique'],
            'learning_style': 'Visuel',
            'phone': '+216 20 123 456'
        },
        {
            'email': 'ahmed.ben.ali@email.com',
            'password': 'demo123',
            'first_name': 'Ahmed',
            'last_name': 'Ben Ali',
            'grade': 'Première',
            'specialties': ['Mathématiques', 'Physique'],
            'learning_style': 'Auditif',
            'phone': '+216 20 234 567'
        },
        {
            'email': 'lea.dubois@email.com',
            'password': 'demo123',
            'first_name': 'Léa',
            'last_name': 'Dubois',
            'grade': 'Terminale',
            'specialties': ['Français', 'Philosophie'],
            'learning_style': 'Kinesthésique',
            'phone': '+216 20 345 678'
        },
        {
            'email': 'youssef.trabelsi@email.com',
            'password': 'demo123',
            'first_name': 'Youssef',
            'last_name': 'Trabelsi',
            'grade': 'Terminale',
            'specialties': ['Mathématiques', 'NSI'],
            'learning_style': 'Logique',
            'phone': '+216 20 456 789'
        },
        {
            'email': 'nour.ben.salem@email.com',
            'password': 'demo123',
            'first_name': 'Nour',
            'last_name': 'Ben Salem',
            'grade': 'Première',
            'specialties': ['Physique', 'Mathématiques'],
            'learning_style': 'Visuel',
            'phone': '+216 20 567 890'
        }
    ]

    students = []
    for student_data in students_data:
        student = Student(
            email=student_data['email'],
            password_hash=generate_password_hash(student_data['password']),
            first_name=student_data['first_name'],
            last_name=student_data['last_name'],
            role='student',
            grade=student_data['grade'],
            specialties=student_data['specialties'],
            learning_style=student_data['learning_style'],
            phone=student_data['phone'],
            is_active=True,
            created_at=datetime.utcnow()
        )
        students.append(student)
        db.session.add(student)

    # Parents
    parents_data = [
        {
            'email': 'parent.martin@email.com',
            'password': 'demo123',
            'first_name': 'Pierre',
            'last_name': 'Martin',
            'phone': '+216 70 123 456',
            'children_emails': ['sarah.martin@email.com']
        },
        {
            'email': 'parent.benali@email.com',
            'password': 'demo123',
            'first_name': 'Fatma',
            'last_name': 'Ben Ali',
            'phone': '+216 70 234 567',
            'children_emails': ['ahmed.ben.ali@email.com']
        },
        {
            'email': 'parent.dubois@email.com',
            'password': 'demo123',
            'first_name': 'Marie',
            'last_name': 'Dubois',
            'phone': '+216 70 345 678',
            'children_emails': ['lea.dubois@email.com']
        }
    ]

    parents = []
    for parent_data in parents_data:
        parent = Parent(
            email=parent_data['email'],
            password_hash=generate_password_hash(parent_data['password']),
            first_name=parent_data['first_name'],
            last_name=parent_data['last_name'],
            role='parent',
            phone=parent_data['phone'],
            is_active=True,
            created_at=datetime.utcnow()
        )
        parents.append(parent)
        db.session.add(parent)

    # Enseignants
    teachers_data = [
        {
            'email': 'marc.dubois@nexus-reussite.com',
            'password': 'teacher123',
            'first_name': 'Marc',
            'last_name': 'Dubois',
            'subjects': ['Mathématiques'],
            'qualifications': ['Agrégé de Mathématiques', 'AEFE'],
            'experience_years': 15,
            'phone': '+216 70 111 222',
            'bio': 'Professeur agrégé de mathématiques avec 15 ans d\'expérience dans les établissements AEFE.'
        },
        {
            'email': 'sophie.martin@nexus-reussite.com',
            'password': 'teacher123',
            'first_name': 'Sophie',
            'last_name': 'Martin',
            'subjects': ['NSI', 'Mathématiques'],
            'qualifications': ['Certifiée NSI', 'DIU NSI', 'AEFE'],
            'experience_years': 8,
            'phone': '+216 70 222 333',
            'bio': 'Spécialiste NSI diplômée DIU avec une longue expérience en programmation Python.'
        },
        {
            'email': 'david.rousseau@nexus-reussite.com',
            'password': 'teacher123',
            'first_name': 'David',
            'last_name': 'Rousseau',
            'subjects': ['Physique-Chimie'],
            'qualifications': ['Docteur en Physique', 'AEFE'],
            'experience_years': 12,
            'phone': '+216 70 333 444',
            'bio': 'Docteur en physique, expert en préparation au Grand Oral et aux concours.'
        }
    ]

    teachers = []
    for teacher_data in teachers_data:
        teacher = Teacher(
            email=teacher_data['email'],
            password_hash=generate_password_hash(teacher_data['password']),
            first_name=teacher_data['first_name'],
            last_name=teacher_data['last_name'],
            role='teacher',
            subjects=teacher_data['subjects'],
            qualifications=teacher_data['qualifications'],
            experience_years=teacher_data['experience_years'],
            phone=teacher_data['phone'],
            bio=teacher_data['bio'],
            is_active=True,
            created_at=datetime.utcnow()
        )
        teachers.append(teacher)
        db.session.add(teacher)

    # Administrateur
    admin = Admin(
        email='admin@nexus-reussite.com',
        password_hash=generate_password_hash('admin123'),
        first_name='Admin',
        last_name='Nexus',
        role='admin',
        phone='+216 70 000 000',
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.session.add(admin)

    db.session.commit()
    print(f"✅ {len(students)} étudiants créés")
    print(f"✅ {len(parents)} parents créés")
    print(f"✅ {len(teachers)} enseignants créés")
    print(f"✅ 1 administrateur créé")

    return students, parents, teachers, admin

def create_demo_content():
    """Créer le contenu pédagogique de démonstration"""
    print("Création du contenu pédagogique...")

    # Parcours de mathématiques
    math_path = LearningPath(
        title='Mathématiques Terminale',
        subject='Mathématiques',
        grade='Terminale',
        description='Parcours complet pour maîtriser le programme de Terminale',
        estimated_hours=120,
        difficulty='Avancé',
        created_at=datetime.utcnow()
    )
    db.session.add(math_path)
    db.session.commit()

    # Modules de mathématiques
    math_modules = [
        {
            'title': 'Limites et continuité',
            'description': 'Comprendre les limites de fonctions et la continuité',
            'content_type': 'lesson',
            'estimated_time': 15,
            'order_index': 1,
            'skills': ['Calcul de limites', 'Théorèmes de continuité', 'Asymptotes']
        },
        {
            'title': 'Dérivation',
            'description': 'Maîtriser les techniques de dérivation et leurs applications',
            'content_type': 'lesson',
            'estimated_time': 18,
            'order_index': 2,
            'skills': ['Calcul de dérivées', 'Équations de tangentes', 'Variations de fonctions']
        },
        {
            'title': 'Intégration',
            'description': 'Techniques d\'intégration et calcul d\'aires',
            'content_type': 'lesson',
            'estimated_time': 20,
            'order_index': 3,
            'skills': ['Calcul de primitives', 'Intégration par parties', 'Calcul d\'aires']
        }
    ]

    modules = []
    for module_data in math_modules:
        module = ContentModule(
            title=module_data['title'],
            description=module_data['description'],
            content_type=module_data['content_type'],
            subject='Mathématiques',
            grade='Terminale',
            estimated_time=module_data['estimated_time'],
            order_index=module_data['order_index'],
            skills=module_data['skills'],
            learning_path_id=math_path.id,
            created_at=datetime.utcnow()
        )
        modules.append(module)
        db.session.add(module)

    db.session.commit()

    # Quiz de démonstration
    quiz = Quiz(
        title='Quiz Limites et Continuité',
        subject='Mathématiques',
        grade='Terminale',
        description='Évaluation des connaissances sur les limites',
        time_limit=30,
        total_points=20,
        module_id=modules[0].id,
        created_at=datetime.utcnow()
    )
    db.session.add(quiz)
    db.session.commit()

    # Questions du quiz
    questions = [
        {
            'question': 'Quelle est la limite de (x²-1)/(x-1) quand x tend vers 1 ?',
            'options': ['0', '1', '2', 'La limite n\'existe pas'],
            'correct_answer': 2,
            'explanation': 'En factorisant le numérateur : (x²-1)/(x-1) = (x+1)(x-1)/(x-1) = x+1. Donc lim(x→1) = 1+1 = 2'
        },
        {
            'question': 'Une fonction continue sur [a,b] est nécessairement :',
            'options': ['Dérivable', 'Bornée', 'Croissante', 'Constante'],
            'correct_answer': 1,
            'explanation': 'D\'après le théorème des valeurs intermédiaires, une fonction continue sur un segment est bornée.'
        }
    ]

    for i, q_data in enumerate(questions):
        question = QuizQuestion(
            quiz_id=quiz.id,
            question=q_data['question'],
            options=q_data['options'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            points=10,
            order_index=i+1
        )
        db.session.add(question)

    db.session.commit()
    print(f"✅ 1 parcours d'apprentissage créé")
    print(f"✅ {len(modules)} modules créés")
    print(f"✅ 1 quiz avec {len(questions)} questions créé")

def create_demo_formulas():
    """Créer les formules de démonstration"""
    print("Création des formules...")

    formulas_data = [
        {
            'name': 'Coaching Premium',
            'type': 'individual',
            'description': 'Suivi individualisé toutes matières avec coach dédié',
            'price': 320,
            'currency': 'TND',
            'duration_months': 1,
            'features': [
                '4h de cours par mois',
                'Accès plateforme 24/7',
                'Reporting hebdomadaire',
                'Coach dédié',
                'Suivi personnalisé'
            ]
        },
        {
            'name': 'Excellence Bac',
            'type': 'individual',
            'description': 'Préparation Bac intensifiée avec objectifs ciblés',
            'price': 420,
            'currency': 'TND',
            'duration_months': 1,
            'features': [
                '6h de cours par mois',
                'Fiche objectifs personnalisée',
                'Simulations d\'examen',
                'Correction détaillée',
                'Suivi progression'
            ]
        },
        {
            'name': 'Groupe Réussite',
            'type': 'group',
            'description': 'Séances hebdomadaires en présentiel sur une matière',
            'price': 180,
            'currency': 'TND',
            'duration_months': 1,
            'features': [
                '2h par semaine',
                'Groupes de 3-5 élèves',
                'Module en ligne inclus',
                'Exercices corrigés',
                'Émulation de groupe'
            ]
        }
    ]

    formulas = []
    for formula_data in formulas_data:
        formula = Formula(
            name=formula_data['name'],
            type=formula_data['type'],
            description=formula_data['description'],
            price=formula_data['price'],
            currency=formula_data['currency'],
            duration_months=formula_data['duration_months'],
            features=formula_data['features'],
            is_active=True,
            created_at=datetime.utcnow()
        )
        formulas.append(formula)
        db.session.add(formula)

    db.session.commit()
    print(f"✅ {len(formulas)} formules créées")

def create_demo_progress():
    """Créer les données de progression de démonstration"""
    print("Création des données de progression...")

    # Récupérer les étudiants et modules
    students = Student.query.all()
    modules = ContentModule.query.all()

    if not students or not modules:
        print("⚠️ Aucun étudiant ou module trouvé pour créer la progression")
        return

    # Créer des progressions pour Sarah (étudiant avancé)
    sarah = next((s for s in students if s.first_name == 'Sarah'), None)
    if sarah and modules:
        for i, module in enumerate(modules[:2]):  # 2 premiers modules terminés
            progress = StudentProgress(
                student_id=sarah.id,
                module_id=module.id,
                status='completed',
                progress_percentage=100,
                time_spent=module.estimated_time * 60,  # en minutes
                last_accessed=datetime.utcnow() - timedelta(days=i+1),
                completed_at=datetime.utcnow() - timedelta(days=i)
            )
            db.session.add(progress)

        # Module en cours
        if len(modules) > 2:
            progress = StudentProgress(
                student_id=sarah.id,
                module_id=modules[2].id,
                status='in_progress',
                progress_percentage=65,
                time_spent=modules[2].estimated_time * 60 * 0.65,
                last_accessed=datetime.utcnow()
            )
            db.session.add(progress)

    # Créer des progressions pour Ahmed (étudiant débutant)
    ahmed = next((s for s in students if s.first_name == 'Ahmed'), None)
    if ahmed and modules:
        progress = StudentProgress(
            student_id=ahmed.id,
            module_id=modules[0].id,
            status='in_progress',
            progress_percentage=30,
            time_spent=modules[0].estimated_time * 60 * 0.3,
            last_accessed=datetime.utcnow()
        )
        db.session.add(progress)

    db.session.commit()
    print("✅ Données de progression créées")

def init_database():
    """Initialiser complètement la base de données"""
    print("🚀 Initialisation de la base de données Nexus Réussite...")

    with app.app_context():
        # Supprimer toutes les tables existantes
        print("Suppression des tables existantes...")
        db.drop_all()

        # Créer toutes les tables
        print("Création des nouvelles tables...")
        db.create_all()

        # Créer les données de démonstration
        create_demo_users()
        create_demo_content()
        create_demo_formulas()
        create_demo_progress()

        print("\n✅ Base de données initialisée avec succès !")
        print("\n📋 Comptes de démonstration créés :")
        print("👨‍🎓 Étudiants :")
        print("  - sarah.martin@email.com / demo123")
        print("  - ahmed.ben.ali@email.com / demo123")
        print("  - lea.dubois@email.com / demo123")
        print("  - youssef.trabelsi@email.com / demo123")
        print("  - nour.ben.salem@email.com / demo123")
        print("\n👨‍👩‍👧‍👦 Parents :")
        print("  - parent.martin@email.com / demo123")
        print("  - parent.benali@email.com / demo123")
        print("  - parent.dubois@email.com / demo123")
        print("\n👨‍🏫 Enseignants :")
        print("  - marc.dubois@nexus-reussite.com / teacher123")
        print("  - sophie.martin@nexus-reussite.com / teacher123")
        print("  - david.rousseau@nexus-reussite.com / teacher123")
        print("\n👨‍💼 Administrateur :")
        print("  - admin@nexus-reussite.com / admin123")

if __name__ == '__main__':
    init_database()

