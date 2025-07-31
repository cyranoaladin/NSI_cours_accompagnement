import asyncio
import logging
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from services.openai_integration import (
    ConversationContext,
    StudentProfile,
    chat_with_aria,
    create_adaptive_quiz,
    generate_personalized_document,
    openai_service,
)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint pour les routes OpenAI
openai_bp = Blueprint("openai", __name__, url_prefix="/api/openai")


@openai_bp.route("/health", methods=["GET"])
@cross_origin()
def health_check():
    """Vérification de l'état du service OpenAI"""
    try:
        status = {
            "service": "OpenAI Integration",
            "status": "operational" if openai_service.client else "simulation_mode",
            "api_configured": bool(openai_service.api_key),
            "models": {
                "chat": openai_service.model_chat,
                "vision": openai_service.model_vision,
                "embedding": openai_service.model_embedding,
                "image": openai_service.model_image,
            },
            "timestamp": datetime.now().isoformat(),
        }

        return jsonify(status), 200

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur lors de la vérification de santé: {e}")
        return jsonify({"error": "Service unavailable"}), 503


@openai_bp.route("/chat", methods=["POST"])
@cross_origin()
def chat_endpoint():
    """Endpoint principal pour le chat avec ARIA"""
    try:
        data = request.get_json()

        # Validation des données requises
        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400

        message = data["message"]
        student_id = data.get("student_id", "anonymous")

        # Construction du contexte
        context = {
            "session_id": data.get(
                "session_id", f"session_{datetime.now().timestamp()}"
            ),
            "subject": data.get("subject", "général"),
            "topic": data.get("topic"),
            "type": data.get("conversation_type", "tutoring"),
            "difficulty_level": data.get("difficulty", "medium"),
        }

        # Appel asynchrone au service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(
                chat_with_aria(message, student_id, context)
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur dans le chat endpoint: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/chat/advanced", methods=["POST"])
@cross_origin()
def advanced_chat_endpoint():
    """Endpoint avancé pour le chat avec profil étudiant complet"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["message", "student_profile", "context"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        message = data["message"]

        # Construction du profil étudiant
        profile_data = data["student_profile"]
        student_profile = StudentProfile(
            id=profile_data.get("id", "anonymous"),
            name=profile_data.get("name", "Étudiant"),
            level=profile_data.get("level", "terminale"),
            specialties=profile_data.get("specialties", ["général"]),
            learning_style=profile_data.get("learning_style", "mixed"),
            strengths=profile_data.get("strengths", []),
            weaknesses=profile_data.get("weaknesses", []),
            goals=profile_data.get("goals", []),
            preferred_difficulty=profile_data.get("preferred_difficulty", "medium"),
        )

        # Construction du contexte
        context_data = data["context"]
        context = ConversationContext(
            student_id=student_profile.id,
            session_id=context_data.get(
                "session_id", f"session_{datetime.now().timestamp()}"
            ),
            subject=context_data.get("subject", "général"),
            topic=context_data.get("topic"),
            difficulty_level=context_data.get("difficulty_level", "medium"),
            conversation_type=context_data.get("conversation_type", "tutoring"),
            previous_messages=context_data.get("previous_messages", []),
            learning_objectives=context_data.get("learning_objectives", []),
            time_limit=context_data.get("time_limit"),
        )

        # Appel au service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(
                openai_service.chat_with_aria(message, context, student_profile)
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur dans l'advanced chat endpoint: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/document/generate", methods=["POST"])
@cross_origin()
def generate_document_endpoint():
    """Génération de documents pédagogiques personnalisés"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["document_type", "subject", "topic"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        document_type = data["document_type"]
        subject = data["subject"]
        topic = data["topic"]
        student_id = data.get("student_id", "anonymous")

        # Appel au service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(
                generate_personalized_document(
                    document_type, subject, topic, student_id
                )
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur dans la génération de document: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/document/generate/advanced", methods=["POST"])
@cross_origin()
def generate_advanced_document_endpoint():
    """Génération avancée de documents avec profil complet"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["document_type", "subject", "topic", "student_profile"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        document_type = data["document_type"]
        subject = data["subject"]
        topic = data["topic"]
        specifications = data.get("specifications", {})

        # Construction du profil étudiant
        profile_data = data["student_profile"]
        student_profile = StudentProfile(
            id=profile_data.get("id", "anonymous"),
            name=profile_data.get("name", "Étudiant"),
            level=profile_data.get("level", "terminale"),
            specialties=profile_data.get("specialties", [subject.lower()]),
            learning_style=profile_data.get("learning_style", "mixed"),
            strengths=profile_data.get("strengths", []),
            weaknesses=profile_data.get("weaknesses", []),
            goals=profile_data.get("goals", []),
        )

        # Appel au service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(
                openai_service.generate_document(
                    document_type, subject, topic, student_profile, specifications
                )
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur dans la génération avancée de document: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/quiz/generate", methods=["POST"])
@cross_origin()
def generate_quiz_endpoint():
    """Génération de quiz adaptatifs"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["subject", "topic", "difficulty", "num_questions"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        subject = data["subject"]
        topic = data["topic"]
        difficulty = data["difficulty"]
        num_questions = data["num_questions"]
        student_id = data.get("student_id", "anonymous")

        # Validation des valeurs
        if difficulty not in ["easy", "medium", "hard"]:
            return (
                jsonify({"error": "Difficulty must be 'easy', 'medium', or 'hard'"}),
                400,
            )

        if (
            not isinstance(num_questions, int)
            or num_questions < 1
            or num_questions > 20
        ):
            return jsonify({"error": "num_questions must be between 1 and 20"}), 400

        # Appel au service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(
                create_adaptive_quiz(
                    subject, topic, difficulty, num_questions, student_id
                )
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur dans la génération de quiz: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/quiz/generate/advanced", methods=["POST"])
@cross_origin()
def generate_advanced_quiz_endpoint():
    """Génération avancée de quiz avec profil complet"""
    try:
        data = request.get_json()

        # Validation
        required_fields = [
            "subject",
            "topic",
            "difficulty",
            "num_questions",
            "student_profile",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        subject = data["subject"]
        topic = data["topic"]
        difficulty = data["difficulty"]
        num_questions = data["num_questions"]

        # Construction du profil étudiant
        profile_data = data["student_profile"]
        student_profile = StudentProfile(
            id=profile_data.get("id", "anonymous"),
            name=profile_data.get("name", "Étudiant"),
            level=profile_data.get("level", "terminale"),
            specialties=profile_data.get("specialties", [subject.lower()]),
            learning_style=profile_data.get("learning_style", "mixed"),
            strengths=profile_data.get("strengths", []),
            weaknesses=profile_data.get("weaknesses", []),
            goals=profile_data.get("goals", []),
        )

        # Appel au service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(
                openai_service.generate_quiz(
                    subject, topic, difficulty, num_questions, student_profile
                )
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur dans la génération avancée de quiz: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/image/generate", methods=["POST"])
@cross_origin()
def generate_image_endpoint():
    """Génération d'images pédagogiques"""
    try:
        data = request.get_json()

        # Validation
        if not data or "prompt" not in data:
            return jsonify({"error": "Prompt is required"}), 400

        prompt = data["prompt"]
        style = data.get("style", "educational")
        size = data.get("size", "1024x1024")

        # Validation de la taille
        valid_sizes = ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
        if size not in valid_sizes:
            return (
                jsonify({"error": f"Size must be one of: {', '.join(valid_sizes)}"}),
                400,
            )

        # Appel au service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(
                openai_service.generate_image(prompt, style, size)
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur dans la génération d'image: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/analyze/work", methods=["POST"])
@cross_origin()
def analyze_work_endpoint():
    """Analyse du travail d'un étudiant"""
    try:
        data = request.get_json()

        # Validation
        required_fields = [
            "work_content",
            "subject",
            "assignment_type",
            "student_profile",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        work_content = data["work_content"]
        subject = data["subject"]
        assignment_type = data["assignment_type"]

        # Construction du profil étudiant
        profile_data = data["student_profile"]
        student_profile = StudentProfile(
            id=profile_data.get("id", "anonymous"),
            name=profile_data.get("name", "Étudiant"),
            level=profile_data.get("level", "terminale"),
            specialties=profile_data.get("specialties", [subject.lower()]),
            learning_style=profile_data.get("learning_style", "mixed"),
            strengths=profile_data.get("strengths", []),
            weaknesses=profile_data.get("weaknesses", []),
            goals=profile_data.get("goals", []),
        )

        # Appel au service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(
                openai_service.analyze_student_work(
                    work_content, subject, assignment_type, student_profile
                )
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur dans l'analyse de travail: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/usage/stats", methods=["GET"])
@cross_origin()
def usage_stats_endpoint():
    """Statistiques d'utilisation de l'API OpenAI"""
    try:
        stats = openai_service.get_usage_statistics()

        return (
            jsonify(
                {
                    "success": True,
                    "data": stats,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur lors de la récupération des statistiques: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/models/available", methods=["GET"])
@cross_origin()
def available_models_endpoint():
    """Liste des modèles disponibles"""
    try:
        models = {
            "chat": {
                "model": openai_service.model_chat,
                "description": "Modèle principal pour les conversations avec ARIA",
                "capabilities": ["text_generation", "reasoning", "tutoring"],
            },
            "vision": {
                "model": openai_service.model_vision,
                "description": "Modèle pour l'analyse d'images et documents",
                "capabilities": [
                    "image_analysis",
                    "document_reading",
                    "diagram_interpretation",
                ],
            },
            "embedding": {
                "model": openai_service.model_embedding,
                "description": "Modèle pour la recherche sémantique",
                "capabilities": [
                    "text_embedding",
                    "similarity_search",
                    "content_matching",
                ],
            },
            "image": {
                "model": openai_service.model_image,
                "description": "Modèle pour la génération d'images pédagogiques",
                "capabilities": [
                    "image_generation",
                    "educational_diagrams",
                    "illustrations",
                ],
            },
        }

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "models": models,
                        "api_configured": bool(openai_service.api_key),
                        "service_status": (
                            "operational"
                            if openai_service.client
                            else "simulation_mode"
                        ),
                    },
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur lors de la récupération des modèles: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/conversation/context", methods=["POST"])
@cross_origin()
def save_conversation_context():
    """Sauvegarde le contexte de conversation pour la continuité"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["session_id", "student_id", "messages"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        session_id = data["session_id"]
        student_id = data["student_id"]
        messages = data["messages"]
        context_metadata = data.get("metadata", {})

        # En production, sauvegarder en base de données
        # Pour la démo, on simule la sauvegarde
        saved_context = {
            "session_id": session_id,
            "student_id": student_id,
            "messages": messages,
            "metadata": context_metadata,
            "saved_at": datetime.now().isoformat(),
            "status": "saved",
        }

        return (
            jsonify(
                {
                    "success": True,
                    "data": saved_context,
                    "message": "Context saved successfully",
                }
            ),
            200,
        )

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur lors de la sauvegarde du contexte: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/conversation/context/<session_id>", methods=["GET"])
@cross_origin()
def get_conversation_context(session_id):
    """Récupère le contexte de conversation sauvegardé"""
    try:
        # En production, récupérer depuis la base de données
        # Pour la démo, on simule la récupération
        demo_context = {
            "session_id": session_id,
            "student_id": "demo_student",
            "messages": [
                {
                    "role": "assistant",
                    "content": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
                    "timestamp": datetime.now().isoformat(),
                }
            ],
            "metadata": {
                "subject": "mathématiques",
                "topic": "fonctions",
                "difficulty_level": "medium",
            },
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
        }

        return jsonify({"success": True, "data": demo_context, "found": True}), 200

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur lors de la récupération du contexte: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@openai_bp.route("/feedback", methods=["POST"])
@cross_origin()
def submit_feedback():
    """Soumission de feedback sur les réponses d'ARIA"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["session_id", "message_id", "rating"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        session_id = data["session_id"]
        message_id = data["message_id"]
        rating = data["rating"]  # 1-5 stars
        comment = data.get("comment", "")
        student_id = data.get("student_id", "anonymous")

        # Validation du rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5"}), 400

        # En production, sauvegarder en base de données pour améliorer ARIA
        feedback_data = {
            "session_id": session_id,
            "message_id": message_id,
            "student_id": student_id,
            "rating": rating,
            "comment": comment,
            "submitted_at": datetime.now().isoformat(),
            "status": "received",
        }

        return (
            jsonify(
                {
                    "success": True,
                    "data": feedback_data,
                    "message": "Feedback received successfully",
                }
            ),
            200,
        )

    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Erreur lors de la soumission du feedback: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# Gestionnaire d'erreurs pour le blueprint
@openai_bp.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "error": "Endpoint not found",
                "available_endpoints": [
                    "/api/openai/health",
                    "/api/openai/chat",
                    "/api/openai/chat/advanced",
                    "/api/openai/document/generate",
                    "/api/openai/document/generate/advanced",
                    "/api/openai/quiz/generate",
                    "/api/openai/quiz/generate/advanced",
                    "/api/openai/image/generate",
                    "/api/openai/analyze/work",
                    "/api/openai/usage/stats",
                    "/api/openai/models/available",
                ],
            }
        ),
        404,
    )


@openai_bp.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify(
            {
                "error": "Method not allowed",
                "message": "Check the HTTP method for this endpoint",
            }
        ),
        405,
    )


@openai_bp.errorhandler(500)
def internal_error(error):
    return (
        jsonify(
            {
                "error": "Internal server error",
                "message": "An unexpected error occurred",
            }
        ),
        500,
    )
