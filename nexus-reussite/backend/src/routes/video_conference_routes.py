"""
Routes API pour la gestion des visioconférences
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from typing import Dict, List, Any

from ..services.video_conference import (
    video_conference_service,
    ConferenceStatus,
    ParticipantRole,
    create_instant_meeting,
    get_meeting_link
)

video_conference_bp = Blueprint('video_conference', __name__, url_prefix='/api/video-conference')

@video_conference_bp.route('/create', methods=['POST'])
@jwt_required()
def create_conference():
    """Crée une nouvelle conférence"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get('role')

        # Vérifier les permissions
        if user_role not in ['teacher', 'admin']:
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        data = request.get_json()

        # Validation des données
        required_fields = ['subject', 'scheduled_start']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400

        # Convertir la date
        try:
            scheduled_start = datetime.fromisoformat(data['scheduled_start'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Format de date invalide'
            }), 400

        # Créer la conférence
        room = video_conference_service.create_conference_room(
            teacher_id=current_user.get('user_id'),
            teacher_name=current_user.get('name', 'Enseignant'),
            subject=data['subject'],
            scheduled_start=scheduled_start,
            duration_minutes=data.get('duration_minutes', 60),
            max_participants=data.get('max_participants', 10),
            description=data.get('description')
        )

        return jsonify({
            'success': True,
            'room_id': room.room_id,
            'room_info': video_conference_service.get_room_info(room.room_id)
        })

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la création de la conférence: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la création de la conférence'
        }), 500

@video_conference_bp.route('/instant', methods=['POST'])
@jwt_required()
def create_instant_conference():
    """Crée une conférence instantanée"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get('role')

        # Vérifier les permissions
        if user_role not in ['teacher', 'admin']:
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        data = request.get_json()
        subject = data.get('subject', 'Cours instantané')

        result = create_instant_meeting(
            teacher_id=current_user.get('user_id'),
            teacher_name=current_user.get('name', 'Enseignant'),
            subject=subject
        )

        return jsonify(result)

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la création de la conférence instantanée: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la création de la conférence'
        }), 500

@video_conference_bp.route('/join/<room_id>', methods=['POST'])
@jwt_required()
def join_conference(room_id):
    """Rejoint une conférence"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_name = current_user.get('name', f'Utilisateur {user_id}')
        user_email = current_user.get('email', f'{user_id}@nexusreussite.tn')
        user_role = current_user.get('role')

        # Déterminer le rôle dans la conférence
        if user_role == 'teacher':
            participant_role = ParticipantRole.MODERATOR
        elif user_role == 'admin':
            participant_role = ParticipantRole.MODERATOR
        else:
            participant_role = ParticipantRole.PARTICIPANT

        result = video_conference_service.join_conference(
            room_id=room_id,
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
            role=participant_role
        )

        return jsonify(result)

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la connexion à la conférence: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la connexion à la conférence'
        }), 500

@video_conference_bp.route('/leave/<room_id>', methods=['POST'])
@jwt_required()
def leave_conference(room_id):
    """Quitte une conférence"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        result = video_conference_service.leave_conference(room_id, user_id)
        return jsonify(result)

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la déconnexion de la conférence: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la déconnexion'
        }), 500

@video_conference_bp.route('/end/<room_id>', methods=['POST'])
@jwt_required()
def end_conference(room_id):
    """Termine une conférence"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get('role')
        teacher_id = current_user.get('user_id')

        # Vérifier les permissions
        if user_role not in ['teacher', 'admin']:
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        result = video_conference_service.end_conference(room_id, teacher_id)
        return jsonify(result)

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la fin de la conférence: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la fin de la conférence'
        }), 500

@video_conference_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_user_rooms():
    """Récupère les salles de l'utilisateur"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        include_history = request.args.get('include_history', False, type=bool)

        if user_role in ['teacher', 'admin']:
            rooms = video_conference_service.get_teacher_rooms(user_id, include_history)
        else:
            rooms = video_conference_service.get_student_rooms(user_id)

        return jsonify({
            'success': True,
            'rooms': rooms
        })

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération des salles: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la récupération des salles'
        }), 500

@video_conference_bp.route('/room/<room_id>', methods=['GET'])
@jwt_required()
def get_room_info(room_id):
    """Récupère les informations d'une salle"""
    try:
        room_info = video_conference_service.get_room_info(room_id)

        if not room_info:
            return jsonify({
                'success': False,
                'error': 'Salle non trouvée'
            }), 404

        return jsonify({
            'success': True,
            'room_info': room_info
        })

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération des informations: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la récupération des informations'
        }), 500

