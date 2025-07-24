import React, { useState, useEffect } from 'react';
import { 
  CheckCircle, 
  Circle, 
  Lock, 
  Play, 
  BookOpen, 
  Video, 
  FileText, 
  Award,
  Clock,
  Target,
  TrendingUp,
  Star
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';

export default function LearningPath({ subject = 'mathematics', studentId }) {
  const [currentPath, setCurrentPath] = useState(null);
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);

  // Parcours de démonstration
  const learningPaths = {
    mathematics: {
      id: 'math-terminale',
      title: 'Mathématiques Terminale',
      description: 'Parcours complet pour maîtriser le programme de Terminale',
      totalModules: 8,
      estimatedHours: 120,
      difficulty: 'Avancé',
      modules: [
        {
          id: 'limits',
          title: 'Limites et continuité',
          description: 'Comprendre les limites de fonctions et la continuité',
          status: 'completed',
          progress: 100,
          estimatedTime: 15,
          lessons: [
            { id: 'limits-1', title: 'Introduction aux limites', type: 'video', duration: 20, completed: true },
            { id: 'limits-2', title: 'Calcul de limites', type: 'lesson', duration: 30, completed: true },
            { id: 'limits-3', title: 'Exercices pratiques', type: 'quiz', duration: 25, completed: true },
            { id: 'limits-4', title: 'Continuité', type: 'lesson', duration: 20, completed: true }
          ],
          skills: ['Calcul de limites', 'Théorèmes de continuité', 'Asymptotes'],
          prerequisites: []
        },
        {
          id: 'derivatives',
          title: 'Dérivation',
          description: 'Maîtriser les techniques de dérivation et leurs applications',
          status: 'completed',
          progress: 100,
          estimatedTime: 18,
          lessons: [
            { id: 'deriv-1', title: 'Définition de la dérivée', type: 'video', duration: 25, completed: true },
            { id: 'deriv-2', title: 'Règles de dérivation', type: 'lesson', duration: 35, completed: true },
            { id: 'deriv-3', title: 'Applications géométriques', type: 'lesson', duration: 30, completed: true },
            { id: 'deriv-4', title: 'Exercices d\'application', type: 'quiz', duration: 20, completed: true }
          ],
          skills: ['Calcul de dérivées', 'Équations de tangentes', 'Variations de fonctions'],
          prerequisites: ['limits']
        },
        {
          id: 'integrals',
          title: 'Intégration',
          description: 'Techniques d\'intégration et calcul d\'aires',
          status: 'current',
          progress: 65,
          estimatedTime: 20,
          lessons: [
            { id: 'int-1', title: 'Primitives', type: 'video', duration: 30, completed: true },
            { id: 'int-2', title: 'Intégrale définie', type: 'lesson', duration: 25, completed: true },
            { id: 'int-3', title: 'Calcul d\'aires', type: 'lesson', duration: 20, completed: false },
            { id: 'int-4', title: 'Exercices d\'intégration', type: 'quiz', duration: 25, completed: false }
          ],
          skills: ['Calcul de primitives', 'Intégration par parties', 'Calcul d\'aires'],
          prerequisites: ['derivatives']
        },
        {
          id: 'exponential',
          title: 'Fonction exponentielle',
          description: 'Propriétés et applications de la fonction exponentielle',
          status: 'locked',
          progress: 0,
          estimatedTime: 12,
          lessons: [
            { id: 'exp-1', title: 'Définition et propriétés', type: 'video', duration: 20, completed: false },
            { id: 'exp-2', title: 'Dérivée et primitive', type: 'lesson', duration: 15, completed: false },
            { id: 'exp-3', title: 'Équations exponentielles', type: 'lesson', duration: 20, completed: false },
            { id: 'exp-4', title: 'Applications', type: 'quiz', duration: 15, completed: false }
          ],
          skills: ['Propriétés exponentielles', 'Résolution d\'équations', 'Modélisation'],
          prerequisites: ['integrals']
        },
        {
          id: 'logarithm',
          title: 'Fonction logarithme',
          description: 'Fonction logarithme népérien et ses applications',
          status: 'locked',
          progress: 0,
          estimatedTime: 12,
          lessons: [
            { id: 'log-1', title: 'Définition du logarithme', type: 'video', duration: 20, completed: false },
            { id: 'log-2', title: 'Propriétés algébriques', type: 'lesson', duration: 15, completed: false },
            { id: 'log-3', title: 'Dérivée et étude', type: 'lesson', duration: 20, completed: false },
            { id: 'log-4', title: 'Exercices pratiques', type: 'quiz', duration: 15, completed: false }
          ],
          skills: ['Propriétés logarithmiques', 'Équations logarithmiques', 'Études de fonctions'],
          prerequisites: ['exponential']
        },
        {
          id: 'trigonometry',
          title: 'Trigonométrie avancée',
          description: 'Fonctions trigonométriques et leurs applications',
          status: 'locked',
          progress: 0,
          estimatedTime: 16,
          lessons: [
            { id: 'trig-1', title: 'Cercle trigonométrique', type: 'video', duration: 25, completed: false },
            { id: 'trig-2', title: 'Fonctions sin, cos, tan', type: 'lesson', duration: 30, completed: false },
            { id: 'trig-3', title: 'Équations trigonométriques', type: 'lesson', duration: 25, completed: false },
            { id: 'trig-4', title: 'Applications géométriques', type: 'quiz', duration: 20, completed: false }
          ],
          skills: ['Résolution d\'équations', 'Transformations', 'Géométrie'],
          prerequisites: ['derivatives']
        },
        {
          id: 'probability',
          title: 'Probabilités',
          description: 'Calcul des probabilités et lois de probabilité',
          status: 'locked',
          progress: 0,
          estimatedTime: 22,
          lessons: [
            { id: 'prob-1', title: 'Probabilités conditionnelles', type: 'video', duration: 30, completed: false },
            { id: 'prob-2', title: 'Variables aléatoires', type: 'lesson', duration: 35, completed: false },
            { id: 'prob-3', title: 'Loi binomiale', type: 'lesson', duration: 25, completed: false },
            { id: 'prob-4', title: 'Loi normale', type: 'lesson', duration: 30, completed: false },
            { id: 'prob-5', title: 'Exercices de synthèse', type: 'quiz', duration: 40, completed: false }
          ],
          skills: ['Probabilités conditionnelles', 'Lois de probabilité', 'Statistiques'],
          prerequisites: ['integrals']
        },
        {
          id: 'geometry',
          title: 'Géométrie dans l\'espace',
          description: 'Géométrie vectorielle et dans l\'espace',
          status: 'locked',
          progress: 0,
          estimatedTime: 18,
          lessons: [
            { id: 'geo-1', title: 'Vecteurs dans l\'espace', type: 'video', duration: 25, completed: false },
            { id: 'geo-2', title: 'Produit scalaire', type: 'lesson', duration: 20, completed: false },
            { id: 'geo-3', title: 'Équations de plans', type: 'lesson', duration: 30, completed: false },
            { id: 'geo-4', title: 'Géométrie analytique', type: 'quiz', duration: 25, completed: false }
          ],
          skills: ['Calcul vectoriel', 'Géométrie analytique', 'Équations de droites et plans'],
          prerequisites: ['derivatives']
        }
      ]
    }
  };

  useEffect(() => {
    loadLearningPath();
  }, [subject, studentId]);

  const loadLearningPath = async () => {
    try {
      setLoading(true);
      
      // Simuler le chargement des données
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const path = learningPaths[subject];
      if (path) {
        setCurrentPath(path);
        
        // Calculer la progression globale
        const totalLessons = path.modules.reduce((acc, module) => acc + module.lessons.length, 0);
        const completedLessons = path.modules.reduce((acc, module) => 
          acc + module.lessons.filter(lesson => lesson.completed).length, 0
        );
        
        setProgress({
          overall: Math.round((completedLessons / totalLessons) * 100),
          modules: path.modules.reduce((acc, module) => {
            acc[module.id] = module.progress;
            return acc;
          }, {})
        });
      }
    } catch (error) {
      console.error('Erreur lors du chargement du parcours:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-6 w-6 text-green-500" />;
      case 'current':
        return <Play className="h-6 w-6 text-blue-500" />;
      case 'locked':
        return <Lock className="h-6 w-6 text-gray-400" />;
      default:
        return <Circle className="h-6 w-6 text-gray-300" />;
    }
  };

  const getLessonIcon = (type) => {
    switch (type) {
      case 'video':
        return <Video className="h-4 w-4" />;
      case 'lesson':
        return <BookOpen className="h-4 w-4" />;
      case 'quiz':
        return <FileText className="h-4 w-4" />;
      default:
        return <Circle className="h-4 w-4" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'current':
        return 'bg-blue-100 text-blue-800';
      case 'locked':
        return 'bg-gray-100 text-gray-500';
      default:
        return 'bg-gray-100 text-gray-500';
    }
  };

  const canAccessModule = (module) => {
    if (module.prerequisites.length === 0) return true;
    
    return module.prerequisites.every(prereqId => {
      const prereqModule = currentPath.modules.find(m => m.id === prereqId);
      return prereqModule && prereqModule.status === 'completed';
    });
  };

  const startModule = (moduleId) => {
    // Logique pour démarrer un module
    console.log('Démarrage du module:', moduleId);
  };

  const continueModule = (moduleId) => {
    // Logique pour continuer un module
    console.log('Continuation du module:', moduleId);
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3 mb-6"></div>
          <div className="grid gap-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!currentPath) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Parcours non trouvé
        </h2>
        <p className="text-gray-600">
          Le parcours d'apprentissage demandé n'existe pas.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête du parcours */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-2xl">{currentPath.title}</CardTitle>
              <CardDescription className="text-lg mt-2">
                {currentPath.description}
              </CardDescription>
            </div>
            <Badge variant="outline" className="text-sm">
              {currentPath.difficulty}
            </Badge>
          </div>
        </CardHeader>
        
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">{progress.overall}%</div>
              <div className="text-sm text-gray-600">Progression globale</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">{currentPath.totalModules}</div>
              <div className="text-sm text-gray-600">Modules</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">{currentPath.estimatedHours}h</div>
              <div className="text-sm text-gray-600">Durée estimée</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-600">
                {currentPath.modules.filter(m => m.status === 'completed').length}
              </div>
              <div className="text-sm text-gray-600">Modules terminés</div>
            </div>
          </div>
          
          <Progress value={progress.overall} className="h-3" />
        </CardContent>
      </Card>

      {/* Liste des modules */}
      <div className="space-y-4">
        {currentPath.modules.map((module, index) => {
          const isAccessible = canAccessModule(module);
          const completedLessons = module.lessons.filter(l => l.completed).length;
          
          return (
            <Card key={module.id} className={`transition-all duration-200 ${
              module.status === 'current' ? 'ring-2 ring-blue-500 shadow-lg' : ''
            } ${!isAccessible ? 'opacity-60' : 'hover:shadow-md'}`}>
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  {/* Icône de statut */}
                  <div className="flex-shrink-0 mt-1">
                    {getStatusIcon(module.status)}
                  </div>
                  
                  {/* Contenu principal */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {index + 1}. {module.title}
                      </h3>
                      <Badge className={getStatusColor(module.status)}>
                        {module.status === 'completed' ? 'Terminé' : 
                         module.status === 'current' ? 'En cours' : 'Verrouillé'}
                      </Badge>
                    </div>
                    
                    <p className="text-gray-600 mb-4">{module.description}</p>
                    
                    {/* Progression du module */}
                    <div className="mb-4">
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Progression</span>
                        <span>{completedLessons}/{module.lessons.length} leçons</span>
                      </div>
                      <Progress value={module.progress} className="h-2" />
                    </div>
                    
                    {/* Informations du module */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div className="flex items-center text-sm text-gray-600">
                        <Clock className="h-4 w-4 mr-2" />
                        {module.estimatedTime}h estimées
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <Target className="h-4 w-4 mr-2" />
                        {module.lessons.length} leçons
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <Award className="h-4 w-4 mr-2" />
                        {module.skills.length} compétences
                      </div>
                    </div>
                    
                    {/* Compétences */}
                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-900 mb-2">Compétences acquises :</h4>
                      <div className="flex flex-wrap gap-2">
                        {module.skills.map((skill, skillIndex) => (
                          <Badge key={skillIndex} variant="secondary" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    
                    {/* Leçons (si module en cours ou terminé) */}
                    {(module.status === 'current' || module.status === 'completed') && (
                      <div className="mb-4">
                        <h4 className="text-sm font-medium text-gray-900 mb-3">Leçons :</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          {module.lessons.map((lesson) => (
                            <div key={lesson.id} className={`flex items-center space-x-3 p-2 rounded ${
                              lesson.completed ? 'bg-green-50' : 'bg-gray-50'
                            }`}>
                              <div className={`h-4 w-4 ${lesson.completed ? 'text-green-500' : 'text-gray-400'}`}>
                                {lesson.completed ? <CheckCircle className="h-4 w-4" /> : getLessonIcon(lesson.type)}
                              </div>
                              <span className={`text-sm flex-1 ${lesson.completed ? 'text-green-700' : 'text-gray-700'}`}>
                                {lesson.title}
                              </span>
                              <span className="text-xs text-gray-500">{lesson.duration}min</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Prérequis */}
                    {module.prerequisites.length > 0 && (
                      <div className="mb-4">
                        <h4 className="text-sm font-medium text-gray-900 mb-2">Prérequis :</h4>
                        <div className="flex flex-wrap gap-2">
                          {module.prerequisites.map((prereqId) => {
                            const prereqModule = currentPath.modules.find(m => m.id === prereqId);
                            return (
                              <Badge key={prereqId} variant="outline" className="text-xs">
                                {prereqModule?.title}
                              </Badge>
                            );
                          })}
                        </div>
                      </div>
                    )}
                    
                    {/* Actions */}
                    <div className="flex space-x-3">
                      {module.status === 'current' && (
                        <Button onClick={() => continueModule(module.id)}>
                          <Play className="h-4 w-4 mr-2" />
                          Continuer
                        </Button>
                      )}
                      
                      {module.status === 'locked' && isAccessible && (
                        <Button onClick={() => startModule(module.id)} variant="outline">
                          <Play className="h-4 w-4 mr-2" />
                          Commencer
                        </Button>
                      )}
                      
                      {module.status === 'completed' && (
                        <Button variant="outline" onClick={() => continueModule(module.id)}>
                          <TrendingUp className="h-4 w-4 mr-2" />
                          Réviser
                        </Button>
                      )}
                      
                      {!isAccessible && module.status === 'locked' && (
                        <Button disabled variant="outline">
                          <Lock className="h-4 w-4 mr-2" />
                          Verrouillé
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Récompenses et badges */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Award className="h-5 w-5 mr-2" />
            Récompenses et badges
          </CardTitle>
          <CardDescription>
            Vos accomplissements dans ce parcours
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <Star className="h-8 w-8 text-yellow-500 mx-auto mb-2" />
              <div className="text-sm font-medium">Débutant</div>
              <div className="text-xs text-gray-600">Premier module terminé</div>
            </div>
            
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <Target className="h-8 w-8 text-blue-500 mx-auto mb-2" />
              <div className="text-sm font-medium">Persévérant</div>
              <div className="text-xs text-gray-600">3 modules terminés</div>
            </div>
            
            <div className="text-center p-4 bg-gray-100 rounded-lg opacity-50">
              <TrendingUp className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <div className="text-sm font-medium">Expert</div>
              <div className="text-xs text-gray-600">Tous les modules terminés</div>
            </div>
            
            <div className="text-center p-4 bg-gray-100 rounded-lg opacity-50">
              <Award className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <div className="text-sm font-medium">Maître</div>
              <div className="text-xs text-gray-600">100% de réussite aux quiz</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

