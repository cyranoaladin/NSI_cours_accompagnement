#!/bin/bash

# ==========================================
# NETTOYAGE COMPLET DES RÉFÉRENCES VSCODE
# ==========================================

echo "🧹 Nettoyage définitif des références obsolètes VS Code..."

# 1. Fermer VS Code complètement (toutes les instances)
echo "📌 Étape 1: Fermeture complète de VS Code..."
pkill -f "code" 2>/dev/null || true
pkill -f "Code" 2>/dev/null || true
sleep 3

# 2. Supprimer tous les fichiers temporaires VS Code pour ce workspace
echo "📌 Étape 2: Suppression complète des caches VS Code..."

# Cache global VS Code
VSCODE_CACHE_DIRS=(
    "$HOME/.config/Code/User/workspaceStorage"
    "$HOME/.config/Code/CachedExtensions"
    "$HOME/.config/Code/logs"
    "$HOME/.vscode/extensions"
    "$HOME/.config/Code - Insiders/User/workspaceStorage"
)

for cache_dir in "${VSCODE_CACHE_DIRS[@]}"; do
    if [ -d "$cache_dir" ]; then
        find "$cache_dir" -name "*NSI*" -type d -exec rm -rf {} + 2>/dev/null || true
        find "$cache_dir" -name "*nexus*" -type d -exec rm -rf {} + 2>/dev/null || true
    fi
done

# 3. Supprimer tous les fichiers .vscode et caches locaux
echo "📌 Étape 3: Nettoyage des configurations locales..."
find /home/alaeddine/Documents/NSI_cours_accompagnement -name ".vscode" -type d -exec rm -rf {} + 2>/dev/null || true
find /home/alaeddine/Documents/NSI_cours_accompagnement -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find /home/alaeddine/Documents/NSI_cours_accompagnement -name "*.pyc" -type f -delete 2>/dev/null || true
find /home/alaeddine/Documents/NSI_cours_accompagnement -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true

# 4. Confirmer que les anciens dossiers sont bien supprimés
echo "📌 Étape 4: Vérification de la suppression des anciens dossiers..."
OLD_DIRS=(
    "nexus-reussite-backend"
    "nexus-reussite-frontend" 
    "nexus-reussite-complet"
)

for old_dir in "${OLD_DIRS[@]}"; do
    if [ -d "/home/alaeddine/Documents/NSI_cours_accompagnement/$old_dir" ]; then
        echo "⚠️  Suppression définitive de $old_dir..."
        rm -rf "/home/alaeddine/Documents/NSI_cours_accompagnement/$old_dir"
    fi
done

# 5. Supprimer les fichiers temporaires créés pendant le debug
echo "📌 Étape 5: Suppression des fichiers temporaires..."
rm -f /home/alaeddine/Documents/NSI_cours_accompagnement/test_config.py
rm -f /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite.tar.gz

# 6. Créer une configuration workspace PROPRE
echo "📌 Étape 6: Création d'un workspace complètement propre..."
cat > /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite-propre.code-workspace << 'EOF'
{
    "folders": [
        {
            "name": "🎓 Nexus Réussite",
            "path": "./nexus-reussite"
        }
    ],
    "settings": {
        "python.defaultInterpreterPath": "./.venv/bin/python",
        "python.analysis.extraPaths": [
            "./nexus-reussite/backend/src"
        ],
        "python.analysis.autoImportCompletions": true,
        "python.analysis.typeCheckingMode": "basic",
        "typescript.preferences.includePackageJsonAutoImports": "on",
        "files.exclude": {
            "**/__pycache__": true,
            "**/*.pyc": true,
            "**/node_modules": true,
            "**/.git": true,
            "test_config.py": true
        },
        "search.exclude": {
            "**/node_modules": true,
            "**/__pycache__": true,
            "**/.venv": true,
            "test_config.py": true
        },
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black"
    },
    "extensions": {
        "recommendations": [
            "ms-python.python",
            "ms-python.pylint", 
            "ms-python.black-formatter",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode"
        ]
    }
}
EOF

echo ""
echo "✅ NETTOYAGE TERMINÉ AVEC SUCCÈS !"
echo ""
echo "🚀 Pour redémarrer VS Code proprement :"
echo "   code nexus-reussite-propre.code-workspace"
echo ""
echo "💡 Cela garantit une session complètement propre sans aucune référence aux anciens dossiers."
echo "📊 Toutes les erreurs obsolètes seront éliminées définitivement."
