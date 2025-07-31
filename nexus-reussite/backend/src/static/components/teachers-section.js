// ===== TEACHERS SECTION - NEXUS RÉUSSITE =====
// Composant JavaScript pour la section enseignants (profils anonymes stratégiques)

class TeachersSection {
  constructor() {
    this.sectionId = 'teachers-section';
    this.teacherProfiles = this.getStrategicProfiles();
    this.initialized = false;
    this.init();
  }

  // PROFILS ENSEIGNANTS ANONYMES STRATÉGIQUES (selon vos spécifications)
  getStrategicProfiles() {
    return [
      {
        id: 'maths-excellence',
        title: 'L\'Excellence en Mathématiques',
        icon: '📊',
        color: 'blue',
        badges: ['Professeur Agrégé', 'Spécialiste Bac Français', '15+ ans d\'expérience'],
        description: 'Notre pôle mathématiques est dirigé par des enseignants agrégés et certifiés, reconnus pour leur capacité à préparer les élèves aux plus hautes exigences du baccalauréat et des concours post-bac.',
        specialties: ['Analyse et Géométrie', 'Probabilités et Statistiques', 'Spécialité Mathématiques'],
        results: '98% de réussite au Bac',
        experience: 'Anciens professeurs lycées français'
      },
      {
        id: 'nsi-expertise-1',
        title: 'L\'Expertise en NSI - Pôle 1',
        icon: '💻',
        color: 'green',
        badges: ['Diplômé DIU NSI', 'Expert Python & Projets', 'Préparation Grand Oral'],
        description: 'Notre premier spécialiste NSI, fort de son diplôme universitaire en informatique, offre un accompagnement pointu sur les aspects techniques et théoriques du programme, de l\'algorithmique à la conception de projets complets.',
        specialties: ['Python Avancé', 'Bases de Données', 'Algorithmes et Structures'],
        results: '100% d\'admissions en études sup.',
        experience: 'Formation DIU NSI certifiée'
      },
      {
        id: 'nsi-expertise-2',
        title: 'L\'Expertise en NSI - Pôle 2',
        icon: '🔧',
        color: 'green',
        badges: ['Diplômé DIU NSI', 'Spécialiste Web & Réseaux', 'Projets Innovants'],
        description: 'Notre second expert NSI se concentre sur les applications web, les réseaux et l\'innovation technologique. Il guide les élèves dans la réalisation de projets ambitieux pour le Grand Oral.',
        specialties: ['Développement Web', 'Réseaux et Internet', 'Intelligence Artificielle'],
        results: 'Projets primés aux concours',
        experience: 'Expertise industrie + enseignement'
      },
      {
        id: 'physique-rigueur-1',
        title: 'La Rigueur en Physique-Chimie - Pôle 1',
        icon: '⚗️',
        color: 'purple',
        badges: ['Professeur Certifié', 'Pédagogie par l\'expérience', 'Annales du Bac'],
        description: 'Avec une approche qui lie la théorie aux applications concrètes, notre premier enseignant de Physique-Chimie démystifie les concepts les plus complexes et entraîne les élèves à la résolution de problèmes type bac.',
        specialties: ['Mécanique et Énergies', 'Chimie Organique', 'Ondes et Particules'],
        results: '95% de mentions au Bac',
        experience: 'Méthode expérimentale éprouvée'
      },
      {
        id: 'physique-rigueur-2',
        title: 'La Rigueur en Physique-Chimie - Pôle 2',
        icon: '🔬',
        color: 'purple',
        badges: ['Professeur Certifié', 'Spécialiste Thermodynamique', 'Prépa Sciences'],
        description: 'Notre second spécialiste Physique-Chimie excelle dans la préparation aux études scientifiques supérieures. Il maîtrise parfaitement les exigences des classes préparatoires et des écoles d\'ingénieurs.',
        specialties: ['Thermodynamique', 'Électricité Avancée', 'Transformation Chimique'],
        results: 'Admissions en prépa scientifique',
        experience: 'Formation classes préparatoires'
      },
      {
        id: 'coaching-strategique',
        title: 'Le Coaching Stratégique',
        icon: '🎯',
        color: 'orange',
        badges: ['Spécialiste Orientation', 'Méthodologie', 'Gestion du Stress'],
        description: 'Notre équipe de coaching est spécialisée dans l\'accompagnement du Grand Oral, la méthodologie de travail et la construction des dossiers d\'orientation comme Parcoursup.',
        specialties: ['Grand Oral', 'Parcoursup', 'Méthodes de Travail'],
        results: '90% d\'admissions en 1er vœu',
        experience: 'Psychologie scolaire + orientation'
      }
    ];
  }

  init() {
    if (this.initialized) return;

    console.log('👨‍🏫 Teachers Section initialized with strategic anonymous profiles');

    // Mise à jour des profils existants
    this.updateExistingProfiles();

    // Ajout d'interactions
    this.setupInteractions();

    // Animation d'entrée
    this.animateProfiles();

    this.initialized = true;
  }

  updateExistingProfiles() {
    const profileCards = document.querySelectorAll('.teacher-card, .profile-card, [data-teacher]');

    if (profileCards.length === 0) {
      console.log('📝 Aucun profil enseignant trouvé pour mise à jour');
      return;
    }

    profileCards.forEach((card, index) => {
      if (this.teacherProfiles[index]) {
        this.updateProfileCard(card, this.teacherProfiles[index]);
      }
    });
  }

