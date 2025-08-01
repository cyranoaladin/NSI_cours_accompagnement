import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authService } from '../services/api';
import wsService from '../services/websocket';

const useAuthStore = create(
  persist(
    (set, get) => ({
      // État
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Actions
      login: async (email, password) => {
        set({ isLoading: true, error: null });

        try {
          const data = await authService.login(email, password);

          set({
            user: data.user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });

          // Connexion WebSocket après authentification
          wsService.connect();

          return { success: true, data };
        } catch (error) {
          const errorMessage = error.response?.data?.message || 'Erreur de connexion';
          set({
            isLoading: false,
            error: errorMessage,
            isAuthenticated: false,
            user: null,
          });

          return { success: false, error: errorMessage };
        }
      },

      register: async (userData) => {
        set({ isLoading: true, error: null });

        try {
          const data = await authService.register(userData);

          set({
            isLoading: false,
            error: null,
          });

          return { success: true, data };
        } catch (error) {
          const errorMessage = error.response?.data?.message || 'Erreur lors de l\'inscription';
          set({
            isLoading: false,
            error: errorMessage,
          });

          return { success: false, error: errorMessage };
        }
      },

      logout: async () => {
        set({ isLoading: true });

        try {
          await authService.logout();
        } catch (error) {
          console.error('Erreur lors de la déconnexion:', error);
        } finally {
          // Déconnexion WebSocket
          wsService.disconnect();

          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      },

      refreshToken: async () => {
        try {
          const token = await authService.refreshToken();
          return token;
        } catch (error) {
          // Token de rafraîchissement invalide, déconnexion
          get().logout();
          throw error;
        }
      },

      updateUser: (userData) => {
        set((state) => ({
          user: { ...state.user, ...userData },
        }));
      },

      clearError: () => {
        set({ error: null });
      },

      // Initialisation depuis le localStorage
      initializeAuth: () => {
        const user = authService.getCurrentUser();
        const token = localStorage.getItem('access_token');

        if (user && token) {
          set({
            user,
            isAuthenticated: true,
          });

          // Connexion WebSocket si utilisateur déjà connecté
          wsService.connect();
        }
      },

      // Vérifier le rôle utilisateur
      hasRole: (role) => {
        const { user } = get();
        return user?.role === role || user?.roles?.includes(role);
      },

      // Vérifier si l'utilisateur est étudiant
      isStudent: () => get().hasRole('student'),

      // Vérifier si l'utilisateur est enseignant
      isTeacher: () => get().hasRole('teacher'),

      // Vérifier si l'utilisateur est parent
      isParent: () => get().hasRole('parent'),

      // Vérifier si l'utilisateur est admin
      isAdmin: () => get().hasRole('admin'),
    }),
    {
      name: 'nexus-auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

export default useAuthStore;
