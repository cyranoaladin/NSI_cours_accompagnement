# Nexus Réussite - Plateforme Éducative NSI

## 🎯 Description
Plateforme d'accompagnement NSI premium pour élèves de Première et Terminale, développée avec une architecture moderne full-stack.

## 🏗️ Architecture

### Backend
- **Framework**: Flask 3.1+ avec Python
- **Base de données**: PostgreSQL + SQLAlchemy
- **Intelligence Artificielle**: OpenAI GPT (Assistant ARIA)
- **Authentification**: JWT + Flask-JWT-Extended
- **API**: REST avec WebSocket pour temps réel

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS + Components UI
- **State Management**: Zustand
- **Routing**: React Router
- **Testing**: Vitest + React Testing Library

## 📁 Structure du projet

```
NSI_cours_accompagnement/
├── README.md                    # Documentation principale
├── .git/                       # Contrôle de version
├── static/                     # Assets statiques globaux
└── nexus-reussite/             # Application principale
    ├── backend/                # API Flask
    │   ├── src/               # Code source Python
    │   ├── requirements.txt   # Dépendances Python
    │   └── venv/             # Environnement virtuel
    ├── frontend/              # Interface React/Vite
    │   ├── src/              # Code source React
    │   ├── dist/             # Build de production
    │   └── package.json      # Dépendances Node.js
    ├── docs/                  # Documentation détaillée
    ├── assets/               # Images et ressources
    ├── scripts/              # Scripts utilitaires
    └── docker-compose.yml    # Configuration Docker
```

## 🚀 Démarrage rapide

### Prérequis
- Python 3.8+
- Node.js 18+
- PostgreSQL (optionnel avec Docker)

### Installation

1. **Cloner le projet**
```bash
git clone <repository>
cd NSI_cours_accompagnement
```

2. **Backend Flask**
```bash
cd nexus-reussite/backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Frontend React**
```bash
cd nexus-reussite/frontend
npm install
```

### Lancement

#### Mode Développement
```bash
# Terminal 1 - Backend
cd nexus-reussite/backend
source venv/bin/activate
python src/main.py

# Terminal 2 - Frontend
cd nexus-reussite/frontend
npm run dev
```

#### Mode Production
```bash
cd nexus-reussite
docker-compose up -d
```

## 🔧 Configuration

Créer un fichier `.env` dans `nexus-reussite/backend/`:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/nexus_db
OPENAI_API_KEY=your-openai-key
```

## 📊 Fonctionnalités

### ✅ Implémentées
- 🔐 Authentification multi-rôles (élève, parent, enseignant, admin)
- 🤖 Assistant IA ARIA avec OpenAI
- 📚 Système de contenu et cours
- 📈 Suivi de progression étudiant
- 🔔 Notifications en temps réel
- 📱 Interface responsive

### 🚧 En développement
- 🎥 Visioconférence intégrée
- 📝 Système d'évaluation automatique
- 📊 Analytics avancées
- 🎮 Gamification

## 🧪 Tests

```bash
# Tests Backend
cd nexus-reussite/backend
python -m pytest

# Tests Frontend
cd nexus-reussite/frontend
npm run test
```

## 📦 Build Production

```bash
# Build Frontend
cd nexus-reussite/frontend
npm run build

# Le build est automatiquement servi par Flask en production
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---
*Développé avec ❤️ pour l'excellence éducative*
