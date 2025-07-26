#!/bin/bash

# Script de lancement complet pour Nexus Réussite
# Ce script démarre le backend Flask et le frontend React en mode développement

echo "🚀 Lancement de la plateforme Nexus Réussite"
echo "============================================="

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt des serveurs..."
    pkill -f "python.*start_server" >/dev/null 2>&1 || true
    pkill -f "vite.*--host" >/dev/null 2>&1 || true
    pkill -f "npm run dev" >/dev/null 2>&1 || true
    echo "✅ Serveurs arrêtés"
    exit 0
}

# Capture des signaux d'interruption
trap cleanup INT TERM

# Variables
BACKEND_PORT=5002
FRONTEND_PORT=3000

echo "📂 Répertoire de travail : $(pwd)"

# Vérification des prérequis
echo "🔍 Vérification des prérequis..."

if [ ! -d "backend" ]; then
    echo "❌ Erreur : dossier 'backend' introuvable"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "❌ Erreur : dossier 'frontend' introuvable"
    exit 1
fi

if [ ! -f "backend/start_server.py" ]; then
    echo "❌ Erreur : script backend 'start_server.py' introuvable"
    exit 1
fi

if [ ! -f "frontend/package.json" ]; then
    echo "❌ Erreur : fichier 'package.json' du frontend introuvable"
    exit 1
fi

echo "✅ Prérequis vérifiés"

# Démarrage du backend
echo ""
echo "🔧 Démarrage du backend Flask..."
cd backend
FLASK_PORT=$BACKEND_PORT python start_server.py > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "⏳ Attente du backend (5 secondes)..."
sleep 5

# Vérification du backend
if curl -s http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
    echo "✅ Backend opérationnel sur http://localhost:$BACKEND_PORT"
else
    echo "❌ Le backend n'a pas pu démarrer sur le port $BACKEND_PORT"
    echo "📄 Logs du backend :"
    tail -10 backend/backend.log 2>/dev/null || echo "Pas de logs disponibles"
    cleanup
fi

# Démarrage du frontend
echo ""
echo "🎨 Démarrage du frontend React..."
cd frontend
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "⏳ Attente du frontend (8 secondes)..."
sleep 8

# Recherche du port réel du frontend
ACTUAL_FRONTEND_PORT=""
for port in 3000 3001 3002 3003 3004 3005; do
    if curl -s http://localhost:$port > /dev/null 2>&1; then
        ACTUAL_FRONTEND_PORT=$port
        break
    fi
done

if [ -n "$ACTUAL_FRONTEND_PORT" ]; then
    echo "✅ Frontend opérationnel sur http://localhost:$ACTUAL_FRONTEND_PORT"
else
    echo "❌ Le frontend n'a pas pu démarrer"
    echo "📄 Logs du frontend :"
    tail -10 frontend/frontend.log 2>/dev/null || echo "Pas de logs disponibles"
    cleanup
fi

# Test de communication API
echo ""
echo "🔗 Test de communication API..."
API_RESPONSE=$(curl -s http://localhost:$BACKEND_PORT/api/config 2>/dev/null)
if echo "$API_RESPONSE" | grep -q "Nexus"; then
    echo "✅ API backend fonctionnelle"
else
    echo "⚠️  API backend accessible mais réponse inattendue"
fi

# Résumé final
echo ""
echo "🌟 NEXUS RÉUSSITE - SERVEURS ACTIFS"
echo "====================================="
echo "📱 Frontend : http://localhost:$ACTUAL_FRONTEND_PORT"
echo "🔧 Backend  : http://localhost:$BACKEND_PORT"
echo "📚 API      : http://localhost:$BACKEND_PORT/api"
echo "💾 Logs     : backend/backend.log, frontend/frontend.log"
echo ""
echo "🎯 Vous pouvez maintenant accéder à l'application"
echo "💡 Appuyez sur Ctrl+C pour arrêter tous les serveurs"
echo ""

# Attente infinie
echo "👂 En attente... (les serveurs continuent de fonctionner)"
while true; do
    sleep 10
    # Vérification périodique que les serveurs sont toujours actifs
    if ! curl -s http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
        echo "❌ Le backend n'est plus accessible"
        cleanup
    fi
    if [ -n "$ACTUAL_FRONTEND_PORT" ] && ! curl -s http://localhost:$ACTUAL_FRONTEND_PORT > /dev/null 2>&1; then
        echo "❌ Le frontend n'est plus accessible"
        cleanup
    fi
done
