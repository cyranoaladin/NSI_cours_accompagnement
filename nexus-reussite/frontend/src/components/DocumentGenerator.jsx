'use client';

import { Download, File, FileText, Settings } from 'lucide-react';
import { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

const DocumentGenerator = () => {
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [formData, setFormData] = useState({
    title: '',
    subject: '',
    level: 'terminale',
    duration: '2h',
    difficulty: 'intermediate',
    topics: [],
    includeCorrection: true,
    format: 'pdf'
  });

  const templates = [
    {
      id: 'exam',
      name: 'Sujet d\'Examen',
      description: 'Génère un sujet d\'examen complet avec questions théoriques et pratiques',
      icon: '📝',
      estimatedTime: '10-15 min'
    },
    {
      id: 'quiz',
      name: 'QCM Rapide',
      description: 'Crée un questionnaire à choix multiples pour évaluer les connaissances',
      icon: '❓',
      estimatedTime: '5-10 min'
    }
  ];

  const topics = [
    'Algorithmique',
    'Structures de données',
    'Programmation Python',
    'Bases de données'
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleTopicToggle = (topic) => {
    setFormData(prev => ({
      ...prev,
      topics: prev.topics.includes(topic)
        ? prev.topics.filter(t => t !== topic)
        : [...prev.topics, topic]
    }));
  };

  const handleGenerate = async () => {
    console.log('Génération de document avec:', { selectedTemplate, formData });
    alert('Document généré avec succès ! (Simulation)');
  };

  const isFormValid = selectedTemplate && formData.title && formData.subject && formData.topics.length > 0;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Générateur de Documents</h1>
          <p className="text-gray-600">
            Créez automatiquement des supports pédagogiques personnalisés avec l'IA
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Card className="mb-6">
              <CardHeader>
                <CardTitle>1. Choisissez un modèle</CardTitle>
                <CardDescription>Sélectionnez le type de document à générer</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {templates.map((template) => (
                    <div
                      key={template.id}
                      className={`p-4 border-2 rounded-lg cursor-pointer transition-colors ${selectedTemplate === template.id
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                        }`}
                      onClick={() => setSelectedTemplate(template.id)}
                    >
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-2xl">{template.icon}</span>
                        <h3 className="font-medium">{template.name}</h3>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{template.description}</p>
                      <p className="text-xs text-blue-600">⏱️ {template.estimatedTime}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {selectedTemplate && (
              <Card>
                <CardHeader>
                  <CardTitle>2. Configuration du document</CardTitle>
                  <CardDescription>Personnalisez votre document selon vos besoins</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Titre du document</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                        placeholder="Ex: Contrôle NSI - Algorithmique"
                        value={formData.title}
                        onChange={(e) => handleInputChange('title', e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Matière</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                        placeholder="Ex: NSI - Numérique et Sciences Informatiques"
                        value={formData.subject}
                        onChange={(e) => handleInputChange('subject', e.target.value)}
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Sujets à inclure</label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      {topics.map((topic) => (
                        <label key={topic} className="flex items-center space-x-2 cursor-pointer">
                          <input
                            type="checkbox"
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            checked={formData.topics.includes(topic)}
                            onChange={() => handleTopicToggle(topic)}
                          />
                          <span className="text-sm">{topic}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          <div>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Actions
                </CardTitle>
              </CardHeader>
              <CardContent>
                {selectedTemplate ? (
                  <div className="space-y-4">
                    <Button
                      className="w-full"
                      onClick={handleGenerate}
                      disabled={!isFormValid}
                    >
                      <FileText className="h-4 w-4 mr-2" />
                      Générer le Document
                    </Button>

                    {isFormValid && (
                      <Button variant="outline" className="w-full">
                        <Download className="h-4 w-4 mr-2" />
                        Télécharger PDF
                      </Button>
                    )}

                    <div className="text-xs text-gray-500 bg-gray-50 p-3 rounded">
                      <File className="h-4 w-4 inline mr-1" />
                      Document au format PDF
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-8">
                    <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
                    <p>Sélectionnez un modèle pour commencer</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentGenerator;
