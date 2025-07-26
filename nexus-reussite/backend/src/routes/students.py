import json
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from sqlalchemy import or_

from src.models.student import Assessment, LearningSession, Student, db

students_bp = Blueprint("students", __name__)


@students_bp.route("/register", methods=["POST"])
@cross_origin()
def register_student():
    """
    Inscription d'un nouveau étudiant
    """
    try:
        data = request.get_json()

        # Validation des données requises
        required_fields = ["full_name", "email", "grade_level"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} est requis"}), 400

        # Vérification de l'unicité de l'email
        existing_student = Student.query.filter_by(email=data["email"]).first()
        if existing_student:
            return jsonify({"error": "Un étudiant avec cet email existe déjà"}), 409

        # Traitement des matières préférées
        preferred_subjects = data.get("preferred_subjects", [])
        if isinstance(preferred_subjects, str):
            preferred_subjects = [preferred_subjects]

        # Création du nouvel étudiant
        student = Student(
            full_name=data["full_name"],
            email=data["email"],
            phone=data.get("phone"),
            grade_level=data["grade_level"],
            school=data.get("school"),
            preferred_subjects=preferred_subjects,
        )

        # Initialisation du profil cognitif de base
        initial_profile = {
            "registration_date": datetime.utcnow().isoformat(),
            "initial_preferences": {
                "subjects": preferred_subjects,
                "grade_level": data["grade_level"],
                "school": data.get("school"),
            },
            "learning_style": "unknown",  # Sera déterminé par ARIA
            "onboarding_completed": False,
        }

        student.cognitive_profile = json.dumps(initial_profile)

        # Sauvegarde en base
        db.session.add(student)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Étudiant inscrit avec succès",
                    "student": student.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erreur lors de l'inscription: {str(e)}"}), 500


@students_bp.route("/<int:student_id>", methods=["GET"])
@cross_origin()
def get_student(student_id):
    """
    Récupère les informations d'un étudiant
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Étudiant non trouvé"}), 404

        return jsonify({"success": True, "student": student.to_dict()})

    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération: {str(e)}"}), 500


@students_bp.route("/<int:student_id>", methods=["PUT"])
@cross_origin()
def update_student(student_id):
    """
    Met à jour les informations d'un étudiant
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Étudiant non trouvé"}), 404

        data = request.get_json()

        # Mise à jour des champs modifiables
        updatable_fields = ["full_name", "phone", "grade_level", "school"]
        for field in updatable_fields:
            if field in data:
                setattr(student, field, data[field])

        # Mise à jour des matières préférées
        if "preferred_subjects" in data:
            preferred_subjects = data["preferred_subjects"]
            if isinstance(preferred_subjects, str):
                preferred_subjects = [preferred_subjects]
            student.preferred_subjects = json.dumps(preferred_subjects)

        # Mise à jour du timestamp
        student.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Étudiant mis à jour avec succès",
                "student": student.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erreur lors de la mise à jour: {str(e)}"}), 500


@students_bp.route("/", methods=["GET"])
@cross_origin()
def list_students():
    """
    Liste tous les étudiants avec pagination et filtres
    """
    try:
        # Paramètres de pagination
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        # Paramètres de filtrage
        grade_level = request.args.get("grade_level")
        school = request.args.get("school")
        search = request.args.get("search")  # Recherche par nom ou email
        active_only = request.args.get("active_only", "true").lower() == "true"

        # Construction de la requête
        query = Student.query

        if active_only:
            query = query.filter_by(is_active=True)

        if grade_level:
            query = query.filter_by(grade_level=grade_level)

        if school:
            query = query.filter_by(school=school)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Student.full_name.ilike(search_pattern),
                    Student.email.ilike(search_pattern),
                )
            )

        # Tri par date de création (plus récents en premier)
        query = query.order_by(Student.created_at.desc())

        # Pagination
        students = query.paginate(page=page, per_page=per_page, error_out=False)

        # Statistiques générales
        total_students = Student.query.filter_by(is_active=True).count()
        grade_distribution = (
            db.session.query(Student.grade_level, db.func.count(Student.id))
            .filter_by(is_active=True)
            .group_by(Student.grade_level)
            .all()
        )

        return jsonify(
            {
                "success": True,
                "students": [student.to_dict() for student in students.items],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": students.total,
                    "pages": students.pages,
                    "has_next": students.has_next,
                    "has_prev": students.has_prev,
                },
                "statistics": {
                    "total_active_students": total_students,
                    "grade_distribution": dict(grade_distribution),
                },
            }
        )

    except Exception as e:
        return (
            jsonify({"error": f"Erreur lors de la récupération de la liste: {str(e)}"}),
            500,
        )


