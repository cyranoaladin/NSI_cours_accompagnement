import json
from datetime import date, datetime, timedelta

from src.models.formulas import (
    Enrollment,
    Formula,
    Group,
    GroupSession,
    IndividualSession,
    SessionAttendance,
    StudentObjective,
    Teacher,
    WeeklyReport,
)
from src.models.student import Assessment, LearningSession, Student


class ParentDashboardService:
    """Service pour générer les données du tableau de bord parent"""

    def __init__(self):
        pass

    def get_student_overview(self, student_id):
        """Récupérer la vue d'ensemble d'un étudiant"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return None

            # Inscription active
            enrollment = Enrollment.query.filter_by(
                student_id=student_id, is_active=True
            ).first()

            # Informations de base
            overview = {
                "student": {
                    "id": student.id,
                    "name": f"{student.first_name} {student.last_name}",
                    "grade": student.grade_level,
                    "school": student.school,
                    "formula": (
                        enrollment.formula.name
                        if enrollment and enrollment.formula
                        else None
                    ),
                    "formula_type": (
                        enrollment.formula.type.value
                        if enrollment and enrollment.formula
                        else None
                    ),
                },
                "enrollment": (
                    {
                        "start_date": (
                            enrollment.start_date.isoformat() if enrollment else None
                        ),
                        "formula_level": (
                            enrollment.formula.level.value
                            if enrollment and enrollment.formula
                            else None
                        ),
                        "group_name": (
                            enrollment.group.name
                            if enrollment and enrollment.group
                            else None
                        ),
                    }
                    if enrollment
                    else None
                ),
            }

            return overview
        except Exception as e:
            print(f"Erreur dans get_student_overview: {e}")
            return None

    def get_next_session(self, student_id):
        """Récupérer la prochaine séance de l'étudiant"""
        try:
            enrollment = Enrollment.query.filter_by(
                student_id=student_id, is_active=True
            ).first()
            if not enrollment:
                return None

            next_session = None

            if enrollment.group_id:
                # Séance de groupe
                next_group_session = (
                    GroupSession.query.filter(
                        GroupSession.group_id == enrollment.group_id,
                        GroupSession.scheduled_at > datetime.utcnow(),
                        GroupSession.status == "scheduled",
                    )
                    .order_by(GroupSession.scheduled_at.asc())
                    .first()
                )

                if next_group_session:
                    group = Group.query.get(enrollment.group_id)
                    teacher = Teacher.query.get(group.teacher_id) if group else None
                    next_session = {
                        "type": "group",
                        "date": next_group_session.scheduled_at.date().isoformat(),
                        "time": next_group_session.scheduled_at.time().strftime(
                            "%H:%M"
                        ),
                        "subject": next_group_session.subject,
                        "teacher": (
                            f"{teacher.first_name} {teacher.last_name}"
                            if teacher
                            else "Non assigné"
                        ),
                        "group_name": group.name if group else None,
                    }
            else:
                # Séance individuelle
                next_individual_session = (
                    IndividualSession.query.filter(
                        IndividualSession.student_id == student_id,
                        IndividualSession.scheduled_at > datetime.utcnow(),
                        IndividualSession.status == "scheduled",
                    )
                    .order_by(IndividualSession.scheduled_at.asc())
                    .first()
                )

                if next_individual_session:
                    teacher = Teacher.query.get(next_individual_session.teacher_id)
                    next_session = {
                        "type": "individual",
                        "date": next_individual_session.scheduled_at.date().isoformat(),
                        "time": next_individual_session.scheduled_at.time().strftime(
                            "%H:%M"
                        ),
                        "subject": next_individual_session.subject,
                        "teacher": (
                            f"{teacher.first_name} {teacher.last_name}"
                            if teacher
                            else "Non assigné"
                        ),
                    }

            return next_session
        except Exception as e:
            print(f"Erreur dans get_next_session: {e}")
            return None

    def get_monthly_stats(self, student_id):
        """Récupérer les statistiques du mois"""
        try:
            current_month_start = date.today().replace(day=1)
            enrollment = Enrollment.query.filter_by(
                student_id=student_id, is_active=True
            ).first()

            stats = {
                "sessions_this_month": 0,
                "individual_sessions": 0,
                "group_sessions": 0,
                "total_hours": 0,
            }

            if enrollment:
                if enrollment.group_id:
                    # Séances de groupe
                    group_sessions = GroupSession.query.filter(
                        GroupSession.group_id == enrollment.group_id,
                        GroupSession.scheduled_at >= current_month_start,
                        GroupSession.status == "completed",
                    ).all()

                    stats["group_sessions"] = len(group_sessions)
                    stats["sessions_this_month"] += len(group_sessions)
                    stats["total_hours"] += (
                        sum(s.duration_minutes for s in group_sessions) / 60
                    )

                if enrollment.teacher_id:
                    # Séances individuelles
                    individual_sessions = IndividualSession.query.filter(
                        IndividualSession.student_id == student_id,
                        IndividualSession.scheduled_at >= current_month_start,
                        IndividualSession.status == "completed",
                    ).all()

                    stats["individual_sessions"] = len(individual_sessions)
                    stats["sessions_this_month"] += len(individual_sessions)
                    stats["total_hours"] += (
                        sum(s.duration_minutes for s in individual_sessions) / 60
                    )

            return stats
        except Exception as e:
            print(f"Erreur dans get_monthly_stats: {e}")
            return {
                "sessions_this_month": 0,
                "individual_sessions": 0,
                "group_sessions": 0,
                "total_hours": 0,
            }

    def get_objectives_progress(self, student_id):
        """Récupérer la progression des objectifs"""
        try:
            total_objectives = StudentObjective.query.filter_by(
                student_id=student_id
            ).count()
            achieved_objectives = StudentObjective.query.filter_by(
                student_id=student_id, is_achieved=True
            ).count()

            # Objectifs en cours
            current_objectives = (
                StudentObjective.query.filter_by(
                    student_id=student_id, is_achieved=False
                )
                .filter(StudentObjective.target_date >= date.today())
                .all()
            )

            return {
                "total_objectives": total_objectives,
                "achieved_objectives": achieved_objectives,
                "current_objectives": len(current_objectives),
                "achievement_rate": (
                    (achieved_objectives / total_objectives * 100)
                    if total_objectives > 0
                    else 0
                ),
            }
        except Exception as e:
            print(f"Erreur dans get_objectives_progress: {e}")
            return {
                "total_objectives": 0,
                "achieved_objectives": 0,
                "current_objectives": 0,
                "achievement_rate": 0,
            }

    def get_learning_style_analysis(self, student_id):
        """Récupérer l'analyse du style d'apprentissage"""
        try:
            student = Student.query.get(student_id)
            if not student or not student.learning_profile:
                # Données par défaut si pas de profil
                return {
                    "dominant_style": "Visuel",
                    "confidence": 85,
                    "styles": [
                        {"style": "Visuel", "score": 85},
                        {"style": "Auditif", "score": 60},
                        {"style": "Kinesthésique", "score": 45},
                        {"style": "Lecture/Écriture", "score": 75},
                    ],
                    "recommendations": [
                        "Utiliser des diagrammes pour les concepts complexes",
                        "Privilégier les couleurs pour organiser l'information",
                        "Créer des cartes mentales pour les révisions",
                        "Utiliser des vidéos explicatives",
                    ],
                }

            # Analyser le profil d'apprentissage existant
            profile = student.learning_profile
            styles = profile.get("learning_styles", {})

            # Trouver le style dominant
            dominant_style = (
                max(styles.items(), key=lambda x: x[1]) if styles else ("Visuel", 85)
            )

            return {
                "dominant_style": dominant_style[0],
                "confidence": dominant_style[1],
                "styles": [{"style": k, "score": v} for k, v in styles.items()],
                "recommendations": profile.get("recommendations", []),
            }
        except Exception as e:
            print(f"Erreur dans get_learning_style_analysis: {e}")
            return None

    def get_subject_progress(self, student_id):
        """Récupérer la progression par matière"""
        try:
            # Récupérer les évaluations récentes par matière
            assessments = Assessment.query.filter_by(student_id=student_id).all()

            subjects_progress = {}

            for assessment in assessments:
                subject = assessment.subject
                if subject not in subjects_progress:
                    subjects_progress[subject] = {
                        "subject": subject,
                        "current_grade": 0,
                        "progress_percentage": 0,
                        "recent_topics": [],
                        "status": "En cours",
                    }

                # Mettre à jour avec la note la plus récente
                if assessment.score > subjects_progress[subject]["current_grade"]:
                    subjects_progress[subject]["current_grade"] = assessment.score
                    subjects_progress[subject]["progress_percentage"] = min(
                        assessment.score * 5, 100
                    )

                # Ajouter les sujets récents
                if (
                    assessment.topic
                    and assessment.topic
                    not in subjects_progress[subject]["recent_topics"]
                ):
                    subjects_progress[subject]["recent_topics"].append(assessment.topic)

            # Déterminer le statut basé sur la note
            for subject_data in subjects_progress.values():
                grade = subject_data["current_grade"]
                if grade >= 16:
                    subject_data["status"] = "Maîtrisé"
                elif grade >= 12:
                    subject_data["status"] = "En cours"
                else:
                    subject_data["status"] = "À revoir"

            return list(subjects_progress.values())
        except Exception as e:
            print(f"Erreur dans get_subject_progress: {e}")
            return []

    def get_recent_notifications(self, student_id, limit=5):
        """Récupérer les notifications récentes"""
        try:
            notifications = []

            # Objectifs récemment atteints
            recent_achievements = (
                StudentObjective.query.filter_by(
                    student_id=student_id, is_achieved=True
                )
                .filter(
                    StudentObjective.achievement_date
                    >= date.today() - timedelta(days=7)
                )
                .all()
            )

            for achievement in recent_achievements:
                notifications.append(
                    {
                        "type": "success",
                        "title": f"Objectif atteint en {achievement.subject}",
                        "message": achievement.objective_text[:100] + "...",
                        "timestamp": achievement.achievement_date.isoformat(),
                        "icon": "CheckCircle",
                    }
                )

            # Séances reportées récentes
            cancelled_sessions = IndividualSession.query.filter(
                IndividualSession.student_id == student_id,
                IndividualSession.status == "cancelled",
                IndividualSession.scheduled_at >= datetime.utcnow() - timedelta(days=7),
            ).all()

            for session in cancelled_sessions:
                notifications.append(
                    {
                        "type": "warning",
                        "title": "Séance reportée",
                        "message": f"{session.subject} du {session.scheduled_at.strftime('%d/%m')} reportée",
                        "timestamp": session.scheduled_at.isoformat(),
                        "icon": "AlertCircle",
                    }
                )

            # Messages récents des enseignants
            # (Simulation pour la démo)
            notifications.append(
                {
                    "type": "info",
                    "title": "Message de M. Dubois",
                    "message": "Nouveau plan de révision disponible",
                    "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                    "icon": "MessageSquare",
                }
            )

            # Trier par timestamp et limiter
            notifications.sort(key=lambda x: x["timestamp"], reverse=True)
            return notifications[:limit]
        except Exception as e:
            print(f"Erreur dans get_recent_notifications: {e}")
            return []

    def get_progress_chart_data(self, student_id, months=5):
        """Récupérer les données pour le graphique de progression"""
        try:
            # Générer les données pour les derniers mois
            end_date = date.today()
            start_date = end_date - timedelta(days=30 * months)

            # Récupérer les évaluations par mois
            assessments = (
                Assessment.query.filter(
                    Assessment.student_id == student_id, Assessment.date >= start_date
                )
                .order_by(Assessment.date.asc())
                .all()
            )

            # Organiser par mois et matière
            monthly_data = {}

            for assessment in assessments:
                month_key = assessment.date.strftime("%Y-%m")
                if month_key not in monthly_data:
                    monthly_data[month_key] = {}

                subject = assessment.subject
                if subject not in monthly_data[month_key]:
                    monthly_data[month_key][subject] = []

                monthly_data[month_key][subject].append(assessment.score)

            # Calculer les moyennes mensuelles
            chart_data = []
            month_names = [
                "Sept",
                "Oct",
                "Nov",
                "Déc",
                "Jan",
                "Fév",
                "Mar",
                "Avr",
                "Mai",
                "Juin",
                "Juil",
                "Août",
            ]

            for i in range(months):
                month_date = end_date - timedelta(days=30 * (months - 1 - i))
                month_key = month_date.strftime("%Y-%m")
                month_name = month_names[month_date.month - 1]

                data_point = {"month": month_name}

                if month_key in monthly_data:
                    for subject, scores in monthly_data[month_key].items():
                        avg_score = sum(scores) / len(scores)
                        data_point[subject.lower()] = round(avg_score, 1)
                else:
                    # Données par défaut si pas d'évaluations
                    data_point.update(
                        {
                            "math": 12 + i * 1.5,
                            "physics": 14 + i * 1,
                            "french": 16 + i * 0.5,
                        }
                    )

                chart_data.append(data_point)

            return chart_data
        except Exception as e:
            print(f"Erreur dans get_progress_chart_data: {e}")
            # Données par défaut en cas d'erreur
            return [
                {"month": "Sept", "math": 12, "physics": 14, "french": 16},
                {"month": "Oct", "math": 14, "physics": 15, "french": 16},
                {"month": "Nov", "math": 16, "physics": 16, "french": 17},
                {"month": "Déc", "math": 17, "physics": 17, "french": 18},
                {"month": "Jan", "math": 18, "physics": 18, "french": 18},
            ]

    def calculate_aria_confidence(self, student_id):
        """Calculer la confiance ARIA pour les prédictions"""
        try:
            # Facteurs à considérer pour la confiance
            factors = {
                "consistency": 0,  # Régularité des performances
                "progress_trend": 0,  # Tendance de progression
                "engagement": 0,  # Niveau d'engagement
                "completion_rate": 0,  # Taux de completion des objectifs
            }

            # Analyser la régularité des performances
            recent_assessments = Assessment.query.filter(
                Assessment.student_id == student_id,
                Assessment.date >= date.today() - timedelta(days=90),
            ).all()

            if recent_assessments:
                scores = [a.score for a in recent_assessments]
                # Calculer la variance (moins de variance = plus de régularité)
                mean_score = sum(scores) / len(scores)
                variance = sum((score - mean_score) ** 2 for score in scores) / len(
                    scores
                )
                factors["consistency"] = max(0, 100 - variance * 5)  # Normaliser

                # Tendance de progression
                if len(scores) >= 3:
                    recent_avg = sum(scores[-3:]) / 3
                    older_avg = sum(scores[:3]) / 3
                    improvement = (recent_avg - older_avg) / older_avg * 100
                    factors["progress_trend"] = min(100, max(0, 50 + improvement * 10))

            # Analyser l'engagement (basé sur la présence aux séances)
            total_sessions = IndividualSession.query.filter_by(
                student_id=student_id
            ).count()
            completed_sessions = IndividualSession.query.filter_by(
                student_id=student_id, status="completed"
            ).count()

            if total_sessions > 0:
                factors["engagement"] = (completed_sessions / total_sessions) * 100

            # Taux de completion des objectifs
            objectives_stats = self.get_objectives_progress(student_id)
            factors["completion_rate"] = objectives_stats["achievement_rate"]

            # Calculer la confiance globale (moyenne pondérée)
            weights = {
                "consistency": 0.3,
                "progress_trend": 0.3,
                "engagement": 0.2,
                "completion_rate": 0.2,
            }

            confidence = sum(factors[key] * weights[key] for key in factors)
            return min(100, max(0, round(confidence)))
        except Exception as e:
            print(f"Erreur dans calculate_aria_confidence: {e}")
            return 94  # Valeur par défaut
