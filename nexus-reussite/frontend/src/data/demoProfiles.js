// Profils de démonstration pour Nexus Réussite
export const demoStudents = [
  {
    id: 'sarah-2025',
    name: 'Sarah Benali',
    avatar: 'SB',
    grade: 'Terminale S',
    school: 'Lycée Français de Tunis',
    profile: 'excellence',
    level: 4,
    xp: 3250,
    streak: 12,
    subjects: ['Mathématiques', 'NSI', 'Physique', 'Français'],
    progress: {
      overall: 85,
      mathématiques: 88,
      nsi: 82,
      physique: 78,
      français: 90
    },
    learningStyle: {
      visual: 85,
      auditory: 45,
      kinesthetic: 35,
      readingWriting: 60
    },
    badges: [
      'Première série de 10 jours',
      'Expert en fonctions',
      'Maître Python',
      'Orateur confirmé',
      'Analyste de données',
      'Résolveur de problèmes'
    ],
    nextSession: {
      date: '2025-07-23',
      time: '14:00',
      subject: 'Mathématiques',
      teacher: 'M. Dubois',
      topic: 'Révision fonctions exponentielles'
    },
    recentActivities: [
      {
        type: 'achievement',
        message: 'Nouveau badge obtenu !',
        detail: 'Vous avez débloqué "Expert en fonctions"',
        date: '2025-07-22',
        time: '16:30'
      },
      {
        type: 'message',
        message: 'Message de M. Dubois',
        detail: 'Excellent travail sur les exercices de probabilités',
        date: '2025-07-22',
        time: '14:15'
      },
      {
        type: 'notification',
        message: 'Session programmée',
        detail: 'Cours de NSI demain à 16h avec Mme Martin',
        date: '2025-07-21',
        time: '18:00'
      }
    ],
    lastARIAInteraction: '2025-07-22T10:30:00Z',
    preferences: {
      notifications: true,
      emailUpdates: true,
      parentalReports: true,
      studyReminders: true
    },
    parentInfo: {
      name: 'Mme Benali',
      email: 'benali.parent@email.com',
      phone: '+216 XX XXX XXX'
    }
  },
  {
    id: 'ahmed-2025',
    name: 'Ahmed Trabelsi',
    avatar: 'AT',
    grade: 'Première S',
    school: 'Lycée International de Carthage',
    profile: 'rattrapage',
    level: 2,
    xp: 1580,
    streak: 5,
    subjects: ['Mathématiques', 'Physique', 'Français'],
    progress: {
      overall: 62,
      mathématiques: 58,
      physique: 65,
      français: 70
    },
    learningStyle: {
      visual: 40,
      auditory: 75,
      kinesthetic: 60,
      readingWriting: 35
    },
    badges: [
      'Premier pas',
      'Persévérant',
      'Auditeur attentif'
    ],
    nextSession: {
      date: '2025-07-24',
      time: '10:00',
      subject: 'Mathématiques',
      teacher: 'M. Dubois',
      topic: 'Renforcement algèbre'
    },
    recentActivities: [
      {
        type: 'achievement',
        message: 'Progression notable !',
        detail: 'Votre niveau en mathématiques s\'améliore',
        date: '2025-07-22',
        time: '11:45'
      },
      {
        type: 'message',
        message: 'Encouragement du professeur',
        detail: 'Continuez vos efforts, les résultats arrivent !',
        date: '2025-07-21',
        time: '15:20'
      }
    ],
    lastARIAInteraction: '2025-07-21T14:15:00Z',
    preferences: {
      notifications: true,
      emailUpdates: false,
      parentalReports: true,
      studyReminders: true
    },
    parentInfo: {
      name: 'M. Trabelsi',
      email: 'trabelsi.parent@email.com',
      phone: '+216 XX XXX XXX'
    }
  },
  {
    id: 'lea-2025',
    name: 'Léa Moreau',
    avatar: 'LM',
    grade: 'Terminale L',
    school: 'Lycée Français Pierre Mendès France',
    profile: 'excellence',
    level: 5,
    xp: 4750,
    streak: 18,
    subjects: ['Français', 'Philosophie', 'Histoire'],
    progress: {
      overall: 92,
      français: 95,
      philosophie: 88,
      histoire: 90
    },
    learningStyle: {
      visual: 60,
      auditory: 55,
      kinesthetic: 25,
      readingWriting: 90
    },
    badges: [
      'Littéraire accomplie',
      'Philosophe en herbe',
      'Historienne passionnée',
      'Oratrice exceptionnelle',
      'Série de 15 jours',
      'Perfectionniste'
    ],
    nextSession: {
      date: '2025-07-23',
      time: '16:00',
      subject: 'Français',
      teacher: 'Mme Rousseau',
      topic: 'Préparation Grand Oral'
    },
    recentActivities: [
      {
        type: 'achievement',
        message: 'Performance exceptionnelle !',
        detail: 'Note parfaite en dissertation française',
        date: '2025-07-22',
        time: '17:00'
      },
      {
        type: 'message',
        message: 'Félicitations de Mme Rousseau',
        detail: 'Votre analyse littéraire est remarquable',
        date: '2025-07-22',
        time: '12:30'
      }
    ],
    lastARIAInteraction: '2025-07-22T09:45:00Z',
    preferences: {
      notifications: true,
      emailUpdates: true,
      parentalReports: true,
      studyReminders: false
    },
    parentInfo: {
      name: 'Mme Moreau',
      email: 'moreau.parent@email.com',
      phone: '+216 XX XXX XXX'
    }
  },
  {
    id: 'youssef-2025',
    name: 'Youssef Khelifi',
    avatar: 'YK',
    grade: 'Terminale S',
    school: 'Lycée Français de Sousse',
    profile: 'standard',
    level: 3,
    xp: 2340,
    streak: 8,
    subjects: ['NSI', 'Mathématiques', 'Physique'],
    progress: {
      overall: 75,
      nsi: 85,
      mathématiques: 70,
      physique: 68
    },
    learningStyle: {
      visual: 70,
      auditory: 40,
      kinesthetic: 80,
      readingWriting: 45
    },
    badges: [
      'Codeur passionné',
      'Expérimentateur',
      'Innovateur',
      'Série de 7 jours'
    ],
    nextSession: {
      date: '2025-07-24',
      time: '14:00',
      subject: 'NSI',
      teacher: 'Mme Martin',
      topic: 'Projet algorithmique'
    },
    recentActivities: [
      {
        type: 'achievement',
        message: 'Projet NSI validé !',
        detail: 'Votre algorithme de tri est parfaitement optimisé',
        date: '2025-07-22',
        time: '15:45'
      },
      {
        type: 'notification',
        message: 'Nouveau défi disponible',
        detail: 'ARIA vous propose un défi de programmation',
        date: '2025-07-21',
        time: '19:30'
      }
    ],
    lastARIAInteraction: '2025-07-22T13:20:00Z',
    preferences: {
      notifications: true,
      emailUpdates: true,
      parentalReports: false,
      studyReminders: true
    },
    parentInfo: {
      name: 'M. Khelifi',
      email: 'khelifi.parent@email.com',
      phone: '+216 XX XXX XXX'
    }
  },
  {
    id: 'nour-2025',
    name: 'Nour Hamdi',
    avatar: 'NH',
    grade: 'Première S',
    school: 'Lycée Français de Sfax',
    profile: 'standard',
    level: 3,
    xp: 2100,
    streak: 6,
    subjects: ['Mathématiques', 'Physique', 'SVT'],
    progress: {
      overall: 73,
      mathématiques: 75,
      physique: 70,
      svt: 78
    },
    learningStyle: {
      visual: 65,
      auditory: 70,
      kinesthetic: 55,
      readingWriting: 50
    },
    badges: [
      'Scientifique curieuse',
      'Observatrice attentive',
      'Équilibrée'
    ],
    nextSession: {
      date: '2025-07-25',
      time: '10:00',
      subject: 'Physique',
      teacher: 'Dr. Rousseau',
      topic: 'TP Optique'
    },
    recentActivities: [
      {
        type: 'message',
        message: 'Retour positif en SVT',
        detail: 'Votre exposé sur la génétique était très bien structuré',
        date: '2025-07-22',
        time: '11:15'
      },
      {
        type: 'achievement',
        message: 'Progression constante',
        detail: 'Vous maintenez un bon rythme de travail',
        date: '2025-07-21',
        time: '16:00'
      }
    ],
    lastARIAInteraction: '2025-07-21T15:30:00Z',
    preferences: {
      notifications: true,
      emailUpdates: true,
      parentalReports: true,
      studyReminders: true
    },
    parentInfo: {
      name: 'Mme Hamdi',
      email: 'hamdi.parent@email.com',
      phone: '+216 XX XXX XXX'
    }
  }
];

