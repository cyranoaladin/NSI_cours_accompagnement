import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  Target, 
  Award, 
  Calendar,
  Clock,
  BookOpen,
  Brain,
  Zap,
  Star,
  Trophy,
  Medal,
  CheckCircle,
  AlertCircle,
  Info,
  BarChart3,
  PieChart,
  LineChart,
  Activity
} from 'lucide-react';

const ProgressTracking = ({ studentId = "sarah_m" }) => {
  const [progressData, setProgressData] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState('month');
  const [selectedSubject, setSelectedSubject] = useState('all');
  const [loading, setLoading] = useState(true);

  // Données de démonstration
  const demoProgressData = {
    student: {
      id: "sarah_m",
      name: "Sarah Mansouri",
      level: "Terminale",
      avatar: "/api/placeholder/80/80"
    },
    overview: {
      overall_progress: 78.5,
      weekly_improvement: 12.3,
      monthly_improvement: 8.7,
      streak_days: 23,
      total_hours: 156,
      completed_modules: 34,
      total_modules: 45,
      current_level: "Avancé",
      next_milestone: "Excellence"
    },
    subjects: [
      {
        id: "mathematics",
        name: "Mathématiques",
        icon: "📐",
        color: "blue",
        progress: 85.2,
        grade: 16.8,
        trend: "up",
        trend_value: 2.3,
        hours_spent: 45,
        modules_completed: 12,
        total_modules: 15,
        last_activity: "2024-01-25T14:30:00Z",
        strengths: ["Analyse", "Géométrie", "Probabilités"],
        weaknesses: ["Arithmétique"],
        next_topics: ["Intégrales", "Équations différentielles"],
        recent_scores: [14.5, 15.2, 16.1, 16.8, 17.2],
        milestones: [
          { name: "Dérivées maîtrisées", completed: true, date: "2024-01-15" },
          { name: "Intégrales en cours", completed: false, progress: 60 },
          { name: "Bac blanc", completed: false, date: "2024-02-15" }
        ]
      },
      {
        id: "nsi",
        name: "NSI",
        icon: "💻",
        color: "green",
        progress: 92.1,
        grade: 17.5,
        trend: "up",
        trend_value: 1.8,
        hours_spent: 38,
        modules_completed: 11,
        total_modules: 12,
        last_activity: "2024-01-25T16:45:00Z",
        strengths: ["Algorithmes", "Python", "Structures de données"],
        weaknesses: ["Bases de données"],
        next_topics: ["IA et Machine Learning", "Projet final"],
        recent_scores: [16.2, 16.8, 17.1, 17.5, 18.0],
        milestones: [
          { name: "Python maîtrisé", completed: true, date: "2024-01-10" },
          { name: "Projet en cours", completed: false, progress: 75 },
          { name: "Grand Oral NSI", completed: false, date: "2024-03-20" }
        ]
      },
      {
        id: "physics",
        name: "Physique-Chimie",
        icon: "⚛️",
        color: "purple",
        progress: 73.4,
        grade: 15.2,
        trend: "stable",
        trend_value: 0.1,
        hours_spent: 32,
        modules_completed: 8,
        total_modules: 12,
        last_activity: "2024-01-24T10:20:00Z",
        strengths: ["Mécanique", "Optique"],
        weaknesses: ["Chimie organique", "Thermodynamique"],
        next_topics: ["Ondes", "Radioactivité"],
        recent_scores: [14.8, 15.0, 15.1, 15.2, 15.3],
        milestones: [
          { name: "Mécanique validée", completed: true, date: "2024-01-08" },
          { name: "Chimie en cours", completed: false, progress: 45 },
          { name: "TP pratiques", completed: false, date: "2024-02-10" }
        ]
      },
      {
        id: "french",
        name: "Français",
        icon: "📚",
        color: "red",
        progress: 81.7,
        grade: 16.3,
        trend: "up",
        trend_value: 1.2,
        hours_spent: 28,
        modules_completed: 9,
        total_modules: 11,
        last_activity: "2024-01-25T11:15:00Z",
        strengths: ["Dissertation", "Analyse littéraire"],
        weaknesses: ["Expression orale"],
        next_topics: ["Grand Oral", "Révisions Bac"],
        recent_scores: [15.5, 15.8, 16.0, 16.3, 16.5],
        milestones: [
          { name: "Méthode dissertation", completed: true, date: "2024-01-12" },
          { name: "Oral en cours", completed: false, progress: 30 },
          { name: "Bac français", completed: false, date: "2024-06-15" }
        ]
      }
    ],
    weekly_activity: [
      { day: "Lun", hours: 3.5, efficiency: 85 },
      { day: "Mar", hours: 4.2, efficiency: 92 },
      { day: "Mer", hours: 2.8, efficiency: 78 },
      { day: "Jeu", hours: 4.0, efficiency: 88 },
      { day: "Ven", hours: 3.2, efficiency: 82 },
      { day: "Sam", hours: 5.1, efficiency: 95 },
      { day: "Dim", hours: 2.5, efficiency: 75 }
    ],
    achievements: [
      {
        id: "streak_master",
        name: "Maître de la Régularité",
        description: "23 jours consécutifs d'activité",
        icon: "🔥",
        earned_date: "2024-01-25",
        rarity: "rare"
      },
      {
        id: "math_expert",
        name: "Expert Mathématiques",
        description: "85% de progression en maths",
        icon: "🧮",
        earned_date: "2024-01-20",
        rarity: "epic"
      },
      {
        id: "code_ninja",
        name: "Ninja du Code",
        description: "Projet Python parfait",
        icon: "🥷",
        earned_date: "2024-01-18",
        rarity: "legendary"
      },
      {
        id: "fast_learner",
        name: "Apprenant Rapide",
        description: "Module terminé en moins de 2h",
        icon: "⚡",
        earned_date: "2024-01-15",
        rarity: "common"
      }
    ],
    goals: [
      {
        id: "bac_mention_tb",
        name: "Mention Très Bien au Bac",
        description: "Obtenir une moyenne ≥ 16/20",
        target_date: "2024-06-15",
        progress: 78,
        status: "in_progress",
        milestones: [
          { name: "Moyenne 15/20", completed: true },
          { name: "Moyenne 16/20", completed: false, progress: 85 },
          { name: "Préparation intensive", completed: false }
        ]
      },
      {
        id: "prepa_admission",
        name: "Admission en Prépa",
        description: "Intégrer une classe préparatoire scientifique",
        target_date: "2024-07-01",
        progress: 65,
        status: "in_progress",
        milestones: [
          { name: "Dossier constitué", completed: true },
          { name: "Notes excellentes", completed: false, progress: 70 },
          { name: "Entretiens", completed: false }
        ]
      },
      {
        id: "nsi_project",
        name: "Projet NSI d'Excellence",
        description: "Créer un projet innovant pour le Grand Oral",
        target_date: "2024-03-15",
        progress: 75,
        status: "in_progress",
        milestones: [
          { name: "Concept défini", completed: true },
          { name: "Développement", completed: false, progress: 75 },
          { name: "Présentation", completed: false }
        ]
      }
    ],
    aria_insights: {
      learning_style: "Visuel",
      optimal_study_time: "14h-17h",
      recommended_break_frequency: "25 minutes",
      strength_areas: ["Logique", "Analyse", "Résolution de problèmes"],
      improvement_areas: ["Expression orale", "Gestion du stress"],
      next_recommendations: [
        "Augmenter la pratique orale en français",
        "Réviser la thermodynamique en physique",
        "Préparer le Grand Oral NSI"
      ],
      motivation_level: 85,
      confidence_level: 78,
      stress_level: 32
    }
  };

  useEffect(() => {
    // Simulation du chargement des données
    setLoading(true);
    setTimeout(() => {
      setProgressData(demoProgressData);
      setLoading(false);
    }, 1000);
  }, [studentId]);

  const getTrendIcon = (trend, value) => {
    if (trend === 'up') return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (trend === 'down') return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-gray-500" />;
  };

  const getProgressColor = (progress) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 60) return 'bg-blue-500';
    if (progress >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getRarityColor = (rarity) => {
    switch (rarity) {
      case 'legendary': return 'bg-gradient-to-r from-yellow-400 to-orange-500';
      case 'epic': return 'bg-gradient-to-r from-purple-400 to-pink-500';
      case 'rare': return 'bg-gradient-to-r from-blue-400 to-cyan-500';
      default: return 'bg-gradient-to-r from-gray-400 to-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!progressData) {
    return (
      <div className="text-center py-8">
        <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">Aucune donnée de progression disponible</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* En-tête avec profil étudiant */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center text-2xl font-bold">
            {progressData.student.name.split(' ').map(n => n[0]).join('')}
          </div>
          <div className="flex-1">
            <h1 className="text-2xl font-bold">{progressData.student.name}</h1>
            <p className="text-blue-100">{progressData.student.level}</p>
            <div className="flex items-center space-x-4 mt-2">
              <div className="flex items-center space-x-1">
                <Zap className="w-4 h-4" />
                <span className="text-sm">{progressData.overview.streak_days} jours</span>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span className="text-sm">{progressData.overview.total_hours}h étudiées</span>
              </div>
              <div className="flex items-center space-x-1">
                <BookOpen className="w-4 h-4" />
                <span className="text-sm">{progressData.overview.completed_modules}/{progressData.overview.total_modules} modules</span>
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">{progressData.overview.overall_progress}%</div>
            <div className="text-sm text-blue-100">Progression globale</div>
            <Badge className="mt-2 bg-white bg-opacity-20">
              {progressData.overview.current_level}
            </Badge>
          </div>
        </div>
      </div>

      {/* Métriques rapides */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Amélioration hebdo</p>
                <p className="text-2xl font-bold text-green-600">+{progressData.overview.weekly_improvement}%</p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Amélioration mensuelle</p>
                <p className="text-2xl font-bold text-blue-600">+{progressData.overview.monthly_improvement}%</p>
              </div>
              <BarChart3 className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Série actuelle</p>
                <p className="text-2xl font-bold text-orange-600">{progressData.overview.streak_days} jours</p>
              </div>
              <Zap className="w-8 h-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Prochain palier</p>
                <p className="text-lg font-bold text-purple-600">{progressData.overview.next_milestone}</p>
              </div>
              <Target className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="subjects" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="subjects">Matières</TabsTrigger>
          <TabsTrigger value="goals">Objectifs</TabsTrigger>
          <TabsTrigger value="achievements">Réussites</TabsTrigger>
          <TabsTrigger value="activity">Activité</TabsTrigger>
          <TabsTrigger value="insights">Insights IA</TabsTrigger>
        </TabsList>

        <TabsContent value="subjects" className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {progressData.subjects.map((subject) => (
              <Card key={subject.id} className="hover:shadow-lg transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="text-2xl">{subject.icon}</div>
                      <div>
                        <CardTitle className="text-lg">{subject.name}</CardTitle>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="text-sm text-gray-600">Note: {subject.grade}/20</span>
                          {getTrendIcon(subject.trend, subject.trend_value)}
                          <span className={`text-sm ${subject.trend === 'up' ? 'text-green-600' : subject.trend === 'down' ? 'text-red-600' : 'text-gray-600'}`}>
                            {subject.trend === 'up' ? '+' : subject.trend === 'down' ? '-' : ''}{subject.trend_value}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">{subject.progress}%</div>
                      <div className="text-xs text-gray-500">{subject.modules_completed}/{subject.total_modules} modules</div>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  {/* Barre de progression */}
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progression</span>
                      <span>{subject.progress}%</span>
                    </div>
                    <Progress value={subject.progress} className="h-2" />
                  </div>

                  {/* Points forts et faibles */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-green-700 mb-2">Points forts</h4>
                      <div className="space-y-1">
                        {subject.strengths.map((strength, index) => (
                          <Badge key={index} variant="outline" className="text-xs bg-green-50 text-green-700 border-green-200">
                            {strength}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-red-700 mb-2">À améliorer</h4>
                      <div className="space-y-1">
                        {subject.weaknesses.map((weakness, index) => (
                          <Badge key={index} variant="outline" className="text-xs bg-red-50 text-red-700 border-red-200">
                            {weakness}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Prochains sujets */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Prochains sujets</h4>
                    <div className="flex flex-wrap gap-1">
                      {subject.next_topics.map((topic, index) => (
                        <Badge key={index} className="text-xs bg-blue-100 text-blue-800">
                          {topic}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Jalons */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Jalons</h4>
                    <div className="space-y-2">
                      {subject.milestones.map((milestone, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          {milestone.completed ? (
                            <CheckCircle className="w-4 h-4 text-green-500" />
                          ) : (
                            <div className="w-4 h-4 border-2 border-gray-300 rounded-full"></div>
                          )}
                          <span className={`text-sm ${milestone.completed ? 'text-green-700' : 'text-gray-600'}`}>
                            {milestone.name}
                          </span>
                          {milestone.progress && !milestone.completed && (
                            <div className="flex-1 ml-2">
                              <Progress value={milestone.progress} className="h-1" />
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Statistiques */}
                  <div className="grid grid-cols-2 gap-4 pt-2 border-t">
                    <div className="text-center">
                      <div className="text-lg font-bold text-blue-600">{subject.hours_spent}h</div>
                      <div className="text-xs text-gray-500">Temps passé</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-green-600">{subject.recent_scores[subject.recent_scores.length - 1]}/20</div>
                      <div className="text-xs text-gray-500">Dernière note</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="goals" className="mt-6">
          <div className="space-y-6">
            {progressData.goals.map((goal) => (
              <Card key={goal.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="flex items-center space-x-2">
                        <Target className="w-5 h-5 text-blue-600" />
                        <span>{goal.name}</span>
                      </CardTitle>
                      <p className="text-gray-600 mt-1">{goal.description}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">{goal.progress}%</div>
                      <Badge className={`mt-1 ${goal.status === 'in_progress' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
                        {goal.status === 'in_progress' ? 'En cours' : 'Terminé'}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>

                <CardContent>
                  <div className="space-y-4">
                    {/* Barre de progression globale */}
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span>Progression globale</span>
                        <span>{goal.progress}%</span>
                      </div>
                      <Progress value={goal.progress} className="h-3" />
                    </div>

                    {/* Date cible */}
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <Calendar className="w-4 h-4" />
                      <span>Objectif: {new Date(goal.target_date).toLocaleDateString('fr-FR')}</span>
                    </div>

                    {/* Jalons détaillés */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-3">Étapes</h4>
                      <div className="space-y-3">
                        {goal.milestones.map((milestone, index) => (
                          <div key={index} className="flex items-center space-x-3">
                            {milestone.completed ? (
                              <CheckCircle className="w-5 h-5 text-green-500" />
                            ) : (
                              <div className="w-5 h-5 border-2 border-gray-300 rounded-full"></div>
                            )}
                            <div className="flex-1">
                              <div className={`text-sm ${milestone.completed ? 'text-green-700 font-medium' : 'text-gray-700'}`}>
                                {milestone.name}
                              </div>
                              {milestone.progress && !milestone.completed && (
                                <div className="mt-1">
                                  <Progress value={milestone.progress} className="h-1" />
                                </div>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="achievements" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {progressData.achievements.map((achievement) => (
              <Card key={achievement.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className={`w-16 h-16 rounded-full ${getRarityColor(achievement.rarity)} flex items-center justify-center text-2xl mb-4 mx-auto`}>
                    {achievement.icon}
                  </div>
                  <div className="text-center">
                    <h3 className="font-bold text-lg mb-2">{achievement.name}</h3>
                    <p className="text-gray-600 text-sm mb-3">{achievement.description}</p>
                    <Badge className={`${getRarityColor(achievement.rarity)} text-white`}>
                      {achievement.rarity === 'legendary' ? 'Légendaire' :
                       achievement.rarity === 'epic' ? 'Épique' :
                       achievement.rarity === 'rare' ? 'Rare' : 'Commun'}
                    </Badge>
                    <div className="text-xs text-gray-500 mt-2">
                      Obtenu le {new Date(achievement.earned_date).toLocaleDateString('fr-FR')}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Statistiques des réussites */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Trophy className="w-5 h-5 text-yellow-600" />
                <span>Statistiques des réussites</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">1</div>
                  <div className="text-sm text-gray-600">Légendaire</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">1</div>
                  <div className="text-sm text-gray-600">Épique</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">1</div>
                  <div className="text-sm text-gray-600">Rare</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-600">1</div>
                  <div className="text-sm text-gray-600">Commun</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="activity" className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Activité hebdomadaire */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="w-5 h-5 text-blue-600" />
                  <span>Activité hebdomadaire</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {progressData.weekly_activity.map((day, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <div className="w-12 text-sm font-medium">{day.day}</div>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2">
                          <div className="flex-1 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full" 
                              style={{ width: `${(day.hours / 6) * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-600">{day.hours}h</span>
                        </div>
                      </div>
                      <div className="w-16 text-right">
                        <Badge className={`text-xs ${day.efficiency >= 90 ? 'bg-green-100 text-green-800' : day.efficiency >= 80 ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'}`}>
                          {day.efficiency}%
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Répartition du temps */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <PieChart className="w-5 h-5 text-green-600" />
                  <span>Répartition du temps</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {progressData.subjects.map((subject, index) => {
                    const totalHours = progressData.subjects.reduce((sum, s) => sum + s.hours_spent, 0);
                    const percentage = (subject.hours_spent / totalHours) * 100;
                    return (
                      <div key={index} className="flex items-center space-x-3">
                        <div className="text-lg">{subject.icon}</div>
                        <div className="flex-1">
                          <div className="flex justify-between text-sm mb-1">
                            <span>{subject.name}</span>
                            <span>{subject.hours_spent}h ({percentage.toFixed(1)}%)</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${getProgressColor(percentage)}`}
                              style={{ width: `${percentage}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="insights" className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Profil d'apprentissage */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="w-5 h-5 text-purple-600" />
                  <span>Profil d'apprentissage ARIA</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Style d'apprentissage</span>
                    <Badge className="bg-purple-100 text-purple-800">
                      {progressData.aria_insights.learning_style}
                    </Badge>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Horaire optimal</span>
                    <span className="font-medium">{progressData.aria_insights.optimal_study_time}</span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Fréquence de pause</span>
                    <span className="font-medium">{progressData.aria_insights.recommended_break_frequency}</span>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Points forts</h4>
                  <div className="flex flex-wrap gap-1">
                    {progressData.aria_insights.strength_areas.map((strength, index) => (
                      <Badge key={index} className="text-xs bg-green-100 text-green-800">
                        {strength}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Axes d'amélioration</h4>
                  <div className="flex flex-wrap gap-1">
                    {progressData.aria_insights.improvement_areas.map((area, index) => (
                      <Badge key={index} className="text-xs bg-orange-100 text-orange-800">
                        {area}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Métriques psychologiques */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="w-5 h-5 text-blue-600" />
                  <span>État psychologique</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>Motivation</span>
                    <span>{progressData.aria_insights.motivation_level}%</span>
                  </div>
                  <Progress value={progressData.aria_insights.motivation_level} className="h-2" />
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>Confiance</span>
                    <span>{progressData.aria_insights.confidence_level}%</span>
                  </div>
                  <Progress value={progressData.aria_insights.confidence_level} className="h-2" />
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>Niveau de stress</span>
                    <span>{progressData.aria_insights.stress_level}%</span>
                  </div>
                  <Progress 
                    value={progressData.aria_insights.stress_level} 
                    className="h-2"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Recommandations ARIA */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="w-5 h-5 text-yellow-600" />
                  <span>Recommandations personnalisées</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {progressData.aria_insights.next_recommendations.map((recommendation, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                      <Info className="w-5 h-5 text-blue-600 mt-0.5" />
                      <div className="flex-1">
                        <p className="text-sm text-blue-900">{recommendation}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProgressTracking;

