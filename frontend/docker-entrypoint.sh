#!/bin/bash

# =========================================
# Nexus Réussite - Frontend Docker Entrypoint
# =========================================

set -e

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function pour attendre qu'un service soit disponible
wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3
    local max_attempts=30
    local attempt=1

    log_info "Attente de $service_name ($host:$port)..."

    while [ $attempt -le $max_attempts ]; do
        if nc -z "$host" "$port" 2>/dev/null; then
            log_info "$service_name est disponible!"
            return 0
        fi

        log_warn "Tentative $attempt/$max_attempts - $service_name indisponible, attente..."
        sleep 2
        attempt=$((attempt + 1))
    done

    log_error "$service_name n'est pas disponible après $max_attempts tentatives"
    return 1
}

# Fonction principale
main() {
    log_info "🚀 Démarrage de Nexus Réussite Frontend"

    # Vérification des variables d'environnement
    if [ -z "$NEXT_PUBLIC_API_URL" ]; then
        log_warn "NEXT_PUBLIC_API_URL non définie, utilisation de la valeur par défaut"
        export NEXT_PUBLIC_API_URL="http://localhost:5000/api"
    fi

    if [ -z "$NEXT_PUBLIC_WS_URL" ]; then
        log_warn "NEXT_PUBLIC_WS_URL non définie, utilisation de la valeur par défaut"
        export NEXT_PUBLIC_WS_URL="ws://localhost:8080/ws"
    fi

    log_info "Configuration Frontend:"
    log_info "  - API URL: $NEXT_PUBLIC_API_URL"
    log_info "  - WebSocket URL: $NEXT_PUBLIC_WS_URL"
    log_info "  - Node Environment: ${NODE_ENV:-development}"

    # Attendre que le backend soit disponible (optionnel en développement)
    if [ "$NODE_ENV" = "production" ]; then
        # Extraire host et port de l'URL API
        API_HOST=$(echo "$NEXT_PUBLIC_API_URL" | sed -E 's|https?://([^:/]+).*|\1|')
        API_PORT=443
        if [[ "$NEXT_PUBLIC_API_URL" == *":5000"* ]]; then
            API_PORT=5000
        elif [[ "$NEXT_PUBLIC_API_URL" == *"http://"* ]]; then
            API_PORT=80
        fi

        # Attendre le backend seulement si c'est localhost
        if [[ "$API_HOST" == "localhost" || "$API_HOST" == "127.0.0.1" ]]; then
            wait_for_service "$API_HOST" "$API_PORT" "Backend API" || log_warn "Backend non disponible, démarrage quand même..."
        fi
    fi

    # Installation des dépendances si node_modules n'existe pas
    if [ ! -d "node_modules" ]; then
        log_info "Installation des dépendances..."
        npm install
    fi

    # Démarrage de l'application
    log_info "🌟 Démarrage de l'application Next.js..."

    if [ "$NODE_ENV" = "production" ]; then
        # Mode production
        log_info "Mode Production - Build et démarrage"
        npm run build
        exec npm start
    else
        # Mode développement
        log_info "Mode Développement - Démarrage avec hot reload"
        exec npm run dev
    fi
}

# Gestion des signaux pour un arrêt propre
trap 'log_info "Arrêt du frontend..."; exit 0' SIGTERM SIGINT

# Point d'entrée
main "$@"
