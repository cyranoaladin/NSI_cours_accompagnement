#!/bin/bash
# Script de redémarrage du serveur de langage Python
echo "🔄 Redémarrage du serveur de langage Python..."

# Tuer tous les processus Pylance/Pyright
pkill -f "pylance"
pkill -f "pyright"
pkill -f "python.*language.*server"

echo "✅ Processus de serveur de langage arrêtés"
echo "📝 Veuillez redémarrer VS Code pour appliquer les changements"
echo ""
echo "Ou dans VS Code:"
echo "1. Ctrl+Shift+P"
echo "2. Taper: Python: Restart Language Server"
echo "3. Ou: Developer: Reload Window"
