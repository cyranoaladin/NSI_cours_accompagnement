import React, { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Video, 
  VideoOff, 
  Mic, 
  MicOff, 
  Phone, 
  PhoneOff,
  Monitor,
  MonitorOff,
  Users,
  MessageSquare,
  Settings,
  Volume2,
  VolumeX,
  Camera,
  CameraOff,
  Maximize,
  Minimize,
  MoreHorizontal,
  Copy,
  ExternalLink,
  Clock,
  Calendar,
  User,
  Shield,
  Wifi,
  WifiOff,
  AlertTriangle,
  CheckCircle,
  Info,
  X,
  Plus,
  Minus,
  RotateCcw,
  Download,
  Upload,
  Share2,
  FileText,
  Image,
  Paperclip,
  Send,
  Smile,
  ThumbsUp,
  Heart,
  Zap,
  Star,
  Award,
  Target,
  BookOpen,
  Brain,
  Lightbulb,
  PenTool,
  Calculator,
  Code,
  Atom,
  Globe,
  Lock,
  Unlock,
  Eye,
  EyeOff,
  Headphones,
  Speaker,
  Keyboard,
  Mouse,
  Gamepad2
} from 'lucide-react'

const VideoConference = ({ 
  session, 
  student, 
  teacher, 
  onJoinSession, 
  onLeaveSession, 
  onSendMessage,
  onShareScreen,
  onRecordSession,
  isVisible,
  onClose 
}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isVideoEnabled, setIsVideoEnabled] = useState(true);
  const [isAudioEnabled, setIsAudioEnabled] = useState(true);
  const [isScreenSharing, setIsScreenSharing] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [connectionQuality, setConnectionQuality] = useState('excellent'); // excellent, good, poor
  const [participants, setParticipants] = useState([]);
  const [chatMessages, setChatMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [sessionDuration, setSessionDuration] = useState(0);
  const [isWaitingRoom, setIsWaitingRoom] = useState(false);
  const [sharedDocuments, setSharedDocuments] = useState([]);
  const [whiteboardActive, setWhiteboardActive] = useState(false);

  const videoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const chatRef = useRef(null);
  const sessionStartTime = useRef(null);

  // Données de démonstration
  const demoSession = {
    id: 'session-001',
    title: 'Cours de Mathématiques - Fonctions Exponentielles',
    teacher: {
      id: 'dubois',
      name: 'M. Dubois',
      avatar: 'MD',
      subject: 'Mathématiques'
    },
    student: {
      id: 'sarah-2025',
      name: 'Sarah Benali',
      avatar: 'SB'
    },
    scheduledTime: '2025-07-23T14:00:00Z',
    duration: 60, // minutes
    type: 'individual', // individual, group
    status: 'active', // scheduled, active, completed
    meetingId: 'nexus-math-001',
    meetingPassword: 'NX2025',
    recordingEnabled: true,
    whiteboardEnabled: true,
    screenShareEnabled: true,
    chatEnabled: true
  };

  const demoChatMessages = [
    {
      id: 'msg-001',
      sender: 'teacher',
      senderName: 'M. Dubois',
      message: 'Bonjour Sarah ! Êtes-vous prête pour notre session sur les fonctions exponentielles ?',
      timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
      type: 'text'
    },
    {
      id: 'msg-002',
      sender: 'student',
      senderName: 'Sarah',
      message: 'Bonjour M. Dubois ! Oui, j\'ai préparé mes questions sur les dérivées.',
      timestamp: new Date(Date.now() - 4 * 60 * 1000).toISOString(),
      type: 'text'
    },
    {
      id: 'msg-003',
      sender: 'teacher',
      senderName: 'M. Dubois',
      message: 'Parfait ! Je vais partager mon écran pour vous montrer quelques exemples.',
      timestamp: new Date(Date.now() - 3 * 60 * 1000).toISOString(),
      type: 'text'
    },
    {
      id: 'msg-004',
      sender: 'system',
      senderName: 'Système',
      message: 'M. Dubois a partagé son écran',
      timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
      type: 'system'
    },
    {
      id: 'msg-005',
      sender: 'student',
      senderName: 'Sarah',
      message: 'Je vois parfaitement ! Merci pour ces explications claires.',
      timestamp: new Date(Date.now() - 1 * 60 * 1000).toISOString(),
      type: 'text'
    }
  ];

  const demoSharedDocuments = [
    {
      id: 'doc-001',
      name: 'Fonctions Exponentielles - Cours.pdf',
      type: 'pdf',
      size: '2.3 MB',
      sharedBy: 'M. Dubois',
      timestamp: new Date(Date.now() - 10 * 60 * 1000).toISOString()
    },
    {
      id: 'doc-002',
      name: 'Exercices - Dérivées.pdf',
      type: 'pdf',
      size: '1.8 MB',
      sharedBy: 'M. Dubois',
      timestamp: new Date(Date.now() - 8 * 60 * 1000).toISOString()
    },
    {
      id: 'doc-003',
      name: 'Graphique_fonction_exp.png',
      type: 'image',
      size: '456 KB',
      sharedBy: 'Sarah',
      timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString()
    }
  ];

  // Simulation de la connexion
  useEffect(() => {
    if (isVisible && !isConnected) {
      // Simulation de la salle d'attente
      setIsWaitingRoom(true);
      setTimeout(() => {
        setIsWaitingRoom(false);
        setIsConnected(true);
        sessionStartTime.current = Date.now();
        setParticipants([demoSession.teacher, demoSession.student]);
        setChatMessages(demoChatMessages);
        setSharedDocuments(demoSharedDocuments);
      }, 3000);
    }
  }, [isVisible, isConnected]);

  // Timer de session
  useEffect(() => {
    let interval;
    if (isConnected && sessionStartTime.current) {
      interval = setInterval(() => {
        setSessionDuration(Math.floor((Date.now() - sessionStartTime.current) / 1000));
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isConnected]);

  // Simulation de la qualité de connexion
  useEffect(() => {
    if (isConnected) {
      const interval = setInterval(() => {
        const qualities = ['excellent', 'good', 'poor'];
        const weights = [0.7, 0.25, 0.05]; // 70% excellent, 25% good, 5% poor
        const random = Math.random();
        let cumulative = 0;
        for (let i = 0; i < qualities.length; i++) {
          cumulative += weights[i];
          if (random <= cumulative) {
            setConnectionQuality(qualities[i]);
            break;
          }
        }
      }, 10000);
      return () => clearInterval(interval);
    }
  }, [isConnected]);

  const formatDuration = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  const getConnectionIcon = () => {
    switch (connectionQuality) {
      case 'excellent': return <Wifi className="w-4 h-4 text-green-600" />;
      case 'good': return <Wifi className="w-4 h-4 text-yellow-600" />;
      case 'poor': return <WifiOff className="w-4 h-4 text-red-600" />;
      default: return <Wifi className="w-4 h-4 text-gray-400" />;
    }
  };

  const handleJoinSession = () => {
    setIsConnected(true);
    sessionStartTime.current = Date.now();
    if (onJoinSession) {
      onJoinSession(demoSession.id);
    }
  };

  const handleLeaveSession = () => {
    setIsConnected(false);
    setIsVideoEnabled(true);
    setIsAudioEnabled(true);
    setIsScreenSharing(false);
    setIsRecording(false);
    setSessionDuration(0);
    sessionStartTime.current = null;
    if (onLeaveSession) {
      onLeaveSession(demoSession.id);
    }
    if (onClose) {
      onClose();
    }
  };

  const toggleVideo = () => {
    setIsVideoEnabled(!isVideoEnabled);
  };

  const toggleAudio = () => {
    setIsAudioEnabled(!isAudioEnabled);
  };

  const toggleScreenShare = () => {
    setIsScreenSharing(!isScreenSharing);
    if (onShareScreen) {
      onShareScreen(!isScreenSharing);
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (onRecordSession) {
      onRecordSession(!isRecording);
    }
  };

  const sendMessage = () => {
    if (newMessage.trim()) {
      const message = {
        id: `msg-${Date.now()}`,
        sender: 'student',
        senderName: student?.name || 'Vous',
        message: newMessage,
        timestamp: new Date().toISOString(),
        type: 'text'
      };
      
      setChatMessages(prev => [...prev, message]);
      setNewMessage('');
      
      if (onSendMessage) {
        onSendMessage(message);
      }
      
      // Simulation de réponse automatique
      setTimeout(() => {
        const autoReply = {
          id: `msg-${Date.now() + 1}`,
          sender: 'teacher',
          senderName: teacher?.name || 'Professeur',
          message: 'Merci pour votre question ! Je vais vous expliquer cela.',
          timestamp: new Date().toISOString(),
          type: 'text'
        };
        setChatMessages(prev => [...prev, autoReply]);
      }, 2000);
    }
  };

  const copyMeetingInfo = () => {
    const meetingInfo = `
Réunion Nexus Réussite
ID: ${demoSession.meetingId}
Mot de passe: ${demoSession.meetingPassword}
Lien: https://meet.nexus-reussite.tn/join/${demoSession.meetingId}
    `.trim();
    
    navigator.clipboard.writeText(meetingInfo);
    // Notification de copie
  };

  if (!isVisible) return null;

  // Salle d'attente
  if (isWaitingRoom) {
    return (
      <div className="nexus-video-conference waiting-room">
        <Card className="nexus-card max-w-md mx-auto">
          <CardHeader className="text-center">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Video className="w-8 h-8 text-blue-600" />
            </div>
            <CardTitle>Salle d'attente</CardTitle>
            <CardDescription>
              Connexion à votre session en cours...
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <div className="space-y-2">
              <h4 className="font-semibold">{demoSession.title}</h4>
              <p className="text-sm text-muted-foreground">
                avec {demoSession.teacher.name}
              </p>
            </div>
            
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-center space-x-4">
                <Button
                  variant={isVideoEnabled ? "default" : "outline"}
                  size="sm"
                  onClick={toggleVideo}
                >
                  {isVideoEnabled ? <Video className="w-4 h-4" /> : <VideoOff className="w-4 h-4" />}
                </Button>
                <Button
                  variant={isAudioEnabled ? "default" : "outline"}
                  size="sm"
                  onClick={toggleAudio}
                >
                  {isAudioEnabled ? <Mic className="w-4 h-4" /> : <MicOff className="w-4 h-4" />}
                </Button>
              </div>
              <p className="text-xs text-muted-foreground">
                Vérifiez votre caméra et microphone
              </p>
            </div>
            
            <Button variant="outline" onClick={onClose}>
              Annuler
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className={`nexus-video-conference ${isFullscreen ? 'fullscreen' : ''}`}>
      {/* Header de la session */}
      <div className="nexus-video-header">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
              <Video className="w-4 h-4 text-green-600" />
            </div>
            <div>
              <h3 className="font-semibold text-sm">{demoSession.title}</h3>
              <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                <Clock className="w-3 h-3" />
                <span>{formatDuration(sessionDuration)}</span>
                <div className="flex items-center space-x-1">
                  {getConnectionIcon()}
                  <span className="capitalize">{connectionQuality}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {isRecording && (
            <Badge className="bg-red-600 text-white animate-pulse">
              <div className="w-2 h-2 bg-white rounded-full mr-2"></div>
              REC
            </Badge>
          )}
          
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsFullscreen(!isFullscreen)}
          >
            {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
          </Button>
          
          <Button variant="ghost" size="sm" onClick={copyMeetingInfo}>
            <Copy className="w-4 h-4" />
          </Button>
          
          <Button variant="ghost" size="sm" onClick={handleLeaveSession}>
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <div className="nexus-video-content">
        {/* Zone vidéo principale */}
        <div className="nexus-video-main">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 h-full">
            {/* Vidéo du professeur */}
            <div className="nexus-video-participant teacher">
              <div className="relative bg-gray-900 rounded-lg overflow-hidden h-full min-h-[300px]">
                {/* Simulation de la vidéo */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-900 to-purple-900 flex items-center justify-center">
                  <div className="text-center text-white">
                    <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-2xl font-bold">
                        {demoSession.teacher.avatar}
                      </span>
                    </div>
                    <h4 className="font-semibold">{demoSession.teacher.name}</h4>
                    <p className="text-sm opacity-75">{demoSession.teacher.subject}</p>
                  </div>
                </div>
                
                {/* Contrôles de la vidéo */}
                <div className="absolute bottom-4 left-4 flex items-center space-x-2">
                  <Badge variant="secondary" className="text-xs">
                    Professeur
                  </Badge>
                  {isScreenSharing && (
                    <Badge className="bg-blue-600 text-white text-xs">
                      <Monitor className="w-3 h-3 mr-1" />
                      Partage d'écran
                    </Badge>
                  )}
                </div>
                
                <div className="absolute bottom-4 right-4 flex items-center space-x-1">
                  <div className="w-6 h-6 bg-green-600 rounded-full flex items-center justify-center">
                    <Mic className="w-3 h-3 text-white" />
                  </div>
                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                    <Video className="w-3 h-3 text-white" />
                  </div>
                </div>
              </div>
            </div>
            
            {/* Vidéo de l'étudiant */}
            <div className="nexus-video-participant student">
              <div className="relative bg-gray-900 rounded-lg overflow-hidden h-full min-h-[300px]">
                {/* Simulation de la vidéo */}
                <div className="absolute inset-0 bg-gradient-to-br from-green-900 to-teal-900 flex items-center justify-center">
                  <div className="text-center text-white">
                    <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-2xl font-bold">
                        {demoSession.student.avatar}
                      </span>
                    </div>
                    <h4 className="font-semibold">{demoSession.student.name}</h4>
                    <p className="text-sm opacity-75">Étudiant</p>
                  </div>
                </div>
                
                {/* Contrôles de la vidéo */}
                <div className="absolute bottom-4 left-4 flex items-center space-x-2">
                  <Badge variant="secondary" className="text-xs">
                    Vous
                  </Badge>
                </div>
                
                <div className="absolute bottom-4 right-4 flex items-center space-x-1">
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center ${
                    isAudioEnabled ? 'bg-green-600' : 'bg-red-600'
                  }`}>
                    {isAudioEnabled ? 
                      <Mic className="w-3 h-3 text-white" /> : 
                      <MicOff className="w-3 h-3 text-white" />
                    }
                  </div>
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center ${
                    isVideoEnabled ? 'bg-blue-600' : 'bg-red-600'
                  }`}>
                    {isVideoEnabled ? 
                      <Video className="w-3 h-3 text-white" /> : 
                      <VideoOff className="w-3 h-3 text-white" />
                    }
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Panneau latéral */}
        <div className="nexus-video-sidebar">
          <div className="flex flex-col h-full">
            {/* Onglets */}
            <div className="flex border-b">
              <button
                onClick={() => setIsChatOpen(true)}
                className={`flex-1 px-4 py-2 text-sm font-medium ${
                  isChatOpen ? 'border-b-2 border-blue-600 text-blue-600' : 'text-muted-foreground'
                }`}
              >
                <MessageSquare className="w-4 h-4 inline mr-2" />
                Chat
              </button>
              <button
                onClick={() => setIsChatOpen(false)}
                className={`flex-1 px-4 py-2 text-sm font-medium ${
                  !isChatOpen ? 'border-b-2 border-blue-600 text-blue-600' : 'text-muted-foreground'
                }`}
              >
                <FileText className="w-4 h-4 inline mr-2" />
                Documents
              </button>
            </div>

            {/* Contenu du chat */}
            {isChatOpen ? (
              <div className="flex flex-col flex-1">
                <div className="flex-1 overflow-y-auto p-4 space-y-3" ref={chatRef}>
                  {chatMessages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${
                        message.sender === 'student' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
                          message.sender === 'student'
                            ? 'bg-blue-600 text-white'
                            : message.sender === 'system'
                            ? 'bg-gray-100 dark:bg-gray-800 text-muted-foreground text-center'
                            : 'bg-gray-100 dark:bg-gray-800'
                        }`}
                      >
                        {message.sender !== 'system' && message.sender !== 'student' && (
                          <div className="font-medium text-xs mb-1 opacity-75">
                            {message.senderName}
                          </div>
                        )}
                        <div>{message.message}</div>
                        <div className="text-xs opacity-50 mt-1">
                          {new Date(message.timestamp).toLocaleTimeString('fr-FR', {
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                
                {/* Zone de saisie */}
                <div className="border-t p-4">
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                      placeholder="Tapez votre message..."
                      className="flex-1 nexus-input text-sm"
                    />
                    <Button size="sm" onClick={sendMessage} disabled={!newMessage.trim()}>
                      <Send className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </div>
            ) : (
              /* Contenu des documents */
              <div className="flex-1 overflow-y-auto p-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold text-sm">Documents partagés</h4>
                    <Button variant="ghost" size="sm">
                      <Plus className="w-4 h-4" />
                    </Button>
                  </div>
                  
                  {sharedDocuments.map((doc) => (
                    <div key={doc.id} className="nexus-shared-document">
                      <div className="flex items-center space-x-3 p-3 rounded-lg border hover:bg-muted/50">
                        <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/20 rounded flex items-center justify-center">
                          {doc.type === 'pdf' ? (
                            <FileText className="w-4 h-4 text-blue-600" />
                          ) : (
                            <Image className="w-4 h-4 text-blue-600" />
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h5 className="font-medium text-sm truncate">{doc.name}</h5>
                          <p className="text-xs text-muted-foreground">
                            {doc.sharedBy} • {doc.size}
                          </p>
                        </div>
                        <Button variant="ghost" size="sm">
                          <Download className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  ))}
                  
                  {sharedDocuments.length === 0 && (
                    <div className="text-center py-8">
                      <FileText className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
                      <p className="text-sm text-muted-foreground">
                        Aucun document partagé
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Contrôles de la session */}
      <div className="nexus-video-controls">
        <div className="flex items-center justify-center space-x-4">
          <Button
            variant={isAudioEnabled ? "default" : "destructive"}
            size="lg"
            onClick={toggleAudio}
            className="rounded-full w-12 h-12"
          >
            {isAudioEnabled ? <Mic className="w-5 h-5" /> : <MicOff className="w-5 h-5" />}
          </Button>
          
          <Button
            variant={isVideoEnabled ? "default" : "destructive"}
            size="lg"
            onClick={toggleVideo}
            className="rounded-full w-12 h-12"
          >
            {isVideoEnabled ? <Video className="w-5 h-5" /> : <VideoOff className="w-5 h-5" />}
          </Button>
          
          <Button
            variant={isScreenSharing ? "default" : "outline"}
            size="lg"
            onClick={toggleScreenShare}
            className="rounded-full w-12 h-12"
          >
            {isScreenSharing ? <MonitorOff className="w-5 h-5" /> : <Monitor className="w-5 h-5" />}
          </Button>
          
          <Button
            variant={isRecording ? "destructive" : "outline"}
            size="lg"
            onClick={toggleRecording}
            className="rounded-full w-12 h-12"
          >
            <div className={`w-3 h-3 rounded-full ${isRecording ? 'bg-white' : 'bg-red-600'}`}></div>
          </Button>
          
          <Button
            variant={whiteboardActive ? "default" : "outline"}
            size="lg"
            onClick={() => setWhiteboardActive(!whiteboardActive)}
            className="rounded-full w-12 h-12"
          >
            <PenTool className="w-5 h-5" />
          </Button>
          
          <Button
            variant="destructive"
            size="lg"
            onClick={handleLeaveSession}
            className="rounded-full w-12 h-12"
          >
            <PhoneOff className="w-5 h-5" />
          </Button>
        </div>
        
        <div className="flex items-center justify-between mt-4 text-sm text-muted-foreground">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <Users className="w-4 h-4" />
              <span>{participants.length} participant{participants.length > 1 ? 's' : ''}</span>
            </div>
            <div className="flex items-center space-x-1">
              {getConnectionIcon()}
              <span className="capitalize">{connectionQuality}</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-1">
            <Clock className="w-4 h-4" />
            <span>{formatDuration(sessionDuration)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Composant pour programmer une session
export const ScheduleVideoSession = ({ onSchedule, teachers, student }) => {
  const [selectedTeacher, setSelectedTeacher] = useState('');
  const [sessionDate, setSessionDate] = useState('');
  const [sessionTime, setSessionTime] = useState('');
  const [duration, setDuration] = useState(60);
  const [subject, setSubject] = useState('');
  const [sessionType, setSessionType] = useState('individual');
  const [notes, setNotes] = useState('');

  const handleSchedule = () => {
    const sessionData = {
      teacherId: selectedTeacher,
      studentId: student?.id,
      date: sessionDate,
      time: sessionTime,
      duration,
      subject,
      type: sessionType,
      notes,
      scheduledAt: new Date().toISOString()
    };
    
    if (onSchedule) {
      onSchedule(sessionData);
    }
  };

  return (
    <Card className="nexus-card max-w-md">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Calendar className="w-5 h-5" />
          <span>Programmer une session</span>
        </CardTitle>
        <CardDescription>
          Planifiez votre prochaine session de cours en ligne
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label className="nexus-form-label">Professeur</label>
          <select
            value={selectedTeacher}
            onChange={(e) => setSelectedTeacher(e.target.value)}
            className="nexus-input w-full"
          >
            <option value="">Sélectionner un professeur</option>
            {teachers?.map((teacher) => (
              <option key={teacher.id} value={teacher.id}>
                {teacher.name} - {teacher.subject}
              </option>
            ))}
          </select>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="nexus-form-label">Date</label>
            <input
              type="date"
              value={sessionDate}
              onChange={(e) => setSessionDate(e.target.value)}
              className="nexus-input w-full"
              min={new Date().toISOString().split('T')[0]}
            />
          </div>
          <div>
            <label className="nexus-form-label">Heure</label>
            <input
              type="time"
              value={sessionTime}
              onChange={(e) => setSessionTime(e.target.value)}
              className="nexus-input w-full"
            />
          </div>
        </div>
        
        <div>
          <label className="nexus-form-label">Durée (minutes)</label>
          <select
            value={duration}
            onChange={(e) => setDuration(parseInt(e.target.value))}
            className="nexus-input w-full"
          >
            <option value={30}>30 minutes</option>
            <option value={60}>1 heure</option>
            <option value={90}>1h30</option>
            <option value={120}>2 heures</option>
          </select>
        </div>
        
        <div>
          <label className="nexus-form-label">Matière</label>
          <input
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder="Ex: Mathématiques - Fonctions"
            className="nexus-input w-full"
          />
        </div>
        
        <div>
          <label className="nexus-form-label">Type de session</label>
          <select
            value={sessionType}
            onChange={(e) => setSessionType(e.target.value)}
            className="nexus-input w-full"
          >
            <option value="individual">Cours individuel</option>
            <option value="group">Cours en groupe</option>
            <option value="review">Session de révision</option>
            <option value="exam_prep">Préparation d'examen</option>
          </select>
        </div>
        
        <div>
          <label className="nexus-form-label">Notes (optionnel)</label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Points spécifiques à aborder, questions préparées..."
            className="nexus-input w-full h-20 resize-none"
          />
        </div>
        
        <div className="flex space-x-2">
          <Button
            onClick={handleSchedule}
            disabled={!selectedTeacher || !sessionDate || !sessionTime}
            className="flex-1"
          >
            <Calendar className="w-4 h-4 mr-2" />
            Programmer
          </Button>
          <Button variant="outline" className="flex-1">
            Annuler
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default VideoConference;

