'use client';

import { ReactNode, useEffect } from 'react';
import { Toaster } from 'sonner';
import { useWebSocketNotifications } from '../hooks/useWebSocket';
import useAuthStore from '../stores/authStore';

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  const { initializeAuth } = useAuthStore();

  // Initialiser l'authentification au montage
  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  return (
    <>
      <AuthProvider>
        {children}
      </AuthProvider>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'white',
            border: '1px solid #e5e7eb',
            color: '#374151',
          },
        }}
      />
    </>
  );
}

function AuthProvider({ children }: { children: ReactNode; }) {
  // Utiliser le hook pour les notifications WebSocket
  useWebSocketNotifications();

  return <>{children}</>;
}
