/**
 * Service WebSocket pour les notifications en temps réel
 */

class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 1000;
    this.listeners = new Map();
    this.isConnected = false;
    this.userId = null;
    this.userRole = null;
    this.heartbeatInterval = null;
  }

  // Connexion WebSocket
  connect(userId, userRole, token) {
    this.userId = userId;
    this.userRole = userRole;
    
    const wsUrl = process.env.NODE_ENV === 'production'
      ? `wss://your-production-domain.com/ws`
      : `ws://localhost:5000/ws`;
    
    try {
      this.ws = new WebSocket(`${wsUrl}?token=${token}&user_id=${userId}&role=${userRole}`);
      
      this.ws.onopen = this.onOpen.bind(this);
      this.ws.onmessage = this.onMessage.bind(this);
      this.ws.onclose = this.onClose.bind(this);
      this.ws.onerror = this.onError.bind(this);
      
    } catch (error) {
      console.error('Erreur lors de la connexion WebSocket:', error);
      this.scheduleReconnect();
    }
  }

  // Événements WebSocket
  onOpen(event) {
    console.log('WebSocket connecté');
    this.isConnected = true;
    this.reconnectAttempts = 0;
    
    // Démarrer le heartbeat
    this.startHeartbeat();
    
    // Notifier les listeners
    this.emit('connected', { userId: this.userId, userRole: this.userRole });
  }

  onMessage(event) {
    try {
      const data = JSON.parse(event.data);
      
      // Gérer les différents types de messages
      switch (data.type) {
        case 'notification':
          this.handleNotification(data.data);
          break;
        case 'progress_update':
          this.handleProgressUpdate(data.data);
          break;
        case 'achievement_unlocked':
          this.handleAchievementUnlocked(data.data);
          break;
        case 'teacher_message':
          this.handleTeacherMessage(data.data);
          break;
        case 'conference_invitation':
          this.handleConferenceInvitation(data.data);
          break;
        case 'system_alert':
          this.handleSystemAlert(data.data);
          break;
        case 'heartbeat':
          this.handleHeartbeat(data.data);
          break;
        case 'broadcast_notification':
          this.handleBroadcastNotification(data.data);
          break;
        default:
          console.log('Message WebSocket non géré:', data);
      }
      
      // Émettre l'événement générique
      this.emit('message', data);
      
    } catch (error) {
      console.error('Erreur lors du parsing du message WebSocket:', error);
    }
  }

  onClose(event) {
    console.log('WebSocket fermé:', event.code, event.reason);
    this.isConnected = false;
    this.stopHeartbeat();
    
    // Notifier les listeners
    this.emit('disconnected', { code: event.code, reason: event.reason });
    
    // Tentative de reconnexion si ce n'est pas une fermeture volontaire
    if (event.code !== 1000) {
      this.scheduleReconnect();
    }
  }

  onError(error) {
    console.error('Erreur WebSocket:', error);
    this.emit('error', error);
  }

  // Gestion des différents types de messages
  handleNotification(notification) {
    console.log('Nouvelle notification:', notification);
    
    // Afficher une notification native si possible
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/favicon.ico',
        tag: notification.id
      });
    }
    
    // Émettre l'événement pour les composants
    this.emit('notification', notification);
  }

  handleProgressUpdate(progressData) {
    console.log('Mise à jour de progression:', progressData);
    this.emit('progress_update', progressData);
  }

  handleAchievementUnlocked(achievement) {
    console.log('Nouveau succès débloqué:', achievement);
    
    // Notification spéciale pour les succès
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('🏆 Nouveau succès débloqué !', {
        body: achievement.name,
        icon: '/favicon.ico',
        tag: `achievement_${achievement.id}`
      });
    }
    
    this.emit('achievement_unlocked', achievement);
  }

  handleTeacherMessage(message) {
    console.log('Message d\'enseignant:', message);
    this.emit('teacher_message', message);
  }

  handleConferenceInvitation(invitation) {
    console.log('Invitation à une conférence:', invitation);
    this.emit('conference_invitation', invitation);
  }

  handleSystemAlert(alert) {
    console.log('Alerte système:', alert);
    this.emit('system_alert', alert);
  }

  handleHeartbeat(data) {
    // Répondre au heartbeat
    this.send({
      type: 'heartbeat_response',
      timestamp: Date.now()
    });
  }

  handleBroadcastNotification(notification) {
    console.log('Notification diffusée:', notification);
    this.emit('broadcast_notification', notification);
  }

  // Gestion du heartbeat
  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.isConnected) {
        this.send({
          type: 'heartbeat',
          timestamp: Date.now()
        });
      }
    }, 30000); // Toutes les 30 secondes
  }

  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  // Reconnexion automatique
  scheduleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1);
      
      console.log(`Tentative de reconnexion ${this.reconnectAttempts}/${this.maxReconnectAttempts} dans ${delay}ms`);
      
      setTimeout(() => {
        if (this.userId && this.userRole) {
          const token = localStorage.getItem('auth_token');
          if (token) {
            this.connect(this.userId, this.userRole, token);
          }
        }
      }, delay);
    } else {
      console.error('Nombre maximum de tentatives de reconnexion atteint');
      this.emit('max_reconnect_attempts_reached');
    }
  }

  // Envoi de messages
  send(data) {
    if (this.isConnected && this.ws) {
      try {
        this.ws.send(JSON.stringify(data));
        return true;
      } catch (error) {
        console.error('Erreur lors de l\'envoi du message:', error);
        return false;
      }
    } else {
      console.warn('WebSocket non connecté, impossible d\'envoyer le message');
      return false;
    }
  }

  // Envoi de notifications
  sendNotification(recipientId, title, message, type = 'info', data = {}) {
    return this.send({
      type: 'send_notification',
      data: {
        recipient_id: recipientId,
        title,
        message,
        notification_type: type,
        data
      }
    });
  }

  // Marquer une notification comme lue
  markNotificationRead(notificationId) {
    return this.send({
      type: 'mark_notification_read',
      data: {
        notification_id: notificationId
      }
    });
  }

  // Rejoindre une salle (pour les notifications de groupe)
  joinRoom(roomId) {
    return this.send({
      type: 'join_room',
      data: {
        room_id: roomId
      }
    });
  }

  // Quitter une salle
  leaveRoom(roomId) {
    return this.send({
      type: 'leave_room',
      data: {
        room_id: roomId
      }
    });
  }

  // Gestion des événements
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Erreur dans le callback de l'événement ${event}:`, error);
        }
      });
    }
  }

  // Déconnexion
  disconnect() {
    this.stopHeartbeat();
    
    if (this.ws) {
      this.ws.close(1000, 'Déconnexion volontaire');
      this.ws = null;
    }
    
    this.isConnected = false;
    this.userId = null;
    this.userRole = null;
    this.reconnectAttempts = 0;
  }

  // Statut de connexion
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      userId: this.userId,
      userRole: this.userRole,
      reconnectAttempts: this.reconnectAttempts
    };
  }

  // Demander la permission pour les notifications natives
  async requestNotificationPermission() {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    }
    return false;
  }

  // Vérifier si les notifications sont supportées
  isNotificationSupported() {
    return 'Notification' in window;
  }

  // Vérifier si les notifications sont autorisées
  isNotificationPermissionGranted() {
    return 'Notification' in window && Notification.permission === 'granted';
  }
}

