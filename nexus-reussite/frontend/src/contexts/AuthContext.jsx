import React, { createContext, useContext, useReducer, useEffect } from 'react';
import apiService from '../services/api';
import webSocketService from '../services/websocket';
import { parseJwt, isTokenExpired } from '../lib/utils';

// État initial
const initialState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
  error: null
};

// Actions
const AUTH_ACTIONS = {
  LOGIN_START: 'LOGIN_START',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILURE: 'LOGIN_FAILURE',
  LOGOUT: 'LOGOUT',
  SET_USER: 'SET_USER',
  SET_LOADING: 'SET_LOADING',
  CLEAR_ERROR: 'CLEAR_ERROR',
  UPDATE_PROFILE: 'UPDATE_PROFILE'
};

// Reducer
function authReducer(state, action) {
  switch (action.type) {
    case AUTH_ACTIONS.LOGIN_START:
      return {
        ...state,
        isLoading: true,
        error: null
      };
    
    case AUTH_ACTIONS.LOGIN_SUCCESS:
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
        error: null
      };
    
    case AUTH_ACTIONS.LOGIN_FAILURE:
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload.error
      };
    
    case AUTH_ACTIONS.LOGOUT:
      return {
        ...initialState,
        isLoading: false
      };
    
    case AUTH_ACTIONS.SET_USER:
      return {
        ...state,
        user: action.payload.user,
        isAuthenticated: true,
        isLoading: false
      };
    
    case AUTH_ACTIONS.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload.isLoading
      };
    
    case AUTH_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null
      };
    
    case AUTH_ACTIONS.UPDATE_PROFILE:
      return {
        ...state,
        user: {
          ...state.user,
          ...action.payload.updates
        }
      };
    
    default:
      return state;
  }
}

// Contexte
const AuthContext = createContext();

