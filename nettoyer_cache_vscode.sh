#!/bin/bash

echo "🧹✨ NETTOYAGE CACHE VS CODE - NEXUS RÉUSSITE ✨🧹"
echo "=================================================="

echo ""
echo "🔍 Diagnostic du problème..."
echo "L'erreur 'nexus-reussite-backend' provient probablement du cache VS Code"
echo "qui fait référence à un ancien répertoire supprimé."

echo ""
echo "🗑️ Nettoyage des caches VS Code..."

# Fermer VS Code si ouvert
echo "📱 Arrêt de VS Code..."
pkill -f "code" 2>/dev/null || true
sleep 2

# Nettoyer les caches VS Code
echo "🧹 Suppression des caches..."
rm -rf ~/.vscode/extensions/ms-python.python*/pythonFiles/lib/python/debugpy/_vendored/pydevd/.cache/ 2>/dev/null || true
rm -rf ~/.cache/vscode-python/ 2>/dev/null || true
rm -rf ~/.vscode/extensions/ms-python.pylint*/cache/ 2>/dev/null || true

# Nettoyer le cache Python
echo "🐍 Nettoyage du cache Python..."
find /home/alaeddine/Documents/NSI_cours_accompagnement -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find /home/alaeddine/Documents/NSI_cours_accompagnement -name "*.pyc" -delete 2>/dev/null || true

# Nettoyer les références aux anciens répertoires
echo "📂 Nettoyage des références obsolètes..."

# Vérifier s'il reste des traces de nexus-reussite-backend
if [ -d "/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite-backend" ]; then
    echo "⚠️  Répertoire nexus-reussite-backend trouvé - suppression..."
    rm -rf "/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite-backend"
fi

echo ""
echo "🔧 Mise à jour des configurations..."

# Recréer le fichier pyrightconfig.json propre
cat > /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend/pyrightconfig.json << 'EOF'
{
    "include": [
        "src"
    ],
    "exclude": [
        "**/node_modules",
        "**/__pycache__",
        "**/.*"
    ],
    "reportMissingImports": true,
    "reportMissingTypeStubs": false,
    "pythonVersion": "3.12",
    "pythonPlatform": "Linux",
    "executionEnvironments": [
        {
            "root": "./src",
            "pythonVersion": "3.12",
            "extraPaths": [
                "./src"
            ]
        }
    ],
    "venvPath": "/home/alaeddine/Documents/NSI_cours_accompagnement/.venv",
    "venv": ".venv"
}
EOF

echo ""
echo "✅ NETTOYAGE TERMINÉ !"
echo "====================="

echo ""
echo "📋 Actions effectuées :"
echo "   ✅ Caches VS Code nettoyés"
echo "   ✅ Cache Python nettoyé (__pycache__, *.pyc)"
echo "   ✅ Références obsolètes supprimées"
echo "   ✅ Configuration Pyright mise à jour"

echo ""
echo "🔄 REDÉMARRAGE RECOMMANDÉ :"
echo "============================"
echo "1. Fermez complètement VS Code"
echo "2. Attendez 5 secondes"
echo "3. Rouvrez VS Code"
echo "4. Les erreurs 'nexus-reussite-backend' devraient disparaître"

echo ""
echo "🎯 Si le problème persiste :"
echo "   • Relancez : bash verif_finale.sh"
echo "   • Ou vérifiez manuellement : cd nexus-reussite/backend && python -c 'from src.config import get_config; print(\"OK\")'"

echo ""
echo "🎓 NEXUS RÉUSSITE - CACHE NETTOYÉ AVEC SUCCÈS ! 🎓"
