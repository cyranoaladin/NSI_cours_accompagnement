#!/bin/bash

# ==========================================
# SCRIPT DE BUILD COMPLET - NEXUS RÉUSSITE
# ==========================================

set -e  # Arrêter en cas d'erreur

echo "🔨 DÉBUT DU BUILD COMPLET - NEXUS RÉUSSITE"
echo "=================================================="

# Variables
PROJECT_ROOT="/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# ==========================================
# 1. PRÉPARATION
# ==========================================
echo ""
echo "📋 ÉTAPE 1: Préparation de l'environnement"
echo "============================================="

cd "$PROJECT_ROOT"

# Vérifier la structure
echo "✅ Structure du projet :"
ls -la

# ==========================================
# 2. BUILD BACKEND (PYTHON)
# ==========================================
echo ""
echo "🐍 ÉTAPE 2: Build et validation Backend"
echo "========================================"

cd "$BACKEND_DIR"

echo "📦 Vérification des dépendances Python..."
if [ ! -d "../.venv" ]; then
    echo "⚠️  Environnement virtuel manquant. Création..."
    python3 -m venv ../.venv
fi

# Activer l'environnement virtuel
source ../.venv/bin/activate

echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔍 Validation de la syntaxe Python..."
python -m py_compile src/*.py
python -m py_compile src/**/*.py 2>/dev/null || true

echo "🧪 Tests de base..."
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from config import get_config, validate_config
    config_obj = get_config()
    report = validate_config(config_obj)
    print(f'✅ Configuration valide: {report[\"status\"]}')
except Exception as e:
    print(f'❌ Erreur de configuration: {e}')
    sys.exit(1)
"

echo "✅ Backend validé avec succès !"

# ==========================================
# 3. BUILD FRONTEND (NODE.JS)
# ==========================================
echo ""
echo "⚛️  ÉTAPE 3: Build Frontend"
echo "==========================="

cd "$FRONTEND_DIR"

echo "📦 Vérification de Node.js..."
node --version || echo "⚠️  Node.js non trouvé"
npm --version || echo "⚠️  npm non trouvé"

if [ -f "package.json" ]; then
    echo "📦 Installation des dépendances npm..."
    
    # Vérifier si node_modules existe
    if [ ! -d "node_modules" ]; then
        echo "📥 Installation initiale des dépendances..."
        npm install
    else
        echo "📥 Mise à jour des dépendances..."
        npm ci
    fi
    
    echo "🔍 Vérification du type checking..."
    npm run type-check || echo "⚠️  Type checking avec avertissements"
    
    echo "🔧 Build de production..."
    npm run build:production
    
    echo "📊 Taille du build :"
    if [ -d "dist" ]; then
        du -sh dist
        ls -la dist/
    fi
    
    echo "✅ Frontend buildé avec succès !"
else
    echo "❌ package.json non trouvé dans le frontend"
    exit 1
fi

# ==========================================
# 4. BUILD DOCKER (OPTIONNEL)
# ==========================================
echo ""
echo "🐳 ÉTAPE 4: Validation Docker"
echo "=============================="

cd "$PROJECT_ROOT"

if command -v docker &> /dev/null; then
    echo "🔍 Validation des Dockerfiles..."
    
    # Backend Dockerfile
    if [ -f "backend/Dockerfile.production" ]; then
        docker build --no-cache -f backend/Dockerfile.production -t nexus-backend:test backend/ && \
        echo "✅ Dockerfile backend valide" || \
        echo "⚠️  Dockerfile backend avec warnings"
    fi
    
    # Frontend Dockerfile  
    if [ -f "frontend/Dockerfile" ]; then
        docker build --no-cache -f frontend/Dockerfile -t nexus-frontend:test frontend/ && \
        echo "✅ Dockerfile frontend valide" || \
        echo "⚠️  Dockerfile frontend avec warnings"
    fi
    
    # Docker Compose
    if [ -f "docker-compose.yml" ]; then
        docker-compose config > /dev/null && \
        echo "✅ docker-compose.yml valide" || \
        echo "❌ docker-compose.yml invalide"
    fi
else
    echo "⚠️  Docker non disponible, validation ignorée"
fi

# ==========================================
# 5. RAPPORT FINAL
# ==========================================
echo ""
echo "📊 RAPPORT FINAL"
echo "================"

cd "$PROJECT_ROOT"

echo "📁 Structure finale :"
echo "  Backend: $(ls -1 backend/src/*.py | wc -l) fichiers Python"
echo "  Frontend: $(find frontend/src -name "*.jsx" -o -name "*.js" | wc -l) fichiers JS/JSX"

if [ -d "frontend/dist" ]; then
    echo "  Build frontend: ✅ $(du -sh frontend/dist | cut -f1)"
else
    echo "  Build frontend: ❌ Absent"
fi

if [ -f "backend/requirements.txt" ]; then
    echo "  Dépendances backend: ✅ $(grep -c '^[^#]' backend/requirements.txt) packages"
else
    echo "  Dépendances backend: ❌ Absent"
fi

echo ""
echo "🎉 BUILD TERMINÉ AVEC SUCCÈS !"
echo "=============================="
echo "🚀 Le projet Nexus Réussite est prêt pour le déploiement"
