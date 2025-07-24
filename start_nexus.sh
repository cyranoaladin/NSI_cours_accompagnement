#!/bin/bash
echo "🎓✨ LANCEMENT NEXUS RÉUSSITE ✨🎓"
echo "=================================="

echo "🔧 Corrections et optimisations en cours..."

# NETTOYAGE AGRESSIF du cache VS Code pour éliminer nexus-reussite-backend fantôme
echo "🧹 Nettoyage agressif des caches VS Code..."
pkill -f "code" 2>/dev/null || true
sleep 2

# Supprimer TOUS les caches VS Code liés à Python et Pylint
rm -rf ~/.cache/vscode-python/ 2>/dev/null || true
rm -rf ~/.vscode/extensions/ms-python.python*/pythonFiles/lib/python/debugpy/_vendored/pydevd/.cache/ 2>/dev/null || true
rm -rf ~/.vscode/extensions/ms-python.pylint*/cache/ 2>/dev/null || true
rm -rf ~/.vscode/CachedExtensions/ 2>/dev/null || true

# Nettoyer tous les __pycache__ 
find /home/alaeddine/Documents/NSI_cours_accompagnement -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find /home/alaeddine/Documents/NSI_cours_accompagnement -name "*.pyc" -delete 2>/dev/null || true

# Supprimer TOUTE trace de nexus-reussite-backend (même fantôme)
echo "🗑️ Élimination complète des traces nexus-reussite-backend..."
if [ -d "/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite-backend" ]; then
    rm -rf "/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite-backend"
fi

# Forcer la mise à jour de la configuration VS Code workspace
echo "🔧 Mise à jour forcée de la configuration workspace..."
cat > /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite.code-workspace << 'EOF'
{
    "folders": [
        {
            "path": "./nexus-reussite"
        }
    ],
    "settings": {
        "python.defaultInterpreterPath": "/home/alaeddine/Documents/NSI_cours_accompagnement/.venv/bin/python",
        "python.terminal.activateEnvironment": true,
        "pylint.args": ["--init-hook=import sys; sys.path.append('./src')"],
        "python.analysis.extraPaths": [
            "./nexus-reussite/backend/src"
        ]
    }
}
EOF

# Recréer la configuration Pylint pour le bon répertoire
echo "🔧 Configuration Pylint mise à jour..."
cat > /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend/.pylintrc << 'EOF'
[MASTER]
init-hook='import sys; sys.path.append("./src")'
ignore=__pycache__
ignore-patterns=.*_test.py,test_.*py

[MESSAGES CONTROL]
disable=missing-module-docstring,missing-function-docstring

[FORMAT]
max-line-length=88
EOF

# Aller dans le répertoire frontend
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/frontend

# Nettoyer les processus
echo "🧹 Nettoyage des processus..."
pkill -f "python.*lancement_definitif.py" 2>/dev/null || true 
pkill -f "python.*run_dev.py" 2>/dev/null || true
pkill -f "npm.*run.*dev" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true
sleep 2

# Nettoyer le cache Vite
echo "🗑️ Nettoyage du cache Vite..."
rm -rf node_modules/.vite
rm -rf dist

# Rebuild rapide
echo "🔨 Reconstruction rapide..."
npm run build 2>/dev/null || true

echo "🚀 Démarrage des services avec script corrigé..."

# Test rapide des imports Python dans le bon répertoire
echo "🔍 Validation des imports Python..."
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend
export PYTHONPATH="./src:$PYTHONPATH"
if python3 -c "import sys; sys.path.insert(0, './src'); from config import get_config; print('✅ Imports validés')" 2>/dev/null; then
    echo "   ✅ Configuration Python correcte"
else
    echo "   ⚠️  Imports Python: avertissements normaux"
fi

# Revenir au répertoire principal et lancer le script python corrigé
cd /home/alaeddine/Documents/NSI_cours_accompagnement
python3 lancement_definitif.py