@students_bp.route("/<int:student_id>/sessions", methods=["GET"])
@cross_origin()
def get_student_sessions(student_id):
    """
    Récupère les sessions d'apprentissage d'un étudiant
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Étudiant non trouvé"}), 404

        # Paramètres de pagination et filtrage
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        subject = request.args.get("subject")
        session_type = request.args.get("session_type")

        # Construction de la requête
        query = LearningSession.query.filter_by(student_id=student_id)

        if subject:
            query = query.filter_by(subject=subject)

        if session_type:
            query = query.filter_by(session_type=session_type)

        query = query.order_by(LearningSession.created_at.desc())

        # Pagination
        sessions = query.paginate(page=page, per_page=per_page, error_out=False)

        # Statistiques des sessions
        total_sessions = LearningSession.query.filter_by(student_id=student_id).count()
        avg_completion = (
            db.session.query(db.func.avg(LearningSession.completion_rate))
            .filter_by(student_id=student_id)
            .scalar()
            or 0
        )

        total_time = (
            db.session.query(db.func.sum(LearningSession.duration_minutes))
            .filter_by(student_id=student_id)
            .scalar()
            or 0
        )

        return jsonify(
            {
                "success": True,
                "sessions": [session.to_dict() for session in sessions.items],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": sessions.total,
                    "pages": sessions.pages,
                    "has_next": sessions.has_next,
                    "has_prev": sessions.has_prev,
                },
                "statistics": {
                    "total_sessions": total_sessions,
                    "avg_completion_rate": float(avg_completion),
                    "total_time_minutes": int(total_time),
                },
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"error": f"Erreur lors de la récupération des sessions: {str(e)}"}
            ),
            500,
        )


@students_bp.route("/<int:student_id>/assessments", methods=["GET"])
@cross_origin()
def get_student_assessments(student_id):
    """
    Récupère les évaluations d'un étudiant
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Étudiant non trouvé"}), 404

        # Paramètres de pagination et filtrage
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        subject = request.args.get("subject")
        assessment_type = request.args.get("assessment_type")
        completed_only = request.args.get("completed_only", "false").lower() == "true"

        # Construction de la requête
        query = Assessment.query.filter_by(student_id=student_id)

        if subject:
            query = query.filter_by(subject=subject)

        if assessment_type:
            query = query.filter_by(assessment_type=assessment_type)

        if completed_only:
            query = query.filter_by(is_completed=True)

        query = query.order_by(Assessment.created_at.desc())

        # Pagination
        assessments = query.paginate(page=page, per_page=per_page, error_out=False)

        # Statistiques des évaluations
        completed_assessments = Assessment.query.filter_by(
            student_id=student_id, is_completed=True
        ).all()

        avg_score = (
            sum([a.score for a in completed_assessments if a.score])
            / len(completed_assessments)
            if completed_assessments
            else 0
        )

        return jsonify(
            {
                "success": True,
                "assessments": [
                    assessment.to_dict() for assessment in assessments.items
                ],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": assessments.total,
                    "pages": assessments.pages,
                    "has_next": assessments.has_next,
                    "has_prev": assessments.has_prev,
                },
                "statistics": {
                    "total_assessments": assessments.total,
                    "completed_assessments": len(completed_assessments),
                    "avg_score": avg_score,
                },
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"error": f"Erreur lors de la récupération des évaluations: {str(e)}"}
            ),
            500,
        )


