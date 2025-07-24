import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';

// Composant ARIAAgent simulé
const ARIAAgent = () => {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async () => {
    if (!currentMessage.trim()) return;

    const userMessage = { role: 'user', content: currentMessage, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/aria/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: currentMessage })
      });

      if (response.ok) {
        const data = await response.json();
        const ariaMessage = { 
          role: 'aria', 
          content: data.response, 
          timestamp: new Date(data.timestamp) 
        };
        setMessages(prev => [...prev, ariaMessage]);
      } else {
        throw new Error('Erreur de communication avec ARIA');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div data-testid="aria-agent">
      <div data-testid="aria-header">
        <h2>ARIA - Assistant IA</h2>
        <button onClick={clearChat} data-testid="clear-chat">
          Effacer
        </button>
      </div>

      <div data-testid="chat-messages" style={{ height: '400px', overflowY: 'auto' }}>
        {messages.length === 0 && (
          <div data-testid="welcome-message">
            Bonjour ! Je suis ARIA, votre assistant IA. Comment puis-je vous aider ?
          </div>
        )}
        
        {messages.map((message, index) => (
          <div 
            key={index} 
            data-testid={`message-${index}`}
            className={`message ${message.role}`}
          >
            <div data-testid={`message-role-${message.role}`}>
              {message.role === 'user' ? 'Vous' : 'ARIA'}
            </div>
            <div data-testid={`message-content-${index}`}>
              {message.content}
            </div>
            <div data-testid={`message-time-${index}`}>
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div data-testid="aria-typing">
            ARIA tape...
          </div>
        )}
      </div>

      {error && (
        <div data-testid="error-message" style={{ color: 'red' }}>
          Erreur: {error}
        </div>
      )}

      <div data-testid="input-section">
        <textarea
          data-testid="message-input"
          value={currentMessage}
          onChange={(e) => setCurrentMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Posez votre question à ARIA..."
          disabled={isLoading}
          rows={3}
        />
        <button 
          data-testid="send-button"
          onClick={sendMessage}
          disabled={isLoading || !currentMessage.trim()}
        >
          {isLoading ? 'Envoi...' : 'Envoyer'}
        </button>
      </div>
    </div>
  );
};

// Import React
import { useState } from 'react';

describe('ARIAAgent', () => {
  it('should render welcome message initially', () => {
    // Act
    render(<ARIAAgent />);
    
    // Assert
    expect(screen.getByTestId('aria-agent')).toBeInTheDocument();
    expect(screen.getByText('ARIA - Assistant IA')).toBeInTheDocument();
    expect(screen.getByTestId('welcome-message')).toBeInTheDocument();
    expect(screen.getByText(/Bonjour ! Je suis ARIA/)).toBeInTheDocument();
  });

  it('should send message and display ARIA response', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    const input = screen.getByTestId('message-input');
    const sendButton = screen.getByTestId('send-button');
    
    // Act
    await user.type(input, 'Bonjour ARIA, comment ça va ?');
    await user.click(sendButton);
    
    // Assert
    await waitFor(() => {
      // Message utilisateur affiché
      expect(screen.getByTestId('message-0')).toBeInTheDocument();
      expect(screen.getByTestId('message-role-user')).toHaveTextContent('Vous');
      expect(screen.getByTestId('message-content-0')).toHaveTextContent('Bonjour ARIA, comment ça va ?');
      
      // Réponse ARIA affichée
      expect(screen.getByTestId('message-1')).toBeInTheDocument();
      expect(screen.getByTestId('message-role-aria')).toHaveTextContent('ARIA');
    });
  });

  it('should clear input after sending message', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    const input = screen.getByTestId('message-input');
    const sendButton = screen.getByTestId('send-button');
    
    // Act
    await user.type(input, 'Test message');
    expect(input.value).toBe('Test message');
    
    await user.click(sendButton);
    
    // Assert
    await waitFor(() => {
      expect(input.value).toBe('');
    });
  });

  it('should handle Enter key to send message', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    const input = screen.getByTestId('message-input');
    
    // Act
    await user.type(input, 'Message avec Enter');
    await user.keyboard('{Enter}');
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('message-0')).toBeInTheDocument();
      expect(screen.getByTestId('message-content-0')).toHaveTextContent('Message avec Enter');
    });
  });

  it('should not send empty messages', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    const sendButton = screen.getByTestId('send-button');
    
    // Act
    await user.click(sendButton);
    
    // Assert
    expect(screen.queryByTestId('message-0')).not.toBeInTheDocument();
    expect(screen.getByTestId('welcome-message')).toBeInTheDocument();
  });

  it('should disable input and button while loading', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    const input = screen.getByTestId('message-input');
    const sendButton = screen.getByTestId('send-button');
    
    // Act
    await user.type(input, 'Test loading');
    await user.click(sendButton);
    
    // Assert - Pendant le chargement
    expect(screen.getByTestId('aria-typing')).toBeInTheDocument();
    expect(input).toBeDisabled();
    expect(sendButton).toBeDisabled();
    expect(sendButton).toHaveTextContent('Envoi...');
    
    // Après le chargement
    await waitFor(() => {
      expect(screen.queryByTestId('aria-typing')).not.toBeInTheDocument();
      expect(input).not.toBeDisabled();
      expect(sendButton).toHaveTextContent('Envoyer');
    });
  });

  it('should clear chat when clear button is clicked', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    // Envoyer un message d'abord
    const input = screen.getByTestId('message-input');
    await user.type(input, 'Message à effacer');
    await user.click(screen.getByTestId('send-button'));
    
    await waitFor(() => {
      expect(screen.getByTestId('message-0')).toBeInTheDocument();
    });
    
    // Act
    await user.click(screen.getByTestId('clear-chat'));
    
    // Assert
    expect(screen.queryByTestId('message-0')).not.toBeInTheDocument();
    expect(screen.getByTestId('welcome-message')).toBeInTheDocument();
  });

  it('should handle API error gracefully', async () => {
    // Arrange
    const { server } = await import('../../mocks/server');
    const { http, HttpResponse } = await import('msw');
    
    server.use(
      http.post('/api/aria/chat', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );
    
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    // Act
    await user.type(screen.getByTestId('message-input'), 'Message qui va échouer');
    await user.click(screen.getByTestId('send-button'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('error-message')).toBeInTheDocument();
      expect(screen.getByText(/Erreur de communication avec ARIA/)).toBeInTheDocument();
    });
  });

  it('should display timestamps for messages', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<ARIAAgent />);
    
    // Act
    await user.type(screen.getByTestId('message-input'), 'Test timestamp');
    await user.click(screen.getByTestId('send-button'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByTestId('message-time-0')).toBeInTheDocument();
      expect(screen.getByTestId('message-time-1')).toBeInTheDocument();
    });
  });
});
