import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

// Composant StudentDashboard simulé (à adapter selon votre implémentation)
const StudentDashboard = ({ userId }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('/api/students/dashboard');
        if (response.ok) {
          const data = await response.json();
          setDashboardData(data);
        } else {
          throw new Error('Erreur lors du chargement');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [userId]);

  if (loading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error}</div>;
  if (!dashboardData) return <div>Aucune donnée</div>;

  return (
    <div data-testid="student-dashboard">
      <h1>Tableau de Bord Étudiant</h1>
      
      <div data-testid="progress-section">
        <h2>Progression</h2>
        <div data-testid="progress-value">{dashboardData.progress}%</div>
        <div>
          {dashboardData.stats.completed_exercises}/{dashboardData.stats.total_exercises} exercices
        </div>
        <div>Score moyen: {dashboardData.stats.average_score}</div>
      </div>
      
      <div data-testid="recent-exercises">
        <h2>Exercices Récents</h2>
        {dashboardData.recent_exercises.map(exercise => (
          <div key={exercise.id} data-testid={`exercise-${exercise.id}`}>
            <span>{exercise.title}</span>
            <span>Score: {exercise.score}</span>
            <span>Date: {exercise.date}</span>
          </div>
        ))}
      </div>
      
      <div data-testid="upcoming-sessions">
        <h2>Prochaines Sessions</h2>
        {dashboardData.upcoming_sessions.map(session => (
          <div key={session.id} data-testid={`session-${session.id}`}>
            <span>{session.subject}</span>
            <span>{new Date(session.date).toLocaleDateString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// Imports React nécessaires
import { useState, useEffect } from 'react';

describe('StudentDashboard', () => {
  it('should display loading state initially', () => {
    // Act
    render(<StudentDashboard userId="123" />);
    
    // Assert
    expect(screen.getByText('Chargement...')).toBeInTheDocument();
  });

  it('should display student progress correctly', async () => {
    // Act
    render(<StudentDashboard userId="123" />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText('Tableau de Bord Étudiant')).toBeInTheDocument();
      expect(screen.getByTestId('progress-value')).toHaveTextContent('75%');
      expect(screen.getByText('15/20 exercices')).toBeInTheDocument();
      expect(screen.getByText('Score moyen: 82')).toBeInTheDocument();
    });
  });

  it('should display recent exercises', async () => {
    // Act
    render(<StudentDashboard userId="123" />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText('Exercices Récents')).toBeInTheDocument();
      expect(screen.getByTestId('exercise-1')).toBeInTheDocument();
      expect(screen.getByText('Dérivées')).toBeInTheDocument();
      expect(screen.getByText('Score: 85')).toBeInTheDocument();
      
      expect(screen.getByTestId('exercise-2')).toBeInTheDocument();
      expect(screen.getByText('Intégrales')).toBeInTheDocument();
      expect(screen.getByText('Score: 78')).toBeInTheDocument();
    });
  });

  it('should display upcoming sessions', async () => {
    // Act
    render(<StudentDashboard userId="123" />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText('Prochaines Sessions')).toBeInTheDocument();
      expect(screen.getByTestId('session-1')).toBeInTheDocument();
      expect(screen.getByText('Mathématiques')).toBeInTheDocument();
    });
  });

  it('should handle empty data gracefully', async () => {
    // Arrange - Override MSW pour retourner des données vides
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.get('/api/students/dashboard', () => {
        return HttpResponse.json({
          progress: 0,
          recent_exercises: [],
          upcoming_sessions: [],
          stats: {
            total_exercises: 0,
            completed_exercises: 0,
            average_score: 0
          }
        });
      })
    );
    
    // Act
    render(<StudentDashboard userId="123" />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('progress-value')).toHaveTextContent('0%');
      expect(screen.getByText('0/0 exercices')).toBeInTheDocument();
    });
  });

  it('should handle API error gracefully', async () => {
    // Arrange - Override MSW pour retourner une erreur
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.get('/api/students/dashboard', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );
    
    // Act
    render(<StudentDashboard userId="123" />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText(/Erreur:/)).toBeInTheDocument();
    });
  });

  it('should refresh data when userId changes', async () => {
    // Arrange
    const { rerender } = render(<StudentDashboard userId="123" />);
    
    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByTestId('student-dashboard')).toBeInTheDocument();
    });
    
    // Act - Change userId
    rerender(<StudentDashboard userId="456" />);
    
    // Assert - Should show loading again
    expect(screen.getByText('Chargement...')).toBeInTheDocument();
    
    // Then load new data
    await waitFor(() => {
      expect(screen.getByTestId('student-dashboard')).toBeInTheDocument();
    });
  });
});
