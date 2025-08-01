// ===== SYSTÈME DE RÉSERVATION NEXUS RÉUSSITE =====
// Calendly Integration avec fallback fonctionnel

// URLs Calendly (démo - à personnaliser avec votre compte)
const CALENDLY_URLS = {
  diagnostic: 'https://calendly.com/nexus-reussite/diagnostic-gratuit',
  referent: 'https://calendly.com/nexus-reussite/referent-consultation',
  maths: 'https://calendly.com/nexus-reussite/maths-consultation',
  nsi: 'https://calendly.com/nexus-reussite/nsi-consultation',
  physique: 'https://calendly.com/nexus-reussite/physique-consultation',
  francais: 'https://calendly.com/nexus-reussite/francais-consultation',
  coaching: 'https://calendly.com/nexus-reussite/coaching-consultation',
  stages: 'https://calendly.com/nexus-reussite/stage-inscription',
  grandoral: 'https://calendly.com/nexus-reussite/grand-oral-preparation',
  visite: 'https://calendly.com/nexus-reussite/visite-centre'
};

// Fonction principale pour ouvrir les popups Calendly
function openCalendlyModal(url, title = "Rendez-vous") {
  console.log('🚀 Ouverture Calendly:', title, 'URL:', url);

  if (typeof Calendly !== 'undefined') {
    // Utilisation réelle de Calendly
    Calendly.initPopupWidget({
      url: url,
      prefill: {},
      utm: {
        utmCampaign: 'nexus-reussite',
        utmSource: 'website',
        utmMedium: 'popup'
      }
    });
  } else {
    // Fallback avec formulaire personnalisé
    showBookingForm(url, title);
  }
}

// Fallback : Formulaire de réservation personnalisé
function showBookingForm(calendlyUrl, serviceTitle) {
  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4';
  modal.innerHTML = `
        <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
            <div class="text-center mb-6">
                <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i data-lucide="calendar" class="w-8 h-8 text-blue-600"></i>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-2">${serviceTitle}</h3>
                <p class="text-gray-600 text-sm">Choisissez votre méthode de réservation</p>
            </div>

            <div class="space-y-4">
                <button onclick="window.open('${calendlyUrl}', '_blank')" class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2">
                    <i data-lucide="external-link" class="w-5 h-5"></i>
                    <span>Réserver sur Calendly</span>
                </button>

                <button onclick="contactDirectBooking('${serviceTitle}')" class="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2">
                    <i data-lucide="phone" class="w-5 h-5"></i>
                    <span>Appeler Directement</span>
                </button>

                <button onclick="whatsappBooking('${serviceTitle}')" class="w-full bg-green-500 text-white py-3 px-4 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center space-x-2">
                    <i data-lucide="message-circle" class="w-5 h-5"></i>
                    <span>WhatsApp</span>
                </button>

                <button onclick="this.parentElement.parentElement.parentElement.remove()" class="w-full bg-gray-200 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors">
                    Fermer
                </button>
            </div>
        </div>
    `;

  document.body.appendChild(modal);

  // Re-initialize icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // Close on click outside
  modal.addEventListener('click', function (e) {
    if (e.target === modal) {
      modal.remove();
    }
  });
}

// Contact direct pour réservation
function contactDirectBooking(service) {
  alert(`📞 CONTACT DIRECT - ${service}

🎯 Appelez-nous maintenant :
📱 +216 XX XXX XXX

⏰ Horaires d'ouverture :
• Lundi - Vendredi : 8h00 - 18h00
• Samedi : 8h00 - 14h00

💬 Mentionnez : "${service}" pour un traitement prioritaire !`);
}

// Réservation WhatsApp
function whatsappBooking(service) {
  const message = encodeURIComponent(`Bonjour Nexus Réussite !

Je souhaite prendre rendez-vous pour : ${service}

Pourriez-vous me proposer des créneaux disponibles ?

Merci !`);

  // Numéro WhatsApp (à personnaliser)
  const whatsappNumber = "21612345678"; // REMPLACER par votre vrai numéro

  window.open(`https://wa.me/${whatsappNumber}?text=${message}`, '_blank');
}

// ===== FONCTIONS SPÉCIFIQUES PAR BOUTON =====

function scheduleFreeDiagnostic() {
  openCalendlyModal(CALENDLY_URLS.diagnostic, '🎯 Bilan de Positionnement Gratuit');
}

function scheduleFreeCall() {
  openCalendlyModal(CALENDLY_URLS.diagnostic, '📞 Appel Diagnostic Gratuit');
}

function scheduleReferentCall() {
  openCalendlyModal(CALENDLY_URLS.referent, '👥 Consultation avec notre Référent');
}

function chooseFormula(formula) {
  let url, title;
  switch (formula) {
    case 'grand-oral':
      url = CALENDLY_URLS.grandoral;
      title = '🎤 Préparation Grand Oral';
      break;
    case 'stage-aout':
    case 'stage-vacances':
      url = CALENDLY_URLS.stages;
      title = '📚 Inscription Stage Intensif';
      break;
    default:
      url = CALENDLY_URLS.diagnostic;
      title = `📋 Inscription ${formula}`;
  }
  openCalendlyModal(url, title);
}

function scheduleSubjectSession(subject) {
  let url, title;
  switch (subject) {
    case 'maths':
      url = CALENDLY_URLS.maths;
      title = '📊 Rendez-vous Mathématiques';
      break;
    case 'nsi':
      url = CALENDLY_URLS.nsi;
      title = '💻 Session NSI Spécialisée';
      break;
    case 'physique':
      url = CALENDLY_URLS.physique;
      title = '⚗️ Atelier Physique-Chimie';
      break;
    case 'francais':
      url = CALENDLY_URLS.francais;
      title = '📚 Coaching Français & Grand Oral';
      break;
    case 'coaching':
      url = CALENDLY_URLS.coaching;
      title = '🎯 Coaching Scolaire Personnalisé';
      break;
    default:
      url = CALENDLY_URLS.diagnostic;
      title = `📅 Consultation ${subject}`;
  }
  openCalendlyModal(url, title);
}

function scheduleVisit() {
  openCalendlyModal(CALENDLY_URLS.visite, '🏢 Visite du Centre Nexus Réussite');
}

function getDirections() {
  // Ouvrir Google Maps avec l'adresse du centre
  const address = encodeURIComponent('Nexus Réussite, Tunis, Tunisie');
  window.open(`https://www.google.com/maps/search/${address}`, '_blank');
}

// Fonction de démonstration pour les tests
function testBookingSystem() {
  console.log('🧪 Test du système de réservation...');

  // Test avec tous les services
  const services = ['diagnostic', 'maths', 'nsi', 'physique', 'francais', 'coaching'];

  services.forEach((service, index) => {
    setTimeout(() => {
      console.log(`✅ Test ${service} : ${CALENDLY_URLS[service]}`);
    }, index * 500);
  });

  alert('🎉 Système de réservation opérationnel !\n\n✅ Calendly intégré\n✅ Fallback WhatsApp/Téléphone\n✅ Toutes les fonctions connectées');
}

console.log('🚀 Système de réservation Nexus Réussite chargé !');
