import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

const TeacherProfiles = () => {
  const [selectedTeacher, setSelectedTeacher] = useState(null);
  const [filterSubject, setFilterSubject] = useState('all');

  // Données des enseignants
  const teachers = [
    {
      id: 1,
      name: "Dr. Amina Benali",
      title: "Professeure Agrégée de Mathématiques",
      subjects: ["Mathématiques", "Spécialité Maths"],
      level: "Terminale",
      experience: "15 ans",
      education: [
        "Agrégation de Mathématiques",
        "Doctorat en Mathématiques Appliquées",
        "Master en Pédagogie Numérique"
      ],
      specialties: [
        "Analyse complexe",
        "Probabilités et statistiques",
        "Préparation concours",
        "Méthodes pédagogiques innovantes"
      ],
      achievements: [
        "Formatrice académique",
        "Auteure de manuels scolaires",
        "Jury de concours nationaux",
        "Prix de l'innovation pédagogique 2023"
      ],
      rating: 4.9,
      reviews: 127,
      availability: "Lundi, Mercredi, Vendredi",
      languages: ["Français", "Arabe", "Anglais"],
      methodology: "Approche progressive avec visualisations et applications concrètes. Adaptation au rythme de chaque élève.",
      testimonials: [
        {
          student: "Sarah M.",
          comment: "Grâce à Dr. Benali, j'ai enfin compris les intégrales ! Sa méthode est claire et patiente.",
          rating: 5,
          date: "2024-01-15"
        },
        {
          student: "Ahmed K.",
          comment: "Excellente préparation pour le bac. Résultats au-delà de mes espérances.",
          rating: 5,
          date: "2024-01-10"
        }
      ],
      photo: "/api/placeholder/150/150",
      certifications: ["AEFE", "Agrégation", "Formation continue"],
      price: "120 DT/h"
    },
    {
      id: 2,
      name: "M. Karim Trabelsi",
      title: "Professeur Certifié NSI - DIU",
      subjects: ["NSI", "Informatique", "Python"],
      level: "Première, Terminale",
      experience: "12 ans",
      education: [
        "DIU Enseigner l'Informatique au Lycée",
        "Master en Informatique",
        "Certification Python Institute"
      ],
      specialties: [
        "Programmation Python",
        "Algorithmes et structures de données",
        "Bases de données",
        "Intelligence artificielle",
        "Préparation Grand Oral NSI"
      ],
      achievements: [
        "Formateur DIU NSI",
        "Développeur applications éducatives",
        "Intervenant conférences tech",
        "Mentor concours informatique"
      ],
      rating: 4.8,
      reviews: 89,
      availability: "Mardi, Jeudi, Samedi",
      languages: ["Français", "Arabe", "Anglais"],
      methodology: "Apprentissage par projets concrets. Coding sessions interactives et debugging collaboratif.",
      testimonials: [
        {
          student: "Léa D.",
          comment: "M. Trabelsi rend la programmation accessible et passionnante. Projets très motivants !",
          rating: 5,
          date: "2024-01-20"
        },
        {
          student: "Youssef H.",
          comment: "Préparation parfaite pour le Grand Oral NSI. Confiance retrouvée !",
          rating: 5,
          date: "2024-01-18"
        }
      ],
      photo: "/api/placeholder/150/150",
      certifications: ["AEFE", "DIU NSI", "Python Institute"],
      price: "110 DT/h"
    },
    {
      id: 3,
      name: "Dr. Fatma Mansouri",
      title: "Professeure Agrégée de Physique-Chimie",
      subjects: ["Physique-Chimie", "Sciences"],
      level: "Première, Terminale",
      experience: "18 ans",
      education: [
        "Agrégation de Physique",
        "Doctorat en Physique des Matériaux",
        "Formation pédagogie expérimentale"
      ],
      specialties: [
        "Mécanique quantique",
        "Thermodynamique",
        "Chimie organique",
        "Expériences virtuelles",
        "Préparation CPGE"
      ],
      achievements: [
        "Responsable laboratoire lycée",
        "Formatrice expériences numériques",
        "Jury olympiades scientifiques",
        "Auteure ressources pédagogiques"
      ],
      rating: 4.9,
      reviews: 156,
      availability: "Lundi, Mercredi, Vendredi, Samedi",
      languages: ["Français", "Arabe", "Anglais"],
      methodology: "Expériences concrètes et simulations. Liens théorie-pratique avec exemples du quotidien.",
      testimonials: [
        {
          student: "Nour B.",
          comment: "Les expériences de Dr. Mansouri sont fascinantes. La physique devient concrète !",
          rating: 5,
          date: "2024-01-22"
        },
        {
          student: "Marc L.",
          comment: "Préparation excellente pour les études d'ingénieur. Bases solides acquises.",
          rating: 5,
          date: "2024-01-16"
        }
      ],
      photo: "/api/placeholder/150/150",
      certifications: ["AEFE", "Agrégation", "Sécurité laboratoire"],
      price: "115 DT/h"
    },
    {
      id: 4,
      name: "Mme. Sonia Gharbi",
      title: "Professeure Certifiée de Français",
      subjects: ["Français", "Littérature", "Grand Oral"],
      level: "Première, Terminale",
      experience: "14 ans",
      education: [
        "CAPES de Lettres Modernes",
        "Master en Littérature Française",
        "Formation Grand Oral"
      ],
      specialties: [
        "Analyse littéraire",
        "Expression écrite et orale",
        "Préparation Grand Oral",
        "Méthodologie dissertation",
        "Théâtre et argumentation"
      ],
      achievements: [
        "Jury Grand Oral",
        "Formatrice expression orale",
        "Coordinatrice projets théâtre",
        "Auteure méthodes pédagogiques"
      ],
      rating: 4.8,
      reviews: 134,
      availability: "Mardi, Jeudi, Vendredi",
      languages: ["Français", "Arabe", "Italien"],
      methodology: "Approche créative et interactive. Ateliers d'écriture et débats argumentés.",
      testimonials: [
        {
          student: "Ines K.",
          comment: "Mme Gharbi m'a donné confiance en moi pour l'oral. Méthodes très efficaces !",
          rating: 5,
          date: "2024-01-25"
        },
        {
          student: "Thomas R.",
          comment: "Analyse littéraire devenue passionnante. Résultats en nette progression.",
          rating: 5,
          date: "2024-01-12"
        }
      ],
      photo: "/api/placeholder/150/150",
      certifications: ["AEFE", "CAPES", "Grand Oral"],
      price: "105 DT/h"
    },
    {
      id: 5,
      name: "M. Mehdi Bouaziz",
      title: "Professeur Certifié de Philosophie",
      subjects: ["Philosophie", "Méthodologie", "Grand Oral"],
      level: "Terminale",
      experience: "11 ans",
      education: [
        "CAPES de Philosophie",
        "Master en Philosophie Politique",
        "Formation pensée critique"
      ],
      specialties: [
        "Dissertation philosophique",
        "Explication de texte",
        "Pensée critique",
        "Éthique et morale",
        "Préparation Grand Oral"
      ],
      achievements: [
        "Formateur académique",
        "Animateur cafés philo",
        "Jury concours éloquence",
        "Auteur articles pédagogiques"
      ],
      rating: 4.7,
      reviews: 98,
      availability: "Lundi, Mercredi, Jeudi",
      languages: ["Français", "Arabe", "Allemand"],
      methodology: "Socratic questioning et débats structurés. Développement de l'esprit critique.",
      testimonials: [
        {
          student: "Amira S.",
          comment: "M. Bouaziz rend la philosophie accessible et passionnante. Méthode claire !",
          rating: 5,
          date: "2024-01-19"
        },
        {
          student: "Lucas M.",
          comment: "Préparation parfaite pour le bac philo. Confiance et méthode acquises.",
          rating: 4,
          date: "2024-01-14"
        }
      ],
      photo: "/api/placeholder/150/150",
      certifications: ["AEFE", "CAPES", "Formation continue"],
      price: "100 DT/h"
    }
  ];

  const subjects = ["Mathématiques", "NSI", "Physique-Chimie", "Français", "Philosophie"];

  const filteredTeachers = filterSubject === 'all' 
    ? teachers 
    : teachers.filter(teacher => teacher.subjects.includes(filterSubject));

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={i < Math.floor(rating) ? "text-yellow-400" : "text-gray-300"}>
        ⭐
      </span>
    ));
  };

  const TeacherCard = ({ teacher }) => (
    <Card className="hover:shadow-lg transition-shadow duration-200 cursor-pointer"
          onClick={() => setSelectedTeacher(teacher)}>
      <CardHeader className="pb-4">
        <div className="flex items-start space-x-4">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
            {teacher.name.split(' ').map(n => n[0]).join('')}
          </div>
          <div className="flex-1">
            <CardTitle className="text-lg font-semibold text-gray-900">
              {teacher.name}
            </CardTitle>
            <p className="text-sm text-gray-600 mb-2">{teacher.title}</p>
            <div className="flex items-center space-x-2 mb-2">
              <div className="flex">{renderStars(teacher.rating)}</div>
              <span className="text-sm text-gray-600">
                {teacher.rating} ({teacher.reviews} avis)
              </span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-lg font-bold text-blue-600">{teacher.price}</div>
            <div className="text-xs text-gray-500">par heure</div>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-3">
          {/* Matières enseignées */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-1">Matières</h4>
            <div className="flex flex-wrap gap-1">
              {teacher.subjects.map((subject, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {subject}
                </Badge>
              ))}
            </div>
          </div>

          {/* Spécialités */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-1">Spécialités</h4>
            <div className="flex flex-wrap gap-1">
              {teacher.specialties.slice(0, 3).map((specialty, index) => (
                <Badge key={index} className="text-xs bg-blue-100 text-blue-800">
                  {specialty}
                </Badge>
              ))}
              {teacher.specialties.length > 3 && (
                <Badge className="text-xs bg-gray-100 text-gray-600">
                  +{teacher.specialties.length - 3}
                </Badge>
              )}
            </div>
          </div>

          {/* Certifications */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-1">Certifications</h4>
            <div className="flex flex-wrap gap-1">
              {teacher.certifications.map((cert, index) => (
                <Badge key={index} className="text-xs bg-green-100 text-green-800">
                  ✓ {cert}
                </Badge>
              ))}
            </div>
          </div>

          {/* Expérience et disponibilité */}
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Expérience:</span>
              <div className="font-medium">{teacher.experience}</div>
            </div>
            <div>
              <span className="text-gray-600">Niveau:</span>
              <div className="font-medium">{teacher.level}</div>
            </div>
          </div>

          {/* Méthodologie */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-1">Approche pédagogique</h4>
            <p className="text-xs text-gray-600 line-clamp-2">{teacher.methodology}</p>
          </div>

          {/* Actions */}
          <div className="flex space-x-2 pt-2">
            <Button 
              variant="outline" 
              size="sm" 
              className="flex-1"
              onClick={(e) => {
                e.stopPropagation();
                setSelectedTeacher(teacher);
              }}
            >
              👁️ Profil complet
            </Button>
            <Button 
              size="sm" 
              className="flex-1 bg-blue-600 hover:bg-blue-700"
              onClick={(e) => {
                e.stopPropagation();
                // Logique de réservation
                console.log('Réserver avec', teacher.name);
              }}
            >
              📅 Réserver
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const TeacherDetailModal = ({ teacher, onClose }) => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* En-tête */}
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-start space-x-4">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-2xl">
                {teacher.name.split(' ').map(n => n[0]).join('')}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{teacher.name}</h2>
                <p className="text-gray-600 mb-2">{teacher.title}</p>
                <div className="flex items-center space-x-2">
                  <div className="flex">{renderStars(teacher.rating)}</div>
                  <span className="text-sm text-gray-600">
                    {teacher.rating}/5 ({teacher.reviews} avis)
                  </span>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className="text-right mr-4">
                <div className="text-2xl font-bold text-blue-600">{teacher.price}</div>
                <div className="text-sm text-gray-500">par heure</div>
              </div>
              <Button variant="outline" onClick={onClose}>✕</Button>
            </div>
          </div>

          <Tabs defaultValue="overview" className="w-full">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
              <TabsTrigger value="education">Formation</TabsTrigger>
              <TabsTrigger value="methodology">Méthode</TabsTrigger>
              <TabsTrigger value="reviews">Avis</TabsTrigger>
              <TabsTrigger value="booking">Réservation</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="mt-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold mb-3">Matières enseignées</h3>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {teacher.subjects.map((subject, index) => (
                      <Badge key={index} className="bg-blue-100 text-blue-800">
                        {subject}
                      </Badge>
                    ))}
                  </div>

                  <h3 className="text-lg font-semibold mb-3">Spécialités</h3>
                  <div className="space-y-2">
                    {teacher.specialties.map((specialty, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <span className="text-blue-600">•</span>
                        <span className="text-sm">{specialty}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">Informations pratiques</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Expérience:</span>
                      <span className="font-medium">{teacher.experience}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Niveau:</span>
                      <span className="font-medium">{teacher.level}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Disponibilité:</span>
                      <span className="font-medium">{teacher.availability}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Langues:</span>
                      <span className="font-medium">{teacher.languages.join(', ')}</span>
                    </div>
                  </div>

                  <h3 className="text-lg font-semibold mb-3 mt-6">Réalisations</h3>
                  <div className="space-y-2">
                    {teacher.achievements.map((achievement, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <span className="text-green-600">✓</span>
                        <span className="text-sm">{achievement}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="education" className="mt-6">
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-3">Formation académique</h3>
                  <div className="space-y-3">
                    {teacher.education.map((edu, index) => (
                      <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                          {index + 1}
                        </div>
                        <span>{edu}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">Certifications</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {teacher.certifications.map((cert, index) => (
                      <div key={index} className="p-3 border border-green-200 rounded-lg bg-green-50">
                        <div className="flex items-center space-x-2">
                          <span className="text-green-600">✓</span>
                          <span className="font-medium text-green-800">{cert}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="methodology" className="mt-6">
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-3">Approche pédagogique</h3>
                  <p className="text-gray-700 leading-relaxed">{teacher.methodology}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-semibold text-blue-900 mb-2">🎯 Objectifs</h4>
                    <ul className="text-sm text-blue-800 space-y-1">
                      <li>• Maîtrise des concepts fondamentaux</li>
                      <li>• Développement de l'autonomie</li>
                      <li>• Préparation optimale aux examens</li>
                      <li>• Confiance en soi renforcée</li>
                    </ul>
                  </div>

                  <div className="p-4 bg-green-50 rounded-lg">
                    <h4 className="font-semibold text-green-900 mb-2">⚙️ Méthodes</h4>
                    <ul className="text-sm text-green-800 space-y-1">
                      <li>• Cours interactifs et personnalisés</li>
                      <li>• Exercices progressifs adaptés</li>
                      <li>• Suivi régulier des progrès</li>
                      <li>• Feedback constructif continu</li>
                    </ul>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="reviews" className="mt-6">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Avis des élèves</h3>
                  <div className="flex items-center space-x-2">
                    <div className="flex">{renderStars(teacher.rating)}</div>
                    <span className="font-medium">{teacher.rating}/5</span>
                    <span className="text-gray-600">({teacher.reviews} avis)</span>
                  </div>
                </div>

                <div className="space-y-4">
                  {teacher.testimonials.map((testimonial, index) => (
                    <div key={index} className="p-4 border border-gray-200 rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-sm font-medium">
                            {testimonial.student[0]}
                          </div>
                          <span className="font-medium">{testimonial.student}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="flex">{renderStars(testimonial.rating)}</div>
                          <span className="text-sm text-gray-500">
                            {new Date(testimonial.date).toLocaleDateString('fr-FR')}
                          </span>
                        </div>
                      </div>
                      <p className="text-gray-700 text-sm">{testimonial.comment}</p>
                    </div>
                  ))}
                </div>

                <Button variant="outline" className="w-full">
                  📝 Voir tous les avis
                </Button>
              </div>
            </TabsContent>

            <TabsContent value="booking" className="mt-6">
              <div className="space-y-6">
                <div className="p-6 bg-blue-50 rounded-lg">
                  <h3 className="text-lg font-semibold text-blue-900 mb-4">
                    Réserver un cours avec {teacher.name}
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Type de cours
                      </label>
                      <select className="w-full p-2 border border-gray-300 rounded-md">
                        <option>Cours individuel (1:1)</option>
                        <option>Mini-groupe (3-5 élèves)</option>
                        <option>Stage intensif</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Matière
                      </label>
                      <select className="w-full p-2 border border-gray-300 rounded-md">
                        {teacher.subjects.map((subject, index) => (
                          <option key={index}>{subject}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Date souhaitée
                      </label>
                      <input 
                        type="date" 
                        className="w-full p-2 border border-gray-300 rounded-md"
                        min={new Date().toISOString().split('T')[0]}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Heure souhaitée
                      </label>
                      <select className="w-full p-2 border border-gray-300 rounded-md">
                        <option>09:00 - 10:00</option>
                        <option>10:00 - 11:00</option>
                        <option>14:00 - 15:00</option>
                        <option>15:00 - 16:00</option>
                        <option>16:00 - 17:00</option>
                      </select>
                    </div>
                  </div>

                  <div className="mt-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Message (optionnel)
                    </label>
                    <textarea 
                      className="w-full p-2 border border-gray-300 rounded-md"
                      rows="3"
                      placeholder="Décrivez vos objectifs ou besoins spécifiques..."
                    ></textarea>
                  </div>

                  <div className="mt-6 flex space-x-3">
                    <Button className="flex-1 bg-blue-600 hover:bg-blue-700">
                      📅 Réserver maintenant
                    </Button>
                    <Button variant="outline" className="flex-1">
                      💬 Contacter d'abord
                    </Button>
                  </div>
                </div>

                <div className="p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold mb-2">📋 Informations importantes</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Confirmation sous 24h par le professeur</li>
                    <li>• Annulation gratuite jusqu'à 24h avant</li>
                    <li>• Premier cours d'évaluation offert</li>
                    <li>• Paiement sécurisé après confirmation</li>
                  </ul>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* En-tête */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          👨‍🏫 Nos Enseignants d'Excellence
        </h1>
        <p className="text-gray-600">
          Professeurs certifiés et agrégés des établissements AEFE, experts dans leur domaine
        </p>
      </div>

      {/* Filtres */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium text-gray-700">
            Filtrer par matière:
          </label>
          <select
            value={filterSubject}
            onChange={(e) => setFilterSubject(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">Toutes les matières</option>
            {subjects.map(subject => (
              <option key={subject} value={subject}>{subject}</option>
            ))}
          </select>
          
          <div className="flex-1"></div>
          
          <div className="text-sm text-gray-600">
            {filteredTeachers.length} enseignant{filteredTeachers.length !== 1 ? 's' : ''} disponible{filteredTeachers.length !== 1 ? 's' : ''}
          </div>
        </div>
      </div>

      {/* Grille des enseignants */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredTeachers.map((teacher) => (
          <TeacherCard key={teacher.id} teacher={teacher} />
        ))}
      </div>

      {/* Modal de détail */}
      {selectedTeacher && (
        <TeacherDetailModal 
          teacher={selectedTeacher} 
          onClose={() => setSelectedTeacher(null)} 
        />
      )}

      {/* Section d'information */}
      <div className="mt-12 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            🏆 L'Excellence Pédagogique Nexus Réussite
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">100%</div>
              <div className="text-sm text-gray-600">Enseignants certifiés AEFE</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">15+</div>
              <div className="text-sm text-gray-600">Années d'expérience moyenne</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">4.8/5</div>
              <div className="text-sm text-gray-600">Note moyenne des élèves</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeacherProfiles;

