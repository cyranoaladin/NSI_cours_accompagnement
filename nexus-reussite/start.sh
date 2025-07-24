#!/bin/bash

# 🚀 Script de déploiement Nexus Réussite
# Usage: ./start.sh [dev|prod]

set -e

MODE=${1:-dev}

echo "🎓 NEXUS RÉUSSITE - Démarrage en mode $MODE"
echo "═══════════════════════════════════════════════"

case $MODE in
  "dev")
    echo "🔧 Mode développement"
    echo "📦 Installation des dépendances..."
    
    # Backend
    echo "⚙️ Configuration Backend..."
    cd backend
    if [ ! -d ".venv" ]; then
      python -m venv .venv
    fi
    source .venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    # Frontend
    echo "🎨 Configuration Frontend..."
    cd frontend
    npm install
    cd ..
    
    echo "🚀 Démarrage des services..."
    echo "Backend: http://localhost:5000"
    echo "Frontend: http://localhost:3000"
    
    # Démarrage en parallèle
    cd backend && source .venv/bin/activate && python run_dev.py &
    cd frontend && npm run dev &
    
    wait
    ;;
    
  "prod")
    echo "🏭 Mode production"
    echo "🐳 Démarrage avec Docker..."
    docker-compose up --build -d
    echo "✅ Services démarrés !"
    echo "🌐 Accès: http://localhost"
    ;;
    
  *)
    echo "❌ Mode non reconnu. Usage: ./start.sh [dev|prod]"
    exit 1
    ;;
esac
