# 📘 Cahier des charges — Portail NSI Premium

## 🧭 1. Contexte et objectifs

Plateforme d'accompagnement NSI pour élèves de Première et Terminale en France et à l’étranger (AEFE, CNED, candidats libres). Objectifs :

- Suivi pédagogique structuré et personnalisé
- Préparation au bac (cours, projets, Grand Oral)
- Espace interactif et motivant

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

## 🎯 3. Fonctionnalités principales

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

## 🎨 4. Charte graphique

### Couleurs
- Bleu nuit `#0F172A` (fond)
- Corail `#F97316` (CTA)
- Blanc `#FFFFFF`
- Gris clair `#F1F5F9`
- Gris foncé `#334155`

### Typographies
- Titres : `Poppins`, sans-serif
- Texte : `Inter`
- Code : `Fira Code`

### UI Components
- Boutons : `rounded-xl`, hover/active/focus
- Cartes : `shadow-md`, `rounded-2xl`
- Inputs : `rounded-lg`, `border-gray-200`
- Badges : `bleu`, `vert`, `orange` selon thème

### Layout & animation
- `max-w-screen-xl`, padding `px-4 md:px-6`
- Framer Motion (page transitions)
- Animations au scroll, lazy loading

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

---