@students_bp.route("/<int:student_id>/dashboard", methods=["GET"])
@cross_origin()
def get_student_dashboard(student_id):
    """
    Récupère les données du tableau de bord d'un étudiant
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Étudiant non trouvé"}), 404

        # Sessions récentes (7 derniers jours)
        from datetime import timedelta

        week_ago = datetime.utcnow() - timedelta(days=7)

        recent_sessions = (
            LearningSession.query.filter(
                LearningSession.student_id == student_id,
                LearningSession.created_at >= week_ago,
            )
            .order_by(LearningSession.created_at.desc())
            .limit(5)
            .all()
        )

        # Évaluations récentes
        recent_assessments = (
            Assessment.query.filter(
                Assessment.student_id == student_id, Assessment.is_completed == True
            )
            .order_by(Assessment.completed_at.desc())
            .limit(3)
            .all()
        )

        # Statistiques de progression
        total_sessions = LearningSession.query.filter_by(student_id=student_id).count()
        total_time = (
            db.session.query(db.func.sum(LearningSession.duration_minutes))
            .filter_by(student_id=student_id)
            .scalar()
            or 0
        )

        # Progression par matière
        subject_stats = (
            db.session.query(
                LearningSession.subject,
                db.func.count(LearningSession.id).label("session_count"),
                db.func.avg(LearningSession.completion_rate).label("avg_completion"),
                db.func.avg(LearningSession.accuracy_rate).label("avg_accuracy"),
            )
            .filter_by(student_id=student_id)
            .group_by(LearningSession.subject)
            .all()
        )

        subject_progress = {}
        for stat in subject_stats:
            subject_progress[stat.subject] = {
                "session_count": stat.session_count,
                "avg_completion": float(stat.avg_completion or 0),
                "avg_accuracy": float(stat.avg_accuracy or 0),
            }

        # Objectifs et recommandations (basés sur le profil ARIA)
        cognitive_profile = (
            json.loads(student.cognitive_profile) if student.cognitive_profile else {}
        )
        performance_data = (
            json.loads(student.performance_data) if student.performance_data else {}
        )

        # Calcul du niveau de progression global
        if recent_assessments:
            recent_scores = [a.score for a in recent_assessments if a.score]
            progress_trend = (
                "improving"
                if len(recent_scores) >= 2 and recent_scores[0] > recent_scores[-1]
                else "stable"
            )
        else:
            progress_trend = "new"

        return jsonify(
            {
                "success": True,
                "student_profile": student.to_dict(),
                "recent_activity": {
                    "sessions": [session.to_dict() for session in recent_sessions],
                    "assessments": [
                        assessment.to_dict() for assessment in recent_assessments
                    ],
                },
                "statistics": {
                    "total_sessions": total_sessions,
                    "total_time_hours": round(total_time / 60, 1),
                    "subject_progress": subject_progress,
                    "progress_trend": progress_trend,
                },
                "recommendations": {
                    "next_session_suggestion": _get_next_session_suggestion(
                        student, subject_progress
                    ),
                    "focus_areas": _get_focus_areas(performance_data),
                    "study_tips": _get_personalized_study_tips(student.learning_style),
                },
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": f"Erreur lors de la récupération du tableau de bord: {str(e)}"
                }
            ),
            500,
        )


def _get_next_session_suggestion(student, subject_progress):
    """Suggère la prochaine session basée sur l'historique"""
    if not subject_progress:
        return {
            "subject": "mathematiques",
            "topic": "Évaluation diagnostique",
            "reason": "Commençons par évaluer votre niveau actuel",
        }

    # Trouve la matière avec le plus faible taux de réussite
    weakest_subject = min(subject_progress.items(), key=lambda x: x[1]["avg_accuracy"])

    return {
        "subject": weakest_subject[0],
        "topic": "Révision ciblée",
        "reason": f"Améliorons vos résultats en {weakest_subject[0]}",
    }


