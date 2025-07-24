import React, { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Brain, 
  Send, 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX, 
  Minimize2, 
  Maximize2, 
  X, 
  Bot,
  User,
  Sparkles,
  FileText,
  Image,
  Video,
  Download,
  Share2,
  ThumbsUp,
  ThumbsDown,
  Copy,
  RefreshCw,
  Settings,
  HelpCircle,
  Lightbulb,
  Target,
  BookOpen,
  Calculator,
  Code,
  Atom,
  PenTool,
  Clock,
  TrendingUp,
  Award,
  Zap,
  Eye,
  EyeOff,
  ChevronDown,
  ChevronUp,
  Play,
  Pause,
  RotateCcw,
  MessageSquare,
  Search,
  Filter,
  Star,
  Heart,
  Bookmark,
  ExternalLink,
  Upload,
  Paperclip,
  Smile,
  MoreHorizontal
} from 'lucide-react'

const ARIAAgent = ({ 
  student, 
  isVisible, 
  onClose, 
  onMinimize, 
  isMinimized, 
  documents, 
  addNotification,
  onGenerateDocument,
  onRequestExercise 
}) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [currentMode, setCurrentMode] = useState('chat'); // chat, tutor, generator, analyzer
  const [selectedSubject, setSelectedSubject] = useState('all');
  const [ariaPersonality, setAriaPersonality] = useState('encouraging'); // encouraging, professional, friendly
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [ariaThinking, setAriaThinking] = useState(false);
  const [attachedFiles, setAttachedFiles] = useState([]);
  const [quickActions, setQuickActions] = useState([]);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);

  // Messages d'accueil personnalisés selon le profil
  const welcomeMessages = {
    first_time: [
      {
        id: 'welcome-1',
        type: 'aria',
        content: `Salut ${student?.name} ! 👋 Je suis ARIA, ton assistant pédagogique intelligent. Je suis là pour t'accompagner dans tes études et t'aider à réussir !`,
        timestamp: new Date(),
        mood: 'excited'
      },
      {
        id: 'welcome-2',
        type: 'aria',
        content: `J'ai analysé ton profil d'apprentissage et je vois que tu es plutôt ${student?.learningStyle?.visual > 70 ? 'visuel' : 'auditif'}. Je vais adapter mes explications en conséquence ! 🎯`,
        timestamp: new Date(),
        mood: 'analytical'
      }
    ],
    returning: [
      {
        id: 'return-1',
        type: 'aria',
        content: `Content de te revoir ${student?.name} ! 😊 Tu as progressé de ${student?.progress?.overall || 0}% depuis notre dernière conversation. Bravo !`,
        timestamp: new Date(),
        mood: 'proud'
      }
    ]
  };

  // Suggestions contextuelles
  const contextualSuggestions = [
    {
      text: "Explique-moi les fonctions exponentielles",
      icon: Calculator,
      subject: 'maths',
      action: () => handleSuggestionClick("Peux-tu m'expliquer les fonctions exponentielles avec des exemples visuels ?")
    },
    {
      text: "Aide-moi avec mon code Python",
      icon: Code,
      subject: 'nsi',
      action: () => handleSuggestionClick("J'ai un problème avec mon code Python, peux-tu m'aider ?")
    },
    {
      text: "Génère un exercice personnalisé",
      icon: Target,
      subject: 'all',
      action: () => setCurrentMode('generator')
    },
    {
      text: "Analyse mon style d'apprentissage",
      icon: Brain,
      subject: 'all',
      action: () => setCurrentMode('analyzer')
    },
    {
      text: "Prépare-moi pour le Grand Oral",
      icon: Mic,
      subject: 'français',
      action: () => handleSuggestionClick("Comment puis-je me préparer efficacement pour le Grand Oral ?")
    },
    {
      text: "Révision rapide avant contrôle",
      icon: Clock,
      subject: 'all',
      action: () => handleSuggestionClick("J'ai un contrôle demain, peux-tu m'aider à réviser rapidement ?")
    }
  ];

  // Actions rapides selon le mode
  const getModeActions = () => {
    switch (currentMode) {
      case 'tutor':
        return [
          { icon: Calculator, text: "Maths", action: () => setSelectedSubject('maths') },
          { icon: Code, text: "NSI", action: () => setSelectedSubject('nsi') },
          { icon: Atom, text: "Physique", action: () => setSelectedSubject('physique') },
          { icon: PenTool, text: "Français", action: () => setSelectedSubject('français') }
        ];
      case 'generator':
        return [
          { icon: FileText, text: "Fiche de cours", action: () => generateContent('course') },
          { icon: Target, text: "Exercices", action: () => generateContent('exercises') },
          { icon: Award, text: "Quiz", action: () => generateContent('quiz') },
          { icon: BookOpen, text: "Résumé", action: () => generateContent('summary') }
        ];
      case 'analyzer':
        return [
          { icon: TrendingUp, text: "Progression", action: () => analyzeProgress() },
          { icon: Brain, text: "Style d'apprentissage", action: () => analyzeLearningStyle() },
          { icon: Target, text: "Points faibles", action: () => analyzeWeaknesses() },
          { icon: Lightbulb, text: "Recommandations", action: () => getRecommendations() }
        ];
      default:
        return [];
    }
  };

  useEffect(() => {
    if (isVisible && messages.length === 0) {
      // Initialiser la conversation selon le contexte
      const isFirstTime = !student?.lastARIAInteraction;
      const welcomeSet = isFirstTime ? welcomeMessages.first_time : welcomeMessages.returning;
      
      setTimeout(() => {
        setMessages(welcomeSet);
        generateQuickActions();
      }, 500);
    }
  }, [isVisible, student]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const generateQuickActions = () => {
    const actions = [];
    
    // Actions basées sur le profil de l'élève
    if (student?.subjects?.includes('Mathématiques')) {
      actions.push({
        text: "Exercice de maths personnalisé",
        action: () => generatePersonalizedExercise('maths')
      });
    }
    
    if (student?.progress?.overall < 70) {
      actions.push({
        text: "Plan de rattrapage",
        action: () => generateCatchupPlan()
      });
    }
    
    if (student?.nextSession) {
      actions.push({
        text: "Préparer ma prochaine session",
        action: () => prepareNextSession()
      });
    }
    
    setQuickActions(actions);
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
    setShowSuggestions(false);
    setTimeout(() => {
      sendMessage(suggestion);
    }, 100);
  };

  const sendMessage = async (messageText = inputMessage) => {
    if (!messageText.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: messageText,
      timestamp: new Date(),
      attachments: attachedFiles
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setAttachedFiles([]);
    setIsTyping(true);
    setAriaThinking(true);

    // Simuler la réflexion d'ARIA
    setTimeout(async () => {
      setAriaThinking(false);
      const ariaResponse = await generateARIAResponse(messageText, userMessage);
      
      setMessages(prev => [...prev, ariaResponse]);
      setIsTyping(false);
      
      // Ajouter à l'historique de conversation
      setConversationHistory(prev => [...prev, userMessage, ariaResponse]);
      
      // Notification si réponse importante
      if (ariaResponse.importance === 'high') {
        addNotification({
          type: 'info',
          title: 'ARIA a une recommandation importante',
          message: ariaResponse.content.substring(0, 100) + '...'
        });
      }
    }, 1500 + Math.random() * 1000);
  };

  const generateARIAResponse = async (userMessage, context) => {
    // Simulation d'une réponse intelligente d'ARIA
    const responses = {
      math: [
        "Excellente question sur les mathématiques ! Laisse-moi t'expliquer avec des exemples concrets...",
        "Je vois que tu travailles sur ce concept. Voici une approche adaptée à ton style d'apprentissage visuel...",
        "C'est un point important ! Je vais te créer un schéma pour mieux comprendre..."
      ],
      nsi: [
        "Parfait ! La programmation, c'est ma spécialité. Regardons ton code ensemble...",
        "Je vais t'aider à déboguer ça. D'abord, analysons la logique de ton algorithme...",
        "Excellente question sur Python ! Voici une solution élégante..."
      ],
      physics: [
        "La physique devient plus claire avec de bons exemples ! Voici ce que je propose...",
        "Je vais t'expliquer ce phénomène avec des analogies du quotidien...",
        "C'est un concept fondamental ! Créons ensemble un schéma explicatif..."
      ],
      french: [
        "Excellente réflexion littéraire ! Développons cette analyse ensemble...",
        "Pour le Grand Oral, je vais t'aider à structurer ton argumentation...",
        "Très bonne question sur la méthodologie ! Voici ma recommandation..."
      ],
      general: [
        "Je comprends ta préoccupation. Analysons cela ensemble...",
        "Excellente question ! Voici ce que je peux t'apporter comme éclairage...",
        "C'est exactement le type de réflexion qui montre ta progression !"
      ]
    };

    // Déterminer le contexte de la question
    let responseCategory = 'general';
    if (userMessage.toLowerCase().includes('math') || userMessage.toLowerCase().includes('fonction') || userMessage.toLowerCase().includes('équation')) {
      responseCategory = 'math';
    } else if (userMessage.toLowerCase().includes('python') || userMessage.toLowerCase().includes('code') || userMessage.toLowerCase().includes('algorithme')) {
      responseCategory = 'nsi';
    } else if (userMessage.toLowerCase().includes('physique') || userMessage.toLowerCase().includes('optique') || userMessage.toLowerCase().includes('mécanique')) {
      responseCategory = 'physics';
    } else if (userMessage.toLowerCase().includes('français') || userMessage.toLowerCase().includes('oral') || userMessage.toLowerCase().includes('dissertation')) {
      responseCategory = 'french';
    }

    const baseResponse = responses[responseCategory][Math.floor(Math.random() * responses[responseCategory].length)];
    
    // Personnaliser selon le profil de l'élève
    let personalizedResponse = baseResponse;
    if (student?.learningStyle?.visual > 70) {
      personalizedResponse += "\n\n📊 Je vais créer un schéma visuel pour t'aider à mieux comprendre.";
    }
    if (student?.learningStyle?.auditory > 70) {
      personalizedResponse += "\n\n🎧 Veux-tu que je t'explique cela à l'oral ?";
    }

    return {
      id: Date.now() + 1,
      type: 'aria',
      content: personalizedResponse,
      timestamp: new Date(),
      mood: 'helpful',
      suggestions: generateFollowUpSuggestions(responseCategory),
      actions: generateResponseActions(responseCategory),
      importance: Math.random() > 0.7 ? 'high' : 'normal'
    };
  };

  const generateFollowUpSuggestions = (category) => {
    const suggestions = {
      math: [
        "Peux-tu me donner un exercice similaire ?",
        "Comment appliquer cela dans un problème concret ?",
        "Quelles sont les erreurs courantes à éviter ?"
      ],
      nsi: [
        "Montre-moi d'autres exemples de code",
        "Comment optimiser cet algorithme ?",
        "Quels sont les cas d'usage pratiques ?"
      ],
      physics: [
        "Peux-tu me donner des exemples du quotidien ?",
        "Comment résoudre des exercices similaires ?",
        "Quelles formules dois-je retenir ?"
      ],
      french: [
        "Comment structurer ma présentation ?",
        "Quels arguments utiliser ?",
        "Comment gérer le stress de l'oral ?"
      ],
      general: [
        "Peux-tu m'en dire plus ?",
        "Comment puis-je m'améliorer ?",
        "Quelles sont tes recommandations ?"
      ]
    };
    
    return suggestions[category] || suggestions.general;
  };

  const generateResponseActions = (category) => {
    const actions = {
      math: [
        { text: "Générer exercice", action: () => generatePersonalizedExercise('maths') },
        { text: "Créer fiche", action: () => onGenerateDocument('math-summary') }
      ],
      nsi: [
        { text: "Analyser code", action: () => analyzeCode() },
        { text: "Projet guidé", action: () => startGuidedProject() }
      ],
      physics: [
        { text: "Schéma explicatif", action: () => generateDiagram() },
        { text: "TP virtuel", action: () => startVirtualLab() }
      ],
      french: [
        { text: "Simulation oral", action: () => startOralSimulation() },
        { text: "Plan détaillé", action: () => generateEssayPlan() }
      ]
    };
    
    return actions[category] || [];
  };

  const generatePersonalizedExercise = (subject) => {
    setAriaThinking(true);
    setTimeout(() => {
      const exercise = {
        id: Date.now(),
        type: 'aria',
        content: `🎯 **Exercice personnalisé en ${subject}**\n\nJ'ai créé un exercice adapté à ton niveau et à ton style d'apprentissage. Il prend en compte tes points forts et les domaines à améliorer.`,
        timestamp: new Date(),
        mood: 'creative',
        isExercise: true,
        exerciseData: {
          subject: subject,
          difficulty: student?.level || 1,
          type: 'personalized',
          estimatedTime: '15-20 minutes'
        }
      };
      
      setMessages(prev => [...prev, exercise]);
      setAriaThinking(false);
      
      if (onRequestExercise) {
        onRequestExercise(subject, student?.level);
      }
    }, 2000);
  };

  const startVoiceInteraction = () => {
    if (!isListening) {
      setIsListening(true);
      // Simulation de reconnaissance vocale
      setTimeout(() => {
        setIsListening(false);
        setInputMessage("Peux-tu m'expliquer les limites en mathématiques ?");
      }, 3000);
    } else {
      setIsListening(false);
    }
  };

  const speakMessage = (message) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(message.content);
      utterance.lang = 'fr-FR';
      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      
      speechSynthesis.speak(utterance);
    }
  };

  const handleFileAttachment = (event) => {
    const files = Array.from(event.target.files);
    setAttachedFiles(prev => [...prev, ...files]);
  };

  const removeAttachment = (index) => {
    setAttachedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const copyMessage = (message) => {
    navigator.clipboard.writeText(message.content);
    addNotification({
      type: 'success',
      title: 'Message copié',
      message: 'Le message a été copié dans le presse-papiers'
    });
  };

  const rateMessage = (messageId, rating) => {
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, userRating: rating }
        : msg
    ));
    
    addNotification({
      type: 'success',
      title: 'Merci pour votre retour !',
      message: 'Votre évaluation aide ARIA à s\'améliorer'
    });
  };

  if (!isVisible) return null;

  return (
    <div className={`nexus-aria-container ${isMinimized ? 'minimized' : ''}`}>
      {/* Header */}
      <div className="nexus-aria-header">
        <div className="flex items-center space-x-3">
          <div className="nexus-aria-avatar">
            <Brain className="w-6 h-6" />
            <div className="nexus-aria-status-indicator"></div>
          </div>
          <div>
            <h3 className="font-semibold">ARIA</h3>
            <p className="text-xs text-muted-foreground">
              {ariaThinking ? 'Réfléchit...' : 'Assistant pédagogique'}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {/* Mode selector */}
          <select 
            value={currentMode} 
            onChange={(e) => setCurrentMode(e.target.value)}
            className="nexus-aria-mode-selector"
          >
            <option value="chat">💬 Chat</option>
            <option value="tutor">👨‍🏫 Tuteur</option>
            <option value="generator">📝 Générateur</option>
            <option value="analyzer">📊 Analyseur</option>
          </select>
          
          <Button variant="ghost" size="sm" onClick={onMinimize}>
            {isMinimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
          </Button>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {!isMinimized && (
        <>
          {/* Mode Actions */}
          {getModeActions().length > 0 && (
            <div className="nexus-aria-mode-actions">
              {getModeActions().map((action, index) => (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  onClick={action.action}
                  className="nexus-aria-action-btn"
                >
                  <action.icon className="w-4 h-4 mr-2" />
                  {action.text}
                </Button>
              ))}
            </div>
          )}

          {/* Messages */}
          <div className="nexus-aria-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`nexus-aria-message ${message.type === 'user' ? 'user' : 'aria'}`}
              >
                <div className="nexus-aria-message-avatar">
                  {message.type === 'user' ? (
                    <User className="w-4 h-4" />
                  ) : (
                    <Brain className="w-4 h-4" />
                  )}
                </div>
                
                <div className="nexus-aria-message-content">
                  <div className="nexus-aria-message-bubble">
                    <div className="nexus-aria-message-text">
                      {message.content}
                    </div>
                    
                    {message.attachments && message.attachments.length > 0 && (
                      <div className="nexus-aria-attachments">
                        {message.attachments.map((file, index) => (
                          <div key={index} className="nexus-aria-attachment">
                            <Paperclip className="w-4 h-4" />
                            <span>{file.name}</span>
                          </div>
                        ))}
                      </div>
                    )}
                    
                    {message.isExercise && (
                      <div className="nexus-aria-exercise-card">
                        <div className="flex items-center space-x-2 mb-2">
                          <Target className="w-4 h-4 text-blue-600" />
                          <span className="font-medium">Exercice personnalisé</span>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          <p>Matière: {message.exerciseData.subject}</p>
                          <p>Durée estimée: {message.exerciseData.estimatedTime}</p>
                        </div>
                        <Button size="sm" className="mt-2">
                          <Play className="w-4 h-4 mr-2" />
                          Commencer l'exercice
                        </Button>
                      </div>
                    )}
                  </div>
                  
                  <div className="nexus-aria-message-meta">
                    <span className="nexus-aria-timestamp">
                      {message.timestamp.toLocaleTimeString('fr-FR', { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </span>
                    
                    {message.type === 'aria' && (
                      <div className="nexus-aria-message-actions">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => speakMessage(message)}
                          disabled={isSpeaking}
                        >
                          {isSpeaking ? <VolumeX className="w-3 h-3" /> : <Volume2 className="w-3 h-3" />}
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyMessage(message)}
                        >
                          <Copy className="w-3 h-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => rateMessage(message.id, 'up')}
                          className={message.userRating === 'up' ? 'text-green-600' : ''}
                        >
                          <ThumbsUp className="w-3 h-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => rateMessage(message.id, 'down')}
                          className={message.userRating === 'down' ? 'text-red-600' : ''}
                        >
                          <ThumbsDown className="w-3 h-3" />
                        </Button>
                      </div>
                    )}
                  </div>
                  
                  {message.suggestions && (
                    <div className="nexus-aria-suggestions">
                      {message.suggestions.map((suggestion, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="nexus-aria-suggestion-btn"
                        >
                          {suggestion}
                        </Button>
                      ))}
                    </div>
                  )}
                  
                  {message.actions && message.actions.length > 0 && (
                    <div className="nexus-aria-message-actions-bar">
                      {message.actions.map((action, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={action.action}
                          className="nexus-aria-action-btn"
                        >
                          {action.text}
                        </Button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {ariaThinking && (
              <div className="nexus-aria-message aria">
                <div className="nexus-aria-message-avatar">
                  <Brain className="w-4 h-4" />
                </div>
                <div className="nexus-aria-message-content">
                  <div className="nexus-aria-thinking">
                    <div className="nexus-aria-thinking-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span className="text-sm text-muted-foreground">ARIA réfléchit...</span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Suggestions contextuelles */}
          {showSuggestions && messages.length <= 2 && (
            <div className="nexus-aria-suggestions-panel">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-sm">Suggestions pour commencer</h4>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowSuggestions(false)}
                >
                  <EyeOff className="w-3 h-3" />
                </Button>
              </div>
              <div className="grid grid-cols-2 gap-2">
                {contextualSuggestions.slice(0, 6).map((suggestion, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    onClick={suggestion.action}
                    className="nexus-aria-suggestion-card"
                  >
                    <suggestion.icon className="w-4 h-4 mr-2" />
                    <span className="text-xs">{suggestion.text}</span>
                  </Button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="nexus-aria-input-container">
            {/* Attachments preview */}
            {attachedFiles.length > 0 && (
              <div className="nexus-aria-attachments-preview">
                {attachedFiles.map((file, index) => (
                  <div key={index} className="nexus-aria-attachment-preview">
                    <Paperclip className="w-3 h-3" />
                    <span className="text-xs">{file.name}</span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeAttachment(index)}
                    >
                      <X className="w-3 h-3" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
            
            <div className="nexus-aria-input-bar">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileAttachment}
                multiple
                accept=".pdf,.doc,.docx,.txt,.jpg,.png,.py"
                className="hidden"
              />
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => fileInputRef.current?.click()}
                className="nexus-aria-input-btn"
              >
                <Paperclip className="w-4 h-4" />
              </Button>
              
              <input
                ref={inputRef}
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Pose ta question à ARIA..."
                className="nexus-aria-input"
                disabled={isTyping}
              />
              
              <Button
                variant="ghost"
                size="sm"
                onClick={startVoiceInteraction}
                className={`nexus-aria-input-btn ${isListening ? 'listening' : ''}`}
              >
                {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
              </Button>
              
              <Button
                onClick={() => sendMessage()}
                disabled={!inputMessage.trim() || isTyping}
                className="nexus-aria-send-btn"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
            
            <div className="nexus-aria-input-footer">
              <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                <span>Mode: {currentMode}</span>
                <span>Matière: {selectedSubject}</span>
                <span>Style: {ariaPersonality}</span>
              </div>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowSuggestions(!showSuggestions)}
              >
                <Lightbulb className="w-3 h-3 mr-1" />
                <span className="text-xs">Suggestions</span>
              </Button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ARIAAgent;

