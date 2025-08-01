/**
 * Profils d'enseignants réels - Nexus Réussite
 * Ces profils correspondent aux enseignants réellement disponibles
 */

export const teacherProfiles = [
  {
    id: 'prof_math_001',
    name: 'Professeur de Mathématiques',
    firstName: 'À définir',
    lastName: 'À définir',
    specialties: ['Mathématiques', 'Physique'],
    experience: 'À préciser',
    qualification: 'À préciser',
    rating: 0,
    description: 'Profil à compléter avec les informations du véritable enseignant',
    photo: '/images/placeholder-teacher.jpg',
    availability: [],
    price: 45,
    subjects: ['mathematiques'],
    levels: ['seconde', 'premiere', 'terminale'],
    isActive: false, // Désactivé jusqu'à configuration complète
    contact: {
      email: 'contact@nexus-reussite.com',
      phone: 'À définir'
    }
  },
  {
    id: 'prof_nsi_001',
    name: 'Professeur de NSI',
    firstName: 'À définir',
    lastName: 'À définir',
    specialties: ['NSI', 'Informatique'],
    experience: 'À préciser',
    qualification: 'À préciser',
    rating: 0,
    description: 'Profil à compléter avec les informations du véritable enseignant',
    photo: '/images/placeholder-teacher.jpg',
    availability: [],
    price: 50,
    subjects: ['nsi', 'informatique'],
    levels: ['premiere', 'terminale'],
    isActive: false,
    contact: {
      email: 'contact@nexus-reussite.com',
      phone: 'À définir'
    }
  },
  {
    id: 'prof_physique_001',
    name: 'Professeur de Physique-Chimie',
    firstName: 'À définir',
    lastName: 'À définir',
    specialties: ['Physique', 'Chimie'],
    experience: 'À préciser',
    qualification: 'À préciser',
    rating: 0,
    description: 'Profil à compléter avec les informations du véritable enseignant',
    photo: '/images/placeholder-teacher.jpg',
    availability: [],
    price: 45,
    subjects: ['physique', 'chimie'],
    levels: ['seconde', 'premiere', 'terminale'],
    isActive: false,
    contact: {
      email: 'contact@nexus-reussite.com',
      phone: 'À définir'
    }
  }
];

export const realFormulas = [
  {
    id: 'individual_math',
    name: 'Cours Particulier - Mathématiques',
    type: 'individual',
    price: 45,
    currency: 'TND',
    duration: '1h',
    description: 'Cours particuliers de mathématiques adaptés au programme tunisien',
    features: [
      'Suivi personnalisé selon le niveau de l\'élève',
      'Exercices adaptés aux examens tunisiens',
      'Méthodes pédagogiques modernes',
      'Support de cours inclus',
      'Préparation spéciale Baccalauréat'
    ],
    subjects: ['Mathématiques'],
    levels: ['Seconde', 'Première', 'Terminale'],
    isActive: true
  },
  {
    id: 'individual_nsi',
    name: 'Cours Particulier - NSI',
    type: 'individual',
    price: 50,
    currency: 'TND',
    duration: '1h',
    description: 'Numérique et Sciences Informatiques - Spécialité Terminale',
    features: [
      'Programmation Python avancée',
      'Algorithmique et structures de données',
      'Projets pratiques et concrets',
      'Préparation Grand Oral',
      'Portfolio de projets'
    ],
    subjects: ['NSI', 'Informatique'],
    levels: ['Première', 'Terminale'],
    isActive: true
  },
  {
    id: 'workshop_bac',
    name: 'Stage Intensif BAC',
    type: 'workshop',
    price: 180,
    currency: 'TND',
    duration: '5 jours',
    description: 'Stage intensif de préparation au Baccalauréat',
    features: [
      'Révisions complètes toutes matières',
      'Examens blancs avec correction',
      'Techniques de gestion du stress',
      'Méthodologie de révision',
      'Groupe de 8 élèves maximum'
    ],
    subjects: ['Multi-disciplinaire'],
    levels: ['Terminale'],
    isActive: true
  },
  {
    id: 'grand_oral',
    name: 'Préparation Grand Oral',
    type: 'workshop',
    price: 120,
    currency: 'TND',
    duration: '4 séances',
    description: 'Accompagnement personnalisé pour le Grand Oral',
    features: [
      'Construction du projet personnel',
      'Techniques de présentation orale',
      'Simulation d\'entretien',
      'Gestion du stress',
      'Entraînements filmés avec analyse'
    ],
    subjects: ['Transversal'],
    levels: ['Terminale'],
    isActive: true
  }
];

export const testimonials = [
  {
    id: 'testimonial_001',
    name: 'Famille Ben Ahmed',
    text: 'Testimonial à remplacer par un vrai retour client',
    rating: 0,
    date: '2024-01-01',
    verified: false,
    student: {
      level: 'Terminale',
      subject: 'Mathématiques'
    }
  },
  {
    id: 'testimonial_002',
    name: 'Parents d\'élève',
    text: 'Testimonial à remplacer par un vrai retour client',
    rating: 0,
    date: '2024-01-01',
    verified: false,
    student: {
      level: 'Première',
      subject: 'NSI'
    }
  }
];

/**
 * Instructions pour la mise en production:
 *
 * 1. Remplacer tous les "À définir" par les vraies informations
 * 2. Ajouter les vraies photos des enseignants
 * 3. Configurer les créneaux de disponibilité réels
 * 4. Mettre isActive: true après validation
 * 5. Ajouter les vrais témoignages clients
 * 6. Vérifier les tarifs avec la direction
 */