// Instance singleton
const webSocketService = new WebSocketService();

export default webSocketService;

// Hook React pour utiliser le WebSocket
export function useWebSocket() {
  const [isConnected, setIsConnected] = React.useState(webSocketService.isConnected);
  const [notifications, setNotifications] = React.useState([]);

  React.useEffect(() => {
    const handleConnected = () => setIsConnected(true);
    const handleDisconnected = () => setIsConnected(false);
    const handleNotification = (notification) => {
      setNotifications(prev => [notification, ...prev].slice(0, 50)); // Garder les 50 dernières
    };

    webSocketService.on('connected', handleConnected);
    webSocketService.on('disconnected', handleDisconnected);
    webSocketService.on('notification', handleNotification);

    return () => {
      webSocketService.off('connected', handleConnected);
      webSocketService.off('disconnected', handleDisconnected);
      webSocketService.off('notification', handleNotification);
    };
  }, []);

  return {
    isConnected,
    notifications,
    send: webSocketService.send.bind(webSocketService),
    sendNotification: webSocketService.sendNotification.bind(webSocketService),
    markNotificationRead: webSocketService.markNotificationRead.bind(webSocketService),
    on: webSocketService.on.bind(webSocketService),
    off: webSocketService.off.bind(webSocketService)
  };
}

