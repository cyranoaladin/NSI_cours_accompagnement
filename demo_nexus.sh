#!/bin/bash

# ==========================================
# NEXUS RÉUSSITE - APERÇU COMPLET
# ==========================================

clear
echo "🎓✨ NEXUS RÉUSSITE - PLATEFORME ÉDUCATIVE INTELLIGENTE ✨🎓"
echo "============================================================="
echo ""
echo "🚀 Préparation de l'aperçu..."

PROJECT_ROOT="/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite"
cd "$PROJECT_ROOT"

# ==========================================
# VÉRIFICATION PRÉALABLE
# ==========================================
echo ""
echo "🔍 Vérification de l'environnement..."

# Backend
cd backend
if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
    echo "✅ Environnement Python activé"
else
    echo "❌ Environnement virtuel manquant"
    exit 1
fi

# Test des imports critiques
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from config import get_config
    from main_production import create_app
    print('✅ Modules Python validés')
except Exception as e:
    print(f'❌ Erreur Python: {e}')
    exit(1)
" || exit 1

# Frontend
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances frontend..."
    npm install -q
fi
echo "✅ Frontend validé"

# ==========================================
# LANCEMENT DES SERVICES
# ==========================================
echo ""
echo "🚀 LANCEMENT DES SERVICES"
echo "========================="

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt de Nexus Réussite..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    echo "✅ Services arrêtés"
    echo ""
    echo "👋 Merci d'avoir testé Nexus Réussite !"
    echo "📝 Pour plus d'infos: consultez le README.md"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Démarrage Backend
echo "🐍 Démarrage du Backend Flask..."
cd "$PROJECT_ROOT/backend"
source ../.venv/bin/activate
python run_dev.py > /tmp/nexus-backend.log 2>&1 &
BACKEND_PID=$!

# Attendre le backend
sleep 4
echo "✅ Backend démarré (PID: $BACKEND_PID)"

# Démarrage Frontend
echo "⚛️  Démarrage du Frontend React..."
cd "$PROJECT_ROOT/frontend"
npm run dev > /tmp/nexus-frontend.log 2>&1 &
FRONTEND_PID=$!

# Attendre le frontend
sleep 6
echo "✅ Frontend démarré (PID: $FRONTEND_PID)"

# ==========================================
# AFFICHAGE DES INFORMATIONS
# ==========================================
echo ""
echo "🎉 NEXUS RÉUSSITE EST OPÉRATIONNEL !"
echo "====================================="
echo ""
echo "🌐 ACCÈS DIRECT:"
echo ""
echo "   📱 INTERFACE UTILISATEUR"
echo "   👉 http://localhost:3000"
echo "      Interface moderne React + TailwindCSS"
echo ""
echo "   🔧 API BACKEND"  
echo "   👉 http://localhost:5000"
echo "   👉 http://localhost:5000/health (statut)"
echo "   👉 http://localhost:5000/api/config (configuration)"
echo ""
echo "🎯 FONCTIONNALITÉS À TESTER:"
echo ""
echo "   🤖 ASSISTANT IA ARIA"
echo "   • Chat intelligent adaptatif"
echo "   • Aide personnalisée aux devoirs"
echo "   • Explications détaillées"
echo ""
echo "   📊 TABLEAUX DE BORD"
echo "   • Suivi des progrès en temps réel"
echo "   • Statistiques d'apprentissage"
echo "   • Graphiques interactifs"
echo ""
echo "   👥 GESTION UTILISATEURS"
echo "   • Profils élèves/professeurs/parents"
echo "   • Authentification sécurisée"
echo "   • Permissions granulaires"
echo ""
echo "   📚 BANQUE D'EXERCICES"
echo "   • Contenu adapté au lycée français"
echo "   • Exercices interactifs"
echo "   • Corrections automatiques"
echo ""
echo "🔍 MONITORING:"
echo "   Backend:  tail -f /tmp/nexus-backend.log"
echo "   Frontend: tail -f /tmp/nexus-frontend.log"
echo ""
echo "⏸️  POUR ARRÊTER: Ctrl+C"
echo ""

# Ouverture automatique du navigateur
if command -v xdg-open > /dev/null; then
    echo "🔗 Ouverture automatique du navigateur..."
    xdg-open "http://localhost:3000" > /dev/null 2>&1 &
    sleep 1
    xdg-open "http://localhost:5000/health" > /dev/null 2>&1 &
fi

echo "🔄 Services actifs - Interface prête !"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Bienvenue dans Nexus Réussite - L'avenir de l'éducation ✨"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Attendre les processus
wait $BACKEND_PID $FRONTEND_PID
