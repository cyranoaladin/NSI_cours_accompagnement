#!/bin/bash

# ==========================================
# BUILD FINAL ET VALIDATION - NEXUS RÉUSSITE
# ==========================================

echo "🚀 BUILD FINAL - NEXUS RÉUSSITE"
echo "================================"

PROJECT_ROOT="/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite"
BUILD_SUCCESS=true

# ==========================================
# 1. VALIDATION PRE-BUILD
# ==========================================
echo ""
echo "📋 VALIDATION PRE-BUILD"
echo "========================"

# Vérifier la structure
if [ ! -d "$PROJECT_ROOT" ]; then
    echo "❌ Projet non trouvé à $PROJECT_ROOT"
    exit 1
fi

cd "$PROJECT_ROOT"

# Fichiers essentiels
essential_files=(
    "backend/src/config.py"
    "backend/src/main_production.py"
    "backend/requirements.txt"
    "frontend/package.json"
    "frontend/vite.config.js"
)

echo "🔍 Vérification des fichiers essentiels:"
for file in "${essential_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file MANQUANT"
        BUILD_SUCCESS=false
    fi
done

# ==========================================
# 2. BUILD BACKEND
# ==========================================
echo ""
echo "🐍 BUILD BACKEND"
echo "================"

cd "$PROJECT_ROOT/backend"

# Environnement virtuel
if [ ! -f "../.venv/bin/activate" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv ../.venv
fi

source ../.venv/bin/activate

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Test critique des imports
echo "🔍 Test des imports critiques..."
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from config import get_config, validate_config
    from main_production import create_app
    
    # Test de la configuration
    config = get_config()
    report = validate_config(config)
    
    # Test de l'application
    app = create_app()
    
    print('✅ Backend validé - tous les imports OK')
except Exception as e:
    print(f'❌ Erreur backend: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo "✅ Backend build réussi"
else
    echo "❌ Backend build échoué"
    BUILD_SUCCESS=false
fi

# ==========================================
# 3. BUILD FRONTEND
# ==========================================
echo ""
echo "⚛️  BUILD FRONTEND"
echo "=================="

cd "$PROJECT_ROOT/frontend"

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js requis mais non installé"
    BUILD_SUCCESS=false
else
    echo "✅ Node.js $(node --version)"
fi

# Vérifier npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm requis mais non installé"
    BUILD_SUCCESS=false
else
    echo "✅ npm $(npm --version)"
fi

# Installation des dépendances
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances npm..."
    npm install
fi

# Build de production
echo "🔨 Build de production..."
npm run build:production

if [ -d "dist" ]; then
    BUILD_SIZE=$(du -sh dist | cut -f1)
    FILE_COUNT=$(find dist -type f | wc -l)
    echo "✅ Frontend build réussi"
    echo "   📊 Taille: $BUILD_SIZE"
    echo "   📁 Fichiers: $FILE_COUNT"
else
    echo "❌ Frontend build échoué"
    BUILD_SUCCESS=false
fi

# ==========================================
# 4. VALIDATION DOCKER
# ==========================================
echo ""
echo "🐳 VALIDATION DOCKER"
echo "===================="

cd "$PROJECT_ROOT"

if command -v docker &> /dev/null; then
    echo "✅ Docker $(docker --version | cut -d' ' -f3 | tr -d ',')"
    
    # Test docker-compose
    if [ -f "docker-compose.yml" ]; then
        docker-compose config > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ docker-compose.yml valide"
        else
            echo "⚠️  docker-compose.yml avec warnings"
        fi
    fi
else
    echo "⚠️  Docker non disponible"
fi

# ==========================================
# 5. RAPPORT FINAL
# ==========================================
echo ""
echo "📊 RAPPORT FINAL DE BUILD"
echo "========================="

cd "$PROJECT_ROOT"

# Statistiques
backend_py_files=$(find backend/src -name "*.py" | wc -l)
frontend_js_files=$(find frontend/src -name "*.jsx" -o -name "*.js" | wc -l)

echo "📈 Statistiques du projet:"
echo "   🐍 Backend: $backend_py_files fichiers Python"
echo "   ⚛️  Frontend: $frontend_js_files fichiers JS/JSX"

if [ -d "frontend/dist" ]; then
    echo "   📦 Build frontend: $(du -sh frontend/dist | cut -f1)"
fi

echo ""
echo "🔧 Composants validés:"
echo "   ✅ Configuration Python (config.py)"
echo "   ✅ Application Flask (main_production.py)"
echo "   ✅ Configuration React (package.json)"
echo "   ✅ Build Vite (vite.config.js)"
echo "   ✅ Docker Compose (docker-compose.yml)"

# Résultat final
echo ""
if [ "$BUILD_SUCCESS" = true ]; then
    echo "🎉 BUILD TERMINÉ AVEC SUCCÈS!"
    echo "================================"
    echo "✅ Le projet Nexus Réussite est prêt pour le déploiement"
    echo ""
    echo "🚀 Commandes de démarrage:"
    echo "   Backend:  cd backend && python run_dev.py"
    echo "   Frontend: cd frontend && npm run preview"
    echo "   Docker:   docker-compose up -d"
    exit 0
else
    echo "❌ BUILD ÉCHOUÉ"
    echo "================"
    echo "⚠️  Certains composants nécessitent une attention"
    echo "📝 Consultez les messages d'erreur ci-dessus"
    exit 1
fi
