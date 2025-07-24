import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  FileText, 
  Download, 
  Share2, 
  Eye, 
  Edit, 
  Trash2, 
  Plus, 
  Search, 
  Filter, 
  Settings, 
  Wand2,
  Brain,
  Target,
  BookOpen,
  Calculator,
  Code,
  Atom,
  PenTool,
  Clock,
  Star,
  Heart,
  Bookmark,
  Copy,
  ExternalLink,
  Upload,
  Image,
  Video,
  Mic,
  Headphones,
  Printer,
  Save,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Info,
  Lightbulb,
  Zap,
  Sparkles,
  Award,
  TrendingUp,
  BarChart3,
  PieChart,
  Activity,
  Users,
  Calendar,
  MapPin,
  Tag,
  Layers,
  Grid,
  List,
  MoreHorizontal,
  ChevronDown,
  ChevronRight,
  X,
  Play,
  Pause,
  RotateCcw
} from 'lucide-react'

const DocumentGenerator = ({ 
  student, 
  onGenerateDocument, 
  onSaveDocument, 
  documents, 
  addNotification,
  isVisible,
  onClose 
}) => {
  const [activeTab, setActiveTab] = useState('generator');
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [generationParams, setGenerationParams] = useState({
    subject: 'all',
    type: 'course',
    difficulty: 3,
    duration: 30,
    style: 'visual',
    topics: [],
    customPrompt: ''
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterSubject, setFilterSubject] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [viewMode, setViewMode] = useState('grid'); // grid, list
  const [selectedDocuments, setSelectedDocuments] = useState([]);
  const [showPreview, setShowPreview] = useState(false);
  const [previewDocument, setPreviewDocument] = useState(null);

  // Templates de documents disponibles
  const documentTemplates = [
    {
      id: 'math-course',
      name: 'Fiche de Cours - Mathématiques',
      description: 'Cours structuré avec définitions, théorèmes et exemples',
      subject: 'maths',
      type: 'course',
      icon: Calculator,
      estimatedTime: '2-3h de travail',
      difficulty: [2, 3, 4, 5],
      features: ['Définitions claires', 'Exemples progressifs', 'Schémas explicatifs', 'Points clés']
    },
    {
      id: 'math-exercises',
      name: 'Série d\'Exercices - Mathématiques',
      description: 'Exercices progressifs avec corrections détaillées',
      subject: 'maths',
      type: 'exercises',
      icon: Target,
      estimatedTime: '1-2h de travail',
      difficulty: [1, 2, 3, 4, 5],
      features: ['Progression par difficulté', 'Corrections détaillées', 'Méthodes de résolution', 'Barème']
    },
    {
      id: 'nsi-project',
      name: 'Projet Guidé - NSI',
      description: 'Projet Python avec étapes détaillées et code commenté',
      subject: 'nsi',
      type: 'project',
      icon: Code,
      estimatedTime: '3-5h de travail',
      difficulty: [3, 4, 5],
      features: ['Code commenté', 'Tests unitaires', 'Documentation', 'Optimisations']
    },
    {
      id: 'physics-lab',
      name: 'TP Virtuel - Physique',
      description: 'Travaux pratiques avec simulations et analyses',
      subject: 'physique',
      type: 'lab',
      icon: Atom,
      estimatedTime: '2-3h de travail',
      difficulty: [2, 3, 4],
      features: ['Simulations interactives', 'Protocole détaillé', 'Analyse des résultats', 'Conclusion']
    },
    {
      id: 'french-analysis',
      name: 'Analyse Littéraire - Français',
      description: 'Analyse d\'œuvre avec plan détaillé et citations',
      subject: 'français',
      type: 'analysis',
      icon: PenTool,
      estimatedTime: '2-4h de travail',
      difficulty: [3, 4, 5],
      features: ['Plan structuré', 'Citations pertinentes', 'Analyse stylistique', 'Contextualisation']
    },
    {
      id: 'quiz-adaptive',
      name: 'Quiz Adaptatif',
      description: 'Quiz personnalisé selon votre niveau et vos lacunes',
      subject: 'all',
      type: 'quiz',
      icon: Brain,
      estimatedTime: '15-30 min',
      difficulty: [1, 2, 3, 4, 5],
      features: ['Questions adaptatives', 'Feedback immédiat', 'Analyse des erreurs', 'Recommandations']
    },
    {
      id: 'revision-sheet',
      name: 'Fiche de Révision',
      description: 'Résumé synthétique pour révisions rapides',
      subject: 'all',
      type: 'summary',
      icon: BookOpen,
      estimatedTime: '30-45 min',
      difficulty: [1, 2, 3, 4],
      features: ['Synthèse visuelle', 'Points essentiels', 'Mnémotechniques', 'Auto-évaluation']
    },
    {
      id: 'oral-preparation',
      name: 'Préparation Grand Oral',
      description: 'Guide complet pour préparer votre présentation',
      subject: 'français',
      type: 'oral',
      icon: Mic,
      estimatedTime: '1-2h de préparation',
      difficulty: [4, 5],
      features: ['Structure de présentation', 'Gestion du stress', 'Questions types', 'Conseils pratiques']
    }
  ];

  // Sujets et topics disponibles
  const subjectTopics = {
    maths: [
      'Fonctions exponentielles', 'Fonctions logarithmes', 'Limites', 'Dérivées', 
      'Intégrales', 'Probabilités', 'Statistiques', 'Géométrie dans l\'espace',
      'Nombres complexes', 'Suites numériques'
    ],
    nsi: [
      'Algorithmes de tri', 'Structures de données', 'Programmation orientée objet',
      'Bases de données', 'Réseaux', 'Cryptographie', 'Intelligence artificielle',
      'Interfaces homme-machine', 'Systèmes d\'exploitation'
    ],
    physique: [
      'Mécanique', 'Thermodynamique', 'Électricité', 'Magnétisme', 'Optique',
      'Ondes', 'Physique quantique', 'Relativité', 'Physique nucléaire'
    ],
    français: [
      'Roman', 'Théâtre', 'Poésie', 'Essai', 'Argumentation', 'Stylistique',
      'Histoire littéraire', 'Genres littéraires', 'Mouvements littéraires'
    ]
  };

  const filteredTemplates = documentTemplates.filter(template => {
    const matchesSubject = generationParams.subject === 'all' || template.subject === generationParams.subject;
    const matchesType = generationParams.type === 'all' || template.type === generationParams.type;
    const matchesDifficulty = template.difficulty.includes(generationParams.difficulty);
    
    return matchesSubject && matchesType && matchesDifficulty;
  });

  const filteredDocuments = documents?.filter(doc => {
    const matchesSearch = doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         doc.subject.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSubject = filterSubject === 'all' || doc.subject.toLowerCase().includes(filterSubject);
    const matchesType = filterType === 'all' || doc.type === filterType;
    
    return matchesSearch && matchesSubject && matchesType;
  }) || [];

  const handleGenerateDocument = async () => {
    if (!selectedTemplate) {
      addNotification({
        type: 'warning',
        title: 'Sélection requise',
        message: 'Veuillez sélectionner un template de document'
      });
      return;
    }

    setIsGenerating(true);
    
    try {
      // Simulation de génération avec ARIA
      await new Promise(resolve => setTimeout(resolve, 3000 + Math.random() * 2000));
      
      const generatedDoc = {
        id: Date.now(),
        title: `${selectedTemplate.name} - ${new Date().toLocaleDateString()}`,
        subject: selectedTemplate.subject,
        type: selectedTemplate.type,
        content: generateMockContent(selectedTemplate),
        createdAt: new Date(),
        estimatedTime: selectedTemplate.estimatedTime,
        difficulty: generationParams.difficulty,
        topics: generationParams.topics,
        personalizedFor: student?.name,
        ariaGenerated: true,
        status: 'generated'
      };
      
      setGeneratedContent(generatedDoc);
      
      addNotification({
        type: 'success',
        title: 'Document généré !',
        message: `${selectedTemplate.name} a été créé avec succès`
      });
      
      if (onGenerateDocument) {
        onGenerateDocument(generatedDoc);
      }
      
    } catch (error) {
      addNotification({
        type: 'error',
        title: 'Erreur de génération',
        message: 'Une erreur est survenue lors de la génération du document'
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const generateMockContent = (template) => {
    const contents = {
      'math-course': `# ${template.name}

## Objectifs d'apprentissage
- Comprendre les concepts fondamentaux
- Maîtriser les techniques de calcul
- Appliquer dans des contextes variés

## I. Définitions et propriétés

### Définition 1
Une fonction exponentielle est une fonction de la forme f(x) = a^x où a > 0 et a ≠ 1.

**Propriétés importantes :**
- Domaine de définition : ℝ
- Ensemble image : ]0, +∞[
- La fonction est strictement croissante si a > 1

## II. Exemples et applications

### Exemple 1
Soit f(x) = 2^x. Calculer f(3) et f(-2).

**Solution :**
- f(3) = 2³ = 8
- f(-2) = 2^(-2) = 1/4 = 0,25

## III. Exercices d'application

1. Résoudre l'équation 3^x = 27
2. Étudier les variations de f(x) = (1/2)^x
3. Tracer la courbe représentative de g(x) = e^x

---
*Document généré par ARIA selon votre profil d'apprentissage*`,

      'math-exercises': `# Série d'Exercices - Fonctions Exponentielles

## Exercice 1 ⭐ (Niveau débutant)
Calculer les valeurs suivantes :
a) 2³
b) 3⁻²
c) (1/4)²

**Correction :**
a) 2³ = 8
b) 3⁻² = 1/9
c) (1/4)² = 1/16

## Exercice 2 ⭐⭐ (Niveau intermédiaire)
Résoudre les équations :
a) 2^x = 16
b) 3^(x+1) = 27
c) (1/2)^x = 8

**Correction :**
a) 2^x = 16 = 2⁴, donc x = 4
b) 3^(x+1) = 27 = 3³, donc x+1 = 3, x = 2
c) (1/2)^x = 8 = 2³ = (1/2)⁻³, donc x = -3

## Exercice 3 ⭐⭐⭐ (Niveau avancé)
Étudier la fonction f(x) = e^x - x - 1
a) Calculer f'(x)
b) Étudier le signe de f'(x)
c) Dresser le tableau de variations

---
*Exercices adaptés à votre niveau par ARIA*`,

      'nsi-project': `# Projet Python - Algorithmes de Tri

## Objectif
Implémenter et comparer différents algorithmes de tri.

## Étape 1 : Tri à bulles
\`\`\`python
def tri_bulles(liste):
    """
    Implémentation du tri à bulles
    Complexité : O(n²)
    """
    n = len(liste)
    for i in range(n):
        for j in range(0, n - i - 1):
            if liste[j] > liste[j + 1]:
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
    return liste

# Test
test_liste = [64, 34, 25, 12, 22, 11, 90]
print("Liste triée :", tri_bulles(test_liste.copy()))
\`\`\`

## Étape 2 : Tri rapide (QuickSort)
\`\`\`python
def tri_rapide(liste):
    """
    Implémentation du tri rapide
    Complexité moyenne : O(n log n)
    """
    if len(liste) <= 1:
        return liste
    
    pivot = liste[len(liste) // 2]
    gauche = [x for x in liste if x < pivot]
    milieu = [x for x in liste if x == pivot]
    droite = [x for x in liste if x > pivot]
    
    return tri_rapide(gauche) + milieu + tri_rapide(droite)
\`\`\`

## Étape 3 : Comparaison des performances
\`\`\`python
import time
import random

def comparer_tris(taille=1000):
    # Génération d'une liste aléatoire
    liste_test = [random.randint(1, 1000) for _ in range(taille)]
    
    # Test tri à bulles
    start = time.time()
    tri_bulles(liste_test.copy())
    temps_bulles = time.time() - start
    
    # Test tri rapide
    start = time.time()
    tri_rapide(liste_test.copy())
    temps_rapide = time.time() - start
    
    print(f"Tri à bulles : {temps_bulles:.4f}s")
    print(f"Tri rapide : {temps_rapide:.4f}s")

comparer_tris()
\`\`\`

---
*Projet généré par ARIA avec votre niveau de programmation*`
    };
    
    return contents[template.id] || `# ${template.name}\n\nContenu généré automatiquement par ARIA selon votre profil d'apprentissage.\n\n*Document personnalisé pour ${student?.name}*`;
  };

  const saveDocument = (document) => {
    if (onSaveDocument) {
      onSaveDocument(document);
    }
    
    addNotification({
      type: 'success',
      title: 'Document sauvegardé',
      message: 'Le document a été ajouté à votre bibliothèque'
    });
  };

  const previewDoc = (document) => {
    setPreviewDocument(document);
    setShowPreview(true);
  };

  const downloadDocument = (document, format = 'pdf') => {
    // Simulation de téléchargement
    addNotification({
      type: 'info',
      title: 'Téléchargement en cours',
      message: `Génération du ${format.toUpperCase()} en cours...`
    });
    
    setTimeout(() => {
      addNotification({
        type: 'success',
        title: 'Téléchargement terminé',
        message: `${document.title}.${format} a été téléchargé`
      });
    }, 2000);
  };

  if (!isVisible) return null;

  return (
    <div className="nexus-document-generator">
      <div className="nexus-generator-header">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
            <Wand2 className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold">Générateur de Documents</h2>
            <p className="text-sm text-muted-foreground">Créez du contenu personnalisé avec ARIA</p>
          </div>
        </div>
        
        <Button variant="ghost" size="sm" onClick={onClose}>
          <X className="w-4 h-4" />
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-6">
          <TabsTrigger value="generator" className="flex items-center space-x-2">
            <Wand2 className="w-4 h-4" />
            <span>Générateur</span>
          </TabsTrigger>
          <TabsTrigger value="library" className="flex items-center space-x-2">
            <BookOpen className="w-4 h-4" />
            <span>Ma Bibliothèque</span>
          </TabsTrigger>
          <TabsTrigger value="templates" className="flex items-center space-x-2">
            <Layers className="w-4 h-4" />
            <span>Templates</span>
          </TabsTrigger>
        </TabsList>

        {/* Générateur */}
        <TabsContent value="generator">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Configuration */}
            <div className="lg:col-span-1 space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Settings className="w-5 h-5" />
                    <span>Configuration</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="nexus-form-label">Matière</label>
                    <select 
                      value={generationParams.subject}
                      onChange={(e) => setGenerationParams(prev => ({ ...prev, subject: e.target.value }))}
                      className="nexus-input w-full"
                    >
                      <option value="all">Toutes matières</option>
                      <option value="maths">Mathématiques</option>
                      <option value="nsi">NSI</option>
                      <option value="physique">Physique</option>
                      <option value="français">Français</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="nexus-form-label">Type de document</label>
                    <select 
                      value={generationParams.type}
                      onChange={(e) => setGenerationParams(prev => ({ ...prev, type: e.target.value }))}
                      className="nexus-input w-full"
                    >
                      <option value="course">Cours</option>
                      <option value="exercises">Exercices</option>
                      <option value="quiz">Quiz</option>
                      <option value="summary">Résumé</option>
                      <option value="project">Projet</option>
                      <option value="lab">TP</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="nexus-form-label">Niveau de difficulté</label>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm">Facile</span>
                      <input
                        type="range"
                        min="1"
                        max="5"
                        value={generationParams.difficulty}
                        onChange={(e) => setGenerationParams(prev => ({ ...prev, difficulty: parseInt(e.target.value) }))}
                        className="flex-1"
                      />
                      <span className="text-sm">Difficile</span>
                    </div>
                    <div className="text-center mt-1">
                      <Badge variant="outline">Niveau {generationParams.difficulty}/5</Badge>
                    </div>
                  </div>
                  
                  <div>
                    <label className="nexus-form-label">Durée de travail estimée</label>
                    <select 
                      value={generationParams.duration}
                      onChange={(e) => setGenerationParams(prev => ({ ...prev, duration: parseInt(e.target.value) }))}
                      className="nexus-input w-full"
                    >
                      <option value={15}>15 minutes</option>
                      <option value={30}>30 minutes</option>
                      <option value={60}>1 heure</option>
                      <option value={120}>2 heures</option>
                      <option value={180}>3 heures</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="nexus-form-label">Style d'apprentissage</label>
                    <select 
                      value={generationParams.style}
                      onChange={(e) => setGenerationParams(prev => ({ ...prev, style: e.target.value }))}
                      className="nexus-input w-full"
                    >
                      <option value="visual">Visuel (schémas, graphiques)</option>
                      <option value="auditory">Auditif (explications détaillées)</option>
                      <option value="kinesthetic">Kinesthésique (pratique, manipulation)</option>
                      <option value="reading">Lecture/Écriture (textes, listes)</option>
                    </select>
                  </div>
                  
                  {generationParams.subject !== 'all' && (
                    <div>
                      <label className="nexus-form-label">Sujets spécifiques</label>
                      <div className="space-y-2 max-h-32 overflow-y-auto">
                        {subjectTopics[generationParams.subject]?.map((topic, index) => (
                          <label key={index} className="flex items-center space-x-2">
                            <input
                              type="checkbox"
                              checked={generationParams.topics.includes(topic)}
                              onChange={(e) => {
                                if (e.target.checked) {
                                  setGenerationParams(prev => ({ 
                                    ...prev, 
                                    topics: [...prev.topics, topic] 
                                  }));
                                } else {
                                  setGenerationParams(prev => ({ 
                                    ...prev, 
                                    topics: prev.topics.filter(t => t !== topic) 
                                  }));
                                }
                              }}
                              className="rounded"
                            />
                            <span className="text-sm">{topic}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div>
                    <label className="nexus-form-label">Instructions personnalisées</label>
                    <textarea
                      value={generationParams.customPrompt}
                      onChange={(e) => setGenerationParams(prev => ({ ...prev, customPrompt: e.target.value }))}
                      placeholder="Ajoutez des instructions spécifiques pour ARIA..."
                      className="nexus-input w-full h-20 resize-none"
                    />
                  </div>
                </CardContent>
              </Card>
              
              {/* Profil d'apprentissage */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Brain className="w-5 h-5 text-purple-600" />
                    <span>Profil ARIA</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span>Style visuel</span>
                      <span>{student?.learningStyle?.visual || 85}%</span>
                    </div>
                    <div className="nexus-progress-bar">
                      <div 
                        className="nexus-progress-fill bg-blue-500"
                        style={{ width: `${student?.learningStyle?.visual || 85}%` }}
                      ></div>
                    </div>
                    
                    <div className="p-3 rounded-lg bg-purple-50 dark:bg-purple-900/20">
                      <p className="text-sm text-purple-700 dark:text-purple-300">
                        ARIA adaptera le contenu à votre style d'apprentissage dominant et à votre niveau actuel.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
            
            {/* Templates et génération */}
            <div className="lg:col-span-2 space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle>Templates Disponibles</CardTitle>
                  <CardDescription>
                    Sélectionnez un template adapté à vos besoins
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-4">
                    {filteredTemplates.map((template) => (
                      <div
                        key={template.id}
                        className={`nexus-template-card ${selectedTemplate?.id === template.id ? 'selected' : ''}`}
                        onClick={() => setSelectedTemplate(template)}
                      >
                        <div className="flex items-start space-x-3">
                          <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                            <template.icon className="w-6 h-6 text-blue-600" />
                          </div>
                          <div className="flex-1">
                            <h4 className="font-semibold">{template.name}</h4>
                            <p className="text-sm text-muted-foreground mb-2">{template.description}</p>
                            <div className="flex items-center space-x-2 mb-2">
                              <Badge variant="outline" className="text-xs">
                                {template.subject}
                              </Badge>
                              <Badge variant="outline" className="text-xs">
                                {template.estimatedTime}
                              </Badge>
                            </div>
                            <div className="flex flex-wrap gap-1">
                              {template.features.slice(0, 2).map((feature, index) => (
                                <span key={index} className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded">
                                  {feature}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  {filteredTemplates.length === 0 && (
                    <div className="text-center py-8">
                      <FileText className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
                      <p className="text-muted-foreground">Aucun template ne correspond à vos critères</p>
                    </div>
                  )}
                </CardContent>
              </Card>
              
              {/* Génération */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>Génération avec ARIA</span>
                    {selectedTemplate && (
                      <Badge className="nexus-badge-info">
                        {selectedTemplate.name}
                      </Badge>
                    )}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {!selectedTemplate ? (
                    <div className="text-center py-8">
                      <Wand2 className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
                      <p className="text-muted-foreground">Sélectionnez un template pour commencer</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                        <div className="flex items-start space-x-3">
                          <Brain className="w-5 h-5 text-blue-600 mt-0.5" />
                          <div>
                            <h4 className="font-medium text-blue-900 dark:text-blue-100">
                              ARIA va générer : {selectedTemplate.name}
                            </h4>
                            <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                              Adapté à votre niveau {generationParams.difficulty}/5 et votre style d'apprentissage {generationParams.style}
                            </p>
                            {generationParams.topics.length > 0 && (
                              <div className="mt-2">
                                <p className="text-sm text-blue-700 dark:text-blue-300">Sujets inclus :</p>
                                <div className="flex flex-wrap gap-1 mt-1">
                                  {generationParams.topics.map((topic, index) => (
                                    <Badge key={index} variant="outline" className="text-xs">
                                      {topic}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      <Button
                        onClick={handleGenerateDocument}
                        disabled={isGenerating}
                        className="w-full nexus-button-primary"
                        size="lg"
                      >
                        {isGenerating ? (
                          <>
                            <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                            ARIA génère votre document...
                          </>
                        ) : (
                          <>
                            <Sparkles className="w-4 h-4 mr-2" />
                            Générer avec ARIA
                          </>
                        )}
                      </Button>
                      
                      {isGenerating && (
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span>Progression</span>
                            <span>Génération en cours...</span>
                          </div>
                          <Progress value={75} className="w-full" />
                          <p className="text-xs text-muted-foreground text-center">
                            ARIA analyse votre profil et adapte le contenu...
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
              
              {/* Document généré */}
              {generatedContent && (
                <Card className="nexus-card">
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                        <span>Document Généré</span>
                      </div>
                      <Badge className="nexus-badge-success">Nouveau</Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-start space-x-4">
                        <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                          <FileText className="w-6 h-6 text-green-600" />
                        </div>
                        <div className="flex-1">
                          <h4 className="font-semibold">{generatedContent.title}</h4>
                          <p className="text-sm text-muted-foreground">{generatedContent.subject}</p>
                          <div className="flex items-center space-x-2 mt-2">
                            <Badge variant="outline">Niveau {generatedContent.difficulty}/5</Badge>
                            <Badge variant="outline">{generatedContent.estimatedTime}</Badge>
                            <Badge className="nexus-badge-info">ARIA</Badge>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          onClick={() => previewDoc(generatedContent)}
                          variant="outline"
                          className="flex-1"
                        >
                          <Eye className="w-4 h-4 mr-2" />
                          Aperçu
                        </Button>
                        <Button
                          onClick={() => saveDocument(generatedContent)}
                          variant="outline"
                          className="flex-1"
                        >
                          <Save className="w-4 h-4 mr-2" />
                          Sauvegarder
                        </Button>
                        <Button
                          onClick={() => downloadDocument(generatedContent)}
                          variant="outline"
                          className="flex-1"
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Télécharger
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </TabsContent>

        {/* Bibliothèque */}
        <TabsContent value="library">
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h3 className="text-lg font-semibold">Ma Bibliothèque</h3>
                <p className="text-sm text-muted-foreground">
                  {filteredDocuments.length} document{filteredDocuments.length > 1 ? 's' : ''} trouvé{filteredDocuments.length > 1 ? 's' : ''}
                </p>
              </div>
              
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
                  <input
                    type="text"
                    placeholder="Rechercher..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="nexus-input pl-10"
                  />
                </div>
                
                <select
                  value={filterSubject}
                  onChange={(e) => setFilterSubject(e.target.value)}
                  className="nexus-input"
                >
                  <option value="all">Toutes matières</option>
                  <option value="maths">Mathématiques</option>
                  <option value="nsi">NSI</option>
                  <option value="physique">Physique</option>
                  <option value="français">Français</option>
                </select>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
                >
                  {viewMode === 'grid' ? <List className="w-4 h-4" /> : <Grid className="w-4 h-4" />}
                </Button>
              </div>
            </div>
            
            {filteredDocuments.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">Aucun document trouvé</h3>
                <p className="text-muted-foreground mb-4">
                  Commencez par générer votre premier document avec ARIA
                </p>
                <Button onClick={() => setActiveTab('generator')}>
                  <Plus className="w-4 h-4 mr-2" />
                  Créer un document
                </Button>
              </div>
            ) : (
              <div className={viewMode === 'grid' ? 'grid md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-4'}>
                {filteredDocuments.map((doc) => (
                  <Card key={doc.id} className="nexus-card hover:shadow-lg transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                            <FileText className="w-5 h-5 text-blue-600" />
                          </div>
                          <div>
                            <h4 className="font-semibold line-clamp-1">{doc.title}</h4>
                            <p className="text-sm text-muted-foreground">{doc.subject}</p>
                          </div>
                        </div>
                        
                        <Button variant="ghost" size="sm">
                          <MoreHorizontal className="w-4 h-4" />
                        </Button>
                      </div>
                      
                      <div className="flex items-center space-x-2 mb-3">
                        <Badge variant="outline" className="text-xs">
                          {doc.type}
                        </Badge>
                        {doc.ariaGenerated && (
                          <Badge className="nexus-badge-info text-xs">ARIA</Badge>
                        )}
                        <Badge variant="outline" className="text-xs">
                          Niveau {doc.difficulty}/5
                        </Badge>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm text-muted-foreground mb-4">
                        <span>{doc.estimatedTime}</span>
                        <span>{new Date(doc.createdAt).toLocaleDateString()}</span>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => previewDoc(doc)}
                          className="flex-1"
                        >
                          <Eye className="w-3 h-3 mr-1" />
                          Voir
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => downloadDocument(doc)}
                        >
                          <Download className="w-3 h-3" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                        >
                          <Share2 className="w-3 h-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </TabsContent>

        {/* Templates */}
        <TabsContent value="templates">
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">Templates Disponibles</h3>
              <p className="text-sm text-muted-foreground">
                Découvrez tous les types de documents que ARIA peut générer pour vous
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {documentTemplates.map((template) => (
                <Card key={template.id} className="nexus-card hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-center space-x-3 mb-4">
                      <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                        <template.icon className="w-6 h-6 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold">{template.name}</h4>
                        <Badge variant="outline" className="text-xs mt-1">
                          {template.subject}
                        </Badge>
                      </div>
                    </div>
                    
                    <p className="text-sm text-muted-foreground mb-4">
                      {template.description}
                    </p>
                    
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Durée estimée</span>
                        <span className="font-medium">{template.estimatedTime}</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Niveaux</span>
                        <div className="flex space-x-1">
                          {template.difficulty.map((level) => (
                            <Badge key={level} variant="outline" className="text-xs">
                              {level}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div>
                        <p className="text-sm text-muted-foreground mb-2">Fonctionnalités :</p>
                        <div className="flex flex-wrap gap-1">
                          {template.features.map((feature, index) => (
                            <span key={index} className="text-xs bg-muted px-2 py-1 rounded">
                              {feature}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                    
                    <Button
                      className="w-full mt-4"
                      onClick={() => {
                        setSelectedTemplate(template);
                        setActiveTab('generator');
                      }}
                    >
                      <Wand2 className="w-4 h-4 mr-2" />
                      Utiliser ce template
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* Modal de prévisualisation */}
      {showPreview && previewDocument && (
        <div className="nexus-modal-overlay">
          <div className="nexus-modal max-w-4xl max-h-[90vh] overflow-hidden">
            <div className="flex items-center justify-between p-4 border-b">
              <div>
                <h3 className="text-lg font-semibold">{previewDocument.title}</h3>
                <p className="text-sm text-muted-foreground">{previewDocument.subject}</p>
              </div>
              <div className="flex items-center space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => downloadDocument(previewDocument)}
                >
                  <Download className="w-4 h-4 mr-2" />
                  Télécharger
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowPreview(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
              <div className="prose prose-sm max-w-none">
                <pre className="whitespace-pre-wrap font-sans">
                  {previewDocument.content}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentGenerator;

