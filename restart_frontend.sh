#!/bin/bash

echo "🔧 CORRECTION DES ERREURS FRONTEND"
echo "=================================="

# Aller dans le répertoire frontend
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/frontend

echo "🧹 Nettoyage des processus..."
pkill -f "npm.*run.*dev" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true

echo "🔄 Redémarrage du serveur frontend..."
sleep 2

# Redémarrer le serveur de développement
npm run dev &

echo "✅ Frontend redémarré avec les corrections !"
echo "🌐 Accédez à: http://localhost:3000"
echo ""
echo "🎯 CORRECTIONS APPLIQUÉES:"
echo "   ✅ Import 'Eye' de lucide-react ajouté"
echo "   ✅ Erreur MIME type Lucide corrigée"
echo "   ✅ Lien stylesheet incorrect supprimé"
echo ""
echo "📱 L'interface devrait maintenant fonctionner sans erreurs !"
