#!/bin/bash

# ==========================================
# DIAGNOSTIC RAPIDE - NEXUS RÉUSSITE  
# ==========================================

echo "🔍 DIAGNOSTIC RAPIDE DES ERREURS POTENTIELLES"
echo "=============================================="

PROJECT_ROOT="/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite"

# 1. Vérification de la structure
echo ""
echo "📁 Structure du projet :"
ls -la "$PROJECT_ROOT" | head -10

# 2. Vérification des fichiers critiques
echo ""
echo "🔍 Fichiers critiques :"
critical_files=(
    "backend/src/config.py"
    "backend/src/main_production.py" 
    "backend/requirements.txt"
    "frontend/package.json"
    "frontend/vite.config.js"
    "docker-compose.yml"
)

for file in "${critical_files[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file MANQUANT"
    fi
done

# 3. Test rapide Python
echo ""
echo "🐍 Test Python rapide :"
cd "$PROJECT_ROOT/backend"

if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
    
    python -c "
import sys
sys.path.insert(0, 'src')
try:
    from config import get_config, validate_config
    print('✅ Imports config OK')
    
    config_obj = get_config()
    print('✅ get_config() OK')
    
    report = validate_config(config_obj)
    print(f'✅ validate_config() OK - Status: {report[\"status\"]}')
    
except Exception as e:
    print(f'❌ Erreur Python: {e}')
" 2>/dev/null || echo "❌ Test Python échoué"
else
    echo "⚠️  Environnement virtuel non trouvé"
fi

# 4. Test rapide Frontend
echo ""
echo "⚛️  Test Frontend rapide :"
cd "$PROJECT_ROOT/frontend"

if [ -f "package.json" ]; then
    echo "✅ package.json trouvé"
    
    if [ -d "node_modules" ]; then
        echo "✅ node_modules installé"
    else
        echo "⚠️  node_modules manquant"
    fi
    
    if [ -d "dist" ]; then
        echo "✅ Build dist existant ($(du -sh dist | cut -f1))"
    else
        echo "⚠️  Build dist manquant"
    fi
else
    echo "❌ package.json manquant"
fi

# 5. Erreurs potentielles
echo ""
echo "⚠️  Recherche d'erreurs potentielles :"

# Erreurs Python
echo "🐍 Erreurs Python potentielles :"
find "$PROJECT_ROOT/backend/src" -name "*.py" -exec python -m py_compile {} \; 2>&1 | head -5 || echo "  Aucune erreur de syntaxe trouvée"

# Erreurs dans les logs
if [ -d "$PROJECT_ROOT/backend/logs" ]; then
    echo "📝 Dernières erreurs dans les logs :"
    find "$PROJECT_ROOT/backend/logs" -name "*.log" -exec tail -3 {} \; 2>/dev/null | head -5 || echo "  Aucun log d'erreur trouvé"
fi

echo ""
echo "✅ Diagnostic terminé"
