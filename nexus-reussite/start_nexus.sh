#!/bin/bash

echo "🚀 Nexus Réussite - Démarrage des serveurs"
echo "==========================================="

# Arrêter les processus existants
pkill -f "python.*start_server" 2>/dev/null || true
pkill -f "vite.*--host" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true

# Démarrer le backend
echo "🔧 Démarrage du backend..."
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend
FLASK_PORT=5002 python start_server.py &
BACKEND_PID=$!

# Attendre le backend
sleep 5

# Vérifier le backend
if curl -s http://localhost:5002/health > /dev/null; then
    echo "✅ Backend opérationnel : http://localhost:5002"
else
    echo "❌ Erreur backend"
    exit 1
fi

# Démarrer le frontend
echo "🎨 Démarrage du frontend..."
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/frontend
npm run dev &
FRONTEND_PID=$!

# Attendre le frontend
sleep 8

# Trouver le port du frontend
FRONTEND_PORT=""
for port in 3000 3001 3002 3003; do
    if curl -s http://localhost:$port > /dev/null; then
        FRONTEND_PORT=$port
        break
    fi
done

if [ -n "$FRONTEND_PORT" ]; then
    echo "✅ Frontend opérationnel : http://localhost:$FRONTEND_PORT"
else
    echo "❌ Erreur frontend"
    exit 1
fi

# Test API
if curl -s http://localhost:5002/api/config | grep -q "Nexus"; then
    echo "✅ API fonctionnelle"
fi

echo ""
echo "🌟 SERVEURS ACTIFS"
echo "Frontend : http://localhost:$FRONTEND_PORT"
echo "Backend  : http://localhost:5002"
echo "API      : http://localhost:5002/api"
echo ""
echo "Les serveurs continuent de fonctionner en arrière-plan"
echo "Pour les arrêter : pkill -f 'python.*start_server'; pkill -f 'vite'"
