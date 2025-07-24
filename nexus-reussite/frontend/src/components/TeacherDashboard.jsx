import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Calendar, 
  BookOpen, 
  TrendingUp, 
  Clock, 
  MessageSquare,
  Video,
  FileText,
  Award,
  AlertCircle
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import apiService from '../services/api';

export default function TeacherDashboard() {
  const [stats, setStats] = useState({
    totalStudents: 0,
    activeClasses: 0,
    completedLessons: 0,
    averageProgress: 0
  });
  const [recentActivities, setRecentActivities] = useState([]);
  const [upcomingClasses, setUpcomingClasses] = useState([]);
  const [studentProgress, setStudentProgress] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Charger les données du tableau de bord
      const [statsResponse, activitiesResponse, classesResponse, progressResponse] = await Promise.all([
        apiService.getDashboardStats('teacher', 'current_teacher_id'),
        apiService.getTeacherActivities(),
        apiService.getUpcomingClasses(),
        apiService.getStudentsProgress()
      ]);

      if (statsResponse.success) {
        setStats(statsResponse.stats);
      }

      // Données de démonstration si les API ne sont pas encore implémentées
      setRecentActivities([
        {
          id: 1,
          type: 'lesson_completed',
          student: 'Sarah Dubois',
          subject: 'Mathématiques',
          description: 'A terminé le chapitre sur les probabilités',
          time: '2024-01-15T10:30:00Z',
          score: 85
        },
        {
          id: 2,
          type: 'question_asked',
          student: 'Ahmed Ben Ali',
          subject: 'NSI',
          description: 'A posé une question sur les algorithmes de tri',
          time: '2024-01-15T09:15:00Z'
        },
        {
          id: 3,
          type: 'assignment_submitted',
          student: 'Léa Martin',
          subject: 'Physique',
          description: 'A rendu le devoir sur l\'optique',
          time: '2024-01-15T08:45:00Z',
          score: 92
        }
      ]);

      setUpcomingClasses([
        {
          id: 1,
          subject: 'Mathématiques Terminale',
          time: '2024-01-15T14:00:00Z',
          duration: 60,
          students: 8,
          type: 'group',
          room: 'Salle A1'
        },
        {
          id: 2,
          subject: 'NSI Première',
          time: '2024-01-15T16:00:00Z',
          duration: 90,
          students: 6,
          type: 'group',
          room: 'Lab Info'
        },
        {
          id: 3,
          subject: 'Cours particulier - Ahmed',
          time: '2024-01-16T10:00:00Z',
          duration: 60,
          students: 1,
          type: 'individual',
          room: 'Visio'
        }
      ]);

      setStudentProgress([
        {
          id: 1,
          name: 'Sarah Dubois',
          subject: 'Mathématiques',
          progress: 85,
          lastActivity: '2024-01-15T10:30:00Z',
          trend: 'up',
          grade: 16.5
        },
        {
          id: 2,
          name: 'Ahmed Ben Ali',
          subject: 'NSI',
          progress: 72,
          lastActivity: '2024-01-15T09:15:00Z',
          trend: 'up',
          grade: 14.2
        },
        {
          id: 3,
          name: 'Léa Martin',
          subject: 'Physique',
          progress: 90,
          lastActivity: '2024-01-15T08:45:00Z',
          trend: 'stable',
          grade: 17.8
        },
        {
          id: 4,
          name: 'Youssef Trabelsi',
          subject: 'Mathématiques',
          progress: 65,
          lastActivity: '2024-01-14T16:20:00Z',
          trend: 'down',
          grade: 12.3
        }
      ]);

      // Calculer les statistiques
      setStats({
        totalStudents: 24,
        activeClasses: 6,
        completedLessons: 18,
        averageProgress: 78
      });

    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short'
    });
  };

  const getActivityIcon = (type) => {
    switch (type) {
      case 'lesson_completed':
        return <BookOpen className="h-4 w-4" />;
      case 'question_asked':
        return <MessageSquare className="h-4 w-4" />;
      case 'assignment_submitted':
        return <FileText className="h-4 w-4" />;
      default:
        return <AlertCircle className="h-4 w-4" />;
    }
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'down':
        return <TrendingUp className="h-4 w-4 text-red-500 transform rotate-180" />;
      default:
        return <div className="h-4 w-4 bg-gray-300 rounded-full" />;
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tableau de bord Enseignant</h1>
          <p className="text-gray-600">Gérez vos cours et suivez la progression de vos élèves</p>
        </div>
        <div className="flex space-x-3">
          <Button>
            <Video className="h-4 w-4 mr-2" />
            Créer une session
          </Button>
          <Button variant="outline">
            <FileText className="h-4 w-4 mr-2" />
            Nouveau contenu
          </Button>
        </div>
      </div>

      {/* Statistiques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Élèves</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalStudents}</p>
              </div>
              <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Users className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Classes Actives</p>
                <p className="text-3xl font-bold text-gray-900">{stats.activeClasses}</p>
              </div>
              <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Calendar className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Cours Terminés</p>
                <p className="text-3xl font-bold text-gray-900">{stats.completedLessons}</p>
              </div>
              <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <BookOpen className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Progression Moyenne</p>
                <p className="text-3xl font-bold text-gray-900">{stats.averageProgress}%</p>
              </div>
              <div className="h-12 w-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="h-6 w-6 text-orange-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Contenu principal */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cours à venir */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Cours à venir
            </CardTitle>
            <CardDescription>
              Vos prochaines sessions d'enseignement
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {upcomingClasses.map((class_) => (
                <div key={class_.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      {class_.type === 'individual' ? (
                        <Users className="h-5 w-5 text-blue-600" />
                      ) : (
                        <BookOpen className="h-5 w-5 text-blue-600" />
                      )}
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{class_.subject}</h4>
                      <div className="flex items-center space-x-2 text-sm text-gray-500">
                        <Clock className="h-4 w-4" />
                        <span>{formatDate(class_.time)} à {formatTime(class_.time)}</span>
                        <span>•</span>
                        <span>{class_.duration} min</span>
                        <span>•</span>
                        <span>{class_.students} élève{class_.students > 1 ? 's' : ''}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant={class_.type === 'individual' ? 'default' : 'secondary'}>
                      {class_.type === 'individual' ? 'Individuel' : 'Groupe'}
                    </Badge>
                    <Button size="sm" variant="outline">
                      <Video className="h-4 w-4 mr-1" />
                      Rejoindre
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Activités récentes */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Clock className="h-5 w-5 mr-2" />
              Activités récentes
            </CardTitle>
            <CardDescription>
              Dernières actions de vos élèves
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3">
                  <div className="h-8 w-8 bg-gray-100 rounded-full flex items-center justify-center">
                    {getActivityIcon(activity.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{activity.student}</p>
                    <p className="text-sm text-gray-500">{activity.description}</p>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-xs text-gray-400">{formatTime(activity.time)}</span>
                      {activity.score && (
                        <>
                          <span className="text-xs text-gray-400">•</span>
                          <Badge variant="outline" className="text-xs">
                            {activity.score}/100
                          </Badge>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Progression des élèves */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <TrendingUp className="h-5 w-5 mr-2" />
            Progression des élèves
          </CardTitle>
          <CardDescription>
            Suivi détaillé de la progression de chaque élève
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {studentProgress.map((student) => (
              <div key={student.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className="h-10 w-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-medium">
                    {student.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">{student.name}</h4>
                    <p className="text-sm text-gray-500">{student.subject}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-6">
                  <div className="text-center">
                    <p className="text-sm font-medium text-gray-900">{student.progress}%</p>
                    <Progress value={student.progress} className="w-20 mt-1" />
                  </div>
                  
                  <div className="text-center">
                    <p className="text-sm font-medium text-gray-900">{student.grade}/20</p>
                    <p className="text-xs text-gray-500">Moyenne</p>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {getTrendIcon(student.trend)}
                    <span className="text-xs text-gray-500">
                      {formatDate(student.lastActivity)}
                    </span>
                  </div>
                  
                  <Button size="sm" variant="outline">
                    <MessageSquare className="h-4 w-4 mr-1" />
                    Contacter
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Actions rapides */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="cursor-pointer hover:shadow-lg transition-shadow">
          <CardContent className="p-6 text-center">
            <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Video className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="font-medium text-gray-900 mb-2">Créer une session</h3>
            <p className="text-sm text-gray-500">Démarrer un cours en visioconférence</p>
          </CardContent>
        </Card>

        <Card className="cursor-pointer hover:shadow-lg transition-shadow">
          <CardContent className="p-6 text-center">
            <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <FileText className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="font-medium text-gray-900 mb-2">Créer du contenu</h3>
            <p className="text-sm text-gray-500">Générer des exercices et supports</p>
          </CardContent>
        </Card>

        <Card className="cursor-pointer hover:shadow-lg transition-shadow">
          <CardContent className="p-6 text-center">
            <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Award className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="font-medium text-gray-900 mb-2">Évaluer les élèves</h3>
            <p className="text-sm text-gray-500">Créer et corriger des évaluations</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

