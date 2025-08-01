import { io } from 'socket.io-client';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  // Connexion au serveur WebSocket
  connect() {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:5000';
    const token = localStorage.getItem('access_token');

    if (!token) {
      console.warn('No auth token found, cannot connect to WebSocket');
      return;
    }

    this.socket = io(wsUrl, {
      auth: {
        token: token,
      },
      transports: ['websocket'],
      upgrade: false,
    });

    // Événements de connexion
    this.socket.on('connect', () => {
      console.log('✅ Connected to WebSocket server');
      this.isConnected = true;
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', (reason) => {
      console.log('❌ Disconnected from WebSocket server:', reason);
      this.isConnected = false;

      if (reason === 'io server disconnect') {
        // Le serveur a fermé la connexion, tentative de reconnexion
        this.handleReconnection();
      }
    });

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      this.handleReconnection();
    });

    // Événements métier
    this.setupBusinessEvents();

    return this.socket;
  }

  // Configuration des événements métier
  setupBusinessEvents() {
    if (!this.socket) return;

    // Notifications en temps réel
    this.socket.on('notification', (data) => {
      console.log('📢 New notification:', data);
      // Dispatch custom event pour les composants React
      window.dispatchEvent(new CustomEvent('newNotification', { detail: data }));
    });

    // Mise à jour de progression
    this.socket.on('progress_update', (data) => {
      console.log('📈 Progress update:', data);
      window.dispatchEvent(new CustomEvent('progressUpdate', { detail: data }));
    });

    // Messages ARIA
    this.socket.on('aria_response', (data) => {
      console.log('🤖 ARIA response:', data);
      window.dispatchEvent(new CustomEvent('ariaResponse', { detail: data }));
    });

    // Mise à jour de statut en ligne
    this.socket.on('user_status', (data) => {
      console.log('👤 User status update:', data);
      window.dispatchEvent(new CustomEvent('userStatusUpdate', { detail: data }));
    });

    // Sessions de classe/conférence
    this.socket.on('class_session_update', (data) => {
      console.log('🎓 Class session update:', data);
      window.dispatchEvent(new CustomEvent('classSessionUpdate', { detail: data }));
    });
  }

  // Gestion de la reconnexion
  handleReconnection() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

    console.log(`🔄 Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);

    setTimeout(() => {
      if (!this.isConnected) {
        this.connect();
      }
    }, delay);
  }

  // Émission d'événements
  emit(event, data) {
    if (this.socket && this.isConnected) {
      this.socket.emit(event, data);
    } else {
      console.warn(`Cannot emit ${event}: WebSocket not connected`);
    }
  }

  // Rejoindre une room (pour les sessions de classe)
  joinRoom(roomId) {
    this.emit('join_room', { room_id: roomId });
  }

  // Quitter une room
  leaveRoom(roomId) {
    this.emit('leave_room', { room_id: roomId });
  }

  // Envoyer un message dans une room
  sendToRoom(roomId, message) {
    this.emit('room_message', {
      room_id: roomId,
      message: message,
    });
  }

  // Mise à jour du statut utilisateur
  updateUserStatus(status) {
    this.emit('update_status', { status });
  }

  // Envoyer un message à ARIA
  sendAriaMessage(message, context = {}) {
    this.emit('aria_message', {
      message,
      context,
      timestamp: new Date().toISOString(),
    });
  }

  // Déconnexion propre
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
      this.reconnectAttempts = 0;
    }
  }

  // Vérifier l'état de connexion
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      socket: this.socket,
      reconnectAttempts: this.reconnectAttempts,
    };
  }

  // Écouter un événement spécifique
  on(event, callback) {
    if (this.socket) {
      this.socket.on(event, callback);
    }
  }

  // Arrêter d'écouter un événement
  off(event, callback) {
    if (this.socket) {
      this.socket.off(event, callback);
    }
  }
}

// Instance singleton
const wsService = new WebSocketService();

export default wsService;
