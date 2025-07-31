// ===== TESTIMONIALS SECTION - NEXUS RÉUSSITE =====
// Composant JavaScript pour la section témoignages (alignement stratégique)

class TestimonialsSection {
  constructor() {
    this.sectionId = 'testimonials-section';
    this.testimonials = this.getStrategicTestimonials();
    this.currentIndex = 0;
    this.autoSlideInterval = null;
    this.init();
  }

  // TÉMOIGNAGES ALIGNÉS STRATÉGIQUEMENT (selon vos spécifications)
  getStrategicTestimonials() {
    return [
      {
        id: 'sarah-m',
        name: 'Sarah M.',
        role: 'Ancienne élève, aujourd\'hui en école d\'ingénieur',
        avatar: '👩‍🎓',
        rating: 5,
        text: 'L\'enseignant de mathématiques qui a fondé Nexus m\'a suivie en Terminale. Sa pédagogie m\'a permis de transformer mes difficultés en une force, aboutissant à une mention Très Bien. Son expertise est un véritable atout.',
        highlight: 'Mention Très Bien obtenue',
        subject: 'Mathématiques'
      },
      {
        id: 'mme-benali',
        name: 'Mme Benali',
        role: 'Mère d\'un ancien élève',
        avatar: '👩‍💼',
        rating: 5,
        text: 'En tant que parent, j\'ai été impressionnée par la rigueur et la modernité de l\'approche de l\'enseignant de NSI. Il a su transmettre à mon fils une passion pour l\'informatique et lui donner des bases solides pour ses études supérieures.',
        highlight: 'Passion pour l\'informatique développée',
        subject: 'NSI'
      },
      {
        id: 'ahmed-k',
        name: 'Ahmed K.',
        role: 'Ancien élève, admis en classe préparatoire',
        avatar: '👨‍🎓',
        rating: 5,
        text: 'La préparation au Grand Oral avec le coach de Nexus est d\'un niveau exceptionnel. Il a su identifier mes points faibles en argumentation et m\'a donné les outils pour présenter mon projet de manière convaincante. C\'était décisif pour mon admission.',
        highlight: 'Admission en classe préparatoire',
        subject: 'Grand Oral'
      }
    ];
  }

  init() {
    console.log('💬 Testimonials Section initialized with strategic content');

    // Mise à jour du contenu si la section existe déjà
    this.updateExistingTestimonials();

    // Configuration du carrousel automatique
    this.setupAutoSlide();

    // Gestion des interactions utilisateur
    this.setupInteractions();
  }

  updateExistingTestimonials() {
    // Recherche des éléments de témoignages existants
    const testimonialCards = document.querySelectorAll('.testimonial-card, [data-testimonial]');

    if (testimonialCards.length === 0) {
      console.log('📝 Aucun élément de témoignage trouvé pour mise à jour');
      return;
    }

    testimonialCards.forEach((card, index) => {
      if (this.testimonials[index]) {
        this.updateTestimonialCard(card, this.testimonials[index]);
      }
    });
  }

  updateTestimonialCard(cardElement, testimonial) {
    // Mise à jour du nom
    const nameElement = cardElement.querySelector('.testimonial-name, [data-name]');
    if (nameElement) {
      nameElement.textContent = testimonial.name;
    }

    // Mise à jour du rôle
    const roleElement = cardElement.querySelector('.testimonial-role, [data-role]');
    if (roleElement) {
      roleElement.textContent = testimonial.role;
    }

    // Mise à jour du texte
    const textElement = cardElement.querySelector('.testimonial-text, [data-text]');
    if (textElement) {
      textElement.textContent = testimonial.text;
    }

    // Mise à jour de l'avatar si présent
    const avatarElement = cardElement.querySelector('.testimonial-avatar, [data-avatar]');
    if (avatarElement) {
      avatarElement.textContent = testimonial.avatar;
    }

    // Ajout de l'indicateur de sujet
    this.addSubjectBadge(cardElement, testimonial.subject);
  }

  addSubjectBadge(cardElement, subject) {
    // Vérifie si un badge existe déjà
    let badge = cardElement.querySelector('.subject-badge');

    if (!badge) {
      badge = document.createElement('div');
      badge.className = 'subject-badge inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium mb-2';

      // Insertion au début de la carte
      cardElement.prepend(badge);
    }

    badge.textContent = subject;
  }

  setupAutoSlide() {
    const testimonialContainer = document.querySelector('.testimonials-container, [data-testimonials]');
    if (!testimonialContainer) return;

    // Auto slide toutes les 6 secondes
    this.autoSlideInterval = setInterval(() => {
      this.nextTestimonial();
    }, 6000);

    // Pause au survol
    testimonialContainer.addEventListener('mouseenter', () => {
      clearInterval(this.autoSlideInterval);
    });

    testimonialContainer.addEventListener('mouseleave', () => {
      this.setupAutoSlide();
    });
  }

  setupInteractions() {
    // Boutons de navigation si présents
    const prevBtn = document.querySelector('.testimonial-prev, [data-testimonial-prev]');
    const nextBtn = document.querySelector('.testimonial-next, [data-testimonial-next]');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => this.prevTestimonial());
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.nextTestimonial());
    }

    // Navigation par clavier
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') this.prevTestimonial();
      if (e.key === 'ArrowRight') this.nextTestimonial();
    });
  }

  nextTestimonial() {
    this.currentIndex = (this.currentIndex + 1) % this.testimonials.length;
    this.updateActiveTestimonial();
  }

  prevTestimonial() {
    this.currentIndex = (this.currentIndex - 1 + this.testimonials.length) % this.testimonials.length;
    this.updateActiveTestimonial();
  }

  updateActiveTestimonial() {
    const testimonialCards = document.querySelectorAll('.testimonial-card, [data-testimonial]');

    testimonialCards.forEach((card, index) => {
      if (index === this.currentIndex) {
        card.classList.add('active', 'opacity-100');
        card.classList.remove('opacity-50');
      } else {
        card.classList.remove('active', 'opacity-100');
        card.classList.add('opacity-50');
      }
    });
  }

  // Méthode pour ajout dynamique de nouveaux témoignages
  addTestimonial(testimonial) {
    this.testimonials.push(testimonial);
    console.log(`✅ Nouveau témoignage ajouté : ${testimonial.name}`);
  }

  // Analytics et tracking
  trackTestimonialView(testimonialId) {
    console.log(`📊 Témoignage vu : ${testimonialId}`);
    // Ici on pourrait ajouter Google Analytics ou autre
  }

  destroy() {
    if (this.autoSlideInterval) {
      clearInterval(this.autoSlideInterval);
    }
    console.log('💬 Testimonials Section détruite');
  }
}

// Auto-initialisation
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.testimonialsSection = new TestimonialsSection();
  });
} else {
  window.testimonialsSection = new TestimonialsSection();
}

// Export modulaire
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TestimonialsSection;
}