@video_conference_bp.route('/schedule-recurring', methods=['POST'])
@jwt_required()
def schedule_recurring_conference():
    """Programme des conférences récurrentes"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get('role')

        # Vérifier les permissions
        if user_role not in ['teacher', 'admin']:
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        data = request.get_json()

        # Validation des données
        required_fields = ['subject', 'start_time', 'recurrence_days', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400

        # Convertir les dates
        try:
            start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Format de date invalide'
            }), 400

        # Programmer les conférences
        scheduled_rooms = video_conference_service.schedule_recurring_conference(
            teacher_id=current_user.get('user_id'),
            teacher_name=current_user.get('name', 'Enseignant'),
            subject=data['subject'],
            start_time=start_time,
            duration_minutes=data.get('duration_minutes', 60),
            recurrence_days=data['recurrence_days'],
            end_date=end_date
        )

        return jsonify({
            'success': True,
            'scheduled_count': len(scheduled_rooms),
            'rooms': [video_conference_service.get_room_info(room.room_id) for room in scheduled_rooms]
        })

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la programmation récurrente: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la programmation'
        }), 500

@video_conference_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_conference_statistics():
    """Récupère les statistiques des conférences"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get('role')

        # Les enseignants voient leurs propres stats, les admins voient tout
        teacher_id = None
        if user_role == 'teacher':
            teacher_id = current_user.get('user_id')
        elif user_role != 'admin':
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        stats = video_conference_service.get_conference_statistics(teacher_id)

        return jsonify({
            'success': True,
            'statistics': stats
        })

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération des statistiques: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la récupération des statistiques'
        }), 500

@video_conference_bp.route('/active', methods=['GET'])
@jwt_required()
def get_active_conferences():
    """Récupère les conférences actives"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get('role')

        active_rooms = []

        for room_id, room in video_conference_service.active_rooms.items():
            room_info = video_conference_service.get_room_info(room_id)

            # Filtrer selon le rôle
            if user_role == 'teacher' and room.teacher_id != current_user.get('user_id'):
                continue
            elif user_role == 'student':
                # Masquer certaines informations pour les élèves
                room_info.pop('recording_url', None)
                room_info['participants'] = [
                    {k: v for k, v in p.items() if k not in ['user_id']}
                    for p in room_info['participants']
                ]

            active_rooms.append(room_info)

        return jsonify({
            'success': True,
            'active_conferences': active_rooms
        })

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération des conférences actives: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la récupération'
        }), 500

@video_conference_bp.route('/quick-link/<room_id>', methods=['GET'])
@jwt_required()
def get_quick_link(room_id):
    """Génère un lien rapide pour rejoindre une conférence"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_name = current_user.get('name', f'Utilisateur {user_id}')
        user_role = current_user.get('role')

        is_teacher = user_role in ['teacher', 'admin']

        meeting_link = get_meeting_link(room_id, user_id, user_name, is_teacher)

        if meeting_link:
            return jsonify({
                'success': True,
                'meeting_link': meeting_link
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Impossible de générer le lien'
            }), 400

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la génération du lien: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la génération du lien'
        }), 500

@video_conference_bp.route('/update/<room_id>', methods=['PUT'])
@jwt_required()
def update_conference(room_id):
    """Met à jour une conférence"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get('role')

        # Vérifier les permissions
        if user_role not in ['teacher', 'admin']:
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        if room_id not in video_conference_service.active_rooms:
            return jsonify({
                'success': False,
                'error': 'Salle non trouvée'
            }), 404

        room = video_conference_service.active_rooms[room_id]

        # Vérifier que c'est l'enseignant propriétaire
        if room.teacher_id != current_user.get('user_id') and user_role != 'admin':
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        data = request.get_json()

        # Mettre à jour les champs modifiables
        if 'description' in data:
            room.description = data['description']

        if 'max_participants' in data:
            room.max_participants = data['max_participants']

        if 'recording_enabled' in data:
            room.recording_enabled = data['recording_enabled']

        if 'scheduled_end' in data:
            try:
                room.scheduled_end = datetime.fromisoformat(data['scheduled_end'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Format de date invalide'
                }), 400

        return jsonify({
            'success': True,
            'message': 'Conférence mise à jour',
            'room_info': video_conference_service.get_room_info(room_id)
        })

    except Exception as e:
        current_app.logger.error(f"Erreur lors de la mise à jour: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de la mise à jour'
        }), 500

@video_conference_bp.route('/cancel/<room_id>', methods=['POST'])
@jwt_required()
def cancel_conference(room_id):
    """Annule une conférence programmée"""
    try:
        current_user = get_jwt_identity()
        user_role = current_user.get('role')

        # Vérifier les permissions
        if user_role not in ['teacher', 'admin']:
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        if room_id not in video_conference_service.active_rooms:
            return jsonify({
                'success': False,
                'error': 'Salle non trouvée'
            }), 404

        room = video_conference_service.active_rooms[room_id]

        # Vérifier que c'est l'enseignant propriétaire
        if room.teacher_id != current_user.get('user_id') and user_role != 'admin':
            return jsonify({
                'success': False,
                'error': 'Permission insuffisante'
            }), 403

        # Vérifier que la conférence n'a pas encore commencé
        if room.status != ConferenceStatus.SCHEDULED:
            return jsonify({
                'success': False,
                'error': 'Impossible d\'annuler une conférence déjà commencée'
            }), 400

        # Annuler la conférence
        room.status = ConferenceStatus.CANCELLED

        # Déplacer vers l'historique
        video_conference_service.room_history.append(room)
        del video_conference_service.active_rooms[room_id]

        return jsonify({
            'success': True,
            'message': 'Conférence annulée'
        })

    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'annulation: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur lors de l\'annulation'
        }), 500

