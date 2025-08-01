'use client';

import { BookOpen, Download, Eye, Filter, Search, Star } from 'lucide-react';
import { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

const ContentLibrary = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedLevel, setSelectedLevel] = useState('all');

  const categories = [
    { id: 'all', name: 'Tout', count: 156 },
    { id: 'algorithms', name: 'Algorithmique', count: 45 },
    { id: 'programming', name: 'Programmation', count: 52 },
    { id: 'databases', name: 'Bases de Données', count: 28 },
    { id: 'ai', name: 'Intelligence Artificielle', count: 31 }
  ];

  const levels = [
    { id: 'all', name: 'Tous niveaux' },
    { id: 'beginner', name: 'Débutant' },
    { id: 'intermediate', name: 'Intermédiaire' },
    { id: 'advanced', name: 'Avancé' }
  ];

  const content = [
    {
      id: 1,
      title: "Introduction aux Algorithmes de Tri",
      description: "Comprendre les algorithmes de tri bubble sort, insertion sort et quick sort",
      category: "algorithms",
      level: "beginner",
      type: "document",
      rating: 4.8,
      downloads: 1247,
      author: "Dr. Marie Dubois",
      date: "2024-01-15",
      tags: ["Python", "Tri", "Complexité"]
    },
    {
      id: 2,
      title: "Structures de Données Avancées",
      description: "Arbres binaires, graphes et tables de hachage expliqués avec exemples",
      category: "programming",
      level: "advanced",
      type: "video",
      rating: 4.9,
      downloads: 892,
      author: "Prof. Jean-Luc Martin",
      date: "2024-01-20",
      tags: ["Structures", "Arbres", "Graphes"]
    },
    {
      id: 3,
      title: "SQL pour Débutants - Guide Complet",
      description: "Maîtriser les requêtes SQL de base aux requêtes complexes",
      category: "databases",
      level: "beginner",
      type: "document",
      rating: 4.7,
      downloads: 2104,
      author: "Dr. Sophie Laurent",
      date: "2024-01-10",
      tags: ["SQL", "Requêtes", "Base de données"]
    },
    {
      id: 4,
      title: "Machine Learning avec Python",
      description: "Introduction pratique au machine learning avec scikit-learn",
      category: "ai",
      level: "intermediate",
      type: "tutorial",
      rating: 4.9,
      downloads: 1567,
      author: "Prof. Alexandre Petit",
      date: "2024-01-25",
      tags: ["Python", "ML", "Scikit-learn"]
    },
    {
      id: 5,
      title: "Optimisation d'Algorithmes",
      description: "Techniques d'optimisation et analyse de complexité",
      category: "algorithms",
      level: "advanced",
      type: "document",
      rating: 4.6,
      downloads: 743,
      author: "Dr. Marie Dubois",
      date: "2024-01-18",
      tags: ["Optimisation", "Complexité", "Performance"]
    },
    {
      id: 6,
      title: "Développement Web avec React",
      description: "Créer des applications web modernes avec React et Next.js",
      category: "programming",
      level: "intermediate",
      type: "video",
      rating: 4.8,
      downloads: 1893,
      author: "Prof. Alexandre Petit",
      date: "2024-01-22",
      tags: ["React", "Next.js", "Web"]
    }
  ];

  const filteredContent = content.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    const matchesLevel = selectedLevel === 'all' || item.level === selectedLevel;

    return matchesSearch && matchesCategory && matchesLevel;
  });

  const getTypeIcon = (type) => {
    switch (type) {
      case 'document': return '📄';
      case 'video': return '🎥';
      case 'tutorial': return '📖';
      default: return '📄';
    }
  };

  const getLevelColor = (level) => {
    switch (level) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Bibliothèque de Contenu</h1>
          <p className="text-gray-600">Accédez à une vaste collection de ressources pédagogiques NSI</p>
        </div>

        {/* Search and Filters */}
        <Card className="mb-8">
          <CardContent className="p-6">
            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <input
                  type="text"
                  placeholder="Rechercher des ressources..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>

              {/* Category Filter */}
              <select
                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name} ({category.count})
                  </option>
                ))}
              </select>

              {/* Level Filter */}
              <select
                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                value={selectedLevel}
                onChange={(e) => setSelectedLevel(e.target.value)}
              >
                {levels.map(level => (
                  <option key={level.id} value={level.id}>
                    {level.name}
                  </option>
                ))}
              </select>

              <Button variant="outline" className="flex items-center gap-2">
                <Filter className="h-4 w-4" />
                Filtres avancés
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredContent.map((item) => (
            <Card key={item.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">{getTypeIcon(item.type)}</span>
                    <div>
                      <CardTitle className="text-lg line-clamp-2">{item.title}</CardTitle>
                      <CardDescription className="line-clamp-2 mt-1">
                        {item.description}
                      </CardDescription>
                    </div>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                <div className="space-y-4">
                  {/* Tags */}
                  <div className="flex flex-wrap gap-1">
                    {item.tags.map((tag, index) => (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                        {tag}
                      </span>
                    ))}
                    <span className={`px-2 py-1 text-xs rounded-full ${getLevelColor(item.level)}`}>
                      {levels.find(l => l.id === item.level)?.name}
                    </span>
                  </div>

                  {/* Author and Date */}
                  <div className="text-sm text-gray-600">
                    <p>Par {item.author}</p>
                    <p>{new Date(item.date).toLocaleDateString('fr-FR')}</p>
                  </div>

                  {/* Rating and Downloads */}
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-1">
                      <Star className="h-4 w-4 text-yellow-500 fill-current" />
                      <span>{item.rating}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Download className="h-4 w-4 text-gray-400" />
                      <span>{item.downloads.toLocaleString()}</span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <Button className="flex-1 flex items-center gap-2" size="sm">
                      <Eye className="h-4 w-4" />
                      Voir
                    </Button>
                    <Button variant="outline" className="flex-1 flex items-center gap-2" size="sm">
                      <Download className="h-4 w-4" />
                      Télécharger
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* No Results */}
        {filteredContent.length === 0 && (
          <Card className="text-center py-12">
            <CardContent>
              <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun contenu trouvé</h3>
              <p className="text-gray-600">
                Essayez de modifier vos critères de recherche ou de filtrage.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default ContentLibrary;
