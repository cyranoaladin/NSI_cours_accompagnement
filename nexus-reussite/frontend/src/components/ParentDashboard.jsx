import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  User, 
  BookOpen, 
  Brain, 
  Trophy, 
  Star, 
  Clock, 
  Target, 
  TrendingUp,
  MessageCircle,
  Calendar,
  FileText,
  Award,
  Zap,
  Users,
  GraduationCap,
  BarChart3,
  CheckCircle,
  AlertCircle,
  Info,
  Eye,
  Download,
  Share2,
  Heart,
  Bookmark,
  ChevronRight,
  Plus,
  Filter,
  Search,
  Bell,
  Settings,
  Home,
  Flame,
  Sparkles,
  Phone,
  Mail,
  Video,
  Send,
  Edit,
  Trash2,
  ChevronDown,
  ExternalLink,
  PieChart,
  Activity,
  Briefcase,
  UserCheck
} from 'lucide-react'

const ParentDashboard = ({ student, students, onSelectStudent, teachers, documents, addNotification }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedPeriod, setSelectedPeriod] = useState('month');
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [selectedTeacher, setSelectedTeacher] = useState(null);

  const getProgressColor = (progress) => {
    if (progress >= 80) return 'text-green-600 bg-green-100 dark:bg-green-900/20';
    if (progress >= 60) return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
    return 'text-red-600 bg-red-100 dark:bg-red-900/20';
  };

  const getSubjectIcon = (subject) => {
    switch (subject.toLowerCase()) {
      case 'mathématiques':
      case 'maths':
        return '📐';
      case 'nsi':
        return '💻';
      case 'physique':
        return '⚛️';
      case 'français':
        return '📚';
      default:
        return '📖';
    }
  };

  const weeklyReports = [
    {
      week: 'Semaine du 15-21 Juillet',
      subjects: [
        {
          name: 'Mathématiques',
          teacher: 'M. Dubois',
          hours: 2,
          topics: ['Fonctions exponentielles', 'Limites'],
          progress: 85,
          grade: 16,
          comment: 'Excellente progression sur les fonctions exponentielles. Sarah maîtrise bien les concepts et applique correctement les méthodes.',
          homework: 'Exercices 45-50 p.127, Révision chapitre 8',
          nextGoals: 'Approfondir les limites et dérivées'
        },
        {
          name: 'NSI',
          teacher: 'Mme Martin',
          hours: 2,
          topics: ['Algorithmes de tri', 'Complexité'],
          progress: 78,
          grade: 15,
          comment: 'Bonne compréhension des algorithmes. Travail à poursuivre sur l\'analyse de complexité.',
          homework: 'Projet tri fusion à terminer',
          nextGoals: 'Structures de données avancées'
        },
        {
          name: 'Physique',
          teacher: 'Dr. Rousseau',
          hours: 1.5,
          topics: ['Optique géométrique', 'Lentilles'],
          progress: 72,
          grade: 14,
          comment: 'Notions comprises mais application pratique à renforcer avec plus d\'exercices.',
          homework: 'TP lentilles convergentes',
          nextGoals: 'Maîtriser les constructions géométriques'
        }
      ],
      globalComment: 'Semaine très productive. Sarah montre une excellente motivation et des progrès constants. L\'IA ARIA l\'aide efficacement dans ses révisions personnalisées.',
      ariaInsights: 'ARIA a identifié que Sarah apprend mieux avec des supports visuels. Recommandation : privilégier les schémas et diagrammes.',
      nextWeekFocus: 'Préparation intensive pour le contrôle de mathématiques du 28 juillet'
    }
  ];

  const messages = [
    {
      id: 1,
      from: 'M. Dubois',
      subject: 'Mathématiques',
      title: 'Excellent travail cette semaine',
      message: 'Sarah a fait d\'excellents progrès sur les fonctions exponentielles. Je recommande de continuer sur cette lancée avec les exercices supplémentaires que j\'ai préparés.',
      date: '2025-07-22',
      time: '14:30',
      read: false,
      priority: 'normal'
    },
    {
      id: 2,
      from: 'Mme Martin',
      subject: 'NSI',
      title: 'Projet à finaliser',
      message: 'Le projet sur les algorithmes de tri avance bien. Sarah peut me contacter si elle a des questions sur la partie complexité.',
      date: '2025-07-21',
      time: '16:45',
      read: true,
      priority: 'normal'
    },
    {
      id: 3,
      from: 'Équipe Nexus',
      subject: 'Général',
      title: 'Nouvelle fonctionnalité ARIA disponible',
      message: 'ARIA peut maintenant générer des exercices personnalisés basés sur le profil d\'apprentissage de Sarah. Découvrez cette fonctionnalité dans l\'onglet Documents.',
      date: '2025-07-20',
      time: '10:00',
      read: true,
      priority: 'info'
    }
  ];

  const upcomingSessions = [
    {
      date: '2025-07-23',
      time: '14:00',
      subject: 'Mathématiques',
      teacher: 'M. Dubois',
      type: 'Cours individuel',
      topic: 'Révision fonctions + Contrôle blanc',
      location: 'Centre Nexus - Salle 2',
      duration: '1h30'
    },
    {
      date: '2025-07-24',
      time: '16:00',
      subject: 'NSI',
      teacher: 'Mme Martin',
      type: 'Cours individuel',
      topic: 'Structures de données - Listes chaînées',
      location: 'Centre Nexus - Salle Info',
      duration: '2h'
    },
    {
      date: '2025-07-26',
      time: '10:00',
      subject: 'Physique',
      teacher: 'Dr. Rousseau',
      type: 'Mini-groupe (4 élèves)',
      topic: 'TP Optique - Manipulation lentilles',
      location: 'Centre Nexus - Labo',
      duration: '2h'
    }
  ];

  const sendMessage = (teacherId, message) => {
    addNotification({
      type: 'success',
      title: 'Message envoyé',
      message: `Votre message a été envoyé à ${teachers.find(t => t.id === teacherId)?.name}`
    });
    setShowMessageModal(false);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header avec sélection d'élève */}
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
          <div className="flex items-center space-x-4 mb-4 md:mb-0">
            <div className="w-16 h-16 nexus-avatar bg-primary text-primary-foreground text-xl">
              {student?.avatar || 'E'}
            </div>
            <div>
              <h1 className="text-2xl font-bold">Suivi de {student?.name || 'votre enfant'}</h1>
              <p className="text-muted-foreground">{student?.grade} - {student?.school}</p>
              <div className="flex items-center space-x-4 mt-2">
                <Badge className="nexus-badge-info">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  {student?.progress?.overall || 0}% de progression
                </Badge>
                <Badge className="nexus-badge-success">
                  <Trophy className="w-3 h-3 mr-1" />
                  Niveau {student?.level || 1}
                </Badge>
                <Badge className="nexus-badge-warning">
                  <Flame className="w-3 h-3 mr-1" />
                  {student?.streak || 0} jours actifs
                </Badge>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Sélecteur d'élève si plusieurs enfants */}
            {students?.length > 1 && (
              <select 
                className="nexus-input"
                value={student?.id || ''}
                onChange={(e) => onSelectStudent(students.find(s => s.id === e.target.value))}
              >
                {students.map(s => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
            )}

            <Button 
              variant="outline"
              onClick={() => setShowMessageModal(true)}
            >
              <MessageCircle className="w-4 h-4 mr-2" />
              Contacter un prof
            </Button>

            <Button className="nexus-button-primary">
              <Calendar className="w-4 h-4 mr-2" />
              Planifier RDV
            </Button>
          </div>
        </div>

        {/* Alerte si besoin d'attention */}
        <Card className="nexus-card border-orange-200 bg-orange-50 dark:bg-orange-900/20">
          <CardContent className="p-4">
            <div className="flex items-center space-x-3">
              <AlertCircle className="w-5 h-5 text-orange-600" />
              <div>
                <h3 className="font-semibold text-orange-900 dark:text-orange-100">
                  Contrôle de mathématiques prévu
                </h3>
                <p className="text-orange-700 dark:text-orange-300">
                  Contrôle sur les fonctions exponentielles le 28 juillet. Sarah est bien préparée selon M. Dubois.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Onglets principaux */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4 mb-8">
          <TabsTrigger value="overview" className="flex items-center space-x-2">
            <BarChart3 className="w-4 h-4" />
            <span>Vue d'ensemble</span>
          </TabsTrigger>
          <TabsTrigger value="profile" className="flex items-center space-x-2">
            <User className="w-4 h-4" />
            <span>Profil Élève</span>
          </TabsTrigger>
          <TabsTrigger value="reports" className="flex items-center space-x-2">
            <FileText className="w-4 h-4" />
            <span>Rapports</span>
          </TabsTrigger>
          <TabsTrigger value="communication" className="flex items-center space-x-2">
            <MessageCircle className="w-4 h-4" />
            <span>Communication</span>
          </TabsTrigger>
        </TabsList>

        {/* Vue d'ensemble */}
        <TabsContent value="overview">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Colonne principale */}
            <div className="lg:col-span-2 space-y-6">
              {/* Métriques principales */}
              <div className="grid md:grid-cols-4 gap-4">
                <Card className="nexus-metric-card">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                      <TrendingUp className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <div className="nexus-metric-value text-green-600">{student?.progress?.overall || 0}%</div>
                      <div className="nexus-metric-label">Progression</div>
                    </div>
                  </div>
                </Card>

                <Card className="nexus-metric-card">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                      <Clock className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <div className="nexus-metric-value text-blue-600">12h</div>
                      <div className="nexus-metric-label">Ce mois</div>
                    </div>
                  </div>
                </Card>

                <Card className="nexus-metric-card">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                      <Brain className="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                      <div className="nexus-metric-value text-purple-600">94%</div>
                      <div className="nexus-metric-label">Confiance ARIA</div>
                    </div>
                  </div>
                </Card>

                <Card className="nexus-metric-card">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg flex items-center justify-center">
                      <Target className="w-6 h-6 text-yellow-600" />
                    </div>
                    <div>
                      <div className="nexus-metric-value text-yellow-600">3/4</div>
                      <div className="nexus-metric-label">Objectifs</div>
                    </div>
                  </div>
                </Card>
              </div>

              {/* Progression par matière */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <BarChart3 className="w-5 h-5" />
                    <span>Progression par Matière</span>
                  </CardTitle>
                  <CardDescription>Évolution des performances sur le mois</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {student?.subjects?.map((subject, index) => {
                      const progress = student.progress?.[subject.toLowerCase()] || 0;
                      const teacher = teachers?.find(t => t.subject.toLowerCase().includes(subject.toLowerCase()));
                      return (
                        <div key={index} className="space-y-3">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <span className="text-lg">{getSubjectIcon(subject)}</span>
                              <div>
                                <span className="font-medium">{subject}</span>
                                <p className="text-sm text-muted-foreground">{teacher?.name}</p>
                              </div>
                            </div>
                            <div className="text-right">
                              <span className="text-lg font-semibold">{progress}%</span>
                              <p className="text-sm text-muted-foreground">Moyenne: 15.2/20</p>
                            </div>
                          </div>
                          <div className="nexus-progress-bar">
                            <div 
                              className={`nexus-progress-fill ${
                                progress >= 80 ? 'bg-green-500' :
                                progress >= 60 ? 'bg-yellow-500' :
                                'bg-red-500'
                              }`}
                              style={{ width: `${progress}%` }}
                            ></div>
                          </div>
                          <div className="flex items-center justify-between text-sm text-muted-foreground">
                            <span>Dernière évaluation: 16/20</span>
                            <span>Tendance: ↗️ +2 points</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>

              {/* Prochaines sessions */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Calendar className="w-5 h-5" />
                    <span>Prochaines Sessions</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {upcomingSessions.map((session, index) => (
                      <div key={index} className="flex items-center space-x-4 p-4 rounded-lg bg-muted/50">
                        <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                          <BookOpen className="w-6 h-6 text-blue-600" />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-1">
                            <h4 className="font-semibold">{session.subject}</h4>
                            <Badge variant="outline">{session.type}</Badge>
                          </div>
                          <p className="text-sm text-muted-foreground mb-1">{session.topic}</p>
                          <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                            <span className="flex items-center space-x-1">
                              <Calendar className="w-3 h-3" />
                              <span>{session.date}</span>
                            </span>
                            <span className="flex items-center space-x-1">
                              <Clock className="w-3 h-3" />
                              <span>{session.time} ({session.duration})</span>
                            </span>
                            <span className="flex items-center space-x-1">
                              <Users className="w-3 h-3" />
                              <span>{session.teacher}</span>
                            </span>
                          </div>
                        </div>
                        <Button variant="outline" size="sm">
                          <Eye className="w-4 h-4 mr-2" />
                          Détails
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Profil d'apprentissage ARIA */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Brain className="w-5 h-5 text-purple-600" />
                    <span>Analyse ARIA</span>
                  </CardTitle>
                  <CardDescription>
                    Profil d'apprentissage de votre enfant
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-3 rounded-lg bg-purple-50 dark:bg-purple-900/20">
                      <h4 className="font-medium text-purple-900 dark:text-purple-100 mb-2">
                        Style dominant: Visuel (85%)
                      </h4>
                      <p className="text-sm text-purple-700 dark:text-purple-300">
                        Votre enfant apprend mieux avec des schémas, graphiques et supports visuels.
                      </p>
                    </div>
                    
                    <div className="space-y-3">
                      {Object.entries(student?.learningStyle || {}).map(([style, percentage]) => (
                        <div key={style} className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="capitalize">
                              {style === 'readingWriting' ? 'Lecture/Écriture' : 
                               style === 'visual' ? 'Visuel' :
                               style === 'auditory' ? 'Auditif' :
                               style === 'kinesthetic' ? 'Kinesthésique' : style}
                            </span>
                            <span className="font-semibold">{percentage}%</span>
                          </div>
                          <div className="nexus-progress-bar">
                            <div 
                              className={`nexus-progress-fill ${
                                percentage >= 80 ? 'bg-green-500' :
                                percentage >= 60 ? 'bg-yellow-500' :
                                'bg-red-500'
                              }`}
                              style={{ width: `${percentage}%` }}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                      <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                        Recommandation ARIA
                      </h4>
                      <p className="text-sm text-blue-700 dark:text-blue-300">
                        Privilégier les exercices avec diagrammes et schémas. Éviter les longs textes.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Messages non lus */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <MessageCircle className="w-5 h-5" />
                      <span>Messages</span>
                    </div>
                    <Badge className="nexus-badge-info">
                      {messages.filter(m => !m.read).length} nouveaux
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {messages.slice(0, 3).map((message) => (
                      <div key={message.id} className={`p-3 rounded-lg border ${
                        !message.read ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200' : 'bg-muted/50'
                      }`}>
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <h4 className="font-medium text-sm">{message.from}</h4>
                            <p className="text-xs text-muted-foreground">{message.subject}</p>
                          </div>
                          {!message.read && (
                            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                          )}
                        </div>
                        <p className="text-sm">{message.title}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {message.date} à {message.time}
                        </p>
                      </div>
                    ))}
                  </div>
                  <Button variant="outline" size="sm" className="w-full mt-4">
                    <Eye className="w-4 h-4 mr-2" />
                    Voir tous les messages
                  </Button>
                </CardContent>
              </Card>

              {/* Actions rapides */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Actions Rapides</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <Calendar className="w-4 h-4 mr-2" />
                    Planifier RDV parent-prof
                  </Button>
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <Download className="w-4 h-4 mr-2" />
                    Télécharger bulletin
                  </Button>
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Envoyer un message
                  </Button>
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <Settings className="w-4 h-4 mr-2" />
                    Paramètres compte
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        {/* Profil Élève */}
        <TabsContent value="profile">
          <div className="grid lg:grid-cols-2 gap-6">
            <div className="space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Informations Générales</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-4">
                      <div className="w-20 h-20 nexus-avatar bg-primary text-primary-foreground text-2xl">
                        {student?.avatar}
                      </div>
                      <div>
                        <h3 className="text-xl font-bold">{student?.name}</h3>
                        <p className="text-muted-foreground">{student?.grade}</p>
                        <p className="text-sm text-muted-foreground">{student?.school}</p>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                      <div>
                        <p className="text-sm text-muted-foreground">Profil</p>
                        <p className="font-medium capitalize">{student?.profile}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Niveau</p>
                        <p className="font-medium">Niveau {student?.level}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">XP Total</p>
                        <p className="font-medium">{student?.xp} points</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Série active</p>
                        <p className="font-medium">{student?.streak} jours</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Style d'Apprentissage</CardTitle>
                  <CardDescription>Analyse détaillée par ARIA</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(student?.learningStyle || {}).map(([style, percentage]) => (
                      <div key={style} className="space-y-2">
                        <div className="flex justify-between">
                          <span className="font-medium capitalize">
                            {style === 'readingWriting' ? 'Lecture/Écriture' : 
                             style === 'visual' ? 'Visuel' :
                             style === 'auditory' ? 'Auditif' :
                             style === 'kinesthetic' ? 'Kinesthésique' : style}
                          </span>
                          <span className="font-semibold">{percentage}%</span>
                        </div>
                        <div className="nexus-progress-bar">
                          <div 
                            className={`nexus-progress-fill ${
                              percentage >= 80 ? 'bg-green-500' :
                              percentage >= 60 ? 'bg-yellow-500' :
                              'bg-red-500'
                            }`}
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {style === 'visual' && percentage >= 80 && 'Privilégier schémas, graphiques et supports visuels'}
                          {style === 'auditory' && percentage >= 80 && 'Favoriser explications orales et discussions'}
                          {style === 'kinesthetic' && percentage >= 80 && 'Encourager manipulation et expérimentation'}
                          {style === 'readingWriting' && percentage >= 80 && 'Utiliser textes, listes et prise de notes'}
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Recommandations ARIA</CardTitle>
                  <CardDescription>Conseils personnalisés pour optimiser l'apprentissage</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 rounded-lg bg-purple-50 dark:bg-purple-900/20">
                      <div className="flex items-start space-x-3">
                        <Brain className="w-5 h-5 text-purple-600 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-purple-900 dark:text-purple-100">
                            Optimisation d'apprentissage
                          </h4>
                          <p className="text-sm text-purple-700 dark:text-purple-300 mt-1">
                            Le style visuel dominant de {student?.name} suggère d'utiliser plus de diagrammes et schémas, 
                            particulièrement en mathématiques et sciences.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                      <div className="flex items-start space-x-3">
                        <Clock className="w-5 h-5 text-blue-600 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-blue-900 dark:text-blue-100">
                            Moment optimal d'étude
                          </h4>
                          <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                            Les meilleures performances sont observées entre 14h et 16h. 
                            Planifiez les matières les plus difficiles à ce moment.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/20">
                      <div className="flex items-start space-x-3">
                        <Target className="w-5 h-5 text-green-600 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-green-900 dark:text-green-100">
                            Points forts à exploiter
                          </h4>
                          <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                            Excellente capacité d'analyse en mathématiques. 
                            Encourager l'approfondissement vers les mathématiques supérieures.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="p-4 rounded-lg bg-yellow-50 dark:bg-yellow-900/20">
                      <div className="flex items-start space-x-3">
                        <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-yellow-900 dark:text-yellow-100">
                            Points d'attention
                          </h4>
                          <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                            La physique nécessite plus de pratique. 
                            Recommandation : augmenter les exercices d'application.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Badges et Réalisations</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-3">
                    {student?.badges?.map((badge, index) => (
                      <div key={index} className="text-center p-3 rounded-lg bg-muted/50">
                        <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/20 rounded-full flex items-center justify-center mx-auto mb-2">
                          <Award className="w-6 h-6 text-yellow-600" />
                        </div>
                        <p className="text-xs font-medium">{badge}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        {/* Rapports */}
        <TabsContent value="reports">
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold">Rapports Hebdomadaires</h2>
                <p className="text-muted-foreground">Suivi détaillé des progrès et commentaires des enseignants</p>
              </div>
              <div className="flex items-center space-x-2">
                <select className="nexus-input">
                  <option value="week">Cette semaine</option>
                  <option value="month">Ce mois</option>
                  <option value="term">Ce trimestre</option>
                </select>
                <Button variant="outline" size="sm">
                  <Download className="w-4 h-4 mr-2" />
                  Exporter PDF
                </Button>
              </div>
            </div>

            {weeklyReports.map((report, reportIndex) => (
              <Card key={reportIndex} className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{report.week}</span>
                    <Badge className="nexus-badge-success">Rapport complet</Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {/* Résumé global */}
                    <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                      <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
                        Commentaire Global
                      </h4>
                      <p className="text-blue-700 dark:text-blue-300">{report.globalComment}</p>
                    </div>

                    {/* Insights ARIA */}
                    <div className="p-4 rounded-lg bg-purple-50 dark:bg-purple-900/20">
                      <h4 className="font-semibold text-purple-900 dark:text-purple-100 mb-2 flex items-center space-x-2">
                        <Brain className="w-4 h-4" />
                        <span>Analyse ARIA</span>
                      </h4>
                      <p className="text-purple-700 dark:text-purple-300">{report.ariaInsights}</p>
                    </div>

                    {/* Détail par matière */}
                    <div className="space-y-4">
                      <h4 className="font-semibold">Détail par Matière</h4>
                      {report.subjects.map((subject, subjectIndex) => (
                        <Card key={subjectIndex} className="nexus-card">
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-4">
                              <div className="flex items-center space-x-3">
                                <span className="text-lg">{getSubjectIcon(subject.name)}</span>
                                <div>
                                  <h5 className="font-semibold">{subject.name}</h5>
                                  <p className="text-sm text-muted-foreground">{subject.teacher}</p>
                                </div>
                              </div>
                              <div className="text-right">
                                <div className="text-2xl font-bold text-primary">{subject.grade}/20</div>
                                <div className="text-sm text-muted-foreground">{subject.hours}h de cours</div>
                              </div>
                            </div>

                            <div className="space-y-3">
                              <div>
                                <p className="text-sm font-medium mb-1">Notions abordées:</p>
                                <div className="flex flex-wrap gap-2">
                                  {subject.topics.map((topic, topicIndex) => (
                                    <Badge key={topicIndex} variant="outline">{topic}</Badge>
                                  ))}
                                </div>
                              </div>

                              <div>
                                <div className="flex justify-between text-sm mb-1">
                                  <span>Progression</span>
                                  <span>{subject.progress}%</span>
                                </div>
                                <div className="nexus-progress-bar">
                                  <div 
                                    className={`nexus-progress-fill ${
                                      subject.progress >= 80 ? 'bg-green-500' :
                                      subject.progress >= 60 ? 'bg-yellow-500' :
                                      'bg-red-500'
                                    }`}
                                    style={{ width: `${subject.progress}%` }}
                                  ></div>
                                </div>
                              </div>

                              <div>
                                <p className="text-sm font-medium mb-1">Commentaire du professeur:</p>
                                <p className="text-sm text-muted-foreground">{subject.comment}</p>
                              </div>

                              <div className="grid md:grid-cols-2 gap-4 pt-3 border-t">
                                <div>
                                  <p className="text-sm font-medium mb-1">Travail à faire:</p>
                                  <p className="text-sm text-muted-foreground">{subject.homework}</p>
                                </div>
                                <div>
                                  <p className="text-sm font-medium mb-1">Objectifs semaine prochaine:</p>
                                  <p className="text-sm text-muted-foreground">{subject.nextGoals}</p>
                                </div>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>

                    {/* Focus semaine prochaine */}
                    <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/20">
                      <h4 className="font-semibold text-green-900 dark:text-green-100 mb-2">
                        Focus Semaine Prochaine
                      </h4>
                      <p className="text-green-700 dark:text-green-300">{report.nextWeekFocus}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Communication */}
        <TabsContent value="communication">
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>Messages</span>
                    <Button size="sm" onClick={() => setShowMessageModal(true)}>
                      <Plus className="w-4 h-4 mr-2" />
                      Nouveau message
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {messages.map((message) => (
                      <div key={message.id} className={`p-4 rounded-lg border ${
                        !message.read ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200' : 'bg-muted/50'
                      }`}>
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 nexus-avatar bg-primary text-primary-foreground text-sm">
                              {message.from.split(' ').map(n => n[0]).join('')}
                            </div>
                            <div>
                              <h4 className="font-semibold">{message.from}</h4>
                              <p className="text-sm text-muted-foreground">{message.subject}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-xs text-muted-foreground">{message.date}</p>
                            <p className="text-xs text-muted-foreground">{message.time}</p>
                            {!message.read && (
                              <Badge className="nexus-badge-info mt-1">Nouveau</Badge>
                            )}
                          </div>
                        </div>
                        <h5 className="font-medium mb-2">{message.title}</h5>
                        <p className="text-sm text-muted-foreground">{message.message}</p>
                        <div className="flex items-center space-x-2 mt-3">
                          <Button variant="outline" size="sm">
                            <MessageCircle className="w-4 h-4 mr-2" />
                            Répondre
                          </Button>
                          <Button variant="outline" size="sm">
                            <Share2 className="w-4 h-4 mr-2" />
                            Transférer
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Équipe Pédagogique</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {teachers?.map((teacher) => (
                      <div key={teacher.id} className="flex items-center space-x-3 p-3 rounded-lg bg-muted/50">
                        <div className="w-12 h-12 nexus-avatar bg-primary text-primary-foreground">
                          {teacher.avatar}
                        </div>
                        <div className="flex-1">
                          <h4 className="font-medium">{teacher.name}</h4>
                          <p className="text-sm text-muted-foreground">{teacher.subject}</p>
                          <div className="flex items-center space-x-1 mt-1">
                            {[...Array(5)].map((_, i) => (
                              <Star 
                                key={i} 
                                className={`w-3 h-3 ${
                                  i < Math.floor(teacher.rating) 
                                    ? 'text-yellow-400 fill-current' 
                                    : 'text-gray-300'
                                }`} 
                              />
                            ))}
                            <span className="text-xs text-muted-foreground ml-1">({teacher.rating})</span>
                          </div>
                        </div>
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => {
                            setSelectedTeacher(teacher);
                            setShowMessageModal(true);
                          }}
                        >
                          <MessageCircle className="w-4 h-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Planifier un Rendez-vous</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <label className="nexus-form-label">Avec qui ?</label>
                      <select className="nexus-input w-full">
                        <option>Sélectionner un enseignant</option>
                        {teachers?.map(teacher => (
                          <option key={teacher.id} value={teacher.id}>{teacher.name}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="nexus-form-label">Type de rendez-vous</label>
                      <select className="nexus-input w-full">
                        <option>Suivi général</option>
                        <option>Point sur une matière</option>
                        <option>Orientation</option>
                        <option>Problème spécifique</option>
                      </select>
                    </div>
                    <div>
                      <label className="nexus-form-label">Créneaux préférés</label>
                      <div className="grid grid-cols-2 gap-2">
                        <label className="flex items-center space-x-2">
                          <input type="checkbox" className="rounded" />
                          <span className="text-sm">Matin</span>
                        </label>
                        <label className="flex items-center space-x-2">
                          <input type="checkbox" className="rounded" />
                          <span className="text-sm">Après-midi</span>
                        </label>
                        <label className="flex items-center space-x-2">
                          <input type="checkbox" className="rounded" />
                          <span className="text-sm">Visio</span>
                        </label>
                        <label className="flex items-center space-x-2">
                          <input type="checkbox" className="rounded" />
                          <span className="text-sm">Présentiel</span>
                        </label>
                      </div>
                    </div>
                    <Button className="w-full nexus-button-primary">
                      <Calendar className="w-4 h-4 mr-2" />
                      Demander un rendez-vous
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Contact Urgence</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <Button variant="outline" className="w-full justify-start">
                      <Phone className="w-4 h-4 mr-2" />
                      +216 XX XXX XXX
                    </Button>
                    <Button variant="outline" className="w-full justify-start">
                      <Mail className="w-4 h-4 mr-2" />
                      contact@nexus-reussite.tn
                    </Button>
                    <Button variant="outline" className="w-full justify-start">
                      <Video className="w-4 h-4 mr-2" />
                      Assistance en ligne
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* Modal de nouveau message */}
      {showMessageModal && (
        <div className="nexus-modal-overlay">
          <div className="nexus-modal max-w-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Nouveau Message</h3>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => setShowMessageModal(false)}
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="nexus-form-label">Destinataire</label>
                <select className="nexus-input w-full">
                  <option>Sélectionner un enseignant</option>
                  {teachers?.map(teacher => (
                    <option key={teacher.id} value={teacher.id}>{teacher.name} - {teacher.subject}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="nexus-form-label">Sujet</label>
                <input 
                  type="text" 
                  className="nexus-input w-full" 
                  placeholder="Objet de votre message"
                />
              </div>
              
              <div>
                <label className="nexus-form-label">Message</label>
                <textarea 
                  className="nexus-input w-full h-32 resize-none" 
                  placeholder="Votre message..."
                ></textarea>
              </div>
              
              <div className="flex space-x-3">
                <Button 
                  className="flex-1 nexus-button-primary"
                  onClick={() => sendMessage('dubois', 'Message test')}
                >
                  <Send className="w-4 h-4 mr-2" />
                  Envoyer
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => setShowMessageModal(false)}
                >
                  Annuler
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ParentDashboard;

