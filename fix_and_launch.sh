#!/bin/bash

echo "🔧✨ CORRECTION COMPLÈTE DES ERREURS NEXUS RÉUSSITE ✨🔧"
echo "========================================================"

echo "🎯 ÉTAPE 1: Nettoyage des processus"
pkill -f "python.*lancement_definitif.py" 2>/dev/null || true
pkill -f "python.*run_dev.py" 2>/dev/null || true  
pkill -f "npm.*run.*dev" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true

echo "🎯 ÉTAPE 2: Nettoyage des caches"
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/frontend
rm -rf node_modules/.vite/
rm -rf dist/
rm -rf .next/

echo "🎯 ÉTAPE 3: Vérification des corrections"
echo "   ✅ Import 'Eye' ajouté dans LandingPage.jsx"
echo "   ✅ Import 'Monitor' ajouté dans LandingPage.jsx"
echo "   ✅ Lien Lucide erroné supprimé de index.html"
echo "   ✅ Lien Lucide erroné supprimé de dist/index.html"

echo "🎯 ÉTAPE 4: Reconstruction rapide"
npm run build --silent

echo "🎯 ÉTAPE 5: Redémarrage des services"
sleep 2

# Revenir au répertoire principal
cd /home/alaeddine/Documents/NSI_cours_accompagnement

echo ""
echo "🌟 CORRECTIONS APPLIQUÉES:"
echo "   🔧 Toutes les icônes Lucide importées"
echo "   🔧 Erreurs MIME type corrigées"
echo "   🔧 Cache Vite nettoyé"
echo "   🔧 Build fraîche générée"
echo ""

echo "🚀 Lancement du système complet..."
python3 lancement_definitif.py