export const demoTeachers = [
  {
    id: 'dubois',
    name: 'M. Dubois',
    avatar: 'MD',
    subject: 'Mathématiques',
    specialties: ['Analyse', 'Probabilités', 'Géométrie'],
    experience: '15 ans',
    rating: 4.8,
    certification: 'Agrégé de Mathématiques',
    school: 'Lycée Français de Tunis',
    bio: 'Professeur agrégé avec 15 ans d\'expérience dans l\'enseignement des mathématiques. Spécialiste de la préparation au baccalauréat et aux concours.',
    achievements: [
      'Agrégation de Mathématiques',
      '95% de réussite au Bac',
      'Formation pédagogie numérique',
      'Membre jury Olympiades'
    ],
    availability: {
      monday: ['14:00-18:00'],
      tuesday: ['09:00-12:00', '14:00-17:00'],
      wednesday: ['14:00-18:00'],
      thursday: ['09:00-12:00', '14:00-17:00'],
      friday: ['14:00-16:00'],
      saturday: ['09:00-12:00']
    },
    contact: {
      email: 'dubois@nexus-reussite.tn',
      phone: '+216 XX XXX XXX'
    }
  },
  {
    id: 'martin',
    name: 'Mme Martin',
    avatar: 'MM',
    subject: 'NSI (Numérique et Sciences Informatiques)',
    specialties: ['Algorithmique', 'Python', 'Bases de données'],
    experience: '8 ans',
    rating: 4.9,
    certification: 'DIU NSI - Certifiée',
    school: 'Lycée International de Carthage',
    bio: 'Professeure certifiée NSI avec diplôme DIU spécialisé. Passionnée par l\'enseignement de la programmation et l\'intelligence artificielle.',
    achievements: [
      'DIU Enseigner l\'Informatique',
      'Certification Python avancé',
      'Projets étudiants primés',
      'Formation IA pédagogique'
    ],
    availability: {
      monday: ['09:00-12:00', '14:00-17:00'],
      tuesday: ['14:00-18:00'],
      wednesday: ['09:00-12:00', '14:00-17:00'],
      thursday: ['14:00-18:00'],
      friday: ['09:00-12:00'],
      saturday: ['14:00-17:00']
    },
    contact: {
      email: 'martin@nexus-reussite.tn',
      phone: '+216 XX XXX XXX'
    }
  },
  {
    id: 'rousseau',
    name: 'Dr. Rousseau',
    avatar: 'DR',
    subject: 'Physique-Chimie',
    specialties: ['Mécanique', 'Optique', 'Thermodynamique'],
    experience: '12 ans',
    rating: 4.7,
    certification: 'Docteur en Physique - Agrégé',
    school: 'Lycée Français Pierre Mendès France',
    bio: 'Docteur en Physique et professeur agrégé. Expert en préparation Grand Oral et en travaux pratiques innovants.',
    achievements: [
      'Doctorat en Physique',
      'Agrégation Physique-Chimie',
      'Recherche en optique quantique',
      'Innovation pédagogique'
    ],
    availability: {
      monday: ['14:00-17:00'],
      tuesday: ['09:00-12:00', '14:00-18:00'],
      wednesday: ['14:00-17:00'],
      thursday: ['09:00-12:00', '14:00-18:00'],
      friday: ['14:00-17:00'],
      saturday: ['09:00-12:00']
    },
    contact: {
      email: 'rousseau@nexus-reussite.tn',
      phone: '+216 XX XXX XXX'
    }
  },
  {
    id: 'bernard',
    name: 'Mme Bernard',
    avatar: 'MB',
    subject: 'Français',
    specialties: ['Littérature', 'Grand Oral', 'Méthodologie'],
    experience: '10 ans',
    rating: 4.8,
    certification: 'Certifiée Lettres Modernes',
    school: 'Lycée Français de Sousse',
    bio: 'Professeure certifiée en Lettres Modernes, spécialiste de la préparation au Grand Oral et de l\'analyse littéraire.',
    achievements: [
      'Certification Lettres Modernes',
      'Formation Grand Oral',
      'Jury concours éloquence',
      'Publications pédagogiques'
    ],
    availability: {
      monday: ['09:00-12:00', '14:00-17:00'],
      tuesday: ['14:00-18:00'],
      wednesday: ['09:00-12:00', '14:00-17:00'],
      thursday: ['14:00-18:00'],
      friday: ['09:00-12:00', '14:00-17:00'],
      saturday: ['09:00-12:00']
    },
    contact: {
      email: 'bernard@nexus-reussite.tn',
      phone: '+216 XX XXX XXX'
    }
  }
];

