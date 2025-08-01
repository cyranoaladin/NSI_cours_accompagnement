#!/bin/bash

# Script de lancement du frontend Next.js
set -e

echo "🚀 Lancement du frontend Nexus Réussite"

# Aller dans le dossier frontend
cd "$(dirname "$0")/../frontend"

# Fonction d'aide
show_help() {
    echo "Usage: $0 [OPTION]"
    echo "Options:"
    echo "  dev       Lancer en mode développement"
    echo "  build     Construire pour la production"
    echo "  start     Lancer en mode production"
    echo "  install   Installer les dépendances"
    echo "  test      Lancer les tests"
    echo "  help      Afficher cette aide"
    exit 0
}

# Vérifier si Node.js est installé
check_node() {
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi

    local node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$node_version" -lt 18 ]; then
        echo "⚠️  Node.js version $node_version détectée. Version 18+ recommandée."
    else
        echo "✅ Node.js version $(node --version) détectée"
    fi
}

# Vérifier si les dépendances sont installées
check_dependencies() {
    if [ ! -d "node_modules" ]; then
        echo "📦 Installation des dépendances..."
        npm install
    fi
}

# Mode développement
start_dev() {
    echo "🔧 Lancement en mode développement..."
    check_node
    check_dependencies

    # Créer le fichier .env.local s'il n'existe pas
    if [ ! -f ".env.local" ]; then
        echo "📝 Création du fichier .env.local..."
        cp .env.local.example .env.local 2>/dev/null || {
            echo "NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1" > .env.local
            echo "NEXT_PUBLIC_WS_URL=http://localhost:5000" >> .env.local
        }
    fi

    echo "🌐 Le serveur sera disponible sur http://localhost:3000"
    npm run dev
}

# Build de production
build_production() {
    echo "🏗️  Construction pour la production..."
    check_node
    check_dependencies
    npm run build
    echo "✅ Build terminé avec succès!"
}

# Mode production
start_production() {
    echo "🚀 Lancement en mode production..."
    check_node

    # Vérifier si le build existe
    if [ ! -d ".next" ]; then
        echo "📦 Aucun build trouvé. Construction en cours..."
        build_production
    fi

    echo "🌐 Le serveur sera disponible sur http://localhost:3000"
    npm run start
}

# Installation des dépendances
install_deps() {
    echo "📦 Installation des dépendances..."
    check_node
    npm install
    echo "✅ Dépendances installées avec succès!"
}

# Tests
run_tests() {
    echo "🧪 Lancement des tests..."
    check_node
    check_dependencies
    npm run test
}

# Traitement des arguments
case "${1:-dev}" in
    "dev"|"development")
        start_dev
        ;;
    "build")
        build_production
        ;;
    "start"|"production"|"prod")
        start_production
        ;;
    "install")
        install_deps
        ;;
    "test")
        run_tests
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Option inconnue: $1"
        show_help
        ;;
esac
