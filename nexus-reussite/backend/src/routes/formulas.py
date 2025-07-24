from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime, date, timedelta
from src.models.formulas import (
    db, Formula, Group, Teacher, Enrollment, IndividualSession,
    GroupSession, SessionAttendance, WeeklyReport, ParentCommunication,
    StudentObjective, FormulaType, FormulaLevel
)
from src.models.student import Student

formulas_bp = Blueprint('formulas', __name__)

@formulas_bp.route('/api/formulas', methods=['GET'])
@cross_origin()
def get_formulas():
    """Récupérer toutes les formules disponibles"""
    try:
        formulas = Formula.query.all()
        return jsonify({
            'success': True,
            'formulas': [{
                'id': f.id,
                'name': f.name,
                'type': f.type.value,
                'level': f.level.value,
                'price_dt': f.price_dt,
                'hours_per_month': f.hours_per_month,
                'max_students': f.max_students,
                'description': f.description,
                'features': f.features
            } for f in formulas]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/formulas/individual', methods=['GET'])
@cross_origin()
def get_individual_formulas():
    """Récupérer les formules individuelles"""
    try:
        formulas = Formula.query.filter_by(type=FormulaType.INDIVIDUAL).all()
        return jsonify({
            'success': True,
            'formulas': [{
                'id': f.id,
                'name': f.name,
                'level': f.level.value,
                'price_dt': f.price_dt,
                'hours_per_month': f.hours_per_month,
                'description': f.description,
                'features': f.features
            } for f in formulas]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/formulas/group', methods=['GET'])
@cross_origin()
def get_group_formulas():
    """Récupérer les formules de groupe"""
    try:
        formulas = Formula.query.filter_by(type=FormulaType.GROUP).all()
        return jsonify({
            'success': True,
            'formulas': [{
                'id': f.id,
                'name': f.name,
                'level': f.level.value,
                'price_dt': f.price_dt,
                'hours_per_month': f.hours_per_month,
                'max_students': f.max_students,
                'description': f.description,
                'features': f.features
            } for f in formulas]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/groups', methods=['GET'])
@cross_origin()
def get_groups():
    """Récupérer tous les groupes disponibles"""
    try:
        groups = Group.query.all()
        return jsonify({
            'success': True,
            'groups': [{
                'id': g.id,
                'name': g.name,
                'subject': g.subject,
                'level': g.level,
                'max_students': g.max_students,
                'current_students': g.current_students,
                'teacher': {
                    'id': g.teacher.id,
                    'name': f"{g.teacher.first_name} {g.teacher.last_name}",
                    'subjects': g.teacher.subjects
                } if g.teacher else None,
                'schedule': g.schedule,
                'available_spots': g.max_students - g.current_students
            } for g in groups]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/groups/<int:group_id>/students', methods=['GET'])
@cross_origin()
def get_group_students(group_id):
    """Récupérer les étudiants d'un groupe"""
    try:
        enrollments = Enrollment.query.filter_by(group_id=group_id, is_active=True).all()
        students = []
        for enrollment in enrollments:
            student = Student.query.get(enrollment.student_id)
            if student:
                students.append({
                    'id': student.id,
                    'name': f"{student.first_name} {student.last_name}",
                    'level': student.grade_level,
                    'enrollment_date': enrollment.start_date.isoformat()
                })

        return jsonify({
            'success': True,
            'students': students
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/teachers', methods=['GET'])
@cross_origin()
def get_teachers():
    """Récupérer tous les enseignants"""
    try:
        teachers = Teacher.query.all()
        return jsonify({
            'success': True,
            'teachers': [{
                'id': t.id,
                'name': f"{t.first_name} {t.last_name}",
                'email': t.email,
                'phone': t.phone,
                'subjects': t.subjects,
                'qualifications': t.qualifications,
                'experience_years': t.experience_years,
                'is_aefe_certified': t.is_aefe_certified,
                'is_nsi_diu': t.is_nsi_diu
            } for t in teachers]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/students/<int:student_id>/enrollment', methods=['POST'])
@cross_origin()
def enroll_student(student_id):
    """Inscrire un étudiant à une formule"""
    try:
        data = request.get_json()
        formula_id = data.get('formula_id')
        group_id = data.get('group_id')  # Optionnel pour les formules de groupe
        teacher_id = data.get('teacher_id')  # Optionnel pour les formules individuelles

        # Vérifier que l'étudiant existe
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'success': False, 'error': 'Étudiant non trouvé'}), 404

        # Vérifier que la formule existe
        formula = Formula.query.get(formula_id)
        if not formula:
            return jsonify({'success': False, 'error': 'Formule non trouvée'}), 404

        # Créer l'inscription
        enrollment = Enrollment(
            student_id=student_id,
            formula_id=formula_id,
            group_id=group_id,
            teacher_id=teacher_id,
            start_date=date.today()
        )

        db.session.add(enrollment)

        # Mettre à jour le nombre d'étudiants dans le groupe si applicable
        if group_id:
            group = Group.query.get(group_id)
            if group:
                group.current_students += 1

        db.session.commit()

        return jsonify({
            'success': True,
            'enrollment_id': enrollment.id,
            'message': 'Inscription réussie'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/students/<int:student_id>/sessions', methods=['GET'])
@cross_origin()
def get_student_sessions(student_id):
    """Récupérer les séances d'un étudiant"""
    try:
        # Séances individuelles
        individual_sessions = IndividualSession.query.filter_by(student_id=student_id).all()

        # Séances de groupe
        enrollments = Enrollment.query.filter_by(student_id=student_id, is_active=True).all()
        group_sessions = []
        for enrollment in enrollments:
            if enrollment.group_id:
                sessions = GroupSession.query.filter_by(group_id=enrollment.group_id).all()
                group_sessions.extend(sessions)

        sessions_data = []

        # Ajouter les séances individuelles
        for session in individual_sessions:
            teacher = Teacher.query.get(session.teacher_id)
            sessions_data.append({
                'id': session.id,
                'type': 'individual',
                'subject': session.subject,
                'scheduled_at': session.scheduled_at.isoformat(),
                'duration_minutes': session.duration_minutes,
                'status': session.status,
                'teacher': {
                    'name': f"{teacher.first_name} {teacher.last_name}",
                    'email': teacher.email
                } if teacher else None,
                'topics_covered': session.topics_covered,
                'homework_assigned': session.homework_assigned,
                'teacher_notes': session.teacher_notes,
                'performance': session.student_performance
            })

        # Ajouter les séances de groupe
        for session in group_sessions:
            group = Group.query.get(session.group_id)
            teacher = Teacher.query.get(group.teacher_id) if group else None

            # Récupérer les informations de présence
            attendance = SessionAttendance.query.filter_by(
                session_id=session.id,
                student_id=student_id
            ).first()

            sessions_data.append({
                'id': session.id,
                'type': 'group',
                'subject': session.subject,
                'scheduled_at': session.scheduled_at.isoformat(),
                'duration_minutes': session.duration_minutes,
                'status': session.status,
                'group': {
                    'name': group.name,
                    'level': group.level
                } if group else None,
                'teacher': {
                    'name': f"{teacher.first_name} {teacher.last_name}",
                    'email': teacher.email
                } if teacher else None,
                'topics_covered': session.topics_covered,
                'homework_assigned': session.homework_assigned,
                'teacher_notes': session.teacher_notes,
                'attendance': {
                    'is_present': attendance.is_present,
                    'participation_score': attendance.participation_score,
                    'individual_notes': attendance.individual_notes
                } if attendance else None
            })

        # Trier par date
        sessions_data.sort(key=lambda x: x['scheduled_at'], reverse=True)

        return jsonify({
            'success': True,
            'sessions': sessions_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/students/<int:student_id>/weekly-reports', methods=['GET'])
@cross_origin()
def get_student_weekly_reports(student_id):
    """Récupérer les rapports hebdomadaires d'un étudiant"""
    try:
        reports = WeeklyReport.query.filter_by(student_id=student_id).order_by(
            WeeklyReport.week_start_date.desc()
        ).all()

        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'week_start_date': report.week_start_date.isoformat(),
                'week_end_date': report.week_end_date.isoformat(),
                'subjects_progress': report.subjects_progress,
                'aria_insights': report.aria_insights,
                'teacher_comments': report.teacher_comments,
                'next_week_objectives': report.next_week_objectives,
                'parent_feedback': report.parent_feedback,
                'is_sent_to_parents': report.is_sent_to_parents,
                'created_at': report.created_at.isoformat()
            })

        return jsonify({
            'success': True,
            'reports': reports_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/students/<int:student_id>/communications', methods=['GET'])
@cross_origin()
def get_student_communications(student_id):
    """Récupérer les communications concernant un étudiant"""
    try:
        communications = ParentCommunication.query.filter_by(
            student_id=student_id
        ).order_by(ParentCommunication.created_at.desc()).all()

        communications_data = []
        for comm in communications:
            communications_data.append({
                'id': comm.id,
                'sender_type': comm.sender_type,
                'sender_id': comm.sender_id,
                'recipient_type': comm.recipient_type,
                'recipient_id': comm.recipient_id,
                'subject': comm.subject,
                'message': comm.message,
                'is_read': comm.is_read,
                'priority': comm.priority,
                'created_at': comm.created_at.isoformat()
            })

        return jsonify({
            'success': True,
            'communications': communications_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/students/<int:student_id>/objectives', methods=['GET'])
@cross_origin()
def get_student_objectives(student_id):
    """Récupérer les objectifs d'un étudiant"""
    try:
        objectives = StudentObjective.query.filter_by(student_id=student_id).order_by(
            StudentObjective.target_date.asc()
        ).all()

        objectives_data = []
        for obj in objectives:
            objectives_data.append({
                'id': obj.id,
                'subject': obj.subject,
                'objective_text': obj.objective_text,
                'target_date': obj.target_date.isoformat(),
                'is_achieved': obj.is_achieved,
                'achievement_date': obj.achievement_date.isoformat() if obj.achievement_date else None,
                'progress_percentage': obj.progress_percentage,
                'created_by': obj.created_by,
                'created_at': obj.created_at.isoformat(),
                'updated_at': obj.updated_at.isoformat()
            })

        return jsonify({
            'success': True,
            'objectives': objectives_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@formulas_bp.route('/api/students/<int:student_id>/dashboard', methods=['GET'])
@cross_origin()
def get_student_dashboard(student_id):
    """Récupérer les données du tableau de bord pour un étudiant"""
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'success': False, 'error': 'Étudiant non trouvé'}), 404

        # Inscription active
        enrollment = Enrollment.query.filter_by(student_id=student_id, is_active=True).first()

        # Prochaine séance
        next_session = None
        if enrollment:
            if enrollment.group_id:
                # Séance de groupe
                next_group_session = GroupSession.query.filter(
                    GroupSession.group_id == enrollment.group_id,
                    GroupSession.scheduled_at > datetime.utcnow(),
                    GroupSession.status == 'scheduled'
                ).order_by(GroupSession.scheduled_at.asc()).first()

                if next_group_session:
                    group = Group.query.get(enrollment.group_id)
                    teacher = Teacher.query.get(group.teacher_id) if group else None
                    next_session = {
                        'type': 'group',
                        'date': next_group_session.scheduled_at.date().isoformat(),
                        'time': next_group_session.scheduled_at.time().strftime('%H:%M'),
                        'subject': next_group_session.subject,
                        'teacher': f"{teacher.first_name} {teacher.last_name}" if teacher else "Non assigné",
                        'group_name': group.name if group else None
                    }
            else:
                # Séance individuelle
                next_individual_session = IndividualSession.query.filter(
                    IndividualSession.student_id == student_id,
                    IndividualSession.scheduled_at > datetime.utcnow(),
                    IndividualSession.status == 'scheduled'
                ).order_by(IndividualSession.scheduled_at.asc()).first()

                if next_individual_session:
                    teacher = Teacher.query.get(next_individual_session.teacher_id)
                    next_session = {
                        'type': 'individual',
                        'date': next_individual_session.scheduled_at.date().isoformat(),
                        'time': next_individual_session.scheduled_at.time().strftime('%H:%M'),
                        'subject': next_individual_session.subject,
                        'teacher': f"{teacher.first_name} {teacher.last_name}" if teacher else "Non assigné"
                    }

        # Statistiques du mois
        current_month_start = date.today().replace(day=1)
        sessions_this_month = 0

        if enrollment:
            if enrollment.group_id:
                group_sessions = GroupSession.query.filter(
                    GroupSession.group_id == enrollment.group_id,
                    GroupSession.scheduled_at >= current_month_start,
                    GroupSession.status == 'completed'
                ).count()
                sessions_this_month += group_sessions
            else:
                individual_sessions = IndividualSession.query.filter(
                    IndividualSession.student_id == student_id,
                    IndividualSession.scheduled_at >= current_month_start,
                    IndividualSession.status == 'completed'
                ).count()
                sessions_this_month += individual_sessions

        # Objectifs atteints
        total_objectives = StudentObjective.query.filter_by(student_id=student_id).count()
        achieved_objectives = StudentObjective.query.filter_by(
            student_id=student_id,
            is_achieved=True
        ).count()

        # Progression globale (simulée pour la démo)
        global_progress = 87  # À calculer selon la logique métier

        # Confiance ARIA (simulée)
        aria_confidence = 94  # À calculer selon l'IA

        return jsonify({
            'success': True,
            'dashboard': {
                'student': {
                    'id': student.id,
                    'name': f"{student.first_name} {student.last_name}",
                    'grade': student.grade_level,
                    'school': student.school,
                    'formula': enrollment.formula.name if enrollment and enrollment.formula else None
                },
                'next_session': next_session,
                'stats': {
                    'global_progress': global_progress,
                    'sessions_this_month': sessions_this_month,
                    'objectives_achieved': achieved_objectives,
                    'total_objectives': total_objectives,
                    'aria_confidence': aria_confidence
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

