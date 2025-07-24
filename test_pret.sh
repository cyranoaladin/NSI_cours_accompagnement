#!/bin/bash

# Test rapide avant lancement
echo "🔍 Test de préparation..."

cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite

# Test backend
echo "🐍 Test backend..."
cd backend
if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
    python -c "
import sys
sys.path.insert(0, 'src')
try:
    from config import get_config
    from main_production import create_app
    print('✅ Backend prêt')
except Exception as e:
    print(f'❌ Backend: {e}')
    exit(1)
"
else
    echo "❌ Environnement virtuel manquant"
    exit 1
fi

# Test frontend  
echo "⚛️  Test frontend..."
cd ../frontend
if [ -d "node_modules" ] && [ -f "package.json" ]; then
    echo "✅ Frontend prêt"
else
    echo "❌ Frontend non configuré"
    exit 1
fi

echo "🎉 Tout est prêt pour le lancement !"
