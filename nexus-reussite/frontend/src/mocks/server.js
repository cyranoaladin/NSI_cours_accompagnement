import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

// Handlers pour simuler les API calls
export const handlers = [
  // Authentification
  http.post('/api/auth/login', () => {
    return HttpResponse.json({
      user: { id: 1, email: 'test@example.com', role: 'student' },
      token: 'mock-jwt-token'
    });
  }),

  http.get('/api/auth/me', () => {
    return HttpResponse.json({
      id: 1,
      email: 'test@example.com',
      first_name: 'Test',
      last_name: 'User',
      role: 'student'
    });
  }),

  // Dashboard étudiant
  http.get('/api/students/dashboard', () => {
    return HttpResponse.json({
      progress: 75,
      recent_exercises: [
        { id: 1, title: 'Dérivées', score: 85, date: '2025-07-23' },
        { id: 2, title: 'Intégrales', score: 78, date: '2025-07-22' }
      ],
      upcoming_sessions: [
        { id: 1, subject: 'Mathématiques', date: '2025-07-24T14:00:00Z' }
      ],
      stats: {
        total_exercises: 20,
        completed_exercises: 15,
        average_score: 82
      }
    });
  }),

  // ARIA Chat
  http.post('/api/aria/chat', async ({ request }) => {
    const { message } = await request.json();
    return HttpResponse.json({
      response: `Bonjour ! Vous avez dit: "${message}". Comment puis-je vous aider avec vos études ?`,
      timestamp: new Date().toISOString()
    });
  }),

  // Documents
  http.get('/api/documents', () => {
    return HttpResponse.json([
      {
        id: 1,
        title: 'Cours de Mathématiques',
        type: 'pdf',
        subject: 'Mathématiques',
        created_at: '2025-07-20'
      },
      {
        id: 2,
        title: 'Exercices NSI',
        type: 'docx',
        subject: 'NSI',
        created_at: '2025-07-21'
      }
    ]);
  }),

  http.post('/api/documents/generate', () => {
    return HttpResponse.json({
      document_id: 'doc_123',
      download_url: '/api/documents/download/doc_123',
      message: 'Document généré avec succès'
    });
  }),

  // Formules
  http.get('/api/formulas', () => {
    return HttpResponse.json([
      {
        id: 1,
        title: 'Théorème de Pythagore',
        formula: 'a² + b² = c²',
        subject: 'Mathématiques',
        level: 'Collège'
      },
      {
        id: 2,
        title: 'Dérivée d\'une fonction puissance',
        formula: '(x^n)\' = n × x^(n-1)',
        subject: 'Mathématiques',
        level: 'Lycée'
      }
    ]);
  })
];

// Configuration du serveur pour les tests
export const server = setupServer(...handlers);
