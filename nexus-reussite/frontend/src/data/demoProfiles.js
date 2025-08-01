export const teacherProfiles = [
  {
    id: 1,
    name: "Dr. Marie Dubois",
    subject: "Algorithmique Avancée",
    experience: "15 ans d'expérience",
    rating: 4.9,
    specialities: ["Python", "Structures de données", "Complexité algorithmique"],
    image: "/api/placeholder/150/150",
    description: "Experte en algorithmique avec une approche pédagogique innovante.",
    availability: "Lundi-Vendredi 9h-18h",
    languages: ["Français", "Anglais"]
  },
  {
    id: 2,
    name: "Prof. Jean-Luc Martin",
    subject: "Bases de Données",
    experience: "12 ans d'expérience",
    rating: 4.8,
    specialities: ["SQL", "NoSQL", "Modélisation de données"],
    image: "/api/placeholder/150/150",
    description: "Spécialiste des systèmes de gestion de bases de données.",
    availability: "Mardi-Samedi 10h-19h",
    languages: ["Français"]
  },
  {
    id: 3,
    name: "Dr. Sophie Laurent",
    subject: "Intelligence Artificielle",
    experience: "10 ans d'expérience",
    rating: 4.9,
    specialities: ["Machine Learning", "Deep Learning", "Computer Vision"],
    image: "/api/placeholder/150/150",
    description: "Docteure en IA, experte en apprentissage automatique.",
    availability: "Lundi-Jeudi 14h-20h",
    languages: ["Français", "Anglais", "Espagnol"]
  },
  {
    id: 4,
    name: "Prof. Alexandre Petit",
    subject: "Développement Web",
    experience: "8 ans d'expérience",
    rating: 4.7,
    specialities: ["React", "Node.js", "TypeScript"],
    image: "/api/placeholder/150/150",
    description: "Développeur full-stack passionné par l'enseignement.",
    availability: "Mercredi-Dimanche 11h-17h",
    languages: ["Français", "Anglais"]
  }
];

export const courseCategories = [
  {
    id: 1,
    name: "Programmation",
    icon: "Code",
    courseCount: 45,
    color: "bg-blue-500"
  },
  {
    id: 2,
    name: "Algorithmique",
    icon: "Zap",
    courseCount: 32,
    color: "bg-green-500"
  },
  {
    id: 3,
    name: "Bases de Données",
    icon: "Database",
    courseCount: 28,
    color: "bg-purple-500"
  },
  {
    id: 4,
    name: "Intelligence Artificielle",
    icon: "Brain",
    courseCount: 19,
    color: "bg-orange-500"
  }
];

export const studentStats = {
  totalStudents: 1247,
  activeStudents: 892,
  completedCourses: 3421,
  averageRating: 4.6
};

export default {
  teacherProfiles,
  courseCategories,
  studentStats
};