def _get_focus_areas(performance_data):
    """Identifie les domaines nécessitant une attention particulière"""
    focus_areas = []

    last_assessment = performance_data.get("last_assessment", {})
    error_patterns = last_assessment.get("error_patterns", {})

    topics_with_errors = error_patterns.get("topics_with_errors", {})
    if topics_with_errors:
        # Les 2 sujets avec le plus d'erreurs
        sorted_topics = sorted(
            topics_with_errors.items(), key=lambda x: x[1], reverse=True
        )
        focus_areas = [topic for topic, _ in sorted_topics[:2]]

    if not focus_areas:
        focus_areas = ["Consolidation des acquis", "Préparation méthodologique"]

    return focus_areas


def _get_personalized_study_tips(learning_style):
    """Retourne des conseils d'étude personnalisés selon le style d'apprentissage"""
    tips = {
        "visual": [
            "Utilisez des diagrammes et des cartes mentales",
            "Surlignez les informations importantes avec des couleurs",
            "Créez des schémas pour organiser vos idées",
        ],
        "auditory": [
            "Lisez vos notes à voix haute",
            "Enregistrez-vous en expliquant les concepts",
            "Participez à des groupes d'étude pour discuter",
        ],
        "kinesthetic": [
            "Prenez des pauses régulières pendant l'étude",
            "Utilisez des objets manipulables pour les concepts abstraits",
            "Alternez entre différents environnements d'étude",
        ],
        "reading_writing": [
            "Rédigez des résumés détaillés après chaque leçon",
            "Créez des listes et des plans structurés",
            "Tenez un journal de vos progrès",
        ],
    }

    return tips.get(learning_style, tips["visual"])


@students_bp.route("/<int:student_id>/deactivate", methods=["POST"])
@cross_origin()
def deactivate_student(student_id):
    """
    Désactive un étudiant (soft delete)
    """
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Étudiant non trouvé"}), 404

        student.is_active = False
        student.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({"success": True, "message": "Étudiant désactivé avec succès"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erreur lors de la désactivation: {str(e)}"}), 500


@students_bp.route("/statistics", methods=["GET"])
@cross_origin()
def get_global_statistics():
    """
    Récupère les statistiques globales des étudiants
    """
    try:
        # Statistiques générales
        total_students = Student.query.filter_by(is_active=True).count()
        total_sessions = LearningSession.query.count()
        total_assessments = Assessment.query.filter_by(is_completed=True).count()

        # Répartition par niveau
        grade_distribution = (
            db.session.query(Student.grade_level, db.func.count(Student.id))
            .filter_by(is_active=True)
            .group_by(Student.grade_level)
            .all()
        )

        # Répartition par école
        school_distribution = (
            db.session.query(Student.school, db.func.count(Student.id))
            .filter(Student.is_active == True, Student.school.isnot(None))
            .group_by(Student.school)
            .all()
        )

        # Matières les plus populaires
        subject_popularity = (
            db.session.query(LearningSession.subject, db.func.count(LearningSession.id))
            .group_by(LearningSession.subject)
            .order_by(db.func.count(LearningSession.id).desc())
            .limit(5)
            .all()
        )

        # Performances moyennes
        avg_completion = (
            db.session.query(db.func.avg(LearningSession.completion_rate)).scalar() or 0
        )

        avg_accuracy = (
            db.session.query(db.func.avg(LearningSession.accuracy_rate)).scalar() or 0
        )

        return jsonify(
            {
                "success": True,
                "global_statistics": {
                    "total_students": total_students,
                    "total_sessions": total_sessions,
                    "total_assessments": total_assessments,
                    "avg_completion_rate": float(avg_completion),
                    "avg_accuracy_rate": float(avg_accuracy),
                },
                "distributions": {
                    "grade_levels": dict(grade_distribution),
                    "schools": dict(school_distribution),
                    "popular_subjects": dict(subject_popularity),
                },
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"error": f"Erreur lors de la récupération des statistiques: {str(e)}"}
            ),
            500,
        )
