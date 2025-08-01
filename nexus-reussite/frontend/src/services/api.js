import axios from 'axios';

// Configuration de base pour l'API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1';

// Instance axios avec configuration par défaut
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token JWT automatiquement
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs de réponse
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expiré, rediriger vers la page de connexion
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

// === SERVICES D'AUTHENTIFICATION ===
export const authService = {
  login: async (email, password) => {
    const response = await apiClient.post('/auth/login', { email, password });
    const { access_token, refresh_token, user } = response.data;

    // Stocker les tokens
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(user));

    return response.data;
  },

  register: async (userData) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  logout: async () => {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },

  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    return access_token;
  },

  getCurrentUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};

// === SERVICES UTILISATEUR ===
export const userService = {
  getProfile: async () => {
    const response = await apiClient.get('/users/profile');
    return response.data;
  },

  updateProfile: async (profileData) => {
    const response = await apiClient.put('/users/profile', profileData);
    return response.data;
  },

  changePassword: async (currentPassword, newPassword) => {
    const response = await apiClient.put('/users/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
    return response.data;
  },
};

// === SERVICES COURS ET CONTENU ===
export const contentService = {
  getCourses: async (params = {}) => {
    const response = await apiClient.get('/courses', { params });
    return response.data;
  },

  getCourse: async (courseId) => {
    const response = await apiClient.get(`/courses/${courseId}`);
    return response.data;
  },

  getLessons: async (courseId) => {
    const response = await apiClient.get(`/courses/${courseId}/lessons`);
    return response.data;
  },

  getLesson: async (lessonId) => {
    const response = await apiClient.get(`/lessons/${lessonId}`);
    return response.data;
  },

  createCourse: async (courseData) => {
    const response = await apiClient.post('/courses', courseData);
    return response.data;
  },

  updateCourse: async (courseId, courseData) => {
    const response = await apiClient.put(`/courses/${courseId}`, courseData);
    return response.data;
  },

  deleteCourse: async (courseId) => {
    const response = await apiClient.delete(`/courses/${courseId}`);
    return response.data;
  },
};

// === SERVICES PROGRESSION ===
export const progressService = {
  getStudentProgress: async (studentId) => {
    const response = await apiClient.get(`/progress/student/${studentId}`);
    return response.data;
  },

  markLessonComplete: async (lessonId) => {
    const response = await apiClient.post(`/progress/lesson/${lessonId}/complete`);
    return response.data;
  },

  getProgressStats: async () => {
    const response = await apiClient.get('/progress/stats');
    return response.data;
  },
};

// === SERVICES ARIA (IA) ===
export const ariaService = {
  sendMessage: async (message, context = {}) => {
    const response = await apiClient.post('/aria/chat', {
      message,
      context,
    });
    return response.data;
  },

  getConversationHistory: async (limit = 50) => {
    const response = await apiClient.get('/aria/history', {
      params: { limit },
    });
    return response.data;
  },

  clearConversation: async () => {
    const response = await apiClient.delete('/aria/history');
    return response.data;
  },
};

// === SERVICES QUIZ ET ÉVALUATIONS ===
export const quizService = {
  getQuizzes: async (courseId) => {
    const response = await apiClient.get(`/courses/${courseId}/quizzes`);
    return response.data;
  },

  getQuiz: async (quizId) => {
    const response = await apiClient.get(`/quizzes/${quizId}`);
    return response.data;
  },

  submitQuizAnswers: async (quizId, answers) => {
    const response = await apiClient.post(`/quizzes/${quizId}/submit`, {
      answers,
    });
    return response.data;
  },

  getQuizResults: async (quizId) => {
    const response = await apiClient.get(`/quizzes/${quizId}/results`);
    return response.data;
  },
};

// === SERVICES NOTIFICATIONS ===
export const notificationService = {
  getNotifications: async () => {
    const response = await apiClient.get('/notifications');
    return response.data;
  },

  markAsRead: async (notificationId) => {
    const response = await apiClient.put(`/notifications/${notificationId}/read`);
    return response.data;
  },

  markAllAsRead: async () => {
    const response = await apiClient.put('/notifications/read-all');
    return response.data;
  },
};

// Export de l'instance axios pour des cas d'usage spécifiques
export default apiClient;
