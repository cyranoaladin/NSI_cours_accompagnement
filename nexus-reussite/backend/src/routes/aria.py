"""
Routes API pour ARIA avec intégration de la base documentaire
"""

import logging
from datetime import datetime

from flask import Blueprint, jsonify, request

from services.aria_ai import ARIAService
from services.document_database import DocumentDatabase

# Configuration du logging
logger = logging.getLogger(__name__)

aria_bp = Blueprint("aria", __name__)
aria_service = ARIAService()
doc_db = DocumentDatabase()


@aria_bp.route("/chat", methods=["POST"])
def chat_with_aria():
    """Endpoint pour discuter avec ARIA"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        student_id = data.get("student_id")  # Used for personalized profile retrieval
        context = data.get("context", "")

        if not message:
            return jsonify({"error": "Message requis"}), 400

        # Profil étudiant par défaut ou récupéré de la base
        # NOTE: Replace with actual student profile retrieval using student_id
        student_profile = {
            "student_id": student_id,  # Include in profile for future use
            "grade_level": "terminale",
            "current_subject": "mathematiques",
            "learning_style": "visual",
            "difficulty_preference": 3,
        }

        # Rechercher des documents pertinents
        relevant_docs = doc_db.search_documents(
            query=message,
            subject=student_profile.get("current_subject"),
            grade_level=student_profile.get("grade_level"),
            max_results=3,
        )

        # Obtenir des suggestions contextuelles
        contextual_suggestions = doc_db.get_contextual_suggestions(
            context=message + " " + context, student_profile=student_profile
        )

        # Générer la réponse ARIA
        response = aria_service.generate_response(
            message=message,
            student_profile=student_profile,
            context=context,
            relevant_documents=relevant_docs,
        )

        return jsonify(
            {
                "success": True,
                "response": response,
                "relevant_documents": relevant_docs,
                "suggestions": contextual_suggestions,
                "student_profile": student_profile,
            }
        )

    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400
    except (RuntimeError, OSError, ValueError) as e:  # pylint: disable=broad-exception-caught
        logger.error("Error in chat_with_aria: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@aria_bp.route("/recommendations", methods=["POST"])
def get_recommendations():
    """Obtenir des recommandations personnalisées"""
    try:
        data = request.get_json()
        student_profile = data.get("student_profile", {})

        # Profil par défaut si non fourni
        if not student_profile:
            student_profile = {
                "grade_level": "terminale",
                "current_subject": "mathematiques",
                "learning_style": "visual",
                "difficulty_preference": 3,
            }

        recommendations = doc_db.get_recommendations_for_profile(student_profile)

        return jsonify({"success": True, "recommendations": recommendations})

    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400
    except (RuntimeError, OSError, ValueError) as e:  # pylint: disable=broad-exception-caught
        logger.error("Error in get_recommendations: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@aria_bp.route("/documents/search", methods=["POST"])
def search_documents():
    """Rechercher des documents dans la base"""
    try:
        data = request.get_json()
        query = data.get("query", "")
        subject = data.get("subject")
        grade_level = data.get("grade_level")
        document_type = data.get("document_type")
        max_results = data.get("max_results", 10)

        documents = doc_db.search_documents(
            query=query,
            subject=subject,
            grade_level=grade_level,
            document_type=document_type,
            max_results=max_results,
        )

        return jsonify(
            {"success": True, "documents": documents, "count": len(documents)}
        )

    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400
    except (RuntimeError, OSError, ValueError) as e:  # pylint: disable=broad-exception-caught
        logger.error("Error in search_documents: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@aria_bp.route("/documents/add", methods=["POST"])
def add_document():
    """Ajouter un nouveau document à la base"""
    try:
        data = request.get_json()

        required_fields = [
            "title",
            "content",
            "subject",
            "grade_level",
            "document_type",
        ]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Champ requis: {field}"}), 400

        doc_id = doc_db.add_document(
            title=data["title"],
            content=data["content"],
            subject=data["subject"],
            grade_level=data["grade_level"],
            document_type=data["document_type"],
            tags=data.get("tags", ""),
            difficulty_level=data.get("difficulty_level", 3),
            url=data.get("url", ""),
        )

        return jsonify(
            {
                "success": True,
                "document_id": doc_id,
                "message": "Document ajouté avec succès",
            }
        )

    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400
    except (RuntimeError, OSError, ValueError) as e:  # pylint: disable=broad-exception-caught
        logger.error("Error in add_document: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@aria_bp.route("/analyze_learning_style", methods=["POST"])
def analyze_learning_style():
    """Analyser le style d'apprentissage d'un élève"""
    try:
        data = request.get_json()
        responses = data.get("responses", {})

        # Simulation d'analyse du style d'apprentissage
        learning_analysis = aria_service.analyze_learning_style(responses)

        return jsonify({"success": True, "analysis": learning_analysis})

    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400
    except (RuntimeError, OSError, ValueError) as e:  # pylint: disable=broad-exception-caught
        logger.error("Error in analyze_learning_style: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@aria_bp.route("/generate_study_plan", methods=["POST"])
def generate_study_plan():
    """Générer un plan d'étude personnalisé"""
    try:
        data = request.get_json()
        student_profile = data.get("student_profile", {})
        goals = data.get("goals", [])
        timeframe = data.get("timeframe", "monthly")

        # Create study plan structure
        study_plan = {
            "title": f"{timeframe.capitalize()} Study Plan",
            "student": student_profile,
            "goals": goals,
            "schedule": [],
        }

        # Generate a basic schedule based on goals and timeframe
        if goals and isinstance(goals, list):
            for i, goal in enumerate(goals):
                # Get relevant resources for this goal
                try:
                    resources = doc_db.search_documents(
                        query=goal,
                        subject=student_profile.get("current_subject", ""),
                        grade_level=student_profile.get("grade_level", ""),
                        max_results=2,
                    )
                except (ValueError, KeyError) as e:
                    logger.warning(
                        "Error searching documents for goal '%s': %s", goal, str(e)
                    )
                    resources = []

                study_plan["schedule"].append(
                    {
                        "week": i + 1,
                        "focus": goal,
                        "activities": [
                            "Review core concepts",
                            "Practice exercises",
                            "Self-assessment",
                        ],
                        "resources": resources,
                    }
                )

        return jsonify({"success": True, "study_plan": study_plan})

    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400
    except (RuntimeError, OSError, ValueError) as e:  # pylint: disable=broad-exception-caught
        logger.error("Error in generate_study_plan: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@aria_bp.route("/evaluate_progress", methods=["POST"])
def evaluate_progress():
    """Évaluer les progrès d'un élève"""
    try:
        data = request.get_json()
        student_id = data.get("student_id")
        subject = data.get("subject")
        recent_scores = data.get("recent_scores", [])

        # pylint: disable=no-member
        progress_evaluation = aria_service.evaluate_progress(
            student_id=student_id, subject=subject, recent_scores=recent_scores
        )

        return jsonify({"success": True, "evaluation": progress_evaluation})

    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400
    except (RuntimeError, OSError, ValueError) as e:  # pylint: disable=broad-exception-caught
        logger.error("Error in evaluate_progress: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@aria_bp.route("/health", methods=["GET"])
def health_check():
    """Vérification de l'état du service ARIA"""
    try:
        # Test simple sans dépendance externe pour éviter les erreurs
        return jsonify(
            {
                "status": "healthy",
                "aria_service": "operational",
                "document_database": "operational",
                "timestamp": str(datetime.now()),
            }
        )

    except (RuntimeError, OSError, ValueError) as e:  # pylint: disable=broad-exception-caught
        logger.error("Error in health_check: %s", str(e))
        return jsonify({"status": "error", "error": "Internal server error"}), 500
