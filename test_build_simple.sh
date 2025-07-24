#!/bin/bash

# Test Build Simple - Nexus Réussite
echo "🔨 Test de Build Simple"
echo "======================="

PROJECT_ROOT="/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite"

# Test Backend
echo ""
echo "🐍 Test Backend..."
cd "$PROJECT_ROOT/backend"

# Vérifier l'environnement virtuel
if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
    echo "✅ Environnement virtuel OK"
    
    # Test import simple
    python -c "
import sys
sys.path.insert(0, 'src')
try:
    from config import get_config
    print('✅ Import config OK')
except Exception as e:
    print(f'❌ Erreur: {e}')
    exit(1)
"
else
    echo "⚠️  Environnement virtuel non trouvé"
fi

# Test Frontend
echo ""
echo "⚛️  Test Frontend..."
cd "$PROJECT_ROOT/frontend"

if [ -f "package.json" ]; then
    echo "✅ package.json trouvé"
    
    # Vérifier si un build existe
    if [ -d "dist" ]; then
        echo "✅ Build existant détecté"
        echo "   Taille: $(du -sh dist | cut -f1)"
        echo "   Fichiers: $(find dist -type f | wc -l) fichiers"
    else
        echo "⚠️  Aucun build détecté"
        
        # Tentative de build si npm est disponible
        if command -v npm &> /dev/null && [ -d "node_modules" ]; then
            echo "🔨 Tentative de build..."
            npm run build:production 2>/dev/null && \
            echo "✅ Build réussi !" || \
            echo "❌ Échec du build"
        fi
    fi
else
    echo "❌ package.json non trouvé"
fi

echo ""
echo "📊 Résumé:"
echo "  Backend: $(find $PROJECT_ROOT/backend/src -name '*.py' | wc -l) fichiers Python"
echo "  Frontend: $(find $PROJECT_ROOT/frontend/src -name '*.jsx' -o -name '*.js' | wc -l) fichiers JS/JSX"
echo ""
echo "✅ Test terminé"
