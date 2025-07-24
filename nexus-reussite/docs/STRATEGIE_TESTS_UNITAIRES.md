# 🧪 STRATÉGIE DE TESTS UNITAIRES - NEXUS RÉUSSITE

**Version :** 1.0  
**Date :** 23 juillet 2025  
**Architecture :** Basé sur la structure finale épurée et validée

---

## 📋 **VUE D'ENSEMBLE**

### **Philosophie de Test**
- **Pyramide des tests** : 70% unitaires, 20% intégration, 10% E2E
- **Tests rapides et fiables** pour garantir la confiance dans le code
- **Isolation des dépendances** pour des tests déterministes
- **Documentation vivante** du comportement attendu

### **Écosystème Technique**

#### **Backend (Flask/Python)**
- **Framework :** `pytest` + `pytest-flask`
- **Mocking :** `unittest.mock`
- **Base de données :** SQLite en mémoire + PostgreSQL test
- **Coverage :** `pytest-cov`

#### **Frontend (React/Vite)**
- **Framework :** `vitest`
- **Testing Library :** `@testing-library/react`
- **Mocking API :** `msw` (Mock Service Worker)
- **User Events :** `@testing-library/user-event`

---

## 🐍 **TESTS BACKEND - ARCHITECTURE ACTUELLE**

### **1. Services (`src/services/`)**

#### **Service OpenAI/ARIA**
```python
# tests/unit/services/test_openai_service.py
import pytest
from unittest.mock import patch, MagicMock
from src.services.openai_service import OpenAIService

class TestOpenAIService:
    
    @patch('openai.ChatCompletion.create')
    def test_generate_aria_response_success(self, mock_openai):
        """Test génération réponse ARIA avec succès"""
        # Arrange
        mock_openai.return_value = {
            "choices": [{
                "message": {
                    "content": "Bonjour ! Je suis ARIA, votre assistante IA."
                }
            }]
        }
        service = OpenAIService()
        
        # Act
        response = service.generate_aria_response(
            "Bonjour ARIA", 
            "student_123", 
            context="mathématiques"
        )
        
        # Assert
        assert response is not None
        assert "ARIA" in response
        mock_openai.assert_called_once()
        
    @patch('openai.ChatCompletion.create')
    def test_generate_aria_response_api_error(self, mock_openai):
        """Test gestion erreur API OpenAI"""
        # Arrange
        mock_openai.side_effect = Exception("API Error")
        service = OpenAIService()
        
        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            service.generate_aria_response("Test", "user_123")
            
    def test_format_message_for_context(self):
        """Test formatage message selon contexte éducatif"""
        # Arrange
        service = OpenAIService()
        message = "Explique-moi les fonctions"
        context = "NSI"
        
        # Act
        formatted = service.format_message_for_context(message, context)
        
        # Assert
        assert "NSI" in formatted
        assert "fonction" in formatted.lower()
        assert len(formatted) > len(message)
```

#### **Service de Gestion des Documents**
```python
# tests/unit/services/test_document_service.py
import pytest
from unittest.mock import patch, mock_open
from src.services.document_service import DocumentService
from src.models.document import Document

class TestDocumentService:
    
    def test_generate_exercise_pdf(self):
        """Test génération PDF d'exercices"""
        # Arrange
        service = DocumentService()
        exercise_data = {
            "title": "Exercices de Mathématiques",
            "level": "Terminale",
            "subject": "Mathématiques",
            "exercises": [
                {"question": "Calculer la dérivée de f(x) = x²", "points": 5}
            ]
        }
        
        # Act
        pdf_path = service.generate_exercise_pdf(exercise_data)
        
        # Assert
        assert pdf_path.endswith('.pdf')
        assert "exercises" in pdf_path
        
    @patch('builtins.open', new_callable=mock_open)
    def test_save_uploaded_document(self, mock_file):
        """Test sauvegarde document uploadé"""
        # Arrange
        service = DocumentService()
        file_data = b"PDF content"
        filename = "cours_maths.pdf"
        user_id = "user_123"
        
        # Act
        saved_path = service.save_uploaded_document(file_data, filename, user_id)
        
        # Assert
        assert saved_path is not None
        assert filename in saved_path
        mock_file.assert_called_once()
```

