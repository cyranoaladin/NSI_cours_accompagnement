#!/bin/bash

# Script de démarrage pour Nexus Réussite
# Usage: ./start.sh [dev|prod]

set -e

MODE=${1:-dev}
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEXUS_DIR="$PROJECT_DIR/nexus-reussite"

echo "🚀 Démarrage de Nexus Réussite en mode: $MODE"
echo "📁 Répertoire: $NEXUS_DIR"

# Vérifier que le projet existe
if [ ! -d "$NEXUS_DIR" ]; then
    echo "❌ Erreur: Le répertoire nexus-reussite n'existe pas"
    exit 1
fi

cd "$NEXUS_DIR"

case $MODE in
    "dev")
        echo "🔧 Mode développement"
        if [ -f "docker-compose.yml" ]; then
            echo "🐳 Démarrage avec Docker..."
            docker-compose up -d
        else
            echo "📦 Démarrage manuel..."
            echo "Backend: http://localhost:5000"
            echo "Frontend: http://localhost:5173"
            # Démarrage en arrière-plan
            cd backend && python src/main_production.py &
            cd ../frontend && npm run dev &
        fi
        ;;
    "prod")
        echo "🏭 Mode production"
        if [ -f "docker-compose.prod.yml" ]; then
            docker-compose -f docker-compose.prod.yml up -d
        else
            echo "❌ Configuration production non trouvée"
            exit 1
        fi
        ;;
    *)
        echo "❌ Mode invalide. Utilisation: ./start.sh [dev|prod]"
        exit 1
        ;;
esac

echo "✅ Nexus Réussite démarré avec succès!"
echo "🌐 Accéder à l'application: http://localhost:5173"
