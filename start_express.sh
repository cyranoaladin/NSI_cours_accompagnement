#!/bin/bash

# Démarrage express Nexus Réussite

echo "⚡ DÉMARRAGE EXPRESS NEXUS RÉUSSITE"
echo "=================================="

cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite

# Arrêter les processus existants
pkill -f "python run_dev.py" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true
sleep 1

# Backend
echo "🐍 Backend..."
cd backend
source ../.venv/bin/activate
python run_dev.py &
BACKEND_PID=$!

# Frontend  
echo "⚛️  Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎯 SERVICES DÉMARRÉS:"
echo "   Backend: http://localhost:5000 (PID: $BACKEND_PID)"
echo "   Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "⏳ Attente de 10 secondes pour stabilisation..."

sleep 10

echo ""
echo "✅ NEXUS RÉUSSITE OPÉRATIONNEL!"
echo "   👉 Interface: http://localhost:3000"
echo "   👉 API: http://localhost:5000"
echo ""
echo "🛑 Pour arrêter: Ctrl+C"

# Attendre
wait
