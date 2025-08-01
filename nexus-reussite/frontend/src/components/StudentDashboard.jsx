'use client';

import { Award, BookOpen, Clock, MessageCircle, Target, TrendingUp } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import useAuthStore from '../stores/authStore';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';

const StudentDashboard = () => {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [activeTab, setActiveTab] = useState('overview');

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  // Données simulées pour la démo
  const studentStats = {
    coursesCompleted: 12,
    totalCourses: 20,
    averageGrade: 16.5,
    studyTime: 47,
    nextExam: 'Structures de données',
    nextExamDate: '2025-02-15'
  };

  const recentCourses = [
    { id: 1, title: 'Algorithmes de tri', progress: 85, lastAccessed: '2025-01-31' },
    { id: 2, title: 'Bases de données', progress: 60, lastAccessed: '2025-01-30' },
    { id: 3, title: 'Programmation orientée objet', progress: 90, lastAccessed: '2025-01-29' },
    { id: 4, title: 'Réseaux informatiques', progress: 45, lastAccessed: '2025-01-28' }
  ];

  const upcomingTasks = [
    { id: 1, title: 'TP Algorithmes de tri', dueDate: '2025-02-05', type: 'tp' },
    { id: 2, title: 'Quiz Bases de données', dueDate: '2025-02-03', type: 'quiz' },
    { id: 3, title: 'Projet POO', dueDate: '2025-02-10', type: 'project' }
  ];

  const getTaskTypeIcon = (type) => {
    switch (type) {
      case 'tp': return '⚗️';
      case 'quiz': return '❓';
      case 'project': return '🚀';
      default: return '📝';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="w-auto mr-4" style={{ height: '40px' }}>
                <img
                  src="/logo_nexus-reussite.png"
                  alt="Nexus Réussite"
                  className="w-auto object-contain"
                  style={{ height: '40px' }}
                />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">Mon Espace Étudiant</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                Bienvenue, {user?.firstName} {user?.lastName}
              </span>
              <Button variant="outline" onClick={handleLogout}>
                Déconnexion
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Cours Terminés</CardTitle>
              <BookOpen className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{studentStats.coursesCompleted}/{studentStats.totalCourses}</div>
              <p className="text-xs text-muted-foreground">
                {Math.round((studentStats.coursesCompleted / studentStats.totalCourses) * 100)}% complétés
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Moyenne Générale</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{studentStats.averageGrade}/20</div>
              <p className="text-xs text-muted-foreground">
                Excellent travail !
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Temps d'Étude</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{studentStats.studyTime}h</div>
              <p className="text-xs text-muted-foreground">
                Cette semaine
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Prochain Examen</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold">{studentStats.nextExam}</div>
              <p className="text-xs text-muted-foreground">
                {studentStats.nextExamDate}
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cours Récents */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Mes Cours en Cours</CardTitle>
                <CardDescription>
                  Continuez votre apprentissage là où vous vous êtes arrêté
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentCourses.map((course) => (
                  <div key={course.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{course.title}</h3>
                      <p className="text-sm text-gray-500">Dernière activité: {course.lastAccessed}</p>
                      <div className="mt-2">
                        <Progress value={course.progress} className="w-full" />
                        <p className="text-xs text-gray-500 mt-1">{course.progress}% complété</p>
                      </div>
                    </div>
                    <Button variant="outline" size="sm" className="ml-4">
                      Continuer
                    </Button>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Tâches à Venir */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Tâches à Venir</CardTitle>
                <CardDescription>
                  N'oubliez pas vos échéances
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {upcomingTasks.map((task) => (
                  <div key={task.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                    <span className="text-lg">{getTaskTypeIcon(task.type)}</span>
                    <div className="flex-1">
                      <h4 className="font-medium text-sm">{task.title}</h4>
                      <p className="text-xs text-gray-500">Échéance: {task.dueDate}</p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Actions Rapides */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Actions Rapides</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button className="w-full justify-start">
                  <BookOpen className="mr-2 h-4 w-4" />
                  Parcourir les Cours
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Award className="mr-2 h-4 w-4" />
                  Mes Évaluations
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <MessageCircle className="mr-2 h-4 w-4" />
                  Assistant ARIA
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Section Progression */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Ma Progression NSI</CardTitle>
            <CardDescription>
              Votre parcours dans le programme de NSI
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">85%</div>
                <p className="text-sm text-gray-600">Première NSI</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">60%</div>
                <p className="text-sm text-gray-600">Terminale NSI</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">16.5/20</div>
                <p className="text-sm text-gray-600">Moyenne Générale</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default StudentDashboard;
