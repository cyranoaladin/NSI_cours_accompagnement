// ===== HERO SECTION - NEXUS RÉUSSITE =====
// Composant JavaScript pour la section héro principale

class HeroSection {
  constructor() {
    this.sectionId = 'hero-section';
    this.initialized = false;
    this.init();
  }

  init() {
    if (this.initialized) return;

    console.log('🚀 Hero Section initialized');

    // Animation d'entrée au chargement
    this.animateOnLoad();

    // Gestion des boutons CTA
    this.setupCTAButtons();

    this.initialized = true;
  }

  animateOnLoad() {
    const heroSection = document.querySelector('#hero-section, .hero-section');
    if (heroSection) {
      // Animation fade-in progressive
      heroSection.style.opacity = '0';
      heroSection.style.transform = 'translateY(20px)';

      setTimeout(() => {
        heroSection.style.transition = 'all 0.8s ease-out';
        heroSection.style.opacity = '1';
        heroSection.style.transform = 'translateY(0)';
      }, 100);
    }
  }

  setupCTAButtons() {
    // Bouton diagnostic gratuit
    const diagnosticBtn = document.querySelector('[href="#diagnostic"]');
    if (diagnosticBtn) {
      diagnosticBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.handleDiagnosticClick();
      });
    }

    // Bouton référent
    const referentBtn = document.querySelector('button[onclick*="scheduleReferentCall"]');
    if (referentBtn) {
      referentBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (typeof scheduleReferentCall === 'function') {
          scheduleReferentCall();
        }
      });
    }
  }

  handleDiagnosticClick() {
    // Scroll vers la section diagnostic avec animation
    const diagnosticSection = document.querySelector('#diagnostic');
    if (diagnosticSection) {
      diagnosticSection.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    } else {
      // Fallback : déclencher le calendrier de réservation
      if (typeof scheduleFreeDiagnostic === 'function') {
        scheduleFreeDiagnostic();
      }
    }
  }

  // Méthode pour mise à jour dynamique du contenu
  updateContent(newContent) {
    const heroTitle = document.querySelector('#hero-section h1, .hero-section h1');
    const heroSubtitle = document.querySelector('#hero-section p, .hero-section p');

    if (heroTitle && newContent.title) {
      heroTitle.innerHTML = newContent.title;
    }

    if (heroSubtitle && newContent.subtitle) {
      heroSubtitle.innerHTML = newContent.subtitle;
    }
  }

  // Animation de hover sur les boutons
  addButtonAnimations() {
    const buttons = document.querySelectorAll('#hero-section button, #hero-section a.btn');
    buttons.forEach(button => {
      button.addEventListener('mouseenter', () => {
        button.style.transform = 'scale(1.05)';
        button.style.boxShadow = '0 8px 25px rgba(59, 130, 246, 0.3)';
      });

      button.addEventListener('mouseleave', () => {
        button.style.transform = 'scale(1)';
        button.style.boxShadow = '';
      });
    });
  }
}

// Auto-initialisation quand le DOM est prêt
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.heroSection = new HeroSection();
  });
} else {
  window.heroSection = new HeroSection();
}

// Export pour utilisation modulaire
if (typeof module !== 'undefined' && module.exports) {
  module.exports = HeroSection;
}