### **2. Modèles (`src/models/`)**

#### **Modèle Utilisateur**
```python
# tests/unit/models/test_user.py
import pytest
from src.models.user import User
from src.database import db

class TestUserModel:
    
    def test_user_creation(self):
        """Test création utilisateur avec données valides"""
        # Arrange & Act
        user = User(
            email="test@nexus-reussite.com",
            first_name="Jean",
            last_name="Dupont",
            role="student"
        )
        
        # Assert
        assert user.email == "test@nexus-reussite.com"
        assert user.full_name == "Jean Dupont"
        assert user.role == "student"
        assert user.is_active is True
        
    def test_password_hashing(self):
        """Test hachage et vérification mot de passe"""
        # Arrange
        user = User(email="test@example.com")
        password = "SecurePassword123!"
        
        # Act
        user.set_password(password)
        
        # Assert
        assert user.password_hash is not None
        assert user.password_hash != password
        assert user.check_password(password) is True
        assert user.check_password("WrongPassword") is False
        
    def test_user_json_serialization(self):
        """Test sérialisation JSON utilisateur"""
        # Arrange
        user = User(
            email="test@example.com",
            first_name="Marie",
            last_name="Martin",
            role="teacher"
        )
        
        # Act
        user_dict = user.to_dict()
        
        # Assert
        assert user_dict['email'] == "test@example.com"
        assert user_dict['full_name'] == "Marie Martin"
        assert user_dict['role'] == "teacher"
        assert 'password_hash' not in user_dict  # Sécurité
```

#### **Modèle Étudiant**
```python
# tests/unit/models/test_student.py
import pytest
from src.models.student import Student
from datetime import datetime

class TestStudentModel:
    
    def test_student_progress_calculation(self):
        """Test calcul progression étudiant"""
        # Arrange
        student = Student(
            user_id=1,
            level="Terminale",
            specialties=["Mathématiques", "NSI"]
        )
        student.completed_exercises = 15
        student.total_exercises = 20
        
        # Act
        progress = student.calculate_progress()
        
        # Assert
        assert progress == 75.0
        
    def test_add_learning_session(self):
        """Test ajout session d'apprentissage"""
        # Arrange
        student = Student(user_id=1)
        session_data = {
            "subject": "Mathématiques",
            "duration": 60,  # minutes
            "exercises_completed": 3,
            "score": 85.5
        }
        
        # Act
        student.add_learning_session(session_data)
        
        # Assert
        assert len(student.learning_sessions) == 1
        assert student.learning_sessions[0]['subject'] == "Mathématiques"
        assert student.total_study_time == 60
```

### **3. Routes API (`src/routes/`)**

#### **Routes Utilisateurs**
```python
# tests/integration/routes/test_user_routes.py
import pytest
import json
from src.main_production import create_app
from src.models.user import User

class TestUserRoutes:
    
    @pytest.fixture
    def client(self):
        app = create_app(testing=True)
        with app.test_client() as client:
            yield client
            
    @pytest.fixture
    def auth_headers(self, client):
        # Créer utilisateur test et récupérer token
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }
        client.post('/api/auth/register', json=user_data)
        
        login_response = client.post('/api/auth/login', json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token = login_response.get_json()['token']
        return {'Authorization': f'Bearer {token}'}
    
    def test_get_user_profile_authenticated(self, client, auth_headers):
        """Test récupération profil utilisateur authentifié"""
        # Act
        response = client.get('/api/user/profile', headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == 'test@example.com'
        assert 'password_hash' not in data
        
    def test_get_user_profile_unauthenticated(self, client):
        """Test accès profil sans authentification"""
        # Act
        response = client.get('/api/user/profile')
        
        # Assert
        assert response.status_code == 401
        
    def test_update_user_profile(self, client, auth_headers):
        """Test mise à jour profil utilisateur"""
        # Arrange
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        
        # Act
        response = client.put('/api/user/profile', 
                            json=update_data, 
                            headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['first_name'] == 'Updated'
```

