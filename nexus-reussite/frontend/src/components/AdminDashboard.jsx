import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Users, 
  BookOpen, 
  TrendingUp, 
  DollarSign,
  Calendar,
  Star,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Eye,
  Edit,
  Trash2,
  Plus,
  Download,
  Upload,
  Filter,
  Search,
  MoreHorizontal,
  Settings,
  Bell,
  Mail,
  Phone,
  MapPin,
  Award,
  Target,
  Activity,
  BarChart3,
  PieChart,
  LineChart,
  Users2,
  GraduationCap,
  Brain,
  Zap,
  Shield,
  Database,
  Server,
  Wifi,
  HardDrive,
  Cpu,
  Network,
  Globe,
  Lock,
  Key,
  UserCheck,
  UserX,
  UserPlus,
  FileText,
  Image,
  Video,
  Headphones,
  Mic,
  Camera,
  Monitor,
  Smartphone,
  Tablet,
  Laptop,
  MonitorSpeaker,
  Printer,
  ScanLine,
  Keyboard,
  Mouse,
  Gamepad2,
  Joystick,
  Headphones as HeadsetIcon,
  Speaker,
  Volume2,
  VolumeX,
  Play,
  Pause,
  Square,
  SkipBack,
  SkipForward,
  Repeat,
  Shuffle,
  Radio,
  Tv,
  Film,
  Music,
  Disc,
  Disc as CassetteIcon,
  Disc as VinylIcon,
  Mic as MicVocalIcon,
  Piano,
  Guitar,
  Drum,
  Volume2 as TrumpetIcon,
  Music as ViolinIcon,
  Music as SaxophoneIcon,
  Music as FluteIcon,
  Music as HarpIcon,
  Guitar as BanjoIcon,
  Piano as AccordionIcon,
  Music as HarmonicaIcon,
  Piano as XylophoneIcon,
  Circle as MaracasIcon,
  Triangle,
  Bell as BellIcon,
  Volume2 as WhistleIcon,
  Megaphone,
  Volume2 as BullhornIcon,
  AlertTriangle as SirenIcon,
  AlarmClock,
  Timer,
  Clock,
  Hourglass,
  Watch,
  Clock3,
  Clock9,
  Clock12,
  ArrowDown as ClockArrowDownIcon,
  ArrowUp as ClockArrowUpIcon
} from 'lucide-react';

const AdminDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState('month');
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  // Données de démonstration pour l'administration
  const demoDashboardData = {
    overview: {
      total_students: 1247,
      active_students: 892,
      total_teachers: 23,
      active_teachers: 19,
      total_courses: 3456,
      completed_courses: 2789,
      revenue_month: 45680,
      revenue_growth: 12.5,
      satisfaction_rate: 4.8,
      retention_rate: 89.3,
      new_registrations_week: 34,
      churn_rate: 2.1
    },
    students: {
      by_level: [
        { level: "Première", count: 523, percentage: 41.9 },
        { level: "Terminale", count: 724, percentage: 58.1 }
      ],
      by_subject: [
        { subject: "Mathématiques", count: 892, color: "blue" },
        { subject: "NSI", count: 456, color: "green" },
        { subject: "Physique-Chimie", count: 678, color: "purple" },
        { subject: "Français", count: 534, color: "red" },
        { subject: "Philosophie", count: 289, color: "yellow" }
      ],
      performance: {
        excellent: 234, // >16/20
        good: 567, // 14-16/20
        average: 389, // 12-14/20
        needs_improvement: 57 // <12/20
      },
      engagement: {
        highly_active: 445, // >20h/mois
        active: 623, // 10-20h/mois
        moderately_active: 156, // 5-10h/mois
        inactive: 23 // <5h/mois
      }
    },
    teachers: {
      list: [
        {
          id: "amina_benali",
          name: "Dr. Amina Benali",
          subject: "Mathématiques",
          students: 89,
          rating: 4.9,
          hours_month: 156,
          status: "active",
          last_login: "2024-01-25T14:30:00Z"
        },
        {
          id: "karim_trabelsi",
          name: "M. Karim Trabelsi",
          subject: "NSI",
          students: 67,
          rating: 4.8,
          hours_month: 134,
          status: "active",
          last_login: "2024-01-25T16:45:00Z"
        },
        {
          id: "fatma_mansouri",
          name: "Dr. Fatma Mansouri",
          subject: "Physique-Chimie",
          students: 78,
          rating: 4.9,
          hours_month: 142,
          status: "active",
          last_login: "2024-01-25T11:20:00Z"
        }
      ],
      performance: {
        top_rated: 8, // >4.7/5
        well_rated: 12, // 4.0-4.7/5
        average_rated: 3, // 3.5-4.0/5
        needs_improvement: 0 // <3.5/5
      }
    },
    courses: {
      by_type: [
        { type: "Individuel", count: 1456, revenue: 28900 },
        { type: "Mini-groupe", count: 1234, revenue: 12340 },
        { type: "Stage intensif", count: 456, revenue: 3650 },
        { type: "Coaching spécialisé", count: 310, revenue: 4960 }
      ],
      completion_rate: 87.3,
      average_duration: 2.4, // heures
      satisfaction: 4.7
    },
    aria: {
      total_interactions: 45678,
      daily_interactions: 1234,
      documents_generated: 8901,
      success_rate: 94.2,
      average_response_time: 1.8, // secondes
      user_satisfaction: 4.6,
      top_queries: [
        { query: "Aide en mathématiques", count: 2345 },
        { query: "Exercices NSI", count: 1876 },
        { query: "Préparation bac", count: 1654 },
        { query: "Grand Oral", count: 1432 },
        { query: "Orientation", count: 1234 }
      ]
    },
    system: {
      server_status: "healthy",
      uptime: 99.8,
      response_time: 245, // ms
      database_size: 2.4, // GB
      storage_used: 67.3, // %
      bandwidth_used: 45.2, // %
      active_sessions: 234,
      errors_24h: 3,
      warnings_24h: 12
    },
    recent_activities: [
      {
        id: 1,
        type: "student_registration",
        message: "Nouvel élève inscrit: Ahmed Khelifi",
        timestamp: "2024-01-25T16:30:00Z",
        user: "Système"
      },
      {
        id: 2,
        type: "course_completion",
        message: "Sarah M. a terminé le module Intégrales",
        timestamp: "2024-01-25T15:45:00Z",
        user: "Sarah Mansouri"
      },
      {
        id: 3,
        type: "teacher_login",
        message: "Dr. Benali s'est connectée",
        timestamp: "2024-01-25T14:30:00Z",
        user: "Dr. Amina Benali"
      },
      {
        id: 4,
        type: "payment_received",
        message: "Paiement reçu: 200 DT - Léa Dubois",
        timestamp: "2024-01-25T13:20:00Z",
        user: "Système"
      },
      {
        id: 5,
        type: "aria_interaction",
        message: "ARIA a généré 15 documents personnalisés",
        timestamp: "2024-01-25T12:15:00Z",
        user: "ARIA"
      }
    ],
    alerts: [
      {
        id: 1,
        type: "warning",
        title: "Serveur de sauvegarde",
        message: "Espace de stockage à 85%",
        timestamp: "2024-01-25T10:30:00Z",
        resolved: false
      },
      {
        id: 2,
        type: "info",
        title: "Mise à jour système",
        message: "Mise à jour programmée pour ce soir",
        timestamp: "2024-01-25T09:15:00Z",
        resolved: false
      },
      {
        id: 3,
        type: "success",
        title: "Sauvegarde complétée",
        message: "Sauvegarde quotidienne terminée avec succès",
        timestamp: "2024-01-25T02:00:00Z",
        resolved: true
      }
    ]
  };

  useEffect(() => {
    // Simulation du chargement des données
    setLoading(true);
    setTimeout(() => {
      setDashboardData(demoDashboardData);
      setLoading(false);
    }, 1000);
  }, [selectedPeriod]);

  const getActivityIcon = (type) => {
    switch (type) {
      case 'student_registration': return <UserPlus className="w-4 h-4 text-green-500" />;
      case 'course_completion': return <CheckCircle className="w-4 h-4 text-blue-500" />;
      case 'teacher_login': return <UserCheck className="w-4 h-4 text-purple-500" />;
      case 'payment_received': return <DollarSign className="w-4 h-4 text-green-500" />;
      case 'aria_interaction': return <Brain className="w-4 h-4 text-orange-500" />;
      default: return <Activity className="w-4 h-4 text-gray-500" />;
    }
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'error': return <XCircle className="w-5 h-5 text-red-500" />;
      case 'warning': return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 'success': return <CheckCircle className="w-5 h-5 text-green-500" />;
      default: return <Bell className="w-5 h-5 text-blue-500" />;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="text-center py-8">
        <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">Erreur lors du chargement des données</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* En-tête */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tableau de Bord Admin</h1>
          <p className="text-gray-600">Nexus Réussite - Gestion de la plateforme</p>
        </div>
        <div className="flex items-center space-x-4">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="week">Cette semaine</option>
            <option value="month">Ce mois</option>
            <option value="quarter">Ce trimestre</option>
            <option value="year">Cette année</option>
          </select>
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Download className="w-4 h-4 mr-2" />
            Exporter
          </Button>
        </div>
      </div>

      {/* Métriques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Élèves actifs</p>
                <p className="text-3xl font-bold text-blue-600">{dashboardData.overview.active_students}</p>
                <p className="text-xs text-gray-500">sur {dashboardData.overview.total_students} inscrits</p>
              </div>
              <Users className="w-12 h-12 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Enseignants actifs</p>
                <p className="text-3xl font-bold text-green-600">{dashboardData.overview.active_teachers}</p>
                <p className="text-xs text-gray-500">sur {dashboardData.overview.total_teachers} total</p>
              </div>
              <GraduationCap className="w-12 h-12 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Revenus du mois</p>
                <p className="text-3xl font-bold text-purple-600">{dashboardData.overview.revenue_month.toLocaleString()} DT</p>
                <p className="text-xs text-green-600">+{dashboardData.overview.revenue_growth}%</p>
              </div>
              <DollarSign className="w-12 h-12 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Satisfaction</p>
                <p className="text-3xl font-bold text-yellow-600">{dashboardData.overview.satisfaction_rate}/5</p>
                <p className="text-xs text-gray-500">Taux de rétention: {dashboardData.overview.retention_rate}%</p>
              </div>
              <Star className="w-12 h-12 text-yellow-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Alertes système */}
      {dashboardData.alerts.filter(alert => !alert.resolved).length > 0 && (
        <Card className="border-l-4 border-l-yellow-500">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Bell className="w-5 h-5 text-yellow-600" />
              <span>Alertes système</span>
              <Badge className="bg-yellow-100 text-yellow-800">
                {dashboardData.alerts.filter(alert => !alert.resolved).length}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {dashboardData.alerts.filter(alert => !alert.resolved).map((alert) => (
                <div key={alert.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                  {getAlertIcon(alert.type)}
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium">{alert.title}</h4>
                      <span className="text-xs text-gray-500">
                        {new Date(alert.timestamp).toLocaleTimeString('fr-FR')}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
                  </div>
                  <Button size="sm" variant="outline">
                    Résoudre
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="students">Élèves</TabsTrigger>
          <TabsTrigger value="teachers">Enseignants</TabsTrigger>
          <TabsTrigger value="courses">Cours</TabsTrigger>
          <TabsTrigger value="aria">ARIA IA</TabsTrigger>
          <TabsTrigger value="system">Système</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Répartition des élèves par niveau */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <PieChart className="w-5 h-5 text-blue-600" />
                  <span>Répartition par niveau</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {dashboardData.students.by_level.map((level, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <div className="flex-1">
                        <div className="flex justify-between text-sm mb-1">
                          <span>{level.level}</span>
                          <span>{level.count} élèves ({level.percentage}%)</span>
                        </div>
                        <Progress value={level.percentage} className="h-2" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Performance des élèves */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="w-5 h-5 text-green-600" />
                  <span>Performance des élèves</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">{dashboardData.students.performance.excellent}</div>
                    <div className="text-sm text-green-700">Excellent (&gt;16/20)</div>
                  </div>
                  <div className="text-center p-3 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{dashboardData.students.performance.good}</div>
                    <div className="text-sm text-blue-700">Bien (14-16/20)</div>
                  </div>
                  <div className="text-center p-3 bg-yellow-50 rounded-lg">
                    <div className="text-2xl font-bold text-yellow-600">{dashboardData.students.performance.average}</div>
                    <div className="text-sm text-yellow-700">Moyen (12-14/20)</div>
                  </div>
                  <div className="text-center p-3 bg-red-50 rounded-lg">
                    <div className="text-2xl font-bold text-red-600">{dashboardData.students.performance.needs_improvement}</div>
                    <div className="text-sm text-red-700">À améliorer (&lt;12/20)</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Activités récentes */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="w-5 h-5 text-purple-600" />
                  <span>Activités récentes</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {dashboardData.recent_activities.map((activity) => (
                    <div key={activity.id} className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg">
                      {getActivityIcon(activity.type)}
                      <div className="flex-1">
                        <p className="text-sm">{activity.message}</p>
                        <p className="text-xs text-gray-500">
                          {new Date(activity.timestamp).toLocaleString('fr-FR')} - {activity.user}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="students" className="mt-6">
          <div className="space-y-6">
            {/* Filtres et actions */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Rechercher un élève..."
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <Button variant="outline">
                  <Filter className="w-4 h-4 mr-2" />
                  Filtres
                </Button>
              </div>
              <Button className="bg-green-600 hover:bg-green-700">
                <Plus className="w-4 h-4 mr-2" />
                Nouvel élève
              </Button>
            </div>

            {/* Statistiques des élèves */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{dashboardData.students.engagement.highly_active}</div>
                    <div className="text-sm text-gray-600">Très actifs</div>
                    <div className="text-xs text-gray-500">&gt;20h/mois</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{dashboardData.students.engagement.active}</div>
                    <div className="text-sm text-gray-600">Actifs</div>
                    <div className="text-xs text-gray-500">10-20h/mois</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600">{dashboardData.students.engagement.moderately_active}</div>
                    <div className="text-sm text-gray-600">Modérément actifs</div>
                    <div className="text-xs text-gray-500">5-10h/mois</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">{dashboardData.students.engagement.inactive}</div>
                    <div className="text-sm text-gray-600">Inactifs</div>
                    <div className="text-xs text-gray-500">&lt;5h/mois</div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Répartition par matière */}
            <Card>
              <CardHeader>
                <CardTitle>Répartition par matière</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {dashboardData.students.by_subject.map((subject, index) => {
                    const percentage = (subject.count / dashboardData.overview.total_students) * 100;
                    return (
                      <div key={index} className="flex items-center space-x-3">
                        <div className="flex-1">
                          <div className="flex justify-between text-sm mb-1">
                            <span>{subject.subject}</span>
                            <span>{subject.count} élèves ({percentage.toFixed(1)}%)</span>
                          </div>
                          <Progress value={percentage} className="h-2" />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="teachers" className="mt-6">
          <div className="space-y-6">
            {/* Actions enseignants */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Rechercher un enseignant..."
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <Button variant="outline">
                  <Filter className="w-4 h-4 mr-2" />
                  Filtres
                </Button>
              </div>
              <Button className="bg-green-600 hover:bg-green-700">
                <Plus className="w-4 h-4 mr-2" />
                Nouvel enseignant
              </Button>
            </div>

            {/* Performance des enseignants */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{dashboardData.teachers.performance.top_rated}</div>
                    <div className="text-sm text-gray-600">Excellents</div>
                    <div className="text-xs text-gray-500">&gt;4.7/5</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{dashboardData.teachers.performance.well_rated}</div>
                    <div className="text-sm text-gray-600">Très bons</div>
                    <div className="text-xs text-gray-500">4.0-4.7/5</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600">{dashboardData.teachers.performance.average_rated}</div>
                    <div className="text-sm text-gray-600">Corrects</div>
                    <div className="text-xs text-gray-500">3.5-4.0/5</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">{dashboardData.teachers.performance.needs_improvement}</div>
                    <div className="text-sm text-gray-600">À améliorer</div>
                    <div className="text-xs text-gray-500">&lt;3.5/5</div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Liste des enseignants */}
            <Card>
              <CardHeader>
                <CardTitle>Enseignants actifs</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {dashboardData.teachers.list.map((teacher) => (
                    <div key={teacher.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                          {teacher.name.split(' ').map(n => n[0]).join('')}
                        </div>
                        <div>
                          <h3 className="font-semibold">{teacher.name}</h3>
                          <p className="text-sm text-gray-600">{teacher.subject}</p>
                          <div className="flex items-center space-x-4 mt-1">
                            <span className="text-xs text-gray-500">{teacher.students} élèves</span>
                            <div className="flex items-center space-x-1">
                              <Star className="w-3 h-3 text-yellow-500" />
                              <span className="text-xs">{teacher.rating}</span>
                            </div>
                            <span className="text-xs text-gray-500">{teacher.hours_month}h/mois</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={`${teacher.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                          {teacher.status === 'active' ? 'Actif' : 'Inactif'}
                        </Badge>
                        <Button size="sm" variant="outline">
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <MoreHorizontal className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="courses" className="mt-6">
          <div className="space-y-6">
            {/* Métriques des cours */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{dashboardData.overview.completed_courses}</div>
                    <div className="text-sm text-gray-600">Cours terminés</div>
                    <div className="text-xs text-gray-500">sur {dashboardData.overview.total_courses} total</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{dashboardData.courses.completion_rate}%</div>
                    <div className="text-sm text-gray-600">Taux de completion</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{dashboardData.courses.average_duration}h</div>
                    <div className="text-sm text-gray-600">Durée moyenne</div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Répartition par type de cours */}
            <Card>
              <CardHeader>
                <CardTitle>Répartition par type de cours</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {dashboardData.courses.by_type.map((type, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                      <div>
                        <h3 className="font-semibold">{type.type}</h3>
                        <p className="text-sm text-gray-600">{type.count} cours</p>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-bold text-green-600">{type.revenue.toLocaleString()} DT</div>
                        <div className="text-sm text-gray-500">Revenus</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="aria" className="mt-6">
          <div className="space-y-6">
            {/* Métriques ARIA */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{dashboardData.aria.total_interactions.toLocaleString()}</div>
                    <div className="text-sm text-gray-600">Interactions totales</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{dashboardData.aria.daily_interactions.toLocaleString()}</div>
                    <div className="text-sm text-gray-600">Interactions/jour</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{dashboardData.aria.documents_generated.toLocaleString()}</div>
                    <div className="text-sm text-gray-600">Documents générés</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600">{dashboardData.aria.success_rate}%</div>
                    <div className="text-sm text-gray-600">Taux de succès</div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Performance ARIA */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Zap className="w-5 h-5 text-orange-600" />
                    <span>Performance ARIA</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Temps de réponse moyen</span>
                      <span>{dashboardData.aria.average_response_time}s</span>
                    </div>
                    <Progress value={(3 - dashboardData.aria.average_response_time) / 3 * 100} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Satisfaction utilisateur</span>
                      <span>{dashboardData.aria.user_satisfaction}/5</span>
                    </div>
                    <Progress value={dashboardData.aria.user_satisfaction * 20} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Taux de succès</span>
                      <span>{dashboardData.aria.success_rate}%</span>
                    </div>
                    <Progress value={dashboardData.aria.success_rate} className="h-2" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Search className="w-5 h-5 text-blue-600" />
                    <span>Requêtes populaires</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {dashboardData.aria.top_queries.map((query, index) => (
                      <div key={index} className="flex items-center justify-between">
                        <span className="text-sm">{query.query}</span>
                        <Badge variant="outline">{query.count}</Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="system" className="mt-6">
          <div className="space-y-6">
            {/* État du système */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-2">
                      <Server className={`w-8 h-8 ${dashboardData.system.server_status === 'healthy' ? 'text-green-500' : 'text-red-500'}`} />
                    </div>
                    <div className="text-sm text-gray-600">Serveur</div>
                    <Badge className={`mt-1 ${dashboardData.system.server_status === 'healthy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {dashboardData.system.server_status === 'healthy' ? 'Opérationnel' : 'Problème'}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{dashboardData.system.uptime}%</div>
                    <div className="text-sm text-gray-600">Disponibilité</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{dashboardData.system.response_time}ms</div>
                    <div className="text-sm text-gray-600">Temps de réponse</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{dashboardData.system.active_sessions}</div>
                    <div className="text-sm text-gray-600">Sessions actives</div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Utilisation des ressources */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <HardDrive className="w-5 h-5 text-blue-600" />
                    <span>Utilisation du stockage</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Espace utilisé</span>
                      <span>{dashboardData.system.storage_used}%</span>
                    </div>
                    <Progress value={dashboardData.system.storage_used} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Base de données</span>
                      <span>{dashboardData.system.database_size} GB</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Network className="w-5 h-5 text-green-600" />
                    <span>Utilisation réseau</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Bande passante</span>
                      <span>{dashboardData.system.bandwidth_used}%</span>
                    </div>
                    <Progress value={dashboardData.system.bandwidth_used} className="h-2" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Logs et erreurs */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <AlertTriangle className="w-5 h-5 text-red-600" />
                    <span>Erreurs (24h)</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-red-600">{dashboardData.system.errors_24h}</div>
                    <div className="text-sm text-gray-600">erreurs détectées</div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <AlertTriangle className="w-5 h-5 text-yellow-600" />
                    <span>Avertissements (24h)</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-yellow-600">{dashboardData.system.warnings_24h}</div>
                    <div className="text-sm text-gray-600">avertissements</div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdminDashboard;

