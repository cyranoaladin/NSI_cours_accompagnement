import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Composant AdminDashboard simulé (version simplifiée avec les parties essentielles)
const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalStudents: 0,
    totalTeachers: 0,
    activeUsers: 0
  });
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddUser, setShowAddUser] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      const [statsResponse, usersResponse] = await Promise.all([
        fetch('/api/admin/stats'),
        fetch('/api/admin/users')
      ]);

      if (statsResponse.ok && usersResponse.ok) {
        const statsData = await statsResponse.json();
        const usersData = await usersResponse.json();
        
        setStats(statsData);
        setUsers(usersData);
      } else {
        throw new Error('Erreur lors du chargement des données');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const deleteUser = async (userId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
      return;
    }

    try {
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setUsers(prev => prev.filter(user => user.id !== userId));
        // Mettre à jour les stats
        loadDashboardData();
      } else {
        throw new Error('Erreur lors de la suppression');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return <div data-testid="loading">Chargement...</div>;
  }

  if (error) {
    return (
      <div data-testid="error-container">
        <div data-testid="error-message">Erreur: {error}</div>
        <button onClick={loadDashboardData} data-testid="retry-button">
          Réessayer
        </button>
      </div>
    );
  }

  return (
    <div data-testid="admin-dashboard">
      <header data-testid="dashboard-header">
        <h1>Tableau de Bord Administrateur</h1>
        <button 
          onClick={() => setShowAddUser(true)}
          data-testid="add-user-button"
        >
          Ajouter un utilisateur
        </button>
      </header>

      <section data-testid="stats-section">
        <h2>Statistiques</h2>
        <div data-testid="stats-grid">
          <div data-testid="stat-total-users">
            <h3>Total Utilisateurs</h3>
            <span>{stats.totalUsers}</span>
          </div>
          <div data-testid="stat-total-students">
            <h3>Étudiants</h3>
            <span>{stats.totalStudents}</span>
          </div>
          <div data-testid="stat-total-teachers">
            <h3>Professeurs</h3>
            <span>{stats.totalTeachers}</span>
          </div>
          <div data-testid="stat-active-users">
            <h3>Utilisateurs Actifs</h3>
            <span>{stats.activeUsers}</span>
          </div>
        </div>
      </section>

      <section data-testid="users-section">
        <h2>Gestion des Utilisateurs</h2>
        {users.length === 0 ? (
          <div data-testid="no-users">Aucun utilisateur trouvé</div>
        ) : (
          <div data-testid="users-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nom</th>
                  <th>Email</th>
                  <th>Rôle</th>
                  <th>Statut</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id} data-testid={`user-row-${user.id}`}>
                    <td data-testid={`user-id-${user.id}`}>{user.id}</td>
                    <td data-testid={`user-name-${user.id}`}>{user.name}</td>
                    <td data-testid={`user-email-${user.id}`}>{user.email}</td>
                    <td data-testid={`user-role-${user.id}`}>{user.role}</td>
                    <td data-testid={`user-status-${user.id}`}>
                      <span className={`status ${user.isActive ? 'active' : 'inactive'}`}>
                        {user.isActive ? 'Actif' : 'Inactif'}
                      </span>
                    </td>
                    <td data-testid={`user-actions-${user.id}`}>
                      <button 
                        onClick={() => deleteUser(user.id)}
                        data-testid={`delete-user-${user.id}`}
                        className="delete-button"
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {showAddUser && (
        <div data-testid="add-user-modal">
          <div data-testid="modal-overlay" onClick={() => setShowAddUser(false)}>
            <div data-testid="modal-content" onClick={e => e.stopPropagation()}>
              <h3>Ajouter un utilisateur</h3>
              <button 
                onClick={() => setShowAddUser(false)}
                data-testid="close-modal"
              >
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Import React
import { useState, useEffect } from 'react';

describe('AdminDashboard', () => {
  beforeEach(() => {
    // Reset any global state if needed
    vi.clearAllMocks();
  });

  it('should render loading state initially', () => {
    // Act
    render(<AdminDashboard />);
    
    // Assert
    expect(screen.getByTestId('loading')).toBeInTheDocument();
    expect(screen.getByText('Chargement...')).toBeInTheDocument();
  });

  it('should render dashboard with stats and users after loading', async () => {
    // Act
    render(<AdminDashboard />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('admin-dashboard')).toBeInTheDocument();
      expect(screen.getByText('Tableau de Bord Administrateur')).toBeInTheDocument();
      expect(screen.getByTestId('stats-section')).toBeInTheDocument();
      expect(screen.getByTestId('users-section')).toBeInTheDocument();
    });
  });

  it('should display correct statistics', async () => {
    // Act
    render(<AdminDashboard />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('stat-total-users')).toBeInTheDocument();
      expect(screen.getByTestId('stat-total-students')).toBeInTheDocument();
      expect(screen.getByTestId('stat-total-teachers')).toBeInTheDocument();
      expect(screen.getByTestId('stat-active-users')).toBeInTheDocument();
    });
  });

  it('should display users table when users exist', async () => {
    // Act
    render(<AdminDashboard />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('users-table')).toBeInTheDocument();
      expect(screen.getByTestId('user-row-1')).toBeInTheDocument();
      expect(screen.getByTestId('user-name-1')).toHaveTextContent('John Doe');
      expect(screen.getByTestId('user-email-1')).toHaveTextContent('john@example.com');
      expect(screen.getByTestId('user-role-1')).toHaveTextContent('student');
    });
  });

  it('should show no users message when users array is empty', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.get('/api/admin/users', () => {
        return HttpResponse.json([]);
      })
    );
    
    // Act
    render(<AdminDashboard />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('no-users')).toBeInTheDocument();
      expect(screen.getByText('Aucun utilisateur trouvé')).toBeInTheDocument();
    });
  });

  it('should open add user modal when add button is clicked', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<AdminDashboard />);
    
    await waitFor(() => {
      expect(screen.getByTestId('admin-dashboard')).toBeInTheDocument();
    });
    
    // Act
    await user.click(screen.getByTestId('add-user-button'));
    
    // Assert
    expect(screen.getByTestId('add-user-modal')).toBeInTheDocument();
    expect(screen.getByText('Ajouter un utilisateur')).toBeInTheDocument();
  });

  it('should close add user modal when close button is clicked', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<AdminDashboard />);
    
    await waitFor(() => {
      expect(screen.getByTestId('admin-dashboard')).toBeInTheDocument();
    });
    
    // Ouvrir le modal
    await user.click(screen.getByTestId('add-user-button'));
    expect(screen.getByTestId('add-user-modal')).toBeInTheDocument();
    
    // Act
    await user.click(screen.getByTestId('close-modal'));
    
    // Assert
    expect(screen.queryByTestId('add-user-modal')).not.toBeInTheDocument();
  });

  it('should close modal when clicking on overlay', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<AdminDashboard />);
    
    await waitFor(() => {
      expect(screen.getByTestId('admin-dashboard')).toBeInTheDocument();
    });
    
    // Ouvrir le modal
    await user.click(screen.getByTestId('add-user-button'));
    
    // Act
    await user.click(screen.getByTestId('modal-overlay'));
    
    // Assert
    expect(screen.queryByTestId('add-user-modal')).not.toBeInTheDocument();
  });

  it('should handle user deletion with confirmation', async () => {
    // Arrange
    const user = userEvent.setup();
    
    // Mock window.confirm
    vi.stubGlobal('confirm', vi.fn(() => true));
    
    render(<AdminDashboard />);
    
    await waitFor(() => {
      expect(screen.getByTestId('user-row-1')).toBeInTheDocument();
    });
    
    // Act
    await user.click(screen.getByTestId('delete-user-1'));
    
    // Assert
    expect(window.confirm).toHaveBeenCalledWith('Êtes-vous sûr de vouloir supprimer cet utilisateur ?');
    
    await waitFor(() => {
      expect(screen.queryByTestId('user-row-1')).not.toBeInTheDocument();
    });
  });

  it('should not delete user when confirmation is cancelled', async () => {
    // Arrange
    const user = userEvent.setup();
    
    // Mock window.confirm to return false
    vi.stubGlobal('confirm', vi.fn(() => false));
    
    render(<AdminDashboard />);
    
    await waitFor(() => {
      expect(screen.getByTestId('user-row-1')).toBeInTheDocument();
    });
    
    // Act
    await user.click(screen.getByTestId('delete-user-1'));
    
    // Assert
    expect(window.confirm).toHaveBeenCalled();
    expect(screen.getByTestId('user-row-1')).toBeInTheDocument();
  });

  it('should handle API error and show error message', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.get('/api/admin/stats', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );
    
    // Act
    render(<AdminDashboard />);
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('error-container')).toBeInTheDocument();
      expect(screen.getByTestId('error-message')).toBeInTheDocument();
      expect(screen.getByText(/Erreur lors du chargement des données/)).toBeInTheDocument();
    });
  });

  it('should retry loading data when retry button is clicked', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    // Premier appel en erreur
    let callCount = 0;
    server.use(
      http.get('/api/admin/stats', () => {
        callCount++;
        if (callCount === 1) {
          return new HttpResponse(null, { status: 500 });
        }
        return HttpResponse.json({ totalUsers: 10, totalStudents: 8, totalTeachers: 2, activeUsers: 9 });
      })
    );
    
    const user = userEvent.setup();
    render(<AdminDashboard />);
    
    await waitFor(() => {
      expect(screen.getByTestId('error-container')).toBeInTheDocument();
    });
    
    // Act
    await user.click(screen.getByTestId('retry-button'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('admin-dashboard')).toBeInTheDocument();
      expect(screen.queryByTestId('error-container')).not.toBeInTheDocument();
    });
  });

  it('should display user status correctly', async () => {
    // Act
    render(<AdminDashboard />);
    
    // Assert
    await waitFor(() => {
      const activeStatus = screen.getByTestId('user-status-1');
      expect(activeStatus).toHaveTextContent('Actif');
      expect(activeStatus.querySelector('.status')).toHaveClass('active');
    });
  });
});