#### **Routes Étudiants**
```python
# tests/integration/routes/test_student_routes.py
import pytest
from tests.integration.routes.test_user_routes import TestUserRoutes

class TestStudentRoutes(TestUserRoutes):
    
    def test_get_student_dashboard_data(self, client, auth_headers):
        """Test récupération données tableau de bord étudiant"""
        # Act
        response = client.get('/api/students/dashboard', headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data
        assert 'recent_exercises' in data
        assert 'upcoming_sessions' in data
        
    def test_submit_exercise_solution(self, client, auth_headers):
        """Test soumission solution exercice"""
        # Arrange
        solution_data = {
            "exercise_id": 1,
            "solution": "f'(x) = 2x",
            "reasoning": "Dérivée d'une fonction polynomiale"
        }
        
        # Act
        response = client.post('/api/students/exercises/submit',
                             json=solution_data,
                             headers=auth_headers)
        
        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert 'score' in data
        assert 'feedback' in data
```

---

## ⚛️ **TESTS FRONTEND - COMPOSANTS REACT**

### **1. Utilitaires (`src/utils/`)**

```javascript
// src/utils/__tests__/dateUtils.test.js
import { describe, it, expect } from 'vitest';
import { formatDate, calculateAge, isValidDate } from '../dateUtils';

describe('dateUtils', () => {
  describe('formatDate', () => {
    it('should format ISO date to French format', () => {
      expect(formatDate('2025-07-23T10:30:00Z')).toBe('23/07/2025');
    });
    
    it('should handle null input gracefully', () => {
      expect(formatDate(null)).toBe('Date invalide');
    });
  });
  
  describe('calculateAge', () => {
    it('should calculate correct age from birthdate', () => {
      const birthdate = '2008-07-23';
      expect(calculateAge(birthdate)).toBe(17);
    });
  });
});
```

### **2. Hooks Personnalisés (`src/hooks/`)**

```javascript
// src/hooks/__tests__/useAuth.test.js
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useAuth } from '../useAuth';

// Mock du service API
vi.mock('../../services/api', () => ({
  authService: {
    login: vi.fn(),
    logout: vi.fn(),
    getCurrentUser: vi.fn()
  }
}));

describe('useAuth', () => {
  it('should handle login flow correctly', async () => {
    // Arrange
    const { result } = renderHook(() => useAuth());
    
    // Act
    await act(async () => {
      await result.current.login('test@example.com', 'password');
    });
    
    // Assert
    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.user).toBeDefined();
  });
  
  it('should handle logout correctly', async () => {
    // Arrange
    const { result } = renderHook(() => useAuth());
    
    // Act
    await act(async () => {
      await result.current.logout();
    });
    
    // Assert
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
  });
});
```

### **3. Composants Principaux**

#### **StudentDashboard**
```javascript
// src/components/__tests__/StudentDashboard.test.jsx
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { StudentDashboard } from '../StudentDashboard';
import { server } from '../../mocks/server';
import { http, HttpResponse } from 'msw';

// Mock des données du dashboard
const mockDashboardData = {
  progress: 75,
  recent_exercises: [
    { id: 1, title: 'Dérivées', score: 85, date: '2025-07-23' }
  ],
  upcoming_sessions: [
    { id: 1, subject: 'Mathématiques', date: '2025-07-24T14:00:00Z' }
  ]
};

describe('StudentDashboard', () => {
  beforeEach(() => {
    server.use(
      http.get('/api/students/dashboard', () => {
        return HttpResponse.json(mockDashboardData);
      })
    );
  });
  
  it('should display student progress correctly', async () => {
    // Act
    render(<StudentDashboard />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText('75%')).toBeInTheDocument();
      expect(screen.getByText('Dérivées')).toBeInTheDocument();
      expect(screen.getByText('Score: 85')).toBeInTheDocument();
    });
  });
  
  it('should show loading state initially', () => {
    // Act
    render(<StudentDashboard />);
    
    // Assert
    expect(screen.getByText('Chargement...')).toBeInTheDocument();
  });
});
```

