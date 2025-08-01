import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useAppStore = create(
  persist(
    (set, get) => ({
      // État de l'interface
      theme: 'light',
      sidebarOpen: true,
      language: 'fr',

      // État de navigation
      currentPage: 'dashboard',
      breadcrumbs: [],

      // États de chargement
      globalLoading: false,
      loadingStates: {},

      // Notifications
      notifications: [],
      unreadCount: 0,

      // Modal et overlay
      activeModal: null,
      modalData: null,

      // WebSocket état
      wsConnected: false,

      // Actions - Interface
      setTheme: (theme) => set({ theme }),

      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),

      setSidebarOpen: (open) => set({ sidebarOpen: open }),

      setLanguage: (language) => set({ language }),

      // Actions - Navigation
      setCurrentPage: (page) => set({ currentPage: page }),

      setBreadcrumbs: (breadcrumbs) => set({ breadcrumbs }),

      addBreadcrumb: (breadcrumb) => set((state) => ({
        breadcrumbs: [...state.breadcrumbs, breadcrumb],
      })),

      // Actions - Chargement
      setGlobalLoading: (loading) => set({ globalLoading: loading }),

      setLoadingState: (key, loading) => set((state) => ({
        loadingStates: {
          ...state.loadingStates,
          [key]: loading,
        },
      })),

      getLoadingState: (key) => {
        const { loadingStates } = get();
        return loadingStates[key] || false;
      },

      // Actions - Notifications
      addNotification: (notification) => {
        const id = Date.now().toString();
        const newNotification = {
          id,
          timestamp: new Date().toISOString(),
          read: false,
          ...notification,
        };

        set((state) => ({
          notifications: [newNotification, ...state.notifications],
          unreadCount: state.unreadCount + 1,
        }));

        return id;
      },

      markNotificationAsRead: (id) => set((state) => ({
        notifications: state.notifications.map((notif) =>
          notif.id === id ? { ...notif, read: true } : notif
        ),
        unreadCount: Math.max(0, state.unreadCount - 1),
      })),

      markAllNotificationsAsRead: () => set((state) => ({
        notifications: state.notifications.map((notif) => ({ ...notif, read: true })),
        unreadCount: 0,
      })),

      removeNotification: (id) => set((state) => ({
        notifications: state.notifications.filter((notif) => notif.id !== id),
        unreadCount: state.notifications.find((n) => n.id === id && !n.read)
          ? state.unreadCount - 1
          : state.unreadCount,
      })),

      clearNotifications: () => set({ notifications: [], unreadCount: 0 }),

      // Actions - Modal
      openModal: (modalType, data = null) => set({
        activeModal: modalType,
        modalData: data,
      }),

      closeModal: () => set({
        activeModal: null,
        modalData: null,
      }),

      // Actions - WebSocket
      setWsConnected: (connected) => set({ wsConnected: connected }),

      // Actions - Utilitaires
      showSuccess: (message, duration = 3000) => {
        const { addNotification } = get();
        const id = addNotification({
          type: 'success',
          title: 'Succès',
          message,
        });

        if (duration > 0) {
          setTimeout(() => {
            get().removeNotification(id);
          }, duration);
        }

        return id;
      },

      showError: (message, duration = 5000) => {
        const { addNotification } = get();
        const id = addNotification({
          type: 'error',
          title: 'Erreur',
          message,
        });

        if (duration > 0) {
          setTimeout(() => {
            get().removeNotification(id);
          }, duration);
        }

        return id;
      },

      showWarning: (message, duration = 4000) => {
        const { addNotification } = get();
        const id = addNotification({
          type: 'warning',
          title: 'Attention',
          message,
        });

        if (duration > 0) {
          setTimeout(() => {
            get().removeNotification(id);
          }, duration);
        }

        return id;
      },

      showInfo: (message, duration = 3000) => {
        const { addNotification } = get();
        const id = addNotification({
          type: 'info',
          title: 'Information',
          message,
        });

        if (duration > 0) {
          setTimeout(() => {
            get().removeNotification(id);
          }, duration);
        }

        return id;
      },

      // Préférences utilisateur
      preferences: {
        autoSave: true,
        notifications: {
          email: true,
          push: true,
          sound: true,
        },
        dashboard: {
          showWelcome: true,
          compactMode: false,
        },
      },

      updatePreferences: (newPreferences) => set((state) => ({
        preferences: {
          ...state.preferences,
          ...newPreferences,
        },
      })),

      // Réinitialisation
      reset: () => set({
        currentPage: 'dashboard',
        breadcrumbs: [],
        globalLoading: false,
        loadingStates: {},
        activeModal: null,
        modalData: null,
        notifications: [],
        unreadCount: 0,
      }),
    }),
    {
      name: 'nexus-app-storage',
      partialize: (state) => ({
        theme: state.theme,
        sidebarOpen: state.sidebarOpen,
        language: state.language,
        preferences: state.preferences,
      }),
    }
  )
);

export default useAppStore;
