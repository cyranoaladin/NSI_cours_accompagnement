import { useCallback, useEffect } from 'react';
import wsService from '../services/websocket';
import useAppStore from '../stores/appStore';
import useAuthStore from '../stores/authStore';

export const useWebSocket = () => {
  const { isAuthenticated } = useAuthStore();
  const { setWsConnected, addNotification } = useAppStore();

  // Connexion automatique si authentifié
  useEffect(() => {
    if (isAuthenticated) {
      wsService.connect();
    } else {
      wsService.disconnect();
    }

    return () => {
      wsService.disconnect();
    };
  }, [isAuthenticated]);

  // Écoute des événements de connexion
  useEffect(() => {
    const handleConnect = () => {
      setWsConnected(true);
    };

    const handleDisconnect = () => {
      setWsConnected(false);
    };

    wsService.on('connect', handleConnect);
    wsService.on('disconnect', handleDisconnect);

    return () => {
      wsService.off('connect', handleConnect);
      wsService.off('disconnect', handleDisconnect);
    };
  }, [setWsConnected]);

  // Gestionnaires d'événements
  const emit = useCallback((event, data) => {
    wsService.emit(event, data);
  }, []);

  const joinRoom = useCallback((roomId) => {
    wsService.joinRoom(roomId);
  }, []);

  const leaveRoom = useCallback((roomId) => {
    wsService.leaveRoom(roomId);
  }, []);

  const sendToRoom = useCallback((roomId, message) => {
    wsService.sendToRoom(roomId, message);
  }, []);

  const updateStatus = useCallback((status) => {
    wsService.updateUserStatus(status);
  }, []);

  const sendAriaMessage = useCallback((message, context = {}) => {
    wsService.sendAriaMessage(message, context);
  }, []);

  return {
    isConnected: wsService.getConnectionStatus().isConnected,
    emit,
    joinRoom,
    leaveRoom,
    sendToRoom,
    updateStatus,
    sendAriaMessage,
    wsService,
  };
};

// Hook pour écouter des événements spécifiques
export const useWebSocketEvent = (eventName, handler, dependencies = []) => {
  useEffect(() => {
    wsService.on(eventName, handler);
    return () => wsService.off(eventName, handler);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [eventName, handler, ...dependencies]);
};

// Hook pour les notifications WebSocket
export const useWebSocketNotifications = () => {
  const { addNotification } = useAppStore();

  useEffect(() => {
    const handleNotification = (event) => {
      const { detail } = event;
      addNotification({
        type: detail.type || 'info',
        title: detail.title,
        message: detail.message,
        data: detail.data,
      });
    };

    window.addEventListener('newNotification', handleNotification);
    return () => window.removeEventListener('newNotification', handleNotification);
  }, [addNotification]);
};

// Hook pour les mises à jour de progression
export const useProgressUpdates = (onProgressUpdate) => {
  useEffect(() => {
    const handleProgressUpdate = (event) => {
      const { detail } = event;
      onProgressUpdate(detail);
    };

    window.addEventListener('progressUpdate', handleProgressUpdate);
    return () => window.removeEventListener('progressUpdate', handleProgressUpdate);
  }, [onProgressUpdate]);
};

// Hook pour ARIA WebSocket
export const useAriaWebSocket = (onResponse) => {
  const { sendAriaMessage } = useWebSocket();

  useEffect(() => {
    const handleAriaResponse = (event) => {
      const { detail } = event;
      onResponse(detail);
    };

    window.addEventListener('ariaResponse', handleAriaResponse);
    return () => window.removeEventListener('ariaResponse', handleAriaResponse);
  }, [onResponse]);

  return { sendAriaMessage };
};
