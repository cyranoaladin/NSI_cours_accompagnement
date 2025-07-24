Voici le cahier des charges complet  pour le portail Nexus Réussite.

📘 Cahier des Charges Technique & Fonctionnel  — Portail Nexus Réussite

Projet : Création de la plateforme web de Nexus Réussite

Version : 2.0 (Intègre le modèle hybride et la tarification)

Date : 22/07/2025

Contact Principal : [Votre Nom/Poste]

1. Introduction et Vision du Projet
1.1 Notre Mission : La Pédagogie Augmentée

Nexus Réussite est un partenaire d'excellence scolaire pour les élèves de Première et Terminale du système français en Tunisie. Notre mission est de connecter le potentiel de chaque élève à ses ambitions futures grâce à un modèle de pédagogie "augmentée". Cet écosystème unique combine :

La puissance et la flexibilité d'un portail numérique intelligent (accès 24/7, ressources, suivi personnalisé).

La valeur irremplaçable de l'interaction humaine directe via des cours en présentiel, en individuel ou en micro-groupes.

Notre narrative : "Le meilleur des deux mondes. Votre portail Nexus Réussite est votre camp de base numérique pour réviser à votre rythme, et nos sessions en présentiel sont vos expéditions guidées pour conquérir les notions les plus complexes avec votre coach."

1.2 Objectifs du Portail

Ce portail est le cœur de notre service et doit remplir trois objectifs majeurs :

Acquisition : Séduire et convaincre les familles de notre expertise via un site public transparent, professionnel et rassurant, présentant clairement nos offres hybrides et nos tarifs.

Rétention & Engagement : Offrir une expérience d'apprentissage et de suivi si fluide et valorisante que les élèves l'utilisent de manière proactive et régulière, tant pour leurs révisions en ligne que pour la gestion de leurs cours en présentiel.

Efficacité Opérationnelle : Fournir aux coachs et administrateurs des outils puissants pour suivre la progression, gérer un planning hybride complexe (en ligne/présentiel), et communiquer efficacement.

2. Cibles et Personas

Le design et les fonctionnalités devront être pensés pour les trois rôles utilisateurs principaux : l'Élève (Adrien, 17 ans), le Parent (Sophie, 48 ans) et le Coach/Enseignant (David, 35 ans). Leurs besoins fondamentaux restent les mêmes, mais la plateforme doit maintenant leur offrir des solutions pour gérer un parcours hybride.

3. Spécifications Fonctionnelles Détaillées
3.1. Site Public (Accessible sans authentification)

Page d'Accueil :

Hero Section avec le slogan et les CTA Découvrir nos offres et Réserver un bilan offert.

Présentation de la pédagogie augmentée (hybride) comme pilier central.

Aperçu des services avec des icônes distinctives pour les modalités : caméra (en ligne), bâtiment (présentiel).

Blocs Témoignages, Confiance, etc.

Nouvelle Page : "Offres et Tarifs" :

Présentation des offres sous forme de cartes comparatives claires.

Tableau des Formules d'Accompagnement :
| Formule | Description | Inclus | Tarif Indicatif |
| :--- | :--- | :--- | :--- |
| Accès Plateforme | L'essentiel pour réviser en autonomie. | Accès 24/7 aux modules, quiz, suivi. | XX TND / mois |
| Formule Hybride | Équilibre parfait entre autonomie et suivi. | Tout de la formule Plateforme + 4h de cours/mois. | À partir de XX TND / mois |
| Formule Immersion| Accompagnement complet pour l'excellence. | Tout de la formule Hybride + 8h de cours/mois. | À partir de XX TND / mois |

Tableau des Cours à la Carte :
| Type de Cours | Description | Tarif Indicatif |
| :--- | :--- | :--- |
| Cours Particulier - En Ligne | 1h de soutien individuel en visio. | XX TND / heure |
| Cours Particulier - Présentiel | 1h de soutien individuel au centre. | XX TND / heure |
| Atelier en Groupe - Présentiel | 2h sur un chapitre clé (3-5 élèves). | XX TND / atelier |

Chaque offre doit comporter un CTA clair (Choisir cette formule ou Réserver un cours).

Nouvelle Page : "Notre Centre" :

Présentation du lieu physique avec des photos de haute qualité.

Carte Google Maps intégrée, adresse complète et horaires.

Page "Nos Services" : Description de chaque service (Maths, NSI...) en précisant systématiquement les modalités disponibles (en ligne, présentiel).

Autres pages : "Notre Pédagogie", "Blog", "Contact/FAQ", "Mentions Légales".

3.2. Authentification et Rôles

Rôles : ELEVE, PARENT, COACH, ADMIN.

Processus : Connexion via Email/Password, Google OAuth, ou Magic Link. Création des comptes par l'admin. Liaison sécurisée Parent-Élève.

3.3. Espace Élève ("Le Cockpit de la Réussite")

Dashboard d'Accueil :

Widget "Mon Agenda" (Crucial) : Affiche les prochains cours et deadlines en précisant le format et le lieu.

Ex: "Cours de Maths avec David | Format : En Présentiel | Lieu : Centre Nexus, Salle Alpha".

Ex: "Coaching | Format : En ligne | Lien de la visio : [cliquable]".

Autres widgets : "Objectifs de la semaine", "Modules en cours", "Gamification".

Nouvelle Fonctionnalité : "Réserver une Session" : Un module accessible depuis le dashboard permettant un parcours de réservation fluide (décrit en détail dans la section 4).

Autres sections : "Cours Interactifs" (vidéos, quiz), "Projets Encadrés", "Préparation Grand Oral", "Carnet de Bord".

