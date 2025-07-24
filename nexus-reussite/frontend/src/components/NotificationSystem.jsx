import React, { useState, useEffect, useCallback } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Bell, 
  X, 
  Check, 
  Info, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  MessageSquare,
  Calendar,
  Award,
  BookOpen,
  Users,
  Settings,
  Volume2,
  VolumeX,
  Smartphone,
  Mail,
  Clock,
  Filter,
  Archive,
  Trash2,
  MoreHorizontal,
  Eye,
  EyeOff,
  Star,
  Heart,
  Share2,
  Download,
  ExternalLink,
  Zap,
  Target,
  TrendingUp,
  Gift,
  Sparkles,
  Crown,
  Shield,
  Flame,
  Brain
} from 'lucide-react'

const NotificationSystem = ({ 
  student, 
  notifications = [], 
  onMarkAsRead, 
  onMarkAllAsRead, 
  onDeleteNotification, 
  onUpdateSettings,
  isVisible,
  onClose 
}) => {
  const [activeTab, setActiveTab] = useState('all');
  const [filter, setFilter] = useState('all');
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [selectedNotifications, setSelectedNotifications] = useState([]);
  const [showSettings, setShowSettings] = useState(false);

  // Types de notifications avec leurs icônes et couleurs
  const notificationTypes = {
    success: {
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
      borderColor: 'border-green-200 dark:border-green-800'
    },
    info: {
      icon: Info,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      borderColor: 'border-blue-200 dark:border-blue-800'
    },
    warning: {
      icon: AlertTriangle,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
      borderColor: 'border-yellow-200 dark:border-yellow-800'
    },
    error: {
      icon: XCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-50 dark:bg-red-900/20',
      borderColor: 'border-red-200 dark:border-red-800'
    },
    achievement: {
      icon: Award,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
      borderColor: 'border-purple-200 dark:border-purple-800'
    },
    message: {
      icon: MessageSquare,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50 dark:bg-indigo-900/20',
      borderColor: 'border-indigo-200 dark:border-indigo-800'
    },
    reminder: {
      icon: Clock,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20',
      borderColor: 'border-orange-200 dark:border-orange-800'
    },
    system: {
      icon: Settings,
      color: 'text-gray-600',
      bgColor: 'bg-gray-50 dark:bg-gray-900/20',
      borderColor: 'border-gray-200 dark:border-gray-800'
    }
  };

  // Notifications de démonstration enrichies
  const demoNotifications = [
    {
      id: 'notif-001',
      type: 'achievement',
      title: 'Nouveau badge débloqué !',
      message: 'Félicitations ! Vous avez obtenu le badge "Expert en fonctions"',
      timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(), // 30 min ago
      read: false,
      priority: 'high',
      category: 'gamification',
      actionUrl: '/profile/badges',
      actionText: 'Voir le badge',
      metadata: {
        badgeName: 'Expert en fonctions',
        xpEarned: 200,
        rarity: 'rare'
      }
    },
    {
      id: 'notif-002',
      type: 'info',
      title: 'Document généré avec succès',
      message: 'ARIA a créé votre fiche de révision personnalisée en mathématiques',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2h ago
      read: false,
      priority: 'medium',
      category: 'documents',
      actionUrl: '/documents/math-revision-001',
      actionText: 'Consulter le document',
      metadata: {
        documentType: 'Fiche de révision',
        subject: 'Mathématiques',
        generatedBy: 'ARIA'
      }
    },
    {
      id: 'notif-003',
      type: 'reminder',
      title: 'Session programmée demain',
      message: 'N\'oubliez pas votre cours de NSI à 16h avec Mme Martin',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(), // 4h ago
      read: true,
      priority: 'high',
      category: 'planning',
      actionUrl: '/planning',
      actionText: 'Voir le planning',
      metadata: {
        sessionType: 'Cours individuel',
        subject: 'NSI',
        teacher: 'Mme Martin',
        date: '2025-07-24',
        time: '16:00'
      }
    },
    {
      id: 'notif-004',
      type: 'message',
      title: 'Message de M. Dubois',
      message: 'Excellent travail sur les exercices de probabilités ! Continuez ainsi.',
      timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(), // 6h ago
      read: true,
      priority: 'medium',
      category: 'communication',
      actionUrl: '/messages/dubois-001',
      actionText: 'Répondre',
      metadata: {
        sender: 'M. Dubois',
        subject: 'Mathématiques',
        messageType: 'feedback'
      }
    },
    {
      id: 'notif-005',
      type: 'success',
      title: 'Quiz terminé avec succès',
      message: 'Score parfait ! 20/20 en probabilités conditionnelles',
      timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
      read: true,
      priority: 'medium',
      category: 'evaluation',
      actionUrl: '/quiz/results/prob-001',
      actionText: 'Voir les résultats',
      metadata: {
        quizType: 'Probabilités conditionnelles',
        score: 20,
        maxScore: 20,
        duration: '15 minutes'
      }
    },
    {
      id: 'notif-006',
      type: 'info',
      title: 'Nouvelle recommandation ARIA',
      message: 'ARIA suggère de réviser les fonctions logarithmes avant votre prochain cours',
      timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
      read: false,
      priority: 'low',
      category: 'ai_recommendation',
      actionUrl: '/aria/recommendations',
      actionText: 'Voir les recommandations',
      metadata: {
        recommendationType: 'Révision',
        subject: 'Mathématiques',
        topic: 'Fonctions logarithmes',
        confidence: 0.85
      }
    },
    {
      id: 'notif-007',
      type: 'warning',
      title: 'Objectif hebdomadaire en retard',
      message: 'Il vous reste 2 jours pour atteindre votre objectif de 5h d\'étude cette semaine',
      timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days ago
      read: false,
      priority: 'medium',
      category: 'goals',
      actionUrl: '/dashboard/goals',
      actionText: 'Voir les objectifs',
      metadata: {
        goalType: 'Temps d\'étude hebdomadaire',
        current: 3,
        target: 5,
        unit: 'heures',
        deadline: '2025-07-25'
      }
    },
    {
      id: 'notif-008',
      type: 'system',
      title: 'Mise à jour de la plateforme',
      message: 'Nouvelles fonctionnalités disponibles ! Découvrez les améliorations d\'ARIA',
      timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), // 1 week ago
      read: true,
      priority: 'low',
      category: 'system',
      actionUrl: '/updates/v2.1',
      actionText: 'Découvrir les nouveautés',
      metadata: {
        version: '2.1.0',
        features: ['ARIA amélioré', 'Nouveau système de badges', 'Interface parent enrichie']
      }
    }
  ];

  const allNotifications = [...notifications, ...demoNotifications];

  // Filtrage des notifications
  const filteredNotifications = allNotifications.filter(notification => {
    if (activeTab === 'unread' && notification.read) return false;
    if (activeTab === 'read' && !notification.read) return false;
    if (filter !== 'all' && notification.category !== filter) return false;
    return true;
  });

  const unreadCount = allNotifications.filter(n => !n.read).length;

  // Formatage de la date
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'À l\'instant';
    if (diffInMinutes < 60) return `Il y a ${diffInMinutes} min`;
    if (diffInMinutes < 1440) return `Il y a ${Math.floor(diffInMinutes / 60)}h`;
    if (diffInMinutes < 10080) return `Il y a ${Math.floor(diffInMinutes / 1440)} jour${Math.floor(diffInMinutes / 1440) > 1 ? 's' : ''}`;
    
    return date.toLocaleDateString('fr-FR', { 
      day: 'numeric', 
      month: 'short',
      year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
  };

  // Gestion des actions
  const handleMarkAsRead = (notificationId) => {
    if (onMarkAsRead) {
      onMarkAsRead(notificationId);
    }
  };

  const handleMarkAllAsRead = () => {
    if (onMarkAllAsRead) {
      onMarkAllAsRead();
    }
  };

  const handleDeleteNotification = (notificationId) => {
    if (onDeleteNotification) {
      onDeleteNotification(notificationId);
    }
  };

  const handleNotificationClick = (notification) => {
    if (!notification.read) {
      handleMarkAsRead(notification.id);
    }
    
    if (notification.actionUrl) {
      // Simulation de navigation
      console.log('Navigate to:', notification.actionUrl);
    }
  };

  const toggleNotificationSelection = (notificationId) => {
    setSelectedNotifications(prev => 
      prev.includes(notificationId)
        ? prev.filter(id => id !== notificationId)
        : [...prev, notificationId]
    );
  };

  const handleBulkAction = (action) => {
    switch (action) {
      case 'markRead':
        selectedNotifications.forEach(id => handleMarkAsRead(id));
        break;
      case 'delete':
        selectedNotifications.forEach(id => handleDeleteNotification(id));
        break;
      case 'archive':
        // Implémentation de l'archivage
        console.log('Archive notifications:', selectedNotifications);
        break;
    }
    setSelectedNotifications([]);
  };

  // Effet sonore pour les nouvelles notifications
  useEffect(() => {
    if (soundEnabled && unreadCount > 0) {
      // Simulation d'un son de notification
      console.log('🔔 Nouvelle notification !');
    }
  }, [unreadCount, soundEnabled]);

  if (!isVisible) return null;

  return (
    <div className="nexus-notification-system">
      <div className="nexus-notification-header">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Bell className="w-6 h-6 text-blue-600" />
            {unreadCount > 0 && (
              <Badge className="absolute -top-2 -right-2 w-5 h-5 flex items-center justify-center p-0 text-xs bg-red-600">
                {unreadCount > 99 ? '99+' : unreadCount}
              </Badge>
            )}
          </div>
          <div>
            <h2 className="text-xl font-bold">Notifications</h2>
            <p className="text-sm text-muted-foreground">
              {unreadCount} non lue{unreadCount > 1 ? 's' : ''} sur {allNotifications.length}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSoundEnabled(!soundEnabled)}
            title={soundEnabled ? 'Désactiver les sons' : 'Activer les sons'}
          >
            {soundEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </Button>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowSettings(!showSettings)}
            title="Paramètres de notification"
          >
            <Settings className="w-4 h-4" />
          </Button>
          
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <div className="nexus-notification-content">
        {/* Onglets et filtres */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div className="flex space-x-1">
            <Button
              variant={activeTab === 'all' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setActiveTab('all')}
            >
              Toutes ({allNotifications.length})
            </Button>
            <Button
              variant={activeTab === 'unread' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setActiveTab('unread')}
            >
              Non lues ({unreadCount})
            </Button>
            <Button
              variant={activeTab === 'read' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setActiveTab('read')}
            >
              Lues ({allNotifications.length - unreadCount})
            </Button>
          </div>
          
          <div className="flex items-center space-x-2">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="nexus-input text-sm"
            >
              <option value="all">Toutes catégories</option>
              <option value="gamification">Gamification</option>
              <option value="documents">Documents</option>
              <option value="planning">Planning</option>
              <option value="communication">Communication</option>
              <option value="evaluation">Évaluations</option>
              <option value="ai_recommendation">Recommandations IA</option>
              <option value="goals">Objectifs</option>
              <option value="system">Système</option>
            </select>
            
            {unreadCount > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleMarkAllAsRead}
              >
                <Check className="w-4 h-4 mr-2" />
                Tout marquer comme lu
              </Button>
            )}
          </div>
        </div>

        {/* Actions en lot */}
        {selectedNotifications.length > 0 && (
          <div className="flex items-center justify-between p-3 mb-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <span className="text-sm font-medium">
              {selectedNotifications.length} notification{selectedNotifications.length > 1 ? 's' : ''} sélectionnée{selectedNotifications.length > 1 ? 's' : ''}
            </span>
            <div className="flex space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleBulkAction('markRead')}
              >
                <Check className="w-3 h-3 mr-1" />
                Marquer comme lues
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleBulkAction('archive')}
              >
                <Archive className="w-3 h-3 mr-1" />
                Archiver
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleBulkAction('delete')}
              >
                <Trash2 className="w-3 h-3 mr-1" />
                Supprimer
              </Button>
            </div>
          </div>
        )}

        {/* Liste des notifications */}
        <div className="space-y-3">
          {filteredNotifications.length === 0 ? (
            <div className="text-center py-12">
              <Bell className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Aucune notification</h3>
              <p className="text-muted-foreground">
                {activeTab === 'unread' 
                  ? 'Toutes vos notifications sont à jour !' 
                  : 'Vous n\'avez pas encore de notifications.'}
              </p>
            </div>
          ) : (
            filteredNotifications.map((notification) => {
              const typeConfig = notificationTypes[notification.type] || notificationTypes.info;
              const TypeIcon = typeConfig.icon;
              
              return (
                <Card
                  key={notification.id}
                  className={`nexus-notification-card ${
                    !notification.read ? 'unread' : ''
                  } ${typeConfig.bgColor} ${typeConfig.borderColor} cursor-pointer transition-all hover:shadow-md`}
                  onClick={() => handleNotificationClick(notification)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start space-x-4">
                      {/* Checkbox de sélection */}
                      <input
                        type="checkbox"
                        checked={selectedNotifications.includes(notification.id)}
                        onChange={(e) => {
                          e.stopPropagation();
                          toggleNotificationSelection(notification.id);
                        }}
                        className="mt-1 rounded"
                      />
                      
                      {/* Icône de type */}
                      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${typeConfig.bgColor}`}>
                        <TypeIcon className={`w-5 h-5 ${typeConfig.color}`} />
                      </div>
                      
                      {/* Contenu principal */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between mb-2">
                          <h4 className={`font-semibold ${!notification.read ? 'text-foreground' : 'text-muted-foreground'}`}>
                            {notification.title}
                          </h4>
                          <div className="flex items-center space-x-2 ml-4">
                            {notification.priority === 'high' && (
                              <Badge variant="destructive" className="text-xs">
                                Urgent
                              </Badge>
                            )}
                            {!notification.read && (
                              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                            )}
                          </div>
                        </div>
                        
                        <p className={`text-sm mb-3 ${!notification.read ? 'text-foreground' : 'text-muted-foreground'}`}>
                          {notification.message}
                        </p>
                        
                        {/* Métadonnées spécifiques */}
                        {notification.metadata && (
                          <div className="flex flex-wrap gap-2 mb-3">
                            {notification.type === 'achievement' && notification.metadata.xpEarned && (
                              <Badge variant="outline" className="text-xs">
                                +{notification.metadata.xpEarned} XP
                              </Badge>
                            )}
                            {notification.metadata.subject && (
                              <Badge variant="outline" className="text-xs">
                                {notification.metadata.subject}
                              </Badge>
                            )}
                            {notification.metadata.teacher && (
                              <Badge variant="outline" className="text-xs">
                                {notification.metadata.teacher}
                              </Badge>
                            )}
                          </div>
                        )}
                        
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-muted-foreground">
                            {formatTimestamp(notification.timestamp)}
                          </span>
                          
                          <div className="flex items-center space-x-2">
                            {notification.actionText && (
                              <Button
                                variant="ghost"
                                size="sm"
                                className="text-xs"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleNotificationClick(notification);
                                }}
                              >
                                {notification.actionText}
                                <ExternalLink className="w-3 h-3 ml-1" />
                              </Button>
                            )}
                            
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteNotification(notification.id);
                              }}
                            >
                              <Trash2 className="w-3 h-3" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })
          )}
        </div>

        {/* Pagination si nécessaire */}
        {filteredNotifications.length > 20 && (
          <div className="flex justify-center mt-6">
            <Button variant="outline">
              Charger plus de notifications
            </Button>
          </div>
        )}
      </div>

      {/* Panneau des paramètres */}
      {showSettings && (
        <div className="nexus-notification-settings">
          <Card className="nexus-card">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Settings className="w-5 h-5" />
                <span>Paramètres de notification</span>
              </CardTitle>
              <CardDescription>
                Personnalisez vos préférences de notification
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Canaux de notification */}
              <div>
                <h4 className="font-semibold mb-3">Canaux de notification</h4>
                <div className="space-y-3">
                  <label className="flex items-center space-x-3">
                    <input type="checkbox" defaultChecked className="rounded" />
                    <Bell className="w-4 h-4" />
                    <span>Notifications dans l'application</span>
                  </label>
                  <label className="flex items-center space-x-3">
                    <input type="checkbox" defaultChecked className="rounded" />
                    <Mail className="w-4 h-4" />
                    <span>Notifications par email</span>
                  </label>
                  <label className="flex items-center space-x-3">
                    <input type="checkbox" className="rounded" />
                    <Smartphone className="w-4 h-4" />
                    <span>Notifications push mobile</span>
                  </label>
                </div>
              </div>
              
              {/* Types de notifications */}
              <div>
                <h4 className="font-semibold mb-3">Types de notifications</h4>
                <div className="space-y-3">
                  <label className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <Award className="w-4 h-4 text-purple-600" />
                      <span>Badges et récompenses</span>
                    </div>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </label>
                  <label className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <MessageSquare className="w-4 h-4 text-indigo-600" />
                      <span>Messages des professeurs</span>
                    </div>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </label>
                  <label className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <Calendar className="w-4 h-4 text-orange-600" />
                      <span>Rappels de sessions</span>
                    </div>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </label>
                  <label className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <Brain className="w-4 h-4 text-blue-600" />
                      <span>Recommandations ARIA</span>
                    </div>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </label>
                  <label className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <Target className="w-4 h-4 text-green-600" />
                      <span>Objectifs et défis</span>
                    </div>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </label>
                </div>
              </div>
              
              {/* Fréquence */}
              <div>
                <h4 className="font-semibold mb-3">Fréquence des résumés</h4>
                <select className="nexus-input w-full">
                  <option value="realtime">Temps réel</option>
                  <option value="hourly">Toutes les heures</option>
                  <option value="daily">Quotidien</option>
                  <option value="weekly">Hebdomadaire</option>
                </select>
              </div>
              
              {/* Heures silencieuses */}
              <div>
                <h4 className="font-semibold mb-3">Heures silencieuses</h4>
                <div className="flex items-center space-x-4">
                  <div>
                    <label className="block text-sm text-muted-foreground mb-1">De</label>
                    <input type="time" defaultValue="22:00" className="nexus-input" />
                  </div>
                  <div>
                    <label className="block text-sm text-muted-foreground mb-1">À</label>
                    <input type="time" defaultValue="08:00" className="nexus-input" />
                  </div>
                </div>
              </div>
              
              <div className="flex space-x-2">
                <Button onClick={() => setShowSettings(false)}>
                  Sauvegarder
                </Button>
                <Button variant="outline" onClick={() => setShowSettings(false)}>
                  Annuler
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

// Composant de notification toast pour les nouvelles notifications
export const NotificationToast = ({ notification, onClose, onAction }) => {
  const typeConfig = {
    success: { icon: CheckCircle, color: 'text-green-600', bgColor: 'bg-green-50 border-green-200' },
    info: { icon: Info, color: 'text-blue-600', bgColor: 'bg-blue-50 border-blue-200' },
    warning: { icon: AlertTriangle, color: 'text-yellow-600', bgColor: 'bg-yellow-50 border-yellow-200' },
    error: { icon: XCircle, color: 'text-red-600', bgColor: 'bg-red-50 border-red-200' },
    achievement: { icon: Award, color: 'text-purple-600', bgColor: 'bg-purple-50 border-purple-200' }
  }[notification.type] || { icon: Info, color: 'text-blue-600', bgColor: 'bg-blue-50 border-blue-200' };

  const TypeIcon = typeConfig.icon;

  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 5000);

    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`nexus-notification-toast ${typeConfig.bgColor} border rounded-lg shadow-lg p-4 max-w-sm`}>
      <div className="flex items-start space-x-3">
        <TypeIcon className={`w-5 h-5 ${typeConfig.color} mt-0.5`} />
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-sm">{notification.title}</h4>
          <p className="text-sm text-muted-foreground mt-1">{notification.message}</p>
          {notification.actionText && (
            <Button
              variant="ghost"
              size="sm"
              className="mt-2 p-0 h-auto text-xs"
              onClick={onAction}
            >
              {notification.actionText}
            </Button>
          )}
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={onClose}
          className="p-0 h-auto"
        >
          <X className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
};

export default NotificationSystem;

