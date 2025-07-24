import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Composant DocumentGenerator simulé
const DocumentGenerator = () => {
  const [formData, setFormData] = useState({
    type: '',
    level: '',
    subject: '',
    title: '',
    exerciseCount: 5
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedUrl, setGeneratedUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.type) {
      setError('Veuillez sélectionner un type');
      return;
    }
    if (!formData.level) {
      setError('Veuillez sélectionner un niveau');
      return;
    }
    if (!formData.subject) {
      setError('Veuillez sélectionner une matière');
      return;
    }

    try {
      setIsGenerating(true);
      setError(null);

      const response = await fetch('/api/documents/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedUrl(data.downloadUrl);
      } else {
        throw new Error('Erreur lors de la génération');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  const resetForm = () => {
    setFormData({
      type: '',
      level: '',
      subject: '',
      title: '',
      exerciseCount: 5
    });
    setGeneratedUrl(null);
    setError(null);
  };

  return (
    <div data-testid="document-generator">
      <h2>Générateur de Documents</h2>
      
      <form onSubmit={handleSubmit} data-testid="generator-form">
        <div>
          <label htmlFor="type">Type de document</label>
          <select
            id="type"
            value={formData.type}
            onChange={(e) => setFormData(prev => ({ ...prev, type: e.target.value }))}
            data-testid="type-select"
          >
            <option value="">Sélectionner...</option>
            <option value="exercices">Fiche d'exercices</option>
            <option value="cours">Cours</option>
            <option value="evaluation">Évaluation</option>
          </select>
        </div>

        <div>
          <label htmlFor="level">Niveau</label>
          <select
            id="level"
            value={formData.level}
            onChange={(e) => setFormData(prev => ({ ...prev, level: e.target.value }))}
            data-testid="level-select"
          >
            <option value="">Sélectionner...</option>
            <option value="Seconde">Seconde</option>
            <option value="Première">Première</option>
            <option value="Terminale">Terminale</option>
          </select>
        </div>

        <div>
          <label htmlFor="subject">Matière</label>
          <select
            id="subject"
            value={formData.subject}
            onChange={(e) => setFormData(prev => ({ ...prev, subject: e.target.value }))}
            data-testid="subject-select"
          >
            <option value="">Sélectionner...</option>
            <option value="Mathématiques">Mathématiques</option>
            <option value="NSI">NSI</option>
            <option value="Physique-Chimie">Physique-Chimie</option>
          </select>
        </div>

        <div>
          <label htmlFor="title">Titre (optionnel)</label>
          <input
            type="text"
            id="title"
            value={formData.title}
            onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
            data-testid="title-input"
            placeholder="Titre du document..."
          />
        </div>

        {formData.type === 'exercices' && (
          <div>
            <label htmlFor="exerciseCount">Nombre d'exercices</label>
            <input
              type="number"
              id="exerciseCount"
              min="1"
              max="20"
              value={formData.exerciseCount}
              onChange={(e) => setFormData(prev => ({ ...prev, exerciseCount: parseInt(e.target.value) }))}
              data-testid="exercise-count-input"
            />
          </div>
        )}

        {error && (
          <div data-testid="error-message" style={{ color: 'red' }}>
            {error}
          </div>
        )}

        <div>
          <button 
            type="submit" 
            disabled={isGenerating}
            data-testid="generate-button"
          >
            {isGenerating ? 'Génération en cours...' : 'Générer'}
          </button>
          
          <button 
            type="button" 
            onClick={resetForm}
            data-testid="reset-button"
          >
            Réinitialiser
          </button>
        </div>
      </form>

      {generatedUrl && (
        <div data-testid="success-section">
          <h3>Document généré avec succès !</h3>
          <a 
            href={generatedUrl} 
            download 
            data-testid="download-link"
          >
            Télécharger le document
          </a>
        </div>
      )}
    </div>
  );
};

// Import React
import { useState } from 'react';

describe('DocumentGenerator', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render form with all required fields', () => {
    // Act
    render(<DocumentGenerator />);
    
    // Assert
    expect(screen.getByTestId('document-generator')).toBeInTheDocument();
    expect(screen.getByLabelText('Type de document')).toBeInTheDocument();
    expect(screen.getByLabelText('Niveau')).toBeInTheDocument();
    expect(screen.getByLabelText('Matière')).toBeInTheDocument();
    expect(screen.getByLabelText('Titre (optionnel)')).toBeInTheDocument();
    expect(screen.getByTestId('generate-button')).toBeInTheDocument();
  });

  it('should show validation error for empty type', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.click(screen.getByTestId('generate-button'));
    
    // Assert
    expect(screen.getByTestId('error-message')).toBeInTheDocument();
    expect(screen.getByText('Veuillez sélectionner un type')).toBeInTheDocument();
  });

  it('should show validation error for empty level', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(screen.getByTestId('type-select'), 'exercices');
    await user.click(screen.getByTestId('generate-button'));
    
    // Assert
    expect(screen.getByText('Veuillez sélectionner un niveau')).toBeInTheDocument();
  });

  it('should show validation error for empty subject', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(screen.getByTestId('type-select'), 'exercices');
    await user.selectOptions(screen.getByTestId('level-select'), 'Terminale');
    await user.click(screen.getByTestId('generate-button'));
    
    // Assert
    expect(screen.getByText('Veuillez sélectionner une matière')).toBeInTheDocument();
  });

  it('should show exercise count field when type is exercices', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(screen.getByTestId('type-select'), 'exercices');
    
    // Assert
    expect(screen.getByTestId('exercise-count-input')).toBeInTheDocument();
    expect(screen.getByLabelText('Nombre d\'exercices')).toBeInTheDocument();
  });

  it('should not show exercise count field for other types', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(screen.getByTestId('type-select'), 'cours');
    
    // Assert
    expect(screen.queryByTestId('exercise-count-input')).not.toBeInTheDocument();
  });

  it('should generate document successfully', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(screen.getByTestId('type-select'), 'exercices');
    await user.selectOptions(screen.getByTestId('level-select'), 'Terminale');
    await user.selectOptions(screen.getByTestId('subject-select'), 'Mathématiques');
    await user.type(screen.getByTestId('title-input'), 'Test Document');
    await user.click(screen.getByTestId('generate-button'));
    
    // Assert
    expect(screen.getByText('Génération en cours...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByTestId('success-section')).toBeInTheDocument();
      expect(screen.getByText('Document généré avec succès !')).toBeInTheDocument();
      expect(screen.getByTestId('download-link')).toBeInTheDocument();
    });
  });

  it('should disable generate button while generating', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(screen.getByTestId('type-select'), 'exercices');
    await user.selectOptions(screen.getByTestId('level-select'), 'Terminale');
    await user.selectOptions(screen.getByTestId('subject-select'), 'Mathématiques');
    await user.click(screen.getByTestId('generate-button'));
    
    // Assert
    expect(screen.getByTestId('generate-button')).toBeDisabled();
    expect(screen.getByText('Génération en cours...')).toBeInTheDocument();
  });

  it('should handle API error gracefully', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.post('/api/documents/generate', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );
    
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(screen.getByTestId('type-select'), 'exercices');
    await user.selectOptions(screen.getByTestId('level-select'), 'Terminale');
    await user.selectOptions(screen.getByTestId('subject-select'), 'Mathématiques');
    await user.click(screen.getByTestId('generate-button'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('error-message')).toBeInTheDocument();
      expect(screen.getByText('Erreur lors de la génération')).toBeInTheDocument();
    });
  });

  it('should reset form when reset button is clicked', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Remplir le formulaire
    await user.selectOptions(screen.getByTestId('type-select'), 'exercices');
    await user.selectOptions(screen.getByTestId('level-select'), 'Terminale');
    await user.selectOptions(screen.getByTestId('subject-select'), 'Mathématiques');
    await user.type(screen.getByTestId('title-input'), 'Test Title');
    
    // Act
    await user.click(screen.getByTestId('reset-button'));
    
    // Assert
    expect(screen.getByTestId('type-select')).toHaveValue('');
    expect(screen.getByTestId('level-select')).toHaveValue('');
    expect(screen.getByTestId('subject-select')).toHaveValue('');
    expect(screen.getByTestId('title-input')).toHaveValue('');
  });

  it('should update exercise count correctly', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<DocumentGenerator />);
    
    // Act
    await user.selectOptions(screen.getByTestId('type-select'), 'exercices');
    const exerciseCountInput = screen.getByTestId('exercise-count-input');
    await user.clear(exerciseCountInput);
    await user.type(exerciseCountInput, '10');
    
    // Assert
    expect(exerciseCountInput).toHaveValue(10);
  });
});