  updateProfileCard(cardElement, profile) {
    // Mise à jour du titre
    const titleElement = cardElement.querySelector('.teacher-title, [data-title]');
    if (titleElement) {
      titleElement.textContent = profile.title;
    }

    // Mise à jour de la description
    const descElement = cardElement.querySelector('.teacher-description, [data-description]');
    if (descElement) {
      descElement.textContent = profile.description;
    }

    // Ajout de l'icône
    const iconElement = cardElement.querySelector('.teacher-icon, [data-icon]');
    if (iconElement) {
      iconElement.textContent = profile.icon;
    }

    // Mise à jour des badges
    this.updateBadges(cardElement, profile.badges);

    // Mise à jour des spécialités
    this.updateSpecialties(cardElement, profile.specialties);

    // Ajout des résultats
    this.addResults(cardElement, profile.results);

    // Application de la couleur thématique
    this.applyColorTheme(cardElement, profile.color);
  }

  updateBadges(cardElement, badges) {
    const badgeContainer = cardElement.querySelector('.badges-container, [data-badges]');

    if (!badgeContainer) {
      // Créer un conteneur de badges
      const newContainer = document.createElement('div');
      newContainer.className = 'badges-container flex flex-wrap gap-2 mb-4';
      cardElement.appendChild(newContainer);
    }

    const container = cardElement.querySelector('.badges-container, [data-badges]');
    container.innerHTML = ''; // Vider le conteneur

    badges.forEach(badge => {
      const badgeElement = document.createElement('span');
      badgeElement.className = 'badge inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium';
      badgeElement.textContent = badge;
      container.appendChild(badgeElement);
    });
  }

  updateSpecialties(cardElement, specialties) {
    const specialtiesContainer = cardElement.querySelector('.specialties-container, [data-specialties]');

    if (!specialtiesContainer) {
      const newContainer = document.createElement('div');
      newContainer.className = 'specialties-container mt-3';
      cardElement.appendChild(newContainer);
    }

    const container = cardElement.querySelector('.specialties-container, [data-specialties]');
    container.innerHTML = '<h4 class="font-medium text-sm text-gray-700 mb-2">Spécialités :</h4>';

    const list = document.createElement('ul');
    list.className = 'text-sm text-gray-600 space-y-1';

    specialties.forEach(specialty => {
      const listItem = document.createElement('li');
      listItem.innerHTML = `• ${specialty}`;
      list.appendChild(listItem);
    });

    container.appendChild(list);
  }

  addResults(cardElement, results) {
    const existingResults = cardElement.querySelector('.results-badge');
    if (existingResults) {
      existingResults.textContent = results;
      return;
    }

    const resultsBadge = document.createElement('div');
    resultsBadge.className = 'results-badge bg-green-100 text-green-800 px-3 py-1 rounded-lg text-sm font-semibold mt-3';
    resultsBadge.textContent = results;
    cardElement.appendChild(resultsBadge);
  }

  applyColorTheme(cardElement, color) {
    const colorClasses = {
      blue: 'border-blue-200 hover:border-blue-300',
      green: 'border-green-200 hover:border-green-300',
      purple: 'border-purple-200 hover:border-purple-300',
      orange: 'border-orange-200 hover:border-orange-300'
    };

    cardElement.className += ` ${colorClasses[color] || colorClasses.blue}`;
  }

  setupInteractions() {
    const profileCards = document.querySelectorAll('.teacher-card, .profile-card, [data-teacher]');

    profileCards.forEach((card, index) => {
      card.addEventListener('mouseenter', () => {
        this.animateCardHover(card, true);
      });

      card.addEventListener('mouseleave', () => {
        this.animateCardHover(card, false);
      });

      card.addEventListener('click', () => {
        this.showProfileDetails(this.teacherProfiles[index]);
      });
    });
  }

  animateCardHover(card, isEnter) {
    if (isEnter) {
      card.style.transform = 'translateY(-8px)';
      card.style.boxShadow = '0 12px 24px rgba(0, 0, 0, 0.15)';
    } else {
      card.style.transform = 'translateY(0)';
      card.style.boxShadow = '';
    }
  }

  animateProfiles() {
    const profileCards = document.querySelectorAll('.teacher-card, .profile-card, [data-teacher]');

    profileCards.forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';

      setTimeout(() => {
        card.style.transition = 'all 0.6s ease-out';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, index * 200); // Animation en cascade
    });
  }

  showProfileDetails(profile) {
    const detailsHtml = `
            <div class="profile-details-modal fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
                <div class="bg-white rounded-2xl p-6 max-w-md w-full">
                    <div class="text-center mb-4">
                        <div class="text-4xl mb-2">${profile.icon}</div>
                        <h3 class="text-xl font-bold">${profile.title}</h3>
                    </div>
                    <p class="text-gray-600 mb-4">${profile.description}</p>
                    <div class="mb-4">
                        <strong>Expérience :</strong> ${profile.experience}
                    </div>
                    <div class="text-center">
                        <div class="bg-green-100 text-green-800 px-3 py-2 rounded-lg inline-block">
                            ${profile.results}
                        </div>
                    </div>
                    <button onclick="this.parentElement.parentElement.remove()" class="mt-4 w-full bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300">
                        Fermer
                    </button>
                </div>
            </div>
        `;

    document.body.insertAdjacentHTML('beforeend', detailsHtml);
  }
}

// Auto-initialisation
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.teachersSection = new TeachersSection();
  });
} else {
  window.teachersSection = new TeachersSection();
}

// Export modulaire
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TeachersSection;
}
