import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

const ContentLibrary = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [selectedLevel, setSelectedLevel] = useState('all');
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(false);

  // Données de démonstration pour la bibliothèque de contenu
  const demoContent = [
    {
      id: 1,
      title: "Les fonctions exponentielles",
      subject: "Mathématiques",
      type: "Fiche de révision",
      level: "Terminale",
      description: "Propriétés, dérivées et applications des fonctions exponentielles",
      tags: ["analyse", "dérivation", "bac"],
      difficulty: "medium",
      duration: "30 min",
      lastUpdated: "2024-01-15",
      downloads: 245,
      rating: 4.8,
      preview: "Définition : La fonction exponentielle est l'unique fonction f définie sur ℝ telle que f'(x) = f(x) et f(0) = 1..."
    },
    {
      id: 2,
      title: "Algorithmes de tri en Python",
      subject: "NSI",
      type: "Cours interactif",
      level: "Terminale",
      description: "Implémentation et analyse des algorithmes de tri classiques",
      tags: ["algorithmes", "python", "complexité"],
      difficulty: "hard",
      duration: "45 min",
      lastUpdated: "2024-01-20",
      downloads: 189,
      rating: 4.9,
      preview: "# Tri par insertion\ndef tri_insertion(liste):\n    for i in range(1, len(liste)):\n        cle = liste[i]..."
    },
    {
      id: 3,
      title: "La mécanique quantique",
      subject: "Physique-Chimie",
      type: "Exercices corrigés",
      level: "Terminale",
      description: "Série d'exercices sur les concepts de base de la mécanique quantique",
      tags: ["quantique", "ondes", "particules"],
      difficulty: "hard",
      duration: "60 min",
      lastUpdated: "2024-01-18",
      downloads: 156,
      rating: 4.6,
      preview: "Exercice 1 : Un électron est confiné dans une boîte unidimensionnelle de longueur L..."
    },
    {
      id: 4,
      title: "L'argumentation au théâtre",
      subject: "Français",
      type: "Méthode",
      level: "Première",
      description: "Techniques d'analyse de l'argumentation dans les textes théâtraux",
      tags: ["théâtre", "argumentation", "analyse"],
      difficulty: "medium",
      duration: "25 min",
      lastUpdated: "2024-01-22",
      downloads: 203,
      rating: 4.7,
      preview: "L'argumentation au théâtre se manifeste à travers plusieurs procédés : les tirades, les dialogues argumentatifs..."
    },
    {
      id: 5,
      title: "Les suites numériques",
      subject: "Mathématiques",
      type: "Quiz interactif",
      level: "Terminale",
      description: "Quiz adaptatif sur les suites arithmétiques et géométriques",
      tags: ["suites", "récurrence", "limites"],
      difficulty: "medium",
      duration: "20 min",
      lastUpdated: "2024-01-25",
      downloads: 312,
      rating: 4.5,
      preview: "Question 1 : Soit (un) une suite arithmétique de premier terme u0 = 3 et de raison r = 2..."
    },
    {
      id: 6,
      title: "Structures de données avancées",
      subject: "NSI",
      type: "Projet guidé",
      level: "Terminale",
      description: "Implémentation d'arbres binaires et de tables de hachage",
      tags: ["structures", "arbres", "hachage"],
      difficulty: "hard",
      duration: "90 min",
      lastUpdated: "2024-01-23",
      downloads: 98,
      rating: 4.8,
      preview: "Projet : Créer une classe ArbreBinaire avec les méthodes d'insertion, de recherche et de parcours..."
    }
  ];

  const subjects = ["Mathématiques", "NSI", "Physique-Chimie", "Français", "Philosophie"];
  const types = ["Fiche de révision", "Cours interactif", "Exercices corrigés", "Méthode", "Quiz interactif", "Projet guidé"];
  const levels = ["Seconde", "Première", "Terminale"];

  useEffect(() => {
    setContent(demoContent);
  }, []);

  const filteredContent = content.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesSubject = selectedSubject === 'all' || item.subject === selectedSubject;
    const matchesType = selectedType === 'all' || item.type === selectedType;
    const matchesLevel = selectedLevel === 'all' || item.level === selectedLevel;

    return matchesSearch && matchesSubject && matchesType && matchesLevel;
  });

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyLabel = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'Facile';
      case 'medium': return 'Moyen';
      case 'hard': return 'Difficile';
      default: return 'Non défini';
    }
  };

  const handleDownload = async (contentId) => {
    setLoading(true);
    try {
      // Simulation d'un téléchargement
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Ici, on ferait appel à l'API pour générer et télécharger le document
      console.log(`Téléchargement du contenu ${contentId}`);
      
      // Mise à jour du compteur de téléchargements
      setContent(prev => prev.map(item => 
        item.id === contentId 
          ? { ...item, downloads: item.downloads + 1 }
          : item
      ));
    } catch (error) {
      console.error('Erreur lors du téléchargement:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = (contentId) => {
    const item = content.find(c => c.id === contentId);
    if (item) {
      // Ouvrir une modal de prévisualisation
      console.log('Prévisualisation:', item);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* En-tête */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          📚 Bibliothèque de Contenu
        </h1>
        <p className="text-gray-600">
          Accédez à une vaste collection de ressources pédagogiques personnalisées par ARIA
        </p>
      </div>

      {/* Barre de recherche et filtres */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {/* Recherche */}
          <div className="lg:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🔍 Rechercher
            </label>
            <input
              type="text"
              placeholder="Titre, description, tags..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Filtre par matière */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📖 Matière
            </label>
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Toutes</option>
              {subjects.map(subject => (
                <option key={subject} value={subject}>{subject}</option>
              ))}
            </select>
          </div>

          {/* Filtre par type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📄 Type
            </label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Tous</option>
              {types.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>

          {/* Filtre par niveau */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🎓 Niveau
            </label>
            <select
              value={selectedLevel}
              onChange={(e) => setSelectedLevel(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Tous</option>
              {levels.map(level => (
                <option key={level} value={level}>{level}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Statistiques de recherche */}
        <div className="mt-4 flex items-center justify-between text-sm text-gray-600">
          <span>
            {filteredContent.length} ressource{filteredContent.length !== 1 ? 's' : ''} trouvée{filteredContent.length !== 1 ? 's' : ''}
          </span>
          <div className="flex items-center space-x-4">
            <span>📊 {content.reduce((sum, item) => sum + item.downloads, 0)} téléchargements total</span>
            <span>⭐ Note moyenne: 4.7/5</span>
          </div>
        </div>
      </div>

      {/* Onglets de catégories */}
      <Tabs defaultValue="all" className="mb-6">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="all">Tout</TabsTrigger>
          <TabsTrigger value="recent">Récent</TabsTrigger>
          <TabsTrigger value="popular">Populaire</TabsTrigger>
          <TabsTrigger value="recommended">Recommandé</TabsTrigger>
          <TabsTrigger value="favorites">Favoris</TabsTrigger>
          <TabsTrigger value="downloaded">Téléchargés</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="mt-6">
          {/* Grille de contenu */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredContent.map((item) => (
              <Card key={item.id} className="hover:shadow-lg transition-shadow duration-200">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg font-semibold text-gray-900 mb-2">
                        {item.title}
                      </CardTitle>
                      <div className="flex items-center space-x-2 mb-2">
                        <Badge variant="outline" className="text-xs">
                          {item.subject}
                        </Badge>
                        <Badge variant="outline" className="text-xs">
                          {item.level}
                        </Badge>
                        <Badge className={`text-xs ${getDifficultyColor(item.difficulty)}`}>
                          {getDifficultyLabel(item.difficulty)}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex items-center text-yellow-500">
                      <span className="text-sm">⭐ {item.rating}</span>
                    </div>
                  </div>
                </CardHeader>

                <CardContent>
                  <div className="space-y-3">
                    {/* Type et durée */}
                    <div className="flex items-center justify-between text-sm text-gray-600">
                      <span className="flex items-center">
                        📄 {item.type}
                      </span>
                      <span className="flex items-center">
                        ⏱️ {item.duration}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-sm text-gray-700 line-clamp-2">
                      {item.description}
                    </p>

                    {/* Aperçu du contenu */}
                    <div className="bg-gray-50 rounded-md p-3">
                      <p className="text-xs text-gray-600 font-mono line-clamp-3">
                        {item.preview}
                      </p>
                    </div>

                    {/* Tags */}
                    <div className="flex flex-wrap gap-1">
                      {item.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>

                    {/* Statistiques */}
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>📥 {item.downloads} téléchargements</span>
                      <span>🗓️ {new Date(item.lastUpdated).toLocaleDateString('fr-FR')}</span>
                    </div>

                    {/* Actions */}
                    <div className="flex space-x-2 pt-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handlePreview(item.id)}
                        className="flex-1"
                      >
                        👁️ Aperçu
                      </Button>
                      <Button
                        size="sm"
                        onClick={() => handleDownload(item.id)}
                        disabled={loading}
                        className="flex-1 bg-blue-600 hover:bg-blue-700"
                      >
                        {loading ? '⏳' : '📥'} Télécharger
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Message si aucun résultat */}
          {filteredContent.length === 0 && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Aucune ressource trouvée
              </h3>
              <p className="text-gray-600 mb-4">
                Essayez de modifier vos critères de recherche ou vos filtres
              </p>
              <Button
                onClick={() => {
                  setSearchTerm('');
                  setSelectedSubject('all');
                  setSelectedType('all');
                  setSelectedLevel('all');
                }}
                variant="outline"
              >
                🔄 Réinitialiser les filtres
              </Button>
            </div>
          )}
        </TabsContent>

        {/* Autres onglets avec contenu filtré */}
        <TabsContent value="recent" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredContent
              .sort((a, b) => new Date(b.lastUpdated) - new Date(a.lastUpdated))
              .slice(0, 6)
              .map((item) => (
                <Card key={item.id} className="hover:shadow-lg transition-shadow duration-200">
                  <CardHeader>
                    <CardTitle className="text-lg">{item.title}</CardTitle>
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">{item.subject}</Badge>
                      <Badge className="bg-green-100 text-green-800">Nouveau</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600 mb-4">{item.description}</p>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm" className="flex-1">
                        👁️ Aperçu
                      </Button>
                      <Button size="sm" className="flex-1">
                        📥 Télécharger
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
          </div>
        </TabsContent>

        <TabsContent value="popular" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredContent
              .sort((a, b) => b.downloads - a.downloads)
              .slice(0, 6)
              .map((item) => (
                <Card key={item.id} className="hover:shadow-lg transition-shadow duration-200">
                  <CardHeader>
                    <CardTitle className="text-lg">{item.title}</CardTitle>
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">{item.subject}</Badge>
                      <Badge className="bg-orange-100 text-orange-800">🔥 Populaire</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600 mb-4">{item.description}</p>
                    <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                      <span>📥 {item.downloads} téléchargements</span>
                      <span>⭐ {item.rating}/5</span>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm" className="flex-1">
                        👁️ Aperçu
                      </Button>
                      <Button size="sm" className="flex-1">
                        📥 Télécharger
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
          </div>
        </TabsContent>

        <TabsContent value="recommended" className="mt-6">
          <div className="bg-blue-50 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">
              🎯 Recommandations personnalisées par ARIA
            </h3>
            <p className="text-blue-700">
              Basées sur votre profil d'apprentissage et vos récentes activités
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredContent
              .filter(item => item.rating >= 4.7)
              .slice(0, 6)
              .map((item) => (
                <Card key={item.id} className="hover:shadow-lg transition-shadow duration-200 border-blue-200">
                  <CardHeader>
                    <CardTitle className="text-lg">{item.title}</CardTitle>
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">{item.subject}</Badge>
                      <Badge className="bg-blue-100 text-blue-800">🎯 Recommandé</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600 mb-4">{item.description}</p>
                    <div className="bg-blue-50 rounded-md p-2 mb-4">
                      <p className="text-xs text-blue-700">
                        💡 ARIA recommande cette ressource car elle correspond à votre style d'apprentissage visuel
                      </p>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm" className="flex-1">
                        👁️ Aperçu
                      </Button>
                      <Button size="sm" className="flex-1 bg-blue-600 hover:bg-blue-700">
                        📥 Télécharger
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
          </div>
        </TabsContent>

        <TabsContent value="favorites" className="mt-6">
          <div className="text-center py-12">
            <div className="text-6xl mb-4">❤️</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Vos ressources favorites
            </h3>
            <p className="text-gray-600 mb-4">
              Ajoutez des ressources à vos favoris en cliquant sur le cœur
            </p>
            <Button variant="outline">
              🔍 Parcourir la bibliothèque
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="downloaded" className="mt-6">
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📥</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Vos téléchargements
            </h3>
            <p className="text-gray-600 mb-4">
              Retrouvez ici toutes les ressources que vous avez téléchargées
            </p>
            <Button variant="outline">
              📚 Voir l'historique
            </Button>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ContentLibrary;