export const demoDocuments = [
  {
    id: 'doc-math-001',
    title: 'Fonctions Exponentielles - Cours Complet',
    subject: 'Mathématiques',
    type: 'course',
    difficulty: 4,
    estimatedTime: '2-3h de travail',
    progress: 85,
    status: 'in_progress',
    createdAt: '2025-07-20T10:00:00Z',
    lastAccessed: '2025-07-22T14:30:00Z',
    ariaGenerated: true,
    personalizedFor: 'Sarah Benali',
    topics: ['Fonctions exponentielles', 'Dérivées', 'Applications'],
    content: `# Fonctions Exponentielles - Cours Complet

## Objectifs d'apprentissage
- Maîtriser la définition et les propriétés des fonctions exponentielles
- Savoir calculer des dérivées de fonctions exponentielles
- Résoudre des équations et inéquations exponentielles

## I. Définition et propriétés fondamentales...`,
    downloads: 12,
    rating: 4.8,
    tags: ['bac', 'terminale', 'analyse']
  },
  {
    id: 'doc-nsi-002',
    title: 'Algorithmes de Tri - Projet Python',
    subject: 'NSI',
    type: 'project',
    difficulty: 3,
    estimatedTime: '3-4h de travail',
    progress: 60,
    status: 'in_progress',
    createdAt: '2025-07-19T15:30:00Z',
    lastAccessed: '2025-07-22T16:45:00Z',
    ariaGenerated: true,
    personalizedFor: 'Youssef Khelifi',
    topics: ['Tri à bulles', 'Tri rapide', 'Complexité'],
    content: `# Projet Python - Algorithmes de Tri

## Objectif
Implémenter et comparer différents algorithmes de tri...`,
    downloads: 8,
    rating: 4.9,
    tags: ['python', 'algorithmes', 'projet']
  },
  {
    id: 'doc-phys-003',
    title: 'TP Optique - Lentilles Convergentes',
    subject: 'Physique',
    type: 'lab',
    difficulty: 3,
    estimatedTime: '2h de manipulation',
    progress: 100,
    status: 'completed',
    createdAt: '2025-07-18T09:00:00Z',
    lastAccessed: '2025-07-21T11:20:00Z',
    ariaGenerated: false,
    personalizedFor: 'Ahmed Trabelsi',
    topics: ['Optique géométrique', 'Lentilles', 'Formation d\'images'],
    content: `# TP Optique - Lentilles Convergentes

## Matériel nécessaire
- Banc d'optique
- Lentille convergente...`,
    downloads: 15,
    rating: 4.6,
    tags: ['tp', 'optique', 'manipulation']
  },
  {
    id: 'doc-fr-004',
    title: 'Préparation Grand Oral - Méthodologie',
    subject: 'Français',
    type: 'oral',
    difficulty: 4,
    estimatedTime: '1-2h de préparation',
    progress: 40,
    status: 'in_progress',
    createdAt: '2025-07-21T14:00:00Z',
    lastAccessed: '2025-07-22T10:15:00Z',
    ariaGenerated: true,
    personalizedFor: 'Léa Moreau',
    topics: ['Structure présentation', 'Gestion stress', 'Argumentation'],
    content: `# Préparation Grand Oral - Guide Méthodologique

## Structure de la présentation
1. Introduction accrocheuse
2. Développement structuré...`,
    downloads: 25,
    rating: 4.9,
    tags: ['grand oral', 'méthodologie', 'présentation']
  },
  {
    id: 'doc-quiz-005',
    title: 'Quiz Adaptatif - Probabilités',
    subject: 'Mathématiques',
    type: 'quiz',
    difficulty: 3,
    estimatedTime: '20-30 min',
    progress: 100,
    status: 'completed',
    createdAt: '2025-07-22T08:30:00Z',
    lastAccessed: '2025-07-22T09:15:00Z',
    ariaGenerated: true,
    personalizedFor: 'Sarah Benali',
    topics: ['Probabilités conditionnelles', 'Loi binomiale'],
    content: `# Quiz Adaptatif - Probabilités

## Question 1
Dans une urne contenant 5 boules rouges et 3 boules bleues...`,
    downloads: 5,
    rating: 4.7,
    tags: ['quiz', 'probabilités', 'évaluation']
  }
];

