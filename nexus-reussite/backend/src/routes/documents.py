import asyncio
import io
import json
import logging
from datetime import datetime
from typing import Any, Dict

from flask import Blueprint, jsonify, request, send_file
from flask_cors import cross_origin

from services.content_engine import content_engine
from services.openai_integration import StudentProfile, openai_service
from services.pdf_generator import (
    DocumentMetadata,
    create_evaluation_report_pdf,
    create_exercise_sheet_pdf,
    create_progress_report_pdf,
    create_revision_sheet_pdf,
    pdf_generator,
)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint pour les routes de documents
documents_bp = Blueprint("documents", __name__, url_prefix="/api/documents")


@documents_bp.route("/health", methods=["GET"])
@cross_origin()
def health_check():
    """Vérification de l'état du service de génération de documents"""
    try:
        status = {
            "service": "Document Generation",
            "status": "operational",
            "pdf_generator": "available",
            "content_engine": "available",
            "supported_formats": ["PDF"],
            "supported_types": [
                "revision_sheet",
                "exercise_sheet",
                "evaluation_report",
                "progress_report",
                "custom_document",
            ],
            "timestamp": datetime.now().isoformat(),
        }

        return jsonify(status), 200

    except (ValueError, TypeError, RuntimeError):
        logger.error("Erreur lors de la vérification de santé: {e}")
        return jsonify({"error": "Service unavailable"}), 503