#### **ARIAAgent**
```javascript
// src/components/__tests__/ARIAAgent.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { ARIAAgent } from '../ARIAAgent';
import { server } from '../../mocks/server';
import { http, HttpResponse } from 'msw';

describe('ARIAAgent', () => {
  beforeEach(() => {
    server.use(
      http.post('/api/aria/chat', () => {
        return HttpResponse.json({
          response: 'Bonjour ! Comment puis-je vous aider avec vos études ?'
        });
      })
    );
  });
  
  it('should send message and display ARIA response', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    const input = screen.getByPlaceholderText('Posez votre question à ARIA...');
    const sendButton = screen.getByRole('button', { name: /envoyer/i });
    
    // Act
    await user.type(input, 'Bonjour ARIA');
    await user.click(sendButton);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText('Bonjour ARIA')).toBeInTheDocument();
      expect(screen.getByText(/Comment puis-je vous aider/)).toBeInTheDocument();
    });
  });
  
  it('should clear input after sending message', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    const input = screen.getByPlaceholderText('Posez votre question à ARIA...');
    const sendButton = screen.getByRole('button', { name: /envoyer/i });
    
    // Act
    await user.type(input, 'Test message');
    await user.click(sendButton);
    
    // Assert
    await waitFor(() => {
      expect(input.value).toBe('');
    });
  });
});
```

#### **DocumentGenerator**
```javascript
// src/components/__tests__/DocumentGenerator.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { DocumentGenerator } from '../DocumentGenerator';

describe('DocumentGenerator', () => {
  it('should generate PDF when form is submitted', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(
      screen.getByLabelText('Type de document'),
      'exercices'
    );
    await user.selectOptions(
      screen.getByLabelText('Niveau'),
      'Terminale'
    );
    await user.selectOptions(
      screen.getByLabelText('Matière'),
      'Mathématiques'
    );
    
    await user.click(screen.getByRole('button', { name: /générer/i }));
    
    // Assert
    expect(screen.getByText('Génération en cours...')).toBeInTheDocument();
  });
  
  it('should show validation errors for empty form', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.click(screen.getByRole('button', { name: /générer/i }));
    
    // Assert
    expect(screen.getByText('Veuillez sélectionner un type')).toBeInTheDocument();
  });
});
```

---

## 🚀 **CONFIGURATION ET SETUP**

### **Backend Setup**
```python
# conftest.py
import pytest
from src.main_production import create_app
from src.database import db

@pytest.fixture
def app():
    """Fixture application Flask pour tests"""
    app = create_app(testing=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Fixture client de test"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Fixture runner CLI"""
    return app.test_cli_runner()
```

### **Frontend Setup**
```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.js'],
    globals: true
  }
});

// src/setupTests.js
import '@testing-library/jest-dom';
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// src/mocks/server.js
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

export const server = setupServer(
  http.get('/api/auth/me', () => {
    return HttpResponse.json({ user: { id: 1, email: 'test@example.com' } });
  })
);
```

---

## 📊 **MÉTRIQUES ET OBJECTIFS**

### **Couverture de Code Cible**
- **Backend :** 90%+ pour services et modèles
- **Frontend :** 85%+ pour hooks et composants critiques

### **Performance des Tests**
- **Tests unitaires :** < 5ms par test
- **Tests d'intégration :** < 100ms par test
- **Suite complète :** < 30 secondes

### **Commandes de Test**
```bash
# Backend
cd nexus-reussite-backend
pytest --cov=src --cov-report=html tests/

# Frontend
cd nexus-reussite-frontend
npm run test
npm run test:coverage
npm run test:watch
```

---

## ✅ **CHECKLIST DE VALIDATION**

### **Avant chaque commit :**
- [ ] Tous les tests passent
- [ ] Couverture minimale respectée
- [ ] Aucun test flakey détecté
- [ ] Documentation des nouveaux tests

### **Avant chaque release :**
- [ ] Tests E2E passent
- [ ] Performance validée
- [ ] Tests de régression OK
- [ ] Métriques de qualité respectées

**Cette stratégie garantit un code robuste et maintenable pour Nexus Réussite !**
