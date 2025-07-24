import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Composant ExerciseList simulé
const ExerciseList = ({ filters = {}, onExerciseSelect }) => {
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    loadExercises();
  }, [filters, currentPage]);

  const loadExercises = async () => {
    try {
      setLoading(true);
      setError(null);

      const queryParams = new URLSearchParams({
        page: currentPage,
        ...filters
      });

      const response = await fetch(`/api/exercises?${queryParams}`);
      
      if (response.ok) {
        const data = await response.json();
        setExercises(data.exercises);
        setTotalPages(data.totalPages);
      } else {
        throw new Error('Erreur lors du chargement des exercices');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExerciseClick = (exercise) => {
    if (onExerciseSelect) {
      onExerciseSelect(exercise);
    }
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      1: 'green',
      2: 'yellow',
      3: 'orange',
      4: 'red',
      5: 'darkred'
    };
    return colors[difficulty] || 'gray';
  };

  if (loading) {
    return <div data-testid="exercises-loading">Chargement des exercices...</div>;
  }

  if (error) {
    return (
      <div data-testid="exercises-error">
        <div>Erreur: {error}</div>
        <button onClick={loadExercises} data-testid="retry-button">
          Réessayer
        </button>
      </div>
    );
  }

  return (
    <div data-testid="exercise-list">
      <div data-testid="exercises-header">
        <h2>Liste des Exercices</h2>
        <div data-testid="exercises-count">
          {exercises.length} exercice{exercises.length !== 1 ? 's' : ''} trouvé{exercises.length !== 1 ? 's' : ''}
        </div>
      </div>

      {exercises.length === 0 ? (
        <div data-testid="no-exercises">
          Aucun exercice trouvé pour ces critères.
        </div>
      ) : (
        <div data-testid="exercises-grid">
          {exercises.map(exercise => (
            <div 
              key={exercise.id} 
              data-testid={`exercise-card-${exercise.id}`}
              className="exercise-card"
              onClick={() => handleExerciseClick(exercise)}
              role="button"
              tabIndex={0}
            >
              <div data-testid={`exercise-title-${exercise.id}`} className="exercise-title">
                {exercise.title}
              </div>
              
              <div data-testid={`exercise-subject-${exercise.id}`} className="exercise-subject">
                {exercise.subject}
              </div>
              
              <div data-testid={`exercise-level-${exercise.id}`} className="exercise-level">
                {exercise.level}
              </div>
              
              <div 
                data-testid={`exercise-difficulty-${exercise.id}`} 
                className="exercise-difficulty"
                style={{ color: getDifficultyColor(exercise.difficulty) }}
              >
                Difficulté: {exercise.difficulty}/5
              </div>
              
              <div data-testid={`exercise-points-${exercise.id}`} className="exercise-points">
                {exercise.points} points
              </div>
              
              {exercise.completion_status && (
                <div 
                  data-testid={`exercise-status-${exercise.id}`}
                  className={`completion-status ${exercise.completion_status}`}
                >
                  {exercise.completion_status === 'completed' ? '✓ Terminé' : '○ En cours'}
                </div>
              )}
              
              {exercise.best_score !== undefined && (
                <div data-testid={`exercise-score-${exercise.id}`} className="best-score">
                  Meilleur score: {exercise.best_score}%
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div data-testid="pagination" className="pagination">
          <button 
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            data-testid="prev-page"
          >
            Précédent
          </button>
          
          <span data-testid="page-info">
            Page {currentPage} sur {totalPages}
          </span>
          
          <button 
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
            data-testid="next-page"
          >
            Suivant
          </button>
        </div>
      )}
    </div>
  );
};

// Import React
import { useState, useEffect } from 'react';

// Mock data
const mockExercises = [
  {
    id: 1,
    title: "Calcul de dérivées",
    subject: "Mathématiques",
    level: "Terminale",
    difficulty: 3,
    points: 10,
    completion_status: "completed",
    best_score: 85
  },
  {
    id: 2,
    title: "Algorithmes de tri",
    subject: "NSI",
    level: "Première",
    difficulty: 4,
    points: 15,
    completion_status: "in_progress",
    best_score: 72
  },
  {
    id: 3,
    title: "Équations différentielles",
    subject: "Mathématiques",
    level: "Terminale",
    difficulty: 5,
    points: 20
  }
];

describe('ExerciseList', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render loading state initially', () => {
    // Act
    render(<ExerciseList />);
    
    // Assert
    expect(screen.getByTestId('exercises-loading')).toBeInTheDocument();
    expect(screen.getByText('Chargement des exercices...')).toBeInTheDocument();
  });

  it('should render exercises list after loading', async () => {
    // Act
    render(<ExerciseList />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('exercise-list')).toBeInTheDocument();
      expect(screen.getByTestId('exercises-header')).toBeInTheDocument();
      expect(screen.getByText('Liste des Exercices')).toBeInTheDocument();
    });
  });

  it('should display correct exercise count', async () => {
    // Act
    render(<ExerciseList />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('exercises-count')).toBeInTheDocument();
      expect(screen.getByText('3 exercices trouvés')).toBeInTheDocument();
    });
  });

  it('should render individual exercise cards with correct data', async () => {
    // Act
    render(<ExerciseList />);
    
    // Assert
    await waitFor(() => {
      // Premier exercice
      expect(screen.getByTestId('exercise-card-1')).toBeInTheDocument();
      expect(screen.getByTestId('exercise-title-1')).toHaveTextContent('Calcul de dérivées');
      expect(screen.getByTestId('exercise-subject-1')).toHaveTextContent('Mathématiques');
      expect(screen.getByTestId('exercise-level-1')).toHaveTextContent('Terminale');
      expect(screen.getByTestId('exercise-difficulty-1')).toHaveTextContent('Difficulté: 3/5');
      expect(screen.getByTestId('exercise-points-1')).toHaveTextContent('10 points');
      expect(screen.getByTestId('exercise-status-1')).toHaveTextContent('✓ Terminé');
      expect(screen.getByTestId('exercise-score-1')).toHaveTextContent('Meilleur score: 85%');
    });
  });

  it('should handle exercise selection when clicked', async () => {
    // Arrange
    const mockOnExerciseSelect = vi.fn();
    const user = userEvent.setup();
    render(<ExerciseList onExerciseSelect={mockOnExerciseSelect} />);
    
    await waitFor(() => {
      expect(screen.getByTestId('exercise-card-1')).toBeInTheDocument();
    });
    
    // Act
    await user.click(screen.getByTestId('exercise-card-1'));
    
    // Assert
    expect(mockOnExerciseSelect).toHaveBeenCalledWith(mockExercises[0]);
  });

  it('should display difficulty with correct colors', async () => {
    // Act
    render(<ExerciseList />);
    
    // Assert
    await waitFor(() => {
      const difficulty1 = screen.getByTestId('exercise-difficulty-1');
      const difficulty2 = screen.getByTestId('exercise-difficulty-2');
      const difficulty3 = screen.getByTestId('exercise-difficulty-3');
      
      expect(difficulty1).toHaveStyle({ color: 'orange' }); // Difficulté 3
      expect(difficulty2).toHaveStyle({ color: 'red' }); // Difficulté 4
      expect(difficulty3).toHaveStyle({ color: 'darkred' }); // Difficulté 5
    });
  });

  it('should show no exercises message when list is empty', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.get('/api/exercises', () => {
        return HttpResponse.json({ exercises: [], totalPages: 0 });
      })
    );
    
    // Act
    render(<ExerciseList />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('no-exercises')).toBeInTheDocument();
      expect(screen.getByText('Aucun exercice trouvé pour ces critères.')).toBeInTheDocument();
    });
  });

  it('should handle API error gracefully', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.get('/api/exercises', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );
    
    // Act
    render(<ExerciseList />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('exercises-error')).toBeInTheDocument();
      expect(screen.getByText(/Erreur lors du chargement des exercices/)).toBeInTheDocument();
      expect(screen.getByTestId('retry-button')).toBeInTheDocument();
    });
  });

  it('should retry loading when retry button is clicked', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    let callCount = 0;
    server.use(
      http.get('/api/exercises', () => {
        callCount++;
        if (callCount === 1) {
          return new HttpResponse(null, { status: 500 });
        }
        return HttpResponse.json({ exercises: mockExercises, totalPages: 1 });
      })
    );
    
    const user = userEvent.setup();
    render(<ExerciseList />);
    
    await waitFor(() => {
      expect(screen.getByTestId('exercises-error')).toBeInTheDocument();
    });
    
    // Act
    await user.click(screen.getByTestId('retry-button'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('exercise-list')).toBeInTheDocument();
      expect(screen.queryByTestId('exercises-error')).not.toBeInTheDocument();
    });
  });

  it('should apply filters when provided', async () => {
    // Arrange
    const filters = {
      subject: 'Mathématiques',
      level: 'Terminale',
      difficulty: 3
    };
    
    // Act
    render(<ExerciseList filters={filters} />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('exercise-list')).toBeInTheDocument();
      // Vérifier que les exercices affichés correspondent aux filtres
      expect(screen.getByTestId('exercise-card-1')).toBeInTheDocument();
      expect(screen.queryByTestId('exercise-card-2')).not.toBeInTheDocument(); // NSI, pas Mathématiques
    });
  });

  it('should handle pagination correctly', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.get('/api/exercises', ({ request }) => {
        const url = new URL(request.url);
        const page = parseInt(url.searchParams.get('page') || '1');
        
        return HttpResponse.json({
          exercises: page === 1 ? [mockExercises[0]] : [mockExercises[1]],
          totalPages: 2
        });
      })
    );
    
    const user = userEvent.setup();
    render(<ExerciseList />);
    
    await waitFor(() => {
      expect(screen.getByTestId('pagination')).toBeInTheDocument();
      expect(screen.getByTestId('page-info')).toHaveTextContent('Page 1 sur 2');
    });
    
    // Act
    await user.click(screen.getByTestId('next-page'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('page-info')).toHaveTextContent('Page 2 sur 2');
    });
  });

  it('should disable pagination buttons appropriately', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.get('/api/exercises', () => {
        return HttpResponse.json({ exercises: [mockExercises[0]], totalPages: 2 });
      })
    );
    
    render(<ExerciseList />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('prev-page')).toBeDisabled(); // Première page
      expect(screen.getByTestId('next-page')).not.toBeDisabled();
    });
  });
});
