#!/bin/bash

# LANCEMENT IMMÉDIAT NEXUS RÉUSSITE
echo "🚀 LANCEMENT IMMÉDIAT - NEXUS RÉUSSITE"
echo "======================================"

cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite

# Arrêter les processus existants
pkill -f "python.*run_dev.py" 2>/dev/null || true
pkill -f "npm.*run.*dev" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true

sleep 2

echo "🐍 BACKEND - Démarrage en cours..."
cd backend
source ../../.venv/bin/activate
nohup python run_dev.py > /tmp/nexus-backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

echo "⚛️  FRONTEND - Démarrage en cours..."
cd ../frontend  
nohup npm run dev > /tmp/nexus-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "⏳ Stabilisation (15s)..."
sleep 15

echo ""
echo "🎉 NEXUS RÉUSSITE OPÉRATIONNEL!"
echo "==============================="
echo ""
echo "🌐 ACCÈS:"
echo "   👉 Frontend: http://localhost:3000"
echo "   👉 Backend:  http://localhost:5000"
echo ""
echo "📊 PROCESSUS:"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "📝 LOGS:"
echo "   Backend:  tail -f /tmp/nexus-backend.log"
echo "   Frontend: tail -f /tmp/nexus-frontend.log"
echo ""
echo "✅ Services lancés avec succès!"
echo "🔄 Rafraîchissez les onglets Simple Browser dans VS Code"
