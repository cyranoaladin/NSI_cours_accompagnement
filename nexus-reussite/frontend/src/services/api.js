/**
 * Service API principal pour Nexus Réussite
 */

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-production-domain.com/api'
  : 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('auth_token');
  }

  // Configuration des headers
  getHeaders(includeAuth = true) {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (includeAuth && this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  // Méthode générique pour les requêtes
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(options.auth !== false),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      
      return await response.text();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  // Méthodes HTTP
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    return this.request(url, { method: 'GET' });
  }

  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }

  // Gestion de l'authentification
  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  getToken() {
    return this.token;
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  // === AUTHENTIFICATION ===
  
  async login(email, password) {
    const response = await this.post('/auth/login', { email, password });
    if (response.success && response.token) {
      this.setToken(response.token);
    }
    return response;
  }

  async register(userData) {
    return this.post('/auth/register', userData);
  }

  async logout() {
    try {
      await this.post('/auth/logout');
    } finally {
      this.clearToken();
    }
  }

  async refreshToken() {
    const response = await this.post('/auth/refresh');
    if (response.success && response.token) {
      this.setToken(response.token);
    }
    return response;
  }

  async getCurrentUser() {
    return this.get('/auth/me');
  }

  // === PROFILS UTILISATEURS ===

  async getProfile() {
    return this.get('/profile');
  }

  async updateProfile(profileData) {
    return this.put('/profile', profileData);
  }

  async uploadAvatar(file) {
    const formData = new FormData();
    formData.append('avatar', file);
    
    return this.request('/profile/avatar', {
      method: 'POST',
      body: formData,
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
  }

  // === ÉTUDIANTS ===

  async getStudents(params = {}) {
    return this.get('/students', params);
  }

  async getStudent(studentId) {
    return this.get(`/students/${studentId}`);
  }

  async createStudent(studentData) {
    return this.post('/students', studentData);
  }

  async updateStudent(studentId, studentData) {
    return this.put(`/students/${studentId}`, studentData);
  }

  async deleteStudent(studentId) {
    return this.delete(`/students/${studentId}`);
  }

  async getStudentProgress(studentId) {
    return this.get(`/students/${studentId}/progress`);
  }

  async updateStudentProgress(studentId, progressData) {
    return this.put(`/students/${studentId}/progress`, progressData);
  }

  // === IA ARIA ===

  async chatWithAria(message, context = {}) {
    return this.post('/aria/chat', { message, context });
  }

  async getAriaRecommendations(studentId) {
    return this.get(`/aria/recommendations/${studentId}`);
  }

  async generatePersonalizedContent(studentId, subject, contentType) {
    return this.post('/aria/generate-content', {
      student_id: studentId,
      subject,
      content_type: contentType
    });
  }

  async getAriaAnalysis(studentId) {
    return this.get(`/aria/analysis/${studentId}`);
  }

  // === GÉNÉRATION DE DOCUMENTS ===

  async generateDocument(documentData) {
    return this.post('/documents/generate', documentData);
  }

  async getDocumentTemplates() {
    return this.get('/documents/templates');
  }

  async getGeneratedDocuments(params = {}) {
    return this.get('/documents', params);
  }

  async downloadDocument(documentId) {
    const response = await fetch(`${this.baseURL}/documents/${documentId}/download`, {
      headers: this.getHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Erreur lors du téléchargement');
    }
    
    return response.blob();
  }

  // === BIBLIOTHÈQUE DE CONTENU ===

  async getContentLibrary(params = {}) {
    return this.get('/content', params);
  }

  async getContentItem(contentId) {
    return this.get(`/content/${contentId}`);
  }

  async searchContent(query, filters = {}) {
    return this.get('/content/search', { query, ...filters });
  }

  async uploadContent(file, metadata) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadata));
    
    return this.request('/content/upload', {
      method: 'POST',
      body: formData,
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
  }

  // === VISIOCONFÉRENCE ===

  async createConference(conferenceData) {
    return this.post('/video-conference/create', conferenceData);
  }

  async createInstantConference(subject) {
    return this.post('/video-conference/instant', { subject });
  }

  async joinConference(roomId) {
    return this.post(`/video-conference/join/${roomId}`);
  }

  async leaveConference(roomId) {
    return this.post(`/video-conference/leave/${roomId}`);
  }

  async endConference(roomId) {
    return this.post(`/video-conference/end/${roomId}`);
  }

  async getUserRooms(includeHistory = false) {
    return this.get('/video-conference/rooms', { include_history: includeHistory });
  }

  async getRoomInfo(roomId) {
    return this.get(`/video-conference/room/${roomId}`);
  }

  async getActiveConferences() {
    return this.get('/video-conference/active');
  }

  async getConferenceStatistics() {
    return this.get('/video-conference/statistics');
  }

  // === NOTIFICATIONS ===

  async getNotifications(params = {}) {
    return this.get('/websocket/notifications', params);
  }

  async markNotificationRead(notificationId) {
    return this.post(`/websocket/notifications/${notificationId}/read`);
  }

  async markAllNotificationsRead() {
    return this.post('/websocket/notifications/mark-all-read');
  }

  async sendNotification(notificationData) {
    return this.post('/websocket/send-notification', notificationData);
  }

  // === GAMIFICATION ===

  async getAchievements(studentId) {
    return this.get(`/gamification/achievements/${studentId}`);
  }

  async unlockAchievement(studentId, achievementId) {
    return this.post(`/gamification/unlock/${studentId}/${achievementId}`);
  }

  async getLeaderboard(params = {}) {
    return this.get('/gamification/leaderboard', params);
  }

  async getStudentStats(studentId) {
    return this.get(`/gamification/stats/${studentId}`);
  }

  // === FORMULES ET TARIFS ===

  async getFormulas() {
    return this.get('/formulas');
  }

  async subscribeToFormula(formulaId, studentId) {
    return this.post('/formulas/subscribe', {
      formula_id: formulaId,
      student_id: studentId
    });
  }

  async getSubscriptions(studentId) {
    return this.get(`/formulas/subscriptions/${studentId}`);
  }

  // === ENSEIGNANTS ===

  async getTeachers() {
    return this.get('/teachers');
  }

  async getTeacher(teacherId) {
    return this.get(`/teachers/${teacherId}`);
  }

  async getTeacherAvailability(teacherId) {
    return this.get(`/teachers/${teacherId}/availability`);
  }

  async bookSession(teacherId, sessionData) {
    return this.post(`/teachers/${teacherId}/book`, sessionData);
  }

  // === RAPPORTS ===

  async getStudentReport(studentId, period = 'week') {
    return this.get(`/reports/student/${studentId}`, { period });
  }

  async getParentReport(parentId, period = 'week') {
    return this.get(`/reports/parent/${parentId}`, { period });
  }

  async getTeacherReport(teacherId, period = 'week') {
    return this.get(`/reports/teacher/${teacherId}`, { period });
  }

  async generateCustomReport(reportConfig) {
    return this.post('/reports/custom', reportConfig);
  }

  // === PAIEMENTS ===

  async getPaymentMethods() {
    return this.get('/payments/methods');
  }

  async processPayment(paymentData) {
    return this.post('/payments/process', paymentData);
  }

  async getPaymentHistory(params = {}) {
    return this.get('/payments/history', params);
  }

  async getInvoices(params = {}) {
    return this.get('/payments/invoices', params);
  }

  // === SUPPORT ===

  async createSupportTicket(ticketData) {
    return this.post('/support/tickets', ticketData);
  }

  async getSupportTickets() {
    return this.get('/support/tickets');
  }

  async updateSupportTicket(ticketId, updateData) {
    return this.put(`/support/tickets/${ticketId}`, updateData);
  }

  async getFAQ() {
    return this.get('/support/faq');
  }

  // === STATISTIQUES ===

  async getDashboardStats(userType, userId) {
    return this.get(`/stats/dashboard/${userType}/${userId}`);
  }

  async getUsageStats(params = {}) {
    return this.get('/stats/usage', params);
  }

  async getPerformanceStats(studentId, subject = null) {
    return this.get(`/stats/performance/${studentId}`, { subject });
  }

  // === UTILITAIRES ===

  async uploadFile(file, category = 'general') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    
    return this.request('/upload', {
      method: 'POST',
      body: formData,
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
  }

  async healthCheck() {
    return this.get('/health', {}, { auth: false });
  }

  async getSystemInfo() {
    return this.get('/info', {}, { auth: false });
  }
}

// Instance singleton
const apiService = new ApiService();

export default apiService;

