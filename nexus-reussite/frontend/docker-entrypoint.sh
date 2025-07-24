#!/bin/sh

# Script d'entrée pour le conteneur frontend Nexus Réussite

set -e

# Fonction de logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Démarrage du conteneur frontend Nexus Réussite..."

# Vérifier que les fichiers sont présents
if [ ! -f "/usr/share/nginx/html/index.html" ]; then
    log "ERREUR: Fichiers de l'application non trouvés"
    exit 1
fi

# Remplacer les variables d'environnement dans les fichiers JS
if [ -n "$REACT_APP_API_URL" ]; then
    log "Configuration de l'URL de l'API: $REACT_APP_API_URL"
    find /usr/share/nginx/html -name "*.js" -exec sed -i "s|REACT_APP_API_URL_PLACEHOLDER|$REACT_APP_API_URL|g" {} \;
fi

if [ -n "$REACT_APP_WS_URL" ]; then
    log "Configuration de l'URL WebSocket: $REACT_APP_WS_URL"
    find /usr/share/nginx/html -name "*.js" -exec sed -i "s|REACT_APP_WS_URL_PLACEHOLDER|$REACT_APP_WS_URL|g" {} \;
fi

# Vérifier la configuration Nginx
log "Vérification de la configuration Nginx..."
nginx -t

log "Configuration terminée, démarrage de Nginx..."

# Exécuter la commande passée en argument
exec "$@"

