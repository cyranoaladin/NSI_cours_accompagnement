# 📘 Cahier des charges — Portail NSI Premium

## 🛍 1. Contexte et objectifs

Plateforme d'accompagnement NSI pour élèves de Première et Terminale spécialité, dans le cadre du système scolaire français, notamment au sein du réseau AEFE en Tunisie. Objectifs :

- Offrir un enseignement conforme aux programmes français
- Préparation exigeante au bac NSI (cours, projets, Grand Oral)
- Accompagnement haut de gamme personnalisé

Public cible : élèves en lycée français à l'étranger, candidats libres, familles expatriées, profils bilingues avec ambition d'excellence.

## ✨ Positionnement et promesse

**NSI Premium** se distingue par :

- Une approche personnalisée et humaine
- Des intervenants titulaires de l'Éducation nationale française
- Des enseignants diplômés du **DIU NSI** (Diplôme Universitaire de Spécialisation en NSI)
- Une méthodologie pédagogique rigoureuse, adaptée à chaque profil
- Une plateforme immersive et interactive, bien au-delà des cours particuliers classiques

---

## 🛠 2. Stack technique

- **Frontend** : React 18, Next.js 14 (App Router), TypeScript, Tailwind CSS, Zustand
- **Backend** : Node.js, API Routes (Next.js), Prisma ORM
- **Base de données** : PostgreSQL (Railway ou Supabase)
- **Auth** : NextAuth.js + OAuth (Google), Magic Link, JWT
- **Tests** : Jest, React Testing Library, Supertest
- **CI/CD** : GitHub Actions, Vercel (frontend), Railway (backend)
- **Fichiers** : UploadThing / Cloudinary

---

## 🌟 3. Fonctionnalités principales

### 3.1 Espace public
- Hero section (slogan, illustration animée)
- Vidéo embed de présentation
- Témoignages (texte/photo)
- CTA : `S’inscrire`, `Demander une démo`
- F.A.Q., mentions légales, partenaires

### 3.2 Authentification
- 3 rôles : `élève`, `enseignant`, `parent`
- Connexion : Email, Google, Magic link
- Lien parent-élève sécurisé

### 3.3 Dashboard élève
- Accueil personnalisé : avatar, progression, deadlines
- Modules à suivre
- Carnet de bord : notes, favoris
- Notifications intelligentes

### 3.4 Cours interactifs
- Organisation : `niveau` > `thèmes`
- Contenu : vidéos ≤7 min, fiches PDF/MD, quiz interactifs
- Activités pratiques, mini-projets guidés
- Algorithme adaptatif : suggère renforcement selon résultats

### 3.5 Projets encadrés
- Choix libre/guidé
- Cahier des charges auto-généré
- Jalons, démos, uploads
- Feedback structuré

### 3.6 Grand Oral
- Simulation IA + enregistrement
- Grille de correction + feedback
- Historique des oraux

### 3.7 Espace parent
- Invitation + vue simplifiée progression élève
- Feedbacks
- Messagerie prof-parent

### 3.8 Admin
- CRUD : utilisateurs, modules, projets
- Statistiques, alertes, exports CSV

---

## 🎨 4. Charte graphique adaptée au contexte AEFE / francophonie Tunisie

### Palette
- Bleu républicain `#001F3F` (institutionnel, rigueur)
- Sable tunisien `#F4A261` (chaleur, ancrage local)
- Corail `#E76F51` (dynamisme, accents)
- Blanc cassé `#FAF9F6`
- Gris foncé `#2F3E46`

### Typographies
- Titres : `Marianne`, typographie de l'administration française (si possible) ou `Poppins`
- Corps de texte : `Inter`
- Code : `Fira Code`

### Icônes et visuels
- Illustrations : visuels en lien avec les sciences informatiques, l'enseignement, la francophonie
- Prévoir des visuels évoquant la méditerranée, l'identité AEFE, la rigueur scientifique

---

## 🔊 Narratif, langage, messages clés pour les développeurs

### Slogans possibles
- "La NSI d'excellence, personnalisée, pour chaque lycéen français partout dans le monde."
- "Un enseignement exigeant et humain, par des professeurs de l'Éducation nationale."
- "Vos ambitions méritent l'excellence de la spécialité NSI."
- "Bien plus que des cours : un véritable accompagnement."

### Call-To-Actions (CTA)
- "Découvrir l’offre NSI Premium"
- "Réserver un entretien personnalisé"
- "Tester gratuitement un module"
- "Je prépare mon Grand Oral avec un expert"

### Ton de la plateforme
- Institutionnel, bienveillant et motivant
- Mots-clés à utiliser : "personnalisé", "suivi rigoureux", "excellence", "engagement", "autonomie accompagnée", "valeurs de l'École républicaine"

### Particularité de l’offre
- Pas un site de cours générique : accompagnement sur mesure
- Mélange de rigueur école française + accessibilité numérique
- Rythme adapté au calendrier scolaire français
- Disponibilité des enseignants pour échanges individuels

### Particularité des enseignants
- Expérience en lycée français à l'étranger
- Titulaires du DIU NSI : expertise validée
- Compétences en individualisation, suivi, orientation, accompagnement

---

## 🧱 5. Architecture technique

- Layouts dynamiques via App Router (par rôle)
- Middlewares : Auth (NextAuth) + RoleGuard
- API REST `/api/modules`, `/api/projects`, etc.
- Prisma Schema :
  - `User`, `Profile`, `Module`, `Project`
  - `Quiz`, `Submission`, `Feedback`, `Badge`, `EventLog`

---

## 🧪 6. Aspects non-fonctionnels

- Responsive (mobile-first)
- SEO (balises dynamiques, sitemap.xml)
- Accessibilité (WCAG 2.1 AA)
- RGPD (cookies, anonymisation)
- Perf : images compressées, CDN, Lighthouse > 90

---

## ⏱ 7. Jalons

- **Sprint 0** : Setup, Prisma schema (1 semaine)
- **Sprint 1** : Auth, routes publiques (2 sem)
- **Sprint 2** : Dashboard + modules cours (2 sem)
- **Sprint 3** : Projets + feedback (2 sem)
- **Sprint 4** : Grand Oral, parents, admin (2 sem)
- **Sprint 5** : QA, tests, prod (1 sem)

---

## 📦 8. Livraison finale

- Repo GitHub organisé et commenté
- Base PostgreSQL + seed
- Tests > 85% couverture
- Documentation API + guide déploiement
- Backups automatisés
- Accès admin sécurisé

---

## 📊 9. Critères de succès

- Score Lighthouse > 90
- Taux de complétion > 70% modules testés
- Feedback utilisateur > 8/10
- NPS > 50
- Fonctionnel et prêt pour le déploiement
