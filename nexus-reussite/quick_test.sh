#!/bin/bash

echo "🔧 Arrêt des processus existants..."
pkill -f "python.*start_server" 2>/dev/null || true
pkill -f "vite.*--host" 2>/dev/null || true
sleep 2

echo "🚀 Démarrage du backend Flask..."
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend
FLASK_PORT=5002 python start_server.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

echo "⏳ Attente backend (5s)..."
sleep 5

# Test backend
if curl -s http://localhost:5002/health > /dev/null; then
    echo "✅ Backend OK"
else
    echo "❌ Backend KO"
    exit 1
fi

echo "🎨 Démarrage du frontend React..."
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo "⏳ Attente frontend (10s)..."
sleep 10

# Test sur plusieurs ports
for PORT in 3000 3001 3002 3003; do
    if curl -s http://localhost:$PORT > /dev/null 2>&1; then
        echo "✅ Frontend accessible sur port $PORT"
        echo "🌐 Application prête : http://localhost:$PORT"
        echo "🔧 Backend API : http://localhost:5002"
        echo ""
        echo "Processus actifs :"
        echo "- Backend PID: $BACKEND_PID"
        echo "- Frontend PID: $FRONTEND_PID"
        echo ""
        echo "Appuyez sur Ctrl+C pour arrêter..."
        
        # Attendre interruption
        trap "echo 'Arrêt des serveurs...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT
        
        while true; do
            sleep 1
        done
        exit 0
    fi
done

echo "❌ Frontend non accessible sur les ports testés"
exit 1
