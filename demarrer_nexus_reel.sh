#!/bin/bash

# ==========================================
# DÉMARRAGE RÉEL - NEXUS RÉUSSITE
# ==========================================

echo "🚀 DÉMARRAGE RÉEL DE NEXUS RÉUSSITE"
echo "===================================="

PROJECT_ROOT="/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -d "$PROJECT_ROOT" ]; then
    echo "❌ Projet non trouvé à $PROJECT_ROOT"
    exit 1
fi

cd "$PROJECT_ROOT"

# ==========================================
# 1. PRÉPARATION BACKEND
# ==========================================
echo ""
echo "🐍 PRÉPARATION DU BACKEND"
echo "========================="

cd backend

# Vérifier l'environnement virtuel
if [ ! -d "../.venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv ../.venv
fi

# Activer l'environnement virtuel
source ../.venv/bin/activate
echo "✅ Environnement virtuel activé"

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dépendances backend installées"

# Test rapide des imports
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from config import get_config
    from main_production import create_app
    print('✅ Imports backend validés')
except Exception as e:
    print(f'❌ Erreur: {e}')
    exit(1)
" || exit 1

# ==========================================
# 2. PRÉPARATION FRONTEND
# ==========================================
echo ""
echo "⚛️  PRÉPARATION DU FRONTEND"
echo "=========================="

cd ../frontend

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js requis mais non trouvé"
    exit 1
fi

echo "✅ Node.js $(node --version)"

# Installer les dépendances si nécessaire
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances frontend..."
    npm install
else
    echo "✅ Dépendances frontend déjà installées"
fi

# ==========================================
# 3. ARRÊT DES PROCESSUS EXISTANTS
# ==========================================
echo ""
echo "🧹 NETTOYAGE DES PROCESSUS EXISTANTS"
echo "====================================="

# Arrêter les processus existants sur les ports
echo "🔍 Arrêt des processus sur les ports 3000 et 5000..."
pkill -f "python run_dev.py" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true

# Attendre un peu
sleep 2

# ==========================================
# 4. DÉMARRAGE DES SERVICES
# ==========================================
echo ""
echo "🚀 DÉMARRAGE DES SERVICES"
echo "========================="

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt des services Nexus Réussite..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    echo "✅ Services arrêtés proprement"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Créer des fichiers de log
LOG_DIR="/tmp/nexus-logs"
mkdir -p "$LOG_DIR"

# Démarrage du backend
echo "🐍 Démarrage du backend Flask..."
cd "$PROJECT_ROOT/backend"
source ../.venv/bin/activate

# Démarrer en arrière-plan
nohup python run_dev.py > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

echo "   Backend PID: $BACKEND_PID"
echo "   Log: $LOG_DIR/backend.log"

# Attendre que le backend soit prêt
echo "⏳ Attente du démarrage du backend..."
for i in {1..10}; do
    if curl -s http://localhost:5000/health > /dev/null 2>&1; then
        echo "✅ Backend opérationnel sur http://localhost:5000"
        break
    fi
    sleep 1
    echo "   Tentative $i/10..."
done

# Démarrage du frontend
echo ""
echo "⚛️  Démarrage du frontend React..."
cd "$PROJECT_ROOT/frontend"

# Démarrer en arrière-plan
nohup npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!

echo "   Frontend PID: $FRONTEND_PID"
echo "   Log: $LOG_DIR/frontend.log"

# Attendre que le frontend soit prêt
echo "⏳ Attente du démarrage du frontend..."
for i in {1..15}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend opérationnel sur http://localhost:3000"
        break
    fi
    sleep 1
    echo "   Tentative $i/15..."
done

# ==========================================
# 5. VÉRIFICATION FINALE
# ==========================================
echo ""
echo "🔍 VÉRIFICATION FINALE"
echo "======================"

# Test backend
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend: http://localhost:5000 - OPÉRATIONNEL"
else
    echo "❌ Backend: Problème de démarrage"
    echo "📋 Log backend:"
    tail -5 "$LOG_DIR/backend.log"
fi

# Test frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend: http://localhost:3000 - OPÉRATIONNEL"
else
    echo "❌ Frontend: Problème de démarrage"
    echo "📋 Log frontend:"
    tail -5 "$LOG_DIR/frontend.log"
fi

# ==========================================
# 6. AFFICHAGE DES INFORMATIONS
# ==========================================
echo ""
echo "🎉 NEXUS RÉUSSITE DÉMARRÉ AVEC SUCCÈS!"
echo "======================================"
echo ""
echo "🌐 ACCÈS DIRECT:"
echo ""
echo "   📱 INTERFACE UTILISATEUR:"
echo "   👉 http://localhost:3000"
echo "      React + Vite + TailwindCSS"
echo ""
echo "   🔧 API BACKEND:"
echo "   👉 http://localhost:5000"
echo "   👉 http://localhost:5000/health"
echo "   👉 http://localhost:5000/api/config"
echo ""
echo "📊 MONITORING:"
echo "   Backend:  tail -f $LOG_DIR/backend.log"
echo "   Frontend: tail -f $LOG_DIR/frontend.log"
echo ""
echo "🔄 PROCESSUS ACTIFS:"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "⏸️  POUR ARRÊTER: Ctrl+C dans ce terminal"
echo ""

# Ouverture automatique du navigateur
if command -v xdg-open > /dev/null; then
    echo "🔗 Ouverture du navigateur..."
    xdg-open "http://localhost:3000" > /dev/null 2>&1 &
    sleep 1
    xdg-open "http://localhost:5000/health" > /dev/null 2>&1 &
fi

echo "✨ Nexus Réussite est maintenant accessible!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Attendre les processus
wait $BACKEND_PID $FRONTEND_PID