@documents_bp.route("/generate/revision-sheet", methods=["POST"])
@cross_origin()
def generate_revision_sheet():
    """Génère une fiche de révision personnalisée"""
    try:
        data = request.get_json()

        # Validation des données requises
        required_fields = ["subject", "topic", "student_name"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        subject = data["subject"]
        topic = data["topic"]
        student_name = data["student_name"]
        student_level = data.get("student_level", "Terminale")

        # Génération du contenu avec l'IA si disponible
        if openai_service.client:
            try:
                # Construction du profil étudiant
                student_profile = StudentProfile(
                    id=data.get("student_id", "anonymous"),
                    name=student_name,
                    level=student_level,
                    specialties=[subject.lower()],
                    learning_style=data.get("learning_style", "mixed"),
                )

                # Génération du contenu avec OpenAI
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    ai_content = loop.run_until_complete(
                        openai_service.generate_document(
                            "revision_sheet", subject, topic, student_profile
                        )
                    )

                    # Extraction du contenu structuré
                    if "structured_content" in ai_content:
                        content = ai_content["structured_content"]
                    else:
                        # Fallback: structure basique
                        content = {
                            "title": f"Fiche de révision - {topic}",
                            "objectives": [f"Maîtriser les concepts clés de {topic}"],
                            "definitions": {},
                            "key_points": [
                                ai_content.get("content", "Contenu généré par IA")
                            ],
                            "examples": [],
                            "tips": [
                                "Relire régulièrement",
                                "Faire des exercices d'application",
                            ],
                        }

                finally:
                    loop.close()

            except (RuntimeError, OSError, ValueError):
                logger.warning("Erreur IA, utilisation du contenu par défaut: {e}")
                content = _get_default_revision_content(subject, topic)
        else:
            # Utilisation du moteur de contenu par défaut
            content = content_engine.generate_revision_sheet_content(
                subject, topic, student_level
            )

        # Génération du PDF
        pdf_bytes = create_revision_sheet_pdf(content, student_name, subject, topic)

        # Création d'un buffer pour l'envoi
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)

        # Nom du fichier
        filename = f"fiche_revision_{subject}_{topic}_{student_name}.pdf".replace(
            " ", "_"
        )

        return send_file(
            pdf_buffer,
            mimetype="application/pd",
            as_attachment=True,
            download_name=filename,
        )

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error("Erreur lors de la génération de fiche de révision: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@documents_bp.route("/generate/exercise-sheet", methods=["POST"])
@cross_origin()
def generate_exercise_sheet():
    """Génère une feuille d'exercices personnalisée"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["subject", "topic", "student_name"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        subject = data["subject"]
        topic = data["topic"]
        student_name = data["student_name"]
        difficulty = data.get("difficulty", "medium")
        num_exercises = data.get("num_exercises", 5)

        # Génération du contenu
        if openai_service.client:
            try:
                student_profile = StudentProfile(
                    id=data.get("student_id", "anonymous"),
                    name=student_name,
                    level=data.get("student_level", "Terminale"),
                    specialties=[subject.lower()],
                    preferred_difficulty=difficulty,
                )

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    ai_content = loop.run_until_complete(
                        openai_service.generate_document(
                            "exercise_sheet",
                            subject,
                            topic,
                            student_profile,
                            {"num_exercises": num_exercises, "difficulty": difficulty},
                        )
                    )

                    if "structured_content" in ai_content:
                        content = ai_content["structured_content"]
                    else:
                        content = _get_default_exercise_content(
                            subject, topic, difficulty, num_exercises
                        )

                finally:
                    loop.close()

            except (RuntimeError, OSError, ValueError):
                logger.warning("Erreur IA, utilisation du contenu par défaut: {e}")
                content = _get_default_exercise_content(
                    subject, topic, difficulty, num_exercises
                )
        else:
            content = content_engine.generate_exercise_sheet_content(
                subject, topic, difficulty, num_exercises
            )

        # Génération du PDF
        pdf_bytes = create_exercise_sheet_pdf(content, student_name, subject, topic)

        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)

        filename = f"exercices_{subject}_{topic}_{student_name}.pdf".replace(" ", "_")

        return send_file(
            pdf_buffer,
            mimetype="application/pd",
            as_attachment=True,
            download_name=filename,
        )

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error("Erreur lors de la génération d'exercices: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@documents_bp.route("/generate/evaluation-report", methods=["POST"])
@cross_origin()
def generate_evaluation_report():
    """Génère un rapport d'évaluation personnalisé"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["student_name", "subject", "evaluation_data"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        student_name = data["student_name"]
        subject = data["subject"]
        evaluation_data = data["evaluation_data"]

        # Génération du contenu du rapport
        if openai_service.client:
            try:
                student_profile = StudentProfile(
                    id=data.get("student_id", "anonymous"),
                    name=student_name,
                    level=data.get("student_level", "Terminale"),
                    specialties=[subject.lower()],
                )

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    ai_content = loop.run_until_complete(
                        openai_service.analyze_student_work(
                            json.dumps(evaluation_data),
                            subject,
                            "evaluation",
                            student_profile,
                        )
                    )

                    # Structuration du contenu pour le PDF
                    content = {
                        "title": f"Rapport d'évaluation - {subject}",
                        "summary": ai_content.get("summary", "Analyse de l'évaluation"),
                        "overall_results": ai_content.get("detailed_analysis", {}),
                        "strengths": ai_content.get("strengths", []),
                        "improvements": ai_content.get("areas_for_improvement", []),
                        "recommendations": ai_content.get("recommendations", []),
                    }

                finally:
                    loop.close()

            except (RuntimeError, OSError, ValueError):
                logger.warning("Erreur IA, utilisation du contenu par défaut: {e}")
                content = _get_default_evaluation_content(evaluation_data, subject)
        else:
            content = _get_default_evaluation_content(evaluation_data, subject)

        # Génération du PDF
        pdf_bytes = create_evaluation_report_pdf(content, student_name, subject)

        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)

        filename = f"rapport_evaluation_{subject}_{student_name}.pdf".replace(" ", "_")

        return send_file(
            pdf_buffer,
            mimetype="application/pd",
            as_attachment=True,
            download_name=filename,
        )

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error("Erreur lors de la génération du rapport d'évaluation: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@documents_bp.route("/generate/progress-report", methods=["POST"])
@cross_origin()
def generate_progress_report():
    """Génère un rapport de progression pour les parents"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["student_name", "progress_data"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        student_name = data["student_name"]
        progress_data = data["progress_data"]

        # Enrichissement du rapport avec l'IA si disponible
        if openai_service.client:
            try:
                student_profile = StudentProfile(
                    id=data.get("student_id", "anonymous"),
                    name=student_name,
                    level=data.get("student_level", "Terminale"),
                )

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Génération d'insights avec l'IA
                    ai_insights = loop.run_until_complete(
                        openai_service.generate_document(
                            "progress_report",
                            "général",
                            "progression",
                            student_profile,
                            {"progress_data": progress_data},
                        )
                    )

                    # Enrichissement des données de progression
                    if "structured_content" in ai_insights:
                        ai_content = ai_insights["structured_content"]
                        progress_data.update(
                            {
                                "overview": ai_content.get(
                                    "overview", progress_data.get("overview", "")
                                ),
                                "parent_recommendations": ai_content.get(
                                    "parent_recommendations", []
                                ),
                                "next_steps": ai_content.get("next_steps", []),
                            }
                        )

                finally:
                    loop.close()

            except (RuntimeError, OSError, ValueError):
                logger.warning("Erreur IA, utilisation des données par défaut: {e}")

        # Génération du PDF
        pdf_bytes = create_progress_report_pdf(progress_data, student_name)

        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)

        filename = f"rapport_progression_{student_name}.pdf".replace(" ", "_")

        return send_file(
            pdf_buffer,
            mimetype="application/pd",
            as_attachment=True,
            download_name=filename,
        )

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error("Erreur lors de la génération du rapport de progression: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@documents_bp.route("/generate/custom", methods=["POST"])
@cross_origin()
def generate_custom_document():
    """Génère un document personnalisé selon les spécifications"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ["document_type", "content", "metadata"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        document_type = data["document_type"]
        content = data["content"]
        metadata_dict = data["metadata"]

        # Construction des métadonnées
        metadata = DocumentMetadata(
            title=metadata_dict.get("title", "Document personnalisé"),
            subject=metadata_dict.get("subject", "Général"),
            student_name=metadata_dict.get("student_name", ""),
            student_level=metadata_dict.get("student_level", ""),
            document_type=document_type,
            topic=metadata_dict.get("topic", ""),
        )

        # Génération selon le type
        if document_type == "revision_sheet":
            pdf_bytes = pdf_generator.generate_revision_sheet(content, metadata)
        elif document_type == "exercise_sheet":
            pdf_bytes = pdf_generator.generate_exercise_sheet(content, metadata)
        elif document_type == "evaluation_report":
            pdf_bytes = pdf_generator.generate_evaluation_report(content, metadata)
        elif document_type == "progress_report":
            pdf_bytes = pdf_generator.generate_progress_report(content, metadata)
        else:
            return (
                jsonify({"error": f"Unsupported document type: {document_type}"}),
                400,
            )

        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)

        filename = f"{document_type}_{metadata.student_name or 'document'}.pdf".replace(
            " ", "_"
        )

        return send_file(
            pdf_buffer,
            mimetype="application/pd",
            as_attachment=True,
            download_name=filename,
        )

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error("Erreur lors de la génération du document personnalisé: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@documents_bp.route("/templates", methods=["GET"])
@cross_origin()
def get_document_templates():
    """Retourne les templates disponibles pour chaque type de document"""
    try:
        templates = {
            "revision_sheet": {
                "name": "Fiche de révision",
                "description": "Fiche synthétique avec définitions, formules et points clés",
                "required_fields": ["subject", "topic", "student_name"],
                "optional_fields": ["student_level", "learning_style"],
                "sections": [
                    "objectives",
                    "prerequisites",
                    "definitions",
                    "formulas",
                    "methods",
                    "examples",
                    "tips",
                    "warnings",
                    "key_points",
                    "further_reading",
                ],
            },
            "exercise_sheet": {
                "name": "Feuille d'exercices",
                "description": "Série d'exercices progressifs avec espaces de réponse",
                "required_fields": ["subject", "topic", "student_name"],
                "optional_fields": ["difficulty", "num_exercises", "duration"],
                "sections": [
                    "instructions",
                    "duration",
                    "total_points",
                    "exercises",
                    "hints",
                ],
            },
            "evaluation_report": {
                "name": "Rapport d'évaluation",
                "description": "Analyse détaillée des performances avec recommandations",
                "required_fields": ["student_name", "subject", "evaluation_data"],
                "optional_fields": ["student_level"],
                "sections": [
                    "summary",
                    "overall_results",
                    "strengths",
                    "improvements",
                    "recommendations",
                    "action_plan",
                ],
            },
            "progress_report": {
                "name": "Rapport de progression",
                "description": "Suivi détaillé de l'évolution de l'élève pour les parents",
                "required_fields": ["student_name", "progress_data"],
                "optional_fields": ["period", "student_level"],
                "sections": [
                    "overview",
                    "subjects_progress",
                    "achieved_goals",
                    "challenges",
                    "parent_recommendations",
                    "next_steps",
                ],
            },
        }

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "templates": templates,
                        "supported_subjects": [
                            "Mathématiques",
                            "NSI",
                            "Physique-Chimie",
                            "Français",
                            "Philosophie",
                            "Histoire-Géographie",
                            "Anglais",
                            "Espagnol",
                            "SVT",
                            "SES",
                        ],
                        "difficulty_levels": ["easy", "medium", "hard"],
                        "student_levels": ["Seconde", "Première", "Terminale"],
                    },
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error("Erreur lors de la récupération des templates: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@documents_bp.route("/preview", methods=["POST"])
@cross_origin()
def preview_document():
    """Génère un aperçu du document sans le télécharger"""
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

        # Génération d'un aperçu du contenu
        if document_type == "revision_sheet":
            preview = {
                "title": f"Fiche de révision - {topic}",
                "sections": [
                    "🎯 Objectifs d'apprentissage",
                    "📚 Prérequis",
                    "📖 Définitions clés",
                    "🧮 Formules importantes",
                    "⚙️ Méthodes et techniques",
                    "💡 Exemples types",
                    "💡 Conseils et astuces",
                    "🔑 Points clés à retenir",
                ],
                "estimated_pages": 2,
            }
        elif document_type == "exercise_sheet":
            preview = {
                "title": f"Exercices - {topic}",
                "sections": [
                    "📋 Instructions",
                    "⏱️ Durée et barème",
                    "📝 Exercices progressifs",
                    "💡 Conseils par exercice",
                ],
                "estimated_pages": 3,
            }
        elif document_type == "evaluation_report":
            preview = {
                "title": "Rapport d'évaluation",
                "sections": [
                    "📊 Résumé exécuti",
                    "📈 Résultats globaux",
                    "✅ Points forts",
                    "📈 Axes d'amélioration",
                    "🎯 Recommandations",
                    "📋 Plan d'action",
                ],
                "estimated_pages": 4,
            }
        elif document_type == "progress_report":
            preview = {
                "title": "Rapport de progression",
                "sections": [
                    "📊 Vue d'ensemble",
                    "📚 Progression par matière",
                    "🎯 Objectifs atteints",
                    "🚀 Défis à relever",
                    "👨‍👩‍👧‍👦 Recommandations parents",
                    "➡️ Prochaines étapes",
                ],
                "estimated_pages": 5,
            }
        else:
            return (
                jsonify({"error": f"Unsupported document type: {document_type}"}),
                400,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "preview": preview,
                        "document_type": document_type,
                        "subject": subject,
                        "topic": topic,
                    },
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error("Erreur lors de la génération de l'aperçu: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# Fonctions utilitaires pour le contenu par défaut
def _get_default_revision_content(subject: str, topic: str) -> Dict[str, Any]:
    """Génère un contenu de révision par défaut"""
    return {
        "title": f"Fiche de révision - {topic}",
        "objectives": [
            f"Comprendre les concepts fondamentaux de {topic}",
            f"Maîtriser les méthodes de résolution en {subject}",
            "Savoir appliquer les connaissances dans des exercices",
        ],
        "definitions": {topic: f"Concept clé en {subject} à maîtriser"},
        "key_points": [
            f"Point essentiel 1 sur {topic}",
            f"Point essentiel 2 sur {topic}",
            f"Point essentiel 3 sur {topic}",
        ],
        "tips": [
            "Relire régulièrement les définitions",
            "Faire des exercices d'application",
            "Créer des schémas de synthèse",
        ],
    }


def _get_default_exercise_content(
    subject: str, topic: str, difficulty: str, num_exercises: int
) -> Dict[str, Any]:
    """Génère un contenu d'exercices par défaut"""
    exercises = []
    for i in range(num_exercises):
        exercises.append(
            {
                "statement": f"Exercice {i+1} sur {topic} - niveau {difficulty}",
                "questions": [
                    f"Question 1 de l'exercice {i+1}",
                    f"Question 2 de l'exercice {i+1}",
                ],
                "points": 4,
                "difficulty": difficulty,
                "hints": [f"Conseil pour l'exercice {i+1}"],
            }
        )

    return {
        "title": f"Exercices - {topic}",
        "instructions": f"Résolvez les exercices suivants sur {topic}",
        "duration": "2 heures",
        "total_points": num_exercises * 4,
        "exercises": exercises,
    }


def _get_default_evaluation_content(
    evaluation_data: Dict, subject: str
) -> Dict[str, Any]:
    """Génère un contenu d'évaluation par défaut"""
    return {
        "title": f"Rapport d'évaluation - {subject}",
        "summary": "Analyse des résultats de l'évaluation",
        "overall_results": {
            "Compréhension": {
                "score": "15/20",
                "comment": "Bonne compréhension générale",
            },
            "Application": {"score": "12/20", "comment": "À améliorer"},
            "Raisonnement": {"score": "14/20", "comment": "Satisfaisant"},
        },
        "strengths": [
            "Bonne maîtrise des concepts de base",
            "Capacité de raisonnement développée",
        ],
        "improvements": [
            "Travailler l'application pratique",
            "Améliorer la rapidité d'exécution",
        ],
        "recommendations": [
            "Faire plus d'exercices d'application",
            "Revoir les méthodes de résolution",
        ],
    }


# Gestionnaires d'erreurs
@documents_bp.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "error": "Endpoint not found",
                "available_endpoints": [
                    "/api/documents/health",
                    "/api/documents/generate/revision-sheet",
                    "/api/documents/generate/exercise-sheet",
                    "/api/documents/generate/evaluation-report",
                    "/api/documents/generate/progress-report",
                    "/api/documents/generate/custom",
                    "/api/documents/templates",
                    "/api/documents/preview",
                ],
            }
        ),
        404,
    )


@documents_bp.errorhandler(405)
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


@documents_bp.errorhandler(500)
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
