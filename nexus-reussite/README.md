# 🎓 Nexus Réussite - Plateforme Éducative Intelligente

## 📋 Description

Nexus Réussite est une plateforme éducative moderne conçue pour l'accompagnement personnalisé des élèves du lycée français. Elle intègre l'intelligence artificielle (ARIA) pour offrir une expérience d'apprentissage adaptative et efficace.

## 🏗️ Architecture du Projet

```
nexus-reussite/
├── backend/          # API Flask + SQLAlchemy + IA
├── frontend/         # Interface React + TypeScript + Vite
├── assets/          # Ressources graphiques et médias
└── docs/            # Documentation technique
```

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.12+
- Node.js 18+
- PostgreSQL ou SQLite

### ⚡ Lancement Immédiat (Aperçu)

**Option 1 - Démarrage Express :**
```bash
chmod +x ../start_simple.sh
../start_simple.sh
```

**Option 2 - Démarrage Complet :**
```bash
chmod +x ../demarrer_nexus_reel.sh
../demarrer_nexus_reel.sh
```

**Accès direct :**
- 🌐 Interface : http://localhost:3000
- 🔧 API : http://localhost:5000

**Note :** Attendez 8-10 secondes après le lancement pour que les services soient complètement opérationnels.

### ⚠️ Note Importante - Configuration VS Code

Si vous voyez des erreurs référençant d'anciens dossiers (`nexus-reussite-backend`, `nexus-reussite-frontend`, etc.), ces erreurs sont **obsolètes** et proviennent du cache VS Code. 

**Solution recommandée :**
1. Fermez complètement VS Code
2. Exécutez le script de nettoyage : `./nettoyer_vscode.sh`
3. Rouvrez avec : `code nexus-reussite.code-workspace`

### Installation Backend
```bash
cd backend
pip install -r requirements.txt
python run_dev.py
```

### Installation Frontend
```bash
cd frontend
npm install
npm run dev
```

### 🔨 Build de Production

#### Build Automatique (Recommandé)
```bash
# Script de build complet avec corrections automatiques
chmod +x ../build_final.sh
../build_final.sh
```

#### Build Manuel
```bash
# Backend
cd backend
source ../.venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
npm run build:production

# Docker (optionnel)
cd ..
docker-compose build
```

#### Validation du Build
```bash
# Test rapide des composants
chmod +x ../test_build_simple.sh
../test_build_simple.sh
```

## 🧪 Tests

### Backend
```bash
cd backend
pytest tests/ -v
```

### Frontend
```bash
cd frontend
npm run test
```

## 🎯 Fonctionnalités Principales

- 🤖 **IA ARIA** : Assistant intelligent adaptatif
- 📊 **Tableaux de bord** : Suivi des progrès en temps réel
- 📚 **Gestion de contenu** : Banque d'exercices et ressources
- 👥 **Multi-utilisateurs** : Élèves, professeurs, parents
- 📱 **Responsive** : Interface adaptative multi-appareils
- 🔐 **Sécurité** : Authentification JWT et protection des données

## 🛠️ Technologies

### Backend
- Flask 3.0 + SQLAlchemy
- OpenAI GPT-4 Integration
- PostgreSQL / SQLite
- JWT Authentication
- Pytest + Pylint

### Frontend
- React 18 + TypeScript
- Vite + TailwindCSS
- React Query + Zustand
- Vitest + Testing Library

## 📈 Statut du Projet

- ✅ Backend : API fonctionnelle avec tests unitaires
- ✅ Frontend : Interface moderne et responsive
- ✅ IA : Intégration ARIA opérationnelle
- ✅ Tests : Couverture de code > 80%
- ✅ Documentation : Guide complet disponible

## 👥 Équipe

Développé avec passion pour l'éducation française moderne.

## 📄 Licence

Projet éducatif - Tous droits réservés.
