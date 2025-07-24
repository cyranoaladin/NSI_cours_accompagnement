Voici une stratégie de test complète, full-stack et prête pour une équipe de développement.

---

# 🧪 Stratégie de Test Complète et Professionnelle - Nexus Réussite

**Version : 2.0 (Post-Audit)**  
**Date : 22/07/2025**  
**Contexte :** Ce guide est basé sur l'architecture de production validée dans `AUDIT_FINAL_SYNTHESE.md` et les spécifications techniques de l'ensemble de la documentation fournie.

## 1. Philosophie et Objectifs de Test

Notre stratégie de test vise à garantir la **confiance** et la **fiabilité** de la plateforme Nexus Réussite, désormais 100% opérationnelle. Chaque test est une assurance que les fonctionnalités critiques fonctionnent comme prévu et que la maintenance future sera sécurisée.

Nous appliquons rigoureusement la pyramide des tests et les principes **F.I.R.S.T.** (Fast, Independent, Repeatable, Self-Validating, Timely).

## 2. Écosystème de Test Full-Stack

### 2.1. Stack Frontend (React + Vite)

Comme défini précédemment, nous utilisons un écosystème moderne et performant :
- **Framework de Test :** **Vitest** (pour sa rapidité et son intégration native à Vite).
- **Bibliothèque de Test :** **React Testing Library (RTL)** (pour tester le comportement du point de vue de l'utilisateur).
- **Interactions Utilisateur :** **`@testing-library/user-event`** (pour des simulations réalistes).
- **Mocking d'API :** **Mock Service Worker (MSW)** (pour intercepter et simuler les réponses des API de manière transparente).
- **Assertions DOM :** **`@testing-library/jest-dom`** (pour des assertions plus lisibles).

### 2.2. Stack Backend (Flask + Python)

Comme spécifié dans la documentation, le backend nécessite sa propre suite de tests robuste :
- **Framework de Test :** **Pytest** (standard de l'industrie pour Python, puissant et extensible).
- **Aide pour Flask :** **`pytest-flask`** (pour fournir des fixtures utiles comme le client de test `client`).
- **Mocking :** La bibliothèque standard `unittest.mock` de Python (pour isoler les services et les dépendances externes comme l'API OpenAI).
- **Base de Données :** Utilisation d'une base de données de test en mémoire (SQLite) ou d'une base de données de test PostgreSQL distincte, gérée par les fixtures de `pytest`.

## 3. Stratégie de Test Détaillée par Couche

### Partie I : Tests Frontend (React)

#### 3.1. Composants UI (Dumb Components)
_(Exemple : `Badge`, `Button`, `Card`)_

L'approche reste la même : tester le rendu conditionnel en fonction des props.
**À Tester :**
- Le rendu initial sans erreur.
- L'affichage correct des `children`.
- L'application des classes CSS ou styles en fonction des `props` (`variant`, `size`, `disabled`).

---

#### 3.2. Custom Hooks
Les hooks sont le cœur de la logique réutilisable du frontend.

**Exemple Mis à Jour : `useAvailableSlots.js`** (pour le module de réservation hybride)
Ce hook doit fetcher les créneaux disponibles pour un coach donné.

**À Tester :**
- [ ] Retourne un état initial correct (`isLoading: true`, `slots: []`).
- [ ] Appelle l'API `/api/availability` avec les bons paramètres (ID du coach, date).
- [ ] Met à jour l'état avec les créneaux reçus en cas de succès.
- [ ] Gère correctement les états d'erreur de l'API.

**`useAvailableSlots.test.js`**
```javascript
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { server } from '../mocks/server'; // Serveur MSW
import { http, HttpResponse } from 'msw';
import { useAvailableSlots } from './useAvailableSlots';

// Mock de l'endpoint défini dans le cahier des charges
server.use(
  http.get('/api/availability', ({ request }) => {
    const url = new URL(request.url);
    const coachId = url.searchParams.get('coachId');
    if (coachId === '1') {
      return HttpResponse.json([
        { startTime: '2025-08-01T10:00:00Z', endTime: '2025-08-01T11:00:00Z' },
        { startTime: '2025-08-01T14:00:00Z', endTime: '2025-08-01T15:00:00Z' },
      ]);
    }
    return HttpResponse.json({ error: 'Coach not found' }, { status: 404 });
  })
);

describe('useAvailableSlots Hook', () => {
  it('should fetch and return available slots for a given coach', async () => {
    const { result } = renderHook(() => useAvailableSlots('1', new Date('2025-08-01')));

    // Attendre que le chargement soit terminé
    await waitFor(() => expect(result.current.isLoading).toBe(false));

    expect(result.current.slots.length).toBe(2);
    expect(result.current.slots[0].startTime).toBe('2025-08-01T10:00:00Z');
  });
});
```---

#### 3.3. State Management (Zustand)
_(Exemple : `authStore.js`)_

**Nouveaux Tests basés sur l'audit :**
- [ ] Vérifier que le rôle de l'utilisateur est correctement stocké (`ELEVE`, `PARENT`, `COACH`, `ADMIN`).
- [ ] Tester les getters dérivés, par exemple `isAdmin`, `isCoach`.

**`authStore.test.js`**
```javascript
import { describe, it, expect } from 'vitest';
import { useAuthStore } from './authStore';

describe('useAuthStore - Role Management', () => {
  it('should correctly identify an admin user', () => {
    const mockAdmin = { id: 1, name: 'Admin', role: 'ADMIN' };
    useAuthStore.getState().login(mockAdmin, 'admin-token');
    
    // On suppose que des getters ont été ajoutés au store
    expect(useAuthStore.getState().isAdmin).toBe(true);
    expect(useAuthStore.getState().isCoach).toBe(false);
  });
});
```
---

#### 3.4. Test d'Intégration Clé : Chat avec ARIA

Ce test valide l'une des fonctionnalités les plus critiques et innovantes.

**Nouveaux Tests basés sur la documentation de l'IA :**
- [ ] La requête vers OpenAI contient le bon `ARIA_SYSTEM_PROMPT` et le profil de l'élève.
- [ ] Le bon modèle OpenAI est appelé (`gpt-4o-mini` comme spécifié).
- [ ] Le système de fallback est déclenché si l'API principale échoue.

**`AriaChat.integration.test.jsx`**
```jsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';
import AriaChat from './AriaChat';

// Mock pour intercepter la requête et vérifier son contenu
const openAIRequestHandler = vi.fn();

server.use(
  http.post('https://api.openai.com/v1/chat/completions', async ({ request }) => {
    const body = await request.json();
    openAIRequestHandler(body); // On stocke le corps de la requête pour l'inspecter
    return HttpResponse.json({
      choices: [{ message: { role: 'assistant', content: 'Réponse mockée.' } }],
    });
  })
);

describe('AriaChat Integration', () => {
  it('should send user profile and context in the prompt to OpenAI', async () => {
    const user = userEvent.setup();
    // Le composant doit être wrappé dans un provider qui fournit le contexte de l'utilisateur
    render(<AriaChat />); 
    
    const input = screen.getByPlaceholderText(/envoyer un message/i);
    await user.type(input, 'Bonjour ARIA');
    await user.click(screen.getByRole('button', { name: /envoyer/i }));
    
    await screen.findByText('Réponse mockée.');
    
    // Vérification du contenu de la requête envoyée à OpenAI
    expect(openAIRequestHandler).toHaveBeenCalled();
    const requestBody = openAIRequestHandler.mock.calls[0][0];
    
    // Vérifier que le bon modèle est utilisé
    expect(requestBody.model).toBe('gpt-4o-mini');
    
    // Vérifier que le prompt système contient des éléments du contexte
    const systemPrompt = requestBody.messages.find(m => m.role === 'system').content;
    expect(systemPrompt).toContain("Tu es ARIA, l'assistante pédagogique intelligente");
    expect(systemPrompt).toContain("PROFIL ÉLÈVE"); // Vérifie que le template est bien utilisé
  });
});
```

### Partie II : Tests Backend (Flask)

C'est ici que l'audit apporte le plus de valeur, en structurant les tests pour l'API.

#### 3.5. Tests Unitaires (Services)

On teste la logique métier pure, en isolant la base de données et les appels externes.

**Exemple : `services/booking_service.py`**

**À Tester :**
- La logique de validation : un élève peut-il réserver ce créneau ?
- La gestion des conflits d'horaires.
- Le calcul du coût d'une réservation.

**`tests/unit/test_booking_service.py`**
```python
import pytest
from unittest.mock import MagicMock
from src.services.booking_service import can_student_book, BookingError

def test_can_student_book_with_available_slot():
    # Arrange: Mock des dépendances (ex: fonctions qui interrogent la DB)
    mock_db_session = MagicMock()
    # Simule qu'il n'y a pas de réservation existante pour cet élève à ce moment-là
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    student_id = 1
    start_time = "2025-09-01T10:00:00Z"
    
    # Act & Assert
    assert can_student_book(mock_db_session, student_id, start_time) is True

def test_can_student_book_with_conflict_raises_error():
    # Arrange
    mock_db_session = MagicMock()
    # Simule qu'une réservation existe déjà
    mock_db_session.query.return_value.filter.return_value.first.return_value = "Existing Booking"
    
    student_id = 1
    start_time = "2025-09-01T10:00:00Z"

    # Act & Assert
    with pytest.raises(BookingError, match="L'élève a déjà un cours sur ce créneau"):
        can_student_book(mock_db_session, student_id, start_time)
```

#### 3.6. Tests d'Intégration (Endpoints API)

On teste les routes de l'API avec un client de test, en interagissant avec une base de données de test.

**Exemple : Endpoint `POST /api/bookings`**

**À Tester :**
- [ ] Un utilisateur authentifié (avec un JWT valide) peut-il créer une réservation ?
- [ ] La route renvoie-t-elle une erreur 401 si le JWT est manquant ou invalide ?
- [ ] La route renvoie-t-elle une erreur 403 si un `PARENT` essaie de réserver pour un autre enfant ? (Test de droits)
- [ ] La route renvoie-t-elle une erreur 400 si les données envoyées sont invalides ?
- [ ] La réservation est-elle bien créée en base de données ?

**`tests/integration/test_bookings_api.py`**
```python
import json

def test_create_booking_as_authenticated_student(client, student_auth_headers):
    """
    GIVEN un client Flask et un header d'authentification valide pour un élève
    WHEN la route POST /api/bookings est appelée avec des données valides
    THEN vérifier que la réponse est 201 et que la réservation est créée
    """
    # Arrange
    booking_data = {
        "coachId": 2,
        "startTime": "2025-09-02T11:00:00Z",
        "endTime": "2025-09-02T12:00:00Z",
        "format": "ONLINE"
    }
    
    # Act
    response = client.post(
        '/api/bookings',
        data=json.dumps(booking_data),
        headers=student_auth_headers, # Fixture qui génère un token JWT pour un élève
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data['data']['status'] == 'CONFIRMED'
    assert response_data['data']['studentId'] == 1 # Supposons que le token est pour l'élève ID 1

def test_create_booking_unauthenticated(client):
    """
    GIVEN un client Flask
    WHEN la route POST /api/bookings est appelée sans authentification
    THEN vérifier que la réponse est 401
    """
    response = client.post('/api/bookings', data=json.dumps({}))
    assert response.status_code == 401
```

### Partie III : Validation des Flux Critiques

#### 3.7. Health Checks

L'audit mentionne des endpoints de monitoring. Ils doivent être testés.

**`tests/integration/test_health_checks.py`**
```python
def test_main_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

def test_database_health_check(client):
    response = client.get('/health/database')
    assert response.status_code == 200
    assert response.get_json()['database'] == 'healthy'
```

## 4. Conclusion et Intégration Continue (CI)

Cette stratégie de test mise à jour couvre l'intégralité de la stack de Nexus Réussite, du frontend au backend, en se basant sur la documentation finale.

**Prochaines Étapes :**
1.  **Exécution Automatisée :** Configurer un workflow GitHub Actions qui exécute `pytest` pour le backend et `npm test` pour le frontend sur chaque Pull Request.
2.  **Couverture de Code :** Générer des rapports de couverture (avec `pytest-cov` et `vitest --coverage`) pour s'assurer qu'au moins 85% du code critique est testé, comme mentionné dans l'audit.
3.  **Tests End-to-End (E2E) :** Pour les parcours les plus critiques (inscription, premier paiement, réservation complète), mettre en place une suite de tests E2E avec **Cypress** ou **Playwright**. Ces tests simuleront un utilisateur réel dans un vrai navigateur, interagissant avec la plateforme entièrement déployée.
