"""
Service de base de données documentaire pour ARIA
Permet à l'IA d'accéder à une base de connaissances structurée
"""

import json
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

class DocumentDatabase:
    def __init__(self, db_path: str = "documents.db"):
        self.db_path = db_path
        self.init_database()
        self.populate_sample_data()

    def init_database(self):
        """Initialise la base de données documentaire"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table des documents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                subject TEXT NOT NULL,
                grade_level TEXT NOT NULL,
                document_type TEXT NOT NULL,
                tags TEXT,
                difficulty_level INTEGER,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Table des liens utiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS useful_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT,
                subject TEXT NOT NULL,
                grade_level TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Table des exercices
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                solution TEXT,
                subject TEXT NOT NULL,
                grade_level TEXT NOT NULL,
                difficulty_level INTEGER,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def populate_sample_data(self):
        """Peuple la base avec des données d'exemple"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Vérifier si des données existent déjà
        cursor.execute("SELECT COUNT(*) FROM documents")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return

        # Documents d'exemple
        sample_documents = [
            {
                "title": "Fonctions Exponentielles - Cours Complet",
                "content": "Les fonctions exponentielles sont fondamentales en Terminale. Propriétés : exp(a+b) = exp(a)×exp(b), dérivée de exp(x) = exp(x), limite en +∞...",
                "subject": "mathematiques",
                "grade_level": "terminale",
                "document_type": "cours",
                "tags": "exponentielles,derivees,limites",
                "difficulty_level": 3,
                "url": "/documents/maths/exponentielles-cours.pdf"
            },
            {
                "title": "Algorithmes de Tri - Python",
                "content": "Implémentation des algorithmes de tri en Python : tri par sélection, tri par insertion, tri rapide. Complexité temporelle et spatiale.",
                "subject": "nsi",
                "grade_level": "terminale",
                "document_type": "cours",
                "tags": "algorithmes,tri,python,complexite",
                "difficulty_level": 4,
                "url": "/documents/nsi/algorithmes-tri.py"
            },
            {
                "title": "Mécanique Quantique - Introduction",
                "content": "Principes de base de la mécanique quantique : dualité onde-particule, principe d'incertitude, équation de Schrödinger simplifiée.",
                "subject": "physique",
                "grade_level": "terminale",
                "document_type": "cours",
                "tags": "quantique,onde,particule,schrodinger",
                "difficulty_level": 5,
                "url": "/documents/physique/mecanique-quantique.pdf"
            },
            {
                "title": "Méthodologie Dissertation Français",
                "content": "Structure d'une dissertation : introduction avec accroche, problématique, plan ; développement en 3 parties ; conclusion avec ouverture.",
                "subject": "francais",
                "grade_level": "premiere",
                "document_type": "methodologie",
                "tags": "dissertation,methodologie,plan,argumentation",
                "difficulty_level": 2,
                "url": "/documents/francais/methodologie-dissertation.pdf"
            }
        ]

        for doc in sample_documents:
            cursor.execute('''
                INSERT INTO documents (title, content, subject, grade_level, document_type, tags, difficulty_level, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (doc["title"], doc["content"], doc["subject"], doc["grade_level"],
                  doc["document_type"], doc["tags"], doc["difficulty_level"], doc["url"]))

        # Liens utiles d'exemple
        sample_links = [
            {
                "title": "Khan Academy - Mathématiques",
                "url": "https://fr.khanacademy.org/math",
                "description": "Cours interactifs et exercices en mathématiques",
                "subject": "mathematiques",
                "grade_level": "tous",
                "category": "plateforme_apprentissage"
            },
            {
                "title": "France IOI - Programmation",
                "url": "http://www.france-ioi.org/",
                "description": "Plateforme d'apprentissage de la programmation",
                "subject": "nsi",
                "grade_level": "tous",
                "category": "exercices_en_ligne"
            },
            {
                "title": "PhET Simulations",
                "url": "https://phet.colorado.edu/fr/",
                "description": "Simulations interactives en physique et chimie",
                "subject": "physique",
                "grade_level": "tous",
                "category": "simulation"
            }
        ]

        for link in sample_links:
            cursor.execute('''
                INSERT INTO useful_links (title, url, description, subject, grade_level, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (link["title"], link["url"], link["description"],
                  link["subject"], link["grade_level"], link["category"]))

        # Exercices d'exemple
        sample_exercises = [
            {
                "title": "Dérivée de fonctions composées",
                "content": "Calculer la dérivée de f(x) = ln(x² + 1)",
                "solution": "f'(x) = (2x)/(x² + 1) en utilisant la dérivée de ln(u) = u'/u",
                "subject": "mathematiques",
                "grade_level": "terminale",
                "difficulty_level": 3,
                "tags": "derivees,logarithme,fonctions_composees"
            },
            {
                "title": "Algorithme de recherche dichotomique",
                "content": "Implémenter une fonction de recherche dichotomique dans un tableau trié",
                "solution": "def recherche_dichotomique(tab, x): ...",
                "subject": "nsi",
                "grade_level": "terminale",
                "difficulty_level": 3,
                "tags": "algorithmes,recherche,dichotomie"
            }
        ]

        for exercise in sample_exercises:
            cursor.execute('''
                INSERT INTO exercises (title, content, solution, subject, grade_level, difficulty_level, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (exercise["title"], exercise["content"], exercise["solution"],
                  exercise["subject"], exercise["grade_level"], exercise["difficulty_level"], exercise["tags"]))

        conn.commit()
        conn.close()

    def search_documents(self, query: str, subject: str = None, grade_level: str = None,
                        document_type: str = None, max_results: int = 10) -> List[Dict]:
        """Recherche des documents selon les critères"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        sql = "SELECT * FROM documents WHERE (title LIKE ? OR content LIKE ? OR tags LIKE ?)"
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]

        if subject:
            sql += " AND subject = ?"
            params.append(subject)

        if grade_level:
            sql += " AND grade_level = ?"
            params.append(grade_level)

        if document_type:
            sql += " AND document_type = ?"
            params.append(document_type)

        sql += " ORDER BY difficulty_level ASC LIMIT ?"
        params.append(max_results)

        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()

        # Convertir en dictionnaires
        columns = ["id", "title", "content", "subject", "grade_level", "document_type",
                  "tags", "difficulty_level", "url", "created_at"]
        return [dict(zip(columns, row)) for row in results]

    def get_recommendations_for_profile(self, student_profile: Dict) -> Dict:
        """Génère des recommandations basées sur le profil de l'élève"""
        subject = student_profile.get("current_subject", "mathematiques")
        grade_level = student_profile.get("grade_level", "terminale")
        difficulty = student_profile.get("difficulty_preference", 3)
        learning_style = student_profile.get("learning_style", "visual")

        recommendations = {
            "documents": [],
            "exercises": [],
            "links": []
        }

        # Documents recommandés
        documents = self.search_documents("", subject=subject, grade_level=grade_level, max_results=5)
        recommendations["documents"] = documents

        # Exercices adaptés au niveau
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM exercises
            WHERE subject = ? AND grade_level = ? AND difficulty_level <= ?
            ORDER BY difficulty_level ASC LIMIT 3
        ''', (subject, grade_level, difficulty))

        exercise_results = cursor.fetchall()
        exercise_columns = ["id", "title", "content", "solution", "subject", "grade_level",
                           "difficulty_level", "tags", "created_at"]
        recommendations["exercises"] = [dict(zip(exercise_columns, row)) for row in exercise_results]

        # Liens utiles
        cursor.execute('''
            SELECT * FROM useful_links
            WHERE subject = ? OR grade_level = 'tous'
            LIMIT 3
        ''', (subject,))

        link_results = cursor.fetchall()
        link_columns = ["id", "title", "url", "description", "subject", "grade_level",
                       "category", "created_at"]
        recommendations["links"] = [dict(zip(link_columns, row)) for row in link_results]

        conn.close()
        return recommendations

    def add_document(self, title: str, content: str, subject: str, grade_level: str,
                    document_type: str, tags: str = "", difficulty_level: int = 3, url: str = "") -> int:
        """Ajoute un nouveau document à la base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO documents (title, content, subject, grade_level, document_type, tags, difficulty_level, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, subject, grade_level, document_type, tags, difficulty_level, url))

        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return doc_id

    def get_contextual_suggestions(self, context: str, student_profile: Dict) -> List[Dict]:
        """Suggestions contextuelles basées sur la conversation en cours"""
        subject = student_profile.get("current_subject", "mathematiques")
        grade_level = student_profile.get("grade_level", "terminale")

        # Analyser le contexte pour extraire des mots-clés
        keywords = context.lower().split()

        suggestions = []
        for keyword in keywords:
            if len(keyword) > 3:  # Ignorer les mots trop courts
                docs = self.search_documents(keyword, subject=subject, grade_level=grade_level, max_results=2)
                suggestions.extend(docs)

        # Supprimer les doublons
        seen_ids = set()
        unique_suggestions = []
        for doc in suggestions:
            if doc["id"] not in seen_ids:
                unique_suggestions.append(doc)
                seen_ids.add(doc["id"])

        return unique_suggestions[:5]  # Limiter à 5 suggestions

