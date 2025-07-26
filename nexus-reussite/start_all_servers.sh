#!/bin/bash

echo "🚀 Démarrage des serveurs Nexus Réussite..."

# Fonction pour arrêter les processus à la fin
cleanup() {
    echo ""
    echo "⏹️  Arrêt des serveurs..."
    pkill -f "python.*start_server" || true
    pkill -f "vite.*--host" || true
    exit 0
}

# Piéger les signaux d'interruption
trap cleanup INT TERM

# Démarrer le backend
echo "🔧 Démarrage du backend Flask..."
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend
FLASK_PORT=5002 python start_server.py &
BACKEND_PID=$!

# Attendre que le backend soit prêt
echo "⏳ Attente du backend..."
sleep 5

# Vérifier que le backend fonctionne
if curl -s http://localhost:5002/health > /dev/null; then
    echo "✅ Backend démarré avec succès sur http://localhost:5002"
else
    echo "❌ Erreur : le backend n'a pas pu démarrer"
    exit 1
fi

# Démarrer le frontend
echo "🎨 Démarrage du frontend React..."
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/frontend
npm run dev &
FRONTEND_PID=$!

# Attendre que le frontend soit prêt
echo "⏳ Attente du frontend..."
sleep 8

# Vérifier que le frontend fonctionne
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend démarré avec succès sur http://localhost:3000"
else
    echo "❌ Erreur : le frontend n'a pas pu démarrer"
fi

echo ""
echo "🌟 Serveurs démarrés avec succès !"
echo "📱 Frontend : http://localhost:3000"
echo "🔧 Backend  : http://localhost:5002"
echo "📚 API      : http://localhost:5002/api"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter tous les serveurs"

# Attendre indéfiniment (les processus continuent en arrière-plan)
wait
