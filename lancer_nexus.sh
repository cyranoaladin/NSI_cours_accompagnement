#!/bin/bash

# ==========================================
# LANCEMENT COMPLET - NEXUS RÉUSSITE
# ==========================================

echo "🚀 LANCEMENT DE NEXUS RÉUSSITE"
echo "==============================="

PROJECT_ROOT="/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite"
cd "$PROJECT_ROOT"

# ==========================================
# 1. PRÉPARATION BACKEND
# ==========================================
echo ""
echo "🐍 PRÉPARATION DU BACKEND"
echo "========================="

cd backend

# Environnement virtuel
if [ ! -d "../.venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv ../.venv
fi

echo "🔧 Activation de l'environnement virtuel..."
source ../.venv/bin/activate

echo "📦 Installation des dépendances backend..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Vérification de la configuration
echo "🔍 Vérification de la configuration..."
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from config import get_config, validate_config
    config = get_config()
    report = validate_config(config)
    print(f'✅ Configuration backend: {report[\"status\"]}')
except Exception as e:
    print(f'⚠️  Configuration avec warnings: {e}')
"

# Initialisation de la base de données si nécessaire
if [ ! -f "documents.db" ]; then
    echo "📊 Initialisation de la base de données..."
    python -c "
import sys
sys.path.insert(0, 'src')
from database import db
from main_production import create_app

app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Base de données initialisée')
" || echo "⚠️  Base de données avec warnings"
fi

echo "✅ Backend prêt !"

# ==========================================
# 2. PRÉPARATION FRONTEND
# ==========================================
echo ""
echo "⚛️  PRÉPARATION DU FRONTEND"
echo "=========================="

cd ../frontend

# Vérification de Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js requis mais non installé"
    echo "💡 Installez Node.js 18+ depuis https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js $(node --version)"

# Installation des dépendances
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances frontend..."
    npm install
else
    echo "✅ Dépendances frontend déjà installées"
fi

echo "✅ Frontend prêt !"

# ==========================================
# 3. DÉMARRAGE DES SERVICES
# ==========================================
echo ""
echo "🚀 DÉMARRAGE DES SERVICES"
echo "========================="

# Créer un fichier de log temporaire
LOG_DIR="/tmp/nexus-logs"
mkdir -p "$LOG_DIR"

echo "📝 Logs disponibles dans: $LOG_DIR"
echo ""
echo "🌐 URLS D'ACCÈS:"
echo "   Backend API:  http://localhost:5000"
echo "   Frontend Web: http://localhost:5173"
echo "   Docs API:     http://localhost:5000/docs"
echo ""
echo "⚠️  Pour arrêter les services: Ctrl+C"
echo ""

# Fonction de nettoyage à l'arrêt
cleanup() {
    echo ""
    echo "🛑 Arrêt des services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    echo "✅ Services arrêtés"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Démarrage du backend
echo "🔄 Démarrage du backend..."
cd "$PROJECT_ROOT/backend"
source ../.venv/bin/activate
python run_dev.py > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

# Attendre que le backend soit prêt
sleep 3

# Test rapide du backend
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend démarré avec succès"
else
    echo "⚠️  Backend en cours de démarrage..."
fi

# Démarrage du frontend
echo "🔄 Démarrage du frontend..."
cd "$PROJECT_ROOT/frontend"
npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!

# Attendre que le frontend soit prêt
sleep 5

echo ""
echo "🎉 NEXUS RÉUSSITE DÉMARRÉ AVEC SUCCÈS !"
echo "======================================="
echo ""
echo "📱 Ouvrez votre navigateur sur:"  
echo "   👉 http://localhost:5173 (Interface principale)"
echo ""
echo "🔧 Backend API disponible sur:"
echo "   👉 http://localhost:5000 (API REST)"
echo ""
echo "📊 Monitoring en temps réel:"
echo "   Backend:  tail -f $LOG_DIR/backend.log"
echo "   Frontend: tail -f $LOG_DIR/frontend.log"
echo ""
echo "⏸️  Pour arrêter: Ctrl+C"

# Attendre les processus
wait $BACKEND_PID $FRONTEND_PID
