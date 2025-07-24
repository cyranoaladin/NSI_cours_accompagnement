#!/bin/bash

# ==========================================
# APERÇU RAPIDE - NEXUS RÉUSSITE
# ==========================================

echo "👀 APERÇU RAPIDE DE NEXUS RÉUSSITE"
echo "==================================="

cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite

# ==========================================
# 1. DÉMARRAGE DU BACKEND
# ==========================================
echo ""
echo "🐍 Démarrage du Backend..."

cd backend

# Activer l'environnement virtuel
source ../.venv/bin/activate

# Démarrer le backend en arrière-plan
echo "🚀 Lancement de l'API Flask..."
python run_dev.py &
BACKEND_PID=$!

echo "⏳ Attente du démarrage du backend..."
sleep 5

# Test de santé du backend
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend opérationnel sur http://localhost:5000"
else
    echo "⚠️  Backend en cours de démarrage..."
fi

# ==========================================
# 2. DÉMARRAGE DU FRONTEND
# ==========================================
echo ""
echo "⚛️  Démarrage du Frontend..."

cd ../frontend

# Démarrer le frontend en arrière-plan
echo "🚀 Lancement de l'interface React..."
npm run dev &
FRONTEND_PID=$!

echo "⏳ Attente du démarrage du frontend..."
sleep 8

# ==========================================
# 3. OUVERTURE AUTOMATIQUE DU NAVIGATEUR
# ==========================================
echo ""
echo "🌐 OUVERTURE DE L'APERÇU"
echo "========================"

# Déterminer la commande d'ouverture de navigateur selon l'OS
if command -v xdg-open > /dev/null; then
    OPEN_CMD="xdg-open"
elif command -v open > /dev/null; then
    OPEN_CMD="open"
elif command -v start > /dev/null; then
    OPEN_CMD="start"
fi

# Ouvrir les URLs dans le navigateur
if [ ! -z "$OPEN_CMD" ]; then
    echo "🔗 Ouverture automatique du navigateur..."
    $OPEN_CMD "http://localhost:3000" > /dev/null 2>&1 &
    sleep 2
    $OPEN_CMD "http://localhost:5000/health" > /dev/null 2>&1 &
fi

# ==========================================
# 4. AFFICHAGE DES INFORMATIONS
# ==========================================
echo ""
echo "🎉 NEXUS RÉUSSITE EST DÉMARRÉ !"
echo "==============================="
echo ""
echo "📱 INTERFACE PRINCIPALE:"
echo "   👉 http://localhost:3000"
echo "      (Interface utilisateur React)"
echo ""
echo "🔧 API BACKEND:"
echo "   👉 http://localhost:5000"
echo "   👉 http://localhost:5000/health (santé)"
echo "   👉 http://localhost:5000/api/config (config)"
echo ""
echo "🎨 FONCTIONNALITÉS DISPONIBLES:"
echo "   • 🤖 Assistant IA ARIA"
echo "   • 📊 Tableaux de bord interactifs"
echo "   • 👥 Gestion multi-utilisateurs"
echo "   • 📚 Banque d'exercices"
echo "   • 📈 Suivi des progrès"
echo ""
echo "⏸️  POUR ARRÊTER:"
echo "   Appuyez sur Ctrl+C dans ce terminal"
echo ""
echo "🔍 LOGS EN TEMPS RÉEL:"
echo "   Backend : Visible dans ce terminal"
echo "   Frontend: Nouvelle fenêtre de terminal ouverte"
echo ""

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt de Nexus Réussite..."
    echo "   Arrêt du backend (PID: $BACKEND_PID)..."
    kill $BACKEND_PID 2>/dev/null || true
    echo "   Arrêt du frontend (PID: $FRONTEND_PID)..." 
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✅ Tous les services arrêtés"
    echo "👋 Merci d'avoir testé Nexus Réussite !"
    exit 0
}

# Intercepter Ctrl+C
trap cleanup SIGINT SIGTERM

echo "🔄 Services en cours d'exécution..."
echo "    (Les logs du backend s'afficheront ci-dessous)"
echo ""

# Attendre les processus (affichage des logs)
wait $BACKEND_PID $FRONTEND_PID
