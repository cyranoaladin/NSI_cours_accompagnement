import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
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
  Play,
  Pause,
  RotateCcw,
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
  User,
  Home,
  Flame,
  Sparkles
} from 'lucide-react'

const StudentDashboard = ({ student, documents, onShowARIA, addNotification }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedSubject, setSelectedSubject] = useState('all');
  const [studyTimer, setStudyTimer] = useState({ active: false, time: 0 });

  useEffect(() => {
    let interval;
    if (studyTimer.active) {
      interval = setInterval(() => {
        setStudyTimer(prev => ({ ...prev, time: prev.time + 1 }));
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [studyTimer.active]);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const toggleTimer = () => {
    setStudyTimer(prev => ({ ...prev, active: !prev.active }));
    if (!studyTimer.active) {
      addNotification({
        type: 'info',
        title: 'Session d\'étude démarrée',
        message: 'Bon travail ! ARIA suit votre progression.'
      });
    }
  };

  const resetTimer = () => {
    setStudyTimer({ active: false, time: 0 });
  };

  const getProgressColor = (progress) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
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

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header avec informations élève */}
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
          <div className="flex items-center space-x-4 mb-4 md:mb-0">
            <div className="w-16 h-16 nexus-avatar bg-primary text-primary-foreground text-xl">
              {student?.avatar || 'E'}
            </div>
            <div>
              <h1 className="text-2xl font-bold">Bonjour {student?.name || 'Élève'} !</h1>
              <p className="text-muted-foreground">{student?.grade} - {student?.school}</p>
              <div className="flex items-center space-x-4 mt-2">
                <Badge className="nexus-badge-info">
                  <Flame className="w-3 h-3 mr-1" />
                  Série de {student?.streak || 0} jours
                </Badge>
                <Badge className="nexus-badge-success">
                  <Trophy className="w-3 h-3 mr-1" />
                  Niveau {student?.level || 1}
                </Badge>
                <Badge className="nexus-badge-warning">
                  <Zap className="w-3 h-3 mr-1" />
                  {student?.xp || 0} XP
                </Badge>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Chronomètre d'étude */}
            <Card className="nexus-card p-4">
              <div className="text-center">
                <div className="text-2xl font-mono font-bold text-primary mb-2">
                  {formatTime(studyTimer.time)}
                </div>
                <div className="flex space-x-2">
                  <Button
                    size="sm"
                    onClick={toggleTimer}
                    className={studyTimer.active ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}
                  >
                    {studyTimer.active ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                  </Button>
                  <Button size="sm" variant="outline" onClick={resetTimer}>
                    <RotateCcw className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </Card>

            <Button onClick={onShowARIA} className="nexus-button-primary">
              <Brain className="w-4 h-4 mr-2" />
              Parler à ARIA
            </Button>
          </div>
        </div>

        {/* Prochaine session */}
        {student?.nextSession && (
          <Card className="nexus-card p-4 bg-blue-50 dark:bg-blue-900/20 border-blue-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-800 rounded-lg flex items-center justify-center">
                  <Calendar className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-blue-900 dark:text-blue-100">Prochaine session</h3>
                  <p className="text-blue-700 dark:text-blue-300">
                    {student.nextSession.subject} avec {student.nextSession.teacher}
                  </p>
                  <p className="text-sm text-blue-600 dark:text-blue-400">
                    {student.nextSession.date} à {student.nextSession.time}
                  </p>
                </div>
              </div>
              <Button variant="outline" size="sm" className="border-blue-300 text-blue-700 hover:bg-blue-100">
                <Eye className="w-4 h-4 mr-2" />
                Voir détails
              </Button>
            </div>
          </Card>
        )}
      </div>

      {/* Onglets principaux */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5 mb-8">
          <TabsTrigger value="overview" className="flex items-center space-x-2">
            <Home className="w-4 h-4" />
            <span>Vue d'ensemble</span>
          </TabsTrigger>
          <TabsTrigger value="progress" className="flex items-center space-x-2">
            <BarChart3 className="w-4 h-4" />
            <span>Progression</span>
          </TabsTrigger>
          <TabsTrigger value="documents" className="flex items-center space-x-2">
            <FileText className="w-4 h-4" />
            <span>Documents</span>
          </TabsTrigger>
          <TabsTrigger value="badges" className="flex items-center space-x-2">
            <Trophy className="w-4 h-4" />
            <span>Badges</span>
          </TabsTrigger>
          <TabsTrigger value="planning" className="flex items-center space-x-2">
            <Calendar className="w-4 h-4" />
            <span>Planning</span>
          </TabsTrigger>
        </TabsList>

        {/* Vue d'ensemble */}
        <TabsContent value="overview">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Colonne principale */}
            <div className="lg:col-span-2 space-y-6">
              {/* Métriques rapides */}
              <div className="grid md:grid-cols-3 gap-4">
                <Card className="nexus-metric-card">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                      <TrendingUp className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <div className="nexus-metric-value text-green-600">{student?.progress?.overall || 0}%</div>
                      <div className="nexus-metric-label">Progression globale</div>
                    </div>
                  </div>
                </Card>

                <Card className="nexus-metric-card">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                      <Target className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <div className="nexus-metric-value text-blue-600">{documents?.length || 0}</div>
                      <div className="nexus-metric-label">Documents actifs</div>
                    </div>
                  </div>
                </Card>

                <Card className="nexus-metric-card">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                      <Flame className="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                      <div className="nexus-metric-value text-purple-600">{student?.streak || 0}</div>
                      <div className="nexus-metric-label">Jours consécutifs</div>
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
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {student?.subjects?.map((subject, index) => {
                      const progress = student.progress?.[subject.toLowerCase()] || 0;
                      return (
                        <div key={index} className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-2">
                              <span className="text-lg">{getSubjectIcon(subject)}</span>
                              <span className="font-medium">{subject}</span>
                            </div>
                            <span className="text-sm font-semibold">{progress}%</span>
                          </div>
                          <div className="nexus-progress-bar">
                            <div 
                              className={`nexus-progress-fill ${getProgressColor(progress)}`}
                              style={{ width: `${progress}%` }}
                            ></div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>

              {/* Activités récentes */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Clock className="w-5 h-5" />
                    <span>Activités Récentes</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {student?.recentActivities?.map((activity, index) => (
                      <div key={index} className="flex items-start space-x-4 p-3 rounded-lg bg-muted/50">
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                          activity.type === 'achievement' ? 'bg-green-100 dark:bg-green-900/20' :
                          activity.type === 'message' ? 'bg-blue-100 dark:bg-blue-900/20' :
                          'bg-gray-100 dark:bg-gray-900/20'
                        }`}>
                          {activity.type === 'achievement' ? (
                            <Trophy className="w-5 h-5 text-green-600" />
                          ) : activity.type === 'message' ? (
                            <MessageCircle className="w-5 h-5 text-blue-600" />
                          ) : (
                            <Bell className="w-5 h-5 text-gray-600" />
                          )}
                        </div>
                        <div className="flex-1">
                          <h4 className="font-medium">{activity.message}</h4>
                          <p className="text-sm text-muted-foreground">{activity.detail}</p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {activity.date} à {activity.time}
                          </p>
                        </div>
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
                    <span>Profil ARIA</span>
                  </CardTitle>
                  <CardDescription>
                    Votre style d'apprentissage analysé par l'IA
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(student?.learningStyle || {}).map(([style, percentage]) => (
                      <div key={style} className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="capitalize">{style === 'readingWriting' ? 'Lecture/Écriture' : style}</span>
                          <span className="font-semibold">{percentage}%</span>
                        </div>
                        <div className="nexus-progress-bar">
                          <div 
                            className={`nexus-progress-fill ${getProgressColor(percentage)}`}
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="w-full mt-4"
                    onClick={onShowARIA}
                  >
                    <Brain className="w-4 h-4 mr-2" />
                    Optimiser avec ARIA
                  </Button>
                </CardContent>
              </Card>

              {/* Badges récents */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Trophy className="w-5 h-5 text-yellow-600" />
                    <span>Badges Récents</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-3">
                    {student?.badges?.slice(0, 4).map((badge, index) => (
                      <div key={index} className="text-center p-3 rounded-lg bg-muted/50">
                        <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/20 rounded-full flex items-center justify-center mx-auto mb-2">
                          <Award className="w-6 h-6 text-yellow-600" />
                        </div>
                        <p className="text-xs font-medium">{badge}</p>
                      </div>
                    ))}
                  </div>
                  <Button variant="outline" size="sm" className="w-full mt-4">
                    <Eye className="w-4 h-4 mr-2" />
                    Voir tous les badges
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
                    <Plus className="w-4 h-4 mr-2" />
                    Nouveau document
                  </Button>
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <Calendar className="w-4 h-4 mr-2" />
                    Planifier session
                  </Button>
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Contacter prof
                  </Button>
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <Settings className="w-4 h-4 mr-2" />
                    Paramètres
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        {/* Progression détaillée */}
        <TabsContent value="progress">
          <div className="space-y-6">
            <Card className="nexus-card">
              <CardHeader>
                <CardTitle>Analyse Détaillée de Progression</CardTitle>
                <CardDescription>
                  Évolution de vos performances sur les 30 derniers jours
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 bg-muted/30 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <BarChart3 className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Graphique de progression</p>
                    <p className="text-sm text-muted-foreground">Données des 30 derniers jours</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="grid md:grid-cols-2 gap-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Objectifs du Mois</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 rounded-lg bg-green-50 dark:bg-green-900/20">
                      <div className="flex items-center space-x-3">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                        <span className="font-medium">Maîtriser les fonctions exponentielles</span>
                      </div>
                      <Badge className="nexus-badge-success">Terminé</Badge>
                    </div>
                    <div className="flex items-center justify-between p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                      <div className="flex items-center space-x-3">
                        <Target className="w-5 h-5 text-blue-600" />
                        <span className="font-medium">Projet NSI - Algorithmes de tri</span>
                      </div>
                      <Badge className="nexus-badge-info">En cours</Badge>
                    </div>
                    <div className="flex items-center justify-between p-3 rounded-lg bg-yellow-50 dark:bg-yellow-900/20">
                      <div className="flex items-center space-x-3">
                        <Clock className="w-5 h-5 text-yellow-600" />
                        <span className="font-medium">Préparation Grand Oral</span>
                      </div>
                      <Badge className="nexus-badge-warning">À venir</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Recommandations ARIA</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-3 rounded-lg bg-purple-50 dark:bg-purple-900/20">
                      <div className="flex items-start space-x-3">
                        <Brain className="w-5 h-5 text-purple-600 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-purple-900 dark:text-purple-100">
                            Optimisation d'apprentissage
                          </h4>
                          <p className="text-sm text-purple-700 dark:text-purple-300">
                            Votre style visuel dominant suggère d'utiliser plus de schémas en mathématiques.
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                      <div className="flex items-start space-x-3">
                        <Sparkles className="w-5 h-5 text-blue-600 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-blue-900 dark:text-blue-100">
                            Moment optimal
                          </h4>
                          <p className="text-sm text-blue-700 dark:text-blue-300">
                            Vos meilleures performances sont entre 14h et 16h. Planifiez les matières difficiles à ce moment.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="w-full mt-4"
                    onClick={onShowARIA}
                  >
                    <Brain className="w-4 h-4 mr-2" />
                    Plus de conseils ARIA
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        {/* Documents */}
        <TabsContent value="documents">
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold">Mes Documents</h2>
                <p className="text-muted-foreground">Cours, exercices et évaluations personnalisés</p>
              </div>
              <div className="flex items-center space-x-2">
                <Button variant="outline" size="sm">
                  <Filter className="w-4 h-4 mr-2" />
                  Filtrer
                </Button>
                <Button size="sm" className="nexus-button-primary">
                  <Plus className="w-4 h-4 mr-2" />
                  Nouveau document
                </Button>
              </div>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {documents?.map((doc) => (
                <Card key={doc.id} className="nexus-card hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg">{doc.title}</CardTitle>
                        <CardDescription>{doc.subject}</CardDescription>
                      </div>
                      <Badge className={
                        doc.status === 'completed' ? 'nexus-badge-success' :
                        doc.status === 'in_progress' ? 'nexus-badge-info' :
                        'nexus-badge-warning'
                      }>
                        {doc.status === 'completed' ? 'Terminé' :
                         doc.status === 'in_progress' ? 'En cours' :
                         'À faire'}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Progression</span>
                        <span className="font-semibold">{doc.progress}%</span>
                      </div>
                      <div className="nexus-progress-bar">
                        <div 
                          className={`nexus-progress-fill ${getProgressColor(doc.progress)}`}
                          style={{ width: `${doc.progress}%` }}
                        ></div>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>{doc.duration} min</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Target className="w-4 h-4" />
                          <span>Niveau {doc.difficulty}/5</span>
                        </div>
                      </div>

                      <div className="flex space-x-2">
                        <Button size="sm" className="flex-1">
                          <Play className="w-4 h-4 mr-2" />
                          {doc.status === 'completed' ? 'Revoir' : 'Continuer'}
                        </Button>
                        <Button size="sm" variant="outline">
                          <Download className="w-4 h-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Share2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </TabsContent>

        {/* Badges et gamification */}
        <TabsContent value="badges">
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Mes Badges et Récompenses</h2>
              <p className="text-muted-foreground">Célébrez vos accomplissements et votre progression</p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <Card className="nexus-card text-center p-6">
                <div className="w-20 h-20 bg-yellow-100 dark:bg-yellow-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Trophy className="w-10 h-10 text-yellow-600" />
                </div>
                <h3 className="text-xl font-bold mb-2">Niveau {student?.level || 1}</h3>
                <p className="text-muted-foreground mb-4">{student?.xp || 0} XP</p>
                <div className="nexus-progress-bar mb-2">
                  <div 
                    className="nexus-progress-fill bg-yellow-500"
                    style={{ width: `${((student?.xp || 0) % 1000) / 10}%` }}
                  ></div>
                </div>
                <p className="text-sm text-muted-foreground">
                  {1000 - ((student?.xp || 0) % 1000)} XP pour le niveau suivant
                </p>
              </Card>

              <Card className="nexus-card text-center p-6">
                <div className="w-20 h-20 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Flame className="w-10 h-10 text-red-600" />
                </div>
                <h3 className="text-xl font-bold mb-2">Série Active</h3>
                <p className="text-muted-foreground mb-4">{student?.streak || 0} jours consécutifs</p>
                <p className="text-sm text-muted-foreground">
                  Continuez votre série en étudiant aujourd'hui !
                </p>
              </Card>

              <Card className="nexus-card text-center p-6">
                <div className="w-20 h-20 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Star className="w-10 h-10 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold mb-2">Badges Obtenus</h3>
                <p className="text-muted-foreground mb-4">{student?.badges?.length || 0} badges</p>
                <p className="text-sm text-muted-foreground">
                  Explorez de nouveaux défis pour plus de badges !
                </p>
              </Card>
            </div>

            <Card className="nexus-card">
              <CardHeader>
                <CardTitle>Collection de Badges</CardTitle>
                <CardDescription>Vos accomplissements et réussites</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-4 gap-4">
                  {student?.badges?.map((badge, index) => (
                    <div key={index} className="text-center p-4 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
                      <div className="w-16 h-16 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-3">
                        <Award className="w-8 h-8 text-white" />
                      </div>
                      <h4 className="font-semibold mb-1">{badge}</h4>
                      <p className="text-xs text-muted-foreground">Obtenu récemment</p>
                    </div>
                  ))}
                  
                  {/* Badges à débloquer */}
                  <div className="text-center p-4 rounded-lg border-2 border-dashed border-muted-foreground/30">
                    <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-3">
                      <Plus className="w-8 h-8 text-muted-foreground" />
                    </div>
                    <h4 className="font-semibold mb-1 text-muted-foreground">Prochain Badge</h4>
                    <p className="text-xs text-muted-foreground">Complétez 5 exercices</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Planning */}
        <TabsContent value="planning">
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold">Mon Planning</h2>
                <p className="text-muted-foreground">Sessions programmées et disponibilités</p>
              </div>
              <Button size="sm" className="nexus-button-primary">
                <Plus className="w-4 h-4 mr-2" />
                Nouvelle session
              </Button>
            </div>

            <div className="grid lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <Card className="nexus-card">
                  <CardHeader>
                    <CardTitle>Calendrier de la Semaine</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-96 bg-muted/30 rounded-lg flex items-center justify-center">
                      <div className="text-center">
                        <Calendar className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                        <p className="text-muted-foreground">Vue calendrier</p>
                        <p className="text-sm text-muted-foreground">Sessions et événements de la semaine</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              <div className="space-y-6">
                <Card className="nexus-card">
                  <CardHeader>
                    <CardTitle>Prochaines Sessions</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {student?.nextSession && (
                        <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                          <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-blue-100 dark:bg-blue-800 rounded-lg flex items-center justify-center">
                              <BookOpen className="w-5 h-5 text-blue-600" />
                            </div>
                            <div className="flex-1">
                              <h4 className="font-medium">{student.nextSession.subject}</h4>
                              <p className="text-sm text-muted-foreground">{student.nextSession.teacher}</p>
                              <p className="text-xs text-muted-foreground">
                                {student.nextSession.date} à {student.nextSession.time}
                              </p>
                            </div>
                          </div>
                        </div>
                      )}
                      
                      <div className="text-center py-8">
                        <Calendar className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
                        <p className="text-muted-foreground">Aucune autre session programmée</p>
                        <Button variant="outline" size="sm" className="mt-3">
                          <Plus className="w-4 h-4 mr-2" />
                          Planifier une session
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="nexus-card">
                  <CardHeader>
                    <CardTitle>Disponibilités</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Lundi</span>
                        <Badge variant="outline">14h-18h</Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Mercredi</span>
                        <Badge variant="outline">16h-20h</Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Samedi</span>
                        <Badge variant="outline">9h-12h</Badge>
                      </div>
                    </div>
                    <Button variant="outline" size="sm" className="w-full mt-4">
                      <Settings className="w-4 h-4 mr-2" />
                      Modifier disponibilités
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default StudentDashboard;