export const demoNotifications = [
  {
    id: 'notif-001',
    type: 'success',
    title: 'Document généré avec succès',
    message: 'Votre fiche de révision en mathématiques est prête',
    timestamp: '2025-07-22T16:30:00Z',
    read: false,
    actionUrl: '/documents/doc-math-001'
  },
  {
    id: 'notif-002',
    type: 'info',
    title: 'Nouvelle recommandation ARIA',
    message: 'ARIA suggère de réviser les fonctions logarithmes',
    timestamp: '2025-07-22T14:15:00Z',
    read: false,
    actionUrl: '/aria'
  },
  {
    id: 'notif-003',
    type: 'warning',
    title: 'Session programmée demain',
    message: 'N\'oubliez pas votre cours de NSI à 16h avec Mme Martin',
    timestamp: '2025-07-22T12:00:00Z',
    read: true,
    actionUrl: '/planning'
  },
  {
    id: 'notif-004',
    type: 'success',
    title: 'Nouveau badge débloqué',
    message: 'Félicitations ! Vous avez obtenu le badge "Expert en fonctions"',
    timestamp: '2025-07-22T10:45:00Z',
    read: true,
    actionUrl: '/profile/badges'
  }
];

// Configuration par défaut pour les nouveaux utilisateurs
export const defaultUserConfig = {
  preferences: {
    theme: 'light',
    language: 'fr',
    notifications: {
      email: true,
      push: true,
      sms: false,
      parentalReports: true
    },
    privacy: {
      shareProgress: true,
      allowAnalytics: true,
      parentalAccess: true
    },
    learning: {
      adaptiveDifficulty: true,
      personalizedContent: true,
      gamification: true
    }
  },
  ariaSettings: {
    personality: 'encouraging',
    responseLength: 'medium',
    includeExamples: true,
    visualAids: true,
    voiceEnabled: false
  }
};

export default {
  demoStudents,
  demoTeachers,
  demoDocuments,
  demoNotifications,
  defaultUserConfig
};