// Provider
export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Vérifier le token au chargement
  useEffect(() => {
    checkAuthStatus();
  }, []);

  // Configurer la reconnexion automatique du WebSocket
  useEffect(() => {
    if (state.isAuthenticated && state.user && state.token) {
      // Connecter le WebSocket
      webSocketService.connect(state.user.id, state.user.role, state.token);
      
      // Gérer la déconnexion automatique en cas d'erreur d'auth
      const handleAuthError = () => {
        console.log('Erreur d\'authentification WebSocket, déconnexion...');
        logout();
      };
      
      webSocketService.on('auth_error', handleAuthError);
      
      return () => {
        webSocketService.off('auth_error', handleAuthError);
      };
    } else {
      // Déconnecter le WebSocket
      webSocketService.disconnect();
    }
  }, [state.isAuthenticated, state.user, state.token]);

  // Vérifier le statut d'authentification
  async function checkAuthStatus() {
    dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: { isLoading: true } });
    
    try {
      const token = apiService.getToken();
      
      if (!token) {
        dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: { isLoading: false } });
        return;
      }

      // Vérifier si le token est expiré
      if (isTokenExpired(token)) {
        console.log('Token expiré, tentative de rafraîchissement...');
        try {
          const refreshResponse = await apiService.refreshToken();
          if (refreshResponse.success) {
            const userData = parseJwt(refreshResponse.token);
            dispatch({
              type: AUTH_ACTIONS.LOGIN_SUCCESS,
              payload: {
                user: userData,
                token: refreshResponse.token
              }
            });
            return;
          }
        } catch (refreshError) {
          console.log('Échec du rafraîchissement du token');
        }
        
        // Si le rafraîchissement échoue, déconnecter
        apiService.clearToken();
        dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: { isLoading: false } });
        return;
      }

      // Récupérer les informations utilisateur
      const userResponse = await apiService.getCurrentUser();
      if (userResponse.success) {
        dispatch({
          type: AUTH_ACTIONS.SET_USER,
          payload: { user: userResponse.user }
        });
      } else {
        throw new Error('Impossible de récupérer les informations utilisateur');
      }
      
    } catch (error) {
      console.error('Erreur lors de la vérification de l\'authentification:', error);
      apiService.clearToken();
      dispatch({
        type: AUTH_ACTIONS.LOGIN_FAILURE,
        payload: { error: error.message }
      });
    }
  }

  // Connexion
  async function login(email, password) {
    dispatch({ type: AUTH_ACTIONS.LOGIN_START });
    
    try {
      const response = await apiService.login(email, password);
      
      if (response.success) {
        const userData = parseJwt(response.token);
        dispatch({
          type: AUTH_ACTIONS.LOGIN_SUCCESS,
          payload: {
            user: userData,
            token: response.token
          }
        });
        return { success: true };
      } else {
        throw new Error(response.error || 'Erreur de connexion');
      }
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.LOGIN_FAILURE,
        payload: { error: error.message }
      });
      return { success: false, error: error.message };
    }
  }

  // Inscription
  async function register(userData) {
    dispatch({ type: AUTH_ACTIONS.LOGIN_START });
    
    try {
      const response = await apiService.register(userData);
      
      if (response.success) {
        // Connexion automatique après inscription
        return await login(userData.email, userData.password);
      } else {
        throw new Error(response.error || 'Erreur lors de l\'inscription');
      }
    } catch (error) {
      dispatch({
        type: AUTH_ACTIONS.LOGIN_FAILURE,
        payload: { error: error.message }
      });
      return { success: false, error: error.message };
    }
  }

  // Déconnexion
  async function logout() {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
    } finally {
      // Déconnecter le WebSocket
      webSocketService.disconnect();
      
      // Nettoyer l'état
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    }
  }

  // Mise à jour du profil
  async function updateProfile(updates) {
    try {
      const response = await apiService.updateProfile(updates);
      
      if (response.success) {
        dispatch({
          type: AUTH_ACTIONS.UPDATE_PROFILE,
          payload: { updates: response.user }
        });
        return { success: true };
      } else {
        throw new Error(response.error || 'Erreur lors de la mise à jour');
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Upload d'avatar
  async function uploadAvatar(file) {
    try {
      const response = await apiService.uploadAvatar(file);
      
      if (response.success) {
        dispatch({
          type: AUTH_ACTIONS.UPDATE_PROFILE,
          payload: { updates: { avatar_url: response.avatar_url } }
        });
        return { success: true, avatar_url: response.avatar_url };
      } else {
        throw new Error(response.error || 'Erreur lors de l\'upload');
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Effacer les erreurs
  function clearError() {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  }

  // Vérifier les permissions
  function hasPermission(permission) {
    if (!state.user) return false;
    
    const userPermissions = state.user.permissions || [];
    return userPermissions.includes(permission);
  }

  // Vérifier le rôle
  function hasRole(role) {
    if (!state.user) return false;
    
    if (Array.isArray(role)) {
      return role.includes(state.user.role);
    }
    
    return state.user.role === role;
  }

  // Vérifier si l'utilisateur est un enseignant
  function isTeacher() {
    return hasRole('teacher');
  }

  // Vérifier si l'utilisateur est un élève
  function isStudent() {
    return hasRole('student');
  }

  // Vérifier si l'utilisateur est un parent
  function isParent() {
    return hasRole('parent');
  }

  // Vérifier si l'utilisateur est un admin
  function isAdmin() {
    return hasRole('admin');
  }

  // Obtenir les informations de l'utilisateur connecté
  function getCurrentUser() {
    return state.user;
  }

  // Obtenir le token
  function getToken() {
    return state.token;
  }

  // Vérifier si l'utilisateur est connecté
  function isAuthenticated() {
    return state.isAuthenticated;
  }

  // Valeurs du contexte
  const value = {
    // État
    user: state.user,
    token: state.token,
    isAuthenticated: state.isAuthenticated,
    isLoading: state.isLoading,
    error: state.error,
    
    // Actions
    login,
    register,
    logout,
    updateProfile,
    uploadAvatar,
    clearError,
    checkAuthStatus,
    
    // Utilitaires
    hasPermission,
    hasRole,
    isTeacher,
    isStudent,
    isParent,
    isAdmin,
    getCurrentUser,
    getToken
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook pour utiliser le contexte
export function useAuth() {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth doit être utilisé dans un AuthProvider');
  }
  
  return context;
}

// HOC pour protéger les routes
export function withAuth(Component, requiredRoles = []) {
  return function AuthenticatedComponent(props) {
    const { isAuthenticated, isLoading, hasRole } = useAuth();
    
    if (isLoading) {
      return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
        </div>
      );
    }
    
    if (!isAuthenticated) {
      // Rediriger vers la page de connexion
      window.location.href = '/login';
      return null;
    }
    
    if (requiredRoles.length > 0 && !hasRole(requiredRoles)) {
      return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Accès non autorisé
            </h2>
            <p className="text-gray-600">
              Vous n'avez pas les permissions nécessaires pour accéder à cette page.
            </p>
          </div>
        </div>
      );
    }
    
    return <Component {...props} />;
  };
}

export default AuthContext;