3.4. Espace Parent ("Le Pont de Confiance")

Vue simplifiée et en lecture seule des données de l'enfant.

Dashboard avec indicateurs d'effort (temps passé, quiz faits).

Accès à l'agenda de l'enfant pour voir les cours planifiés (en ligne et présentiel).

Accès aux rapports du coach et à une messagerie sécurisée.

3.5. Espace Coach / Admin ("La Tour de Contrôle")

Gestion des Utilisateurs et du Contenu (CRUD) : Fonctionnalités de base inchangées.

Vue "Mes Élèves" : Suivi détaillé de la progression de chaque élève.

NOUVEAUX OUTILS DE PLANIFICATION HYBRIDE :

Gestion des Disponibilités : Chaque coach peut définir ses plages horaires disponibles dans un calendrier, en spécifiant si elles sont pour du en ligne ou du présentiel.

Gestion des Lieux (Admin) : Interface CRUD pour gérer les salles de cours physiques (nom, capacité, équipement).

Module de Planification Globale : Vue centralisée (calendrier) affichant les réservations, l'occupation des salles et la disponibilité des coachs pour éviter tout conflit.

4. Module Clé : Gestion et Réservation Hybride

Ce module est au cœur de la nouvelle stratégie et doit être particulièrement soigné.

4.1. Parcours Utilisateur (Élève/Parent)

Accès : Bouton Réserver un cours depuis le dashboard.

Étape 1 : Choix du Service (Matière, Coaching...).

Étape 2 : Choix de la Modalité (Boutons clairs : Individuel en Ligne, Individuel en Présentiel, Rejoindre un Atelier de Groupe).

Étape 3 : Sélection du Créneau : Affichage d'un calendrier avec les créneaux disponibles. Pour les ateliers, affichage de la liste des sessions planifiées avec les places restantes.

Étape 4 : Confirmation : Récapitulatif clair (service, coach, date, heure, lieu/format, prix).

Notification : Email de confirmation et ajout automatique à l'agenda de l'élève et du coach sur la plateforme.

4.2. Outils Administrateur / Coach

Mon Planning : Vue calendrier personnelle affichant tous les cours, peu importe la modalité.

Gestion des Ateliers de Groupe (Admin) : Formulaire pour créer un atelier (titre, coach, date, salle, places, prix). Suivi des inscriptions.

Gestion des Salles (Admin) : Vue planning de l'occupation des salles physiques.

5. Charte Graphique et UI/UX

Personnalité : Experte, rassurante, moderne, humaine, premium.

Logo : Concept de "Nexus" (connexion, pont).

Couleurs (validées) : Bleu nuit (#0F172A), Corail (#F97316), Blanc, Gris clairs et foncés.

Typographies (validées) : Poppins (Titres), Inter (Texte), Fira Code (Code).

UI Components & Animations : Utilisation de rounded-xl/2xl, shadow-lg, effets de survol subtils, et Framer Motion pour des transitions fluides.

6. Spécifications Techniques

Frontend : React 18, Next.js 14 (App Router), TypeScript, Tailwind CSS, Zustand.

Backend : API Routes de Next.js, Node.js, Prisma ORM.

Base de Données : PostgreSQL.

Modélisation (Additions pour le modèle hybride) : Ajout des schémas Prisma suivants :

Location (ou Room): id, name, capacity

Availability: id, coachId, startTime, endTime, isForInPerson (boolean)

Booking (ou Event): id, studentId, coachId, startTime, endTime, format (enum: ONLINE, IN_PERSON), locationId (optionnel, clé étrangère vers Location), status (enum: CONFIRMED, CANCELLED)

Authentification : NextAuth.js (Google, Email/Password, Magic Link).

Fichiers : Cloudinary ou AWS S3.

API (Additions pour le modèle hybride) : Création de nouvelles routes dédiées :

GET /api/availability?coachId=...&date=...

GET /api/workshops?date=...

POST /api/bookings

PUT /api/bookings/:id/cancel

Tests : Jest + React Testing Library, Supertest (>80% de couverture).

Déploiement & CI/CD : Vercel, GitHub Actions.

7. Exigences Non-Fonctionnelles

Performance : Score Lighthouse > 90.

Responsive Design : Mobile-First.

Accessibilité (A11y) : WCAG 2.1 niveau AA.

SEO : Optimisation complète du site public.

Sécurité & RGPD : HTTPS, protection contre les failles courantes, gestion du consentement.

8. Jalons et Livrables (Plan de Sprints Révisé)

Le projet sera découpé en sprints de 2 semaines.

Sprint 0 (1 semaine) : Setup du projet, BDD avec schémas Prisma complets (incluant le modèle hybride).

Sprint 1 (2 sem) : Site public (incluant pages Offres/Tarifs et Centre) et authentification.

Sprint 2 (2 sem) : Espaces Élève & Parent (Dashboards, affichage de l'agenda hybride).

Sprint 3 (2 sem) : Espace Coach/Admin (outils de base, gestion de contenu et utilisateurs).

Sprint 4 (2 sem) : Développement du module de réservation hybride (back-end & front-end).

Sprint 5 (2 sem) : Finalisation des autres fonctionnalités (Projets, Grand Oral, Quiz).

Sprint 6 (1 sem) : QA, tests de bout en bout, corrections, préparation à la mise en production.

9. Livrables Attendus

Dépôt GitHub complet et commenté.

Base de données PostgreSQL déployée avec script de seeding.

Suite de tests complète.

Documentation technique (setup, architecture, API).

Déploiement fonctionnel sur Vercel.

Accès administrateur sécurisé.