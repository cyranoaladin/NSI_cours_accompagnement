#!/bin/bash
# ==========================================
# NEXUS RÉUSSITE - SCRIPT D'ENTRÉE DOCKER
# ==========================================
# Script d'initialisation pour le conteneur backend

set -e

echo "🚀 Démarrage de Nexus Réussite Backend..."

# Fonction de logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Vérifier les variables d'environnement critiques
check_env() {
    log "🔍 Vérification de la configuration..."
    
    if [ -z "$OPENAI_API_KEY" ]; then
        log "⚠️  AVERTISSEMENT: OPENAI_API_KEY non définie - L'IA ne fonctionnera pas"
    else
        log "✅ OpenAI API Key configurée"
    fi
    
    if [ -z "$SECRET_KEY" ]; then
        log "⚠️  AVERTISSEMENT: SECRET_KEY non définie - Utilisation d'une clé par défaut"
    fi
    
    if [ -z "$DATABASE_URL" ]; then
        log "ℹ️  DATABASE_URL non définie - Utilisation de SQLite par défaut"
    else
        log "✅ Base de données configurée"
    fi
}

# Attendre que la base de données soit disponible
wait_for_db() {
    if [[ "$DATABASE_URL" == postgres* ]]; then
        log "⏳ Attente de la base de données PostgreSQL..."
        
        # Extraire les informations de connexion
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        
        if [ -z "$DB_PORT" ]; then
            DB_PORT=5432
        fi
        
        # Attendre que PostgreSQL soit disponible
        timeout=30
        while ! nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; do
            timeout=$((timeout - 1))
            if [ $timeout -eq 0 ]; then
                log "❌ Timeout: Impossible de se connecter à PostgreSQL"
                exit 1
            fi
            log "⏳ Attente de PostgreSQL ($timeout secondes restantes)..."
            sleep 1
        done
        
        log "✅ PostgreSQL est disponible"
    fi
}

# Initialiser la base de données si nécessaire
init_db() {
    log "📋 Vérification de la base de données..."
    
    # Vérifier si les tables existent
    python -c "
from src.main_production import create_app, db
from src.config import validate_config

app = create_app()
with app.app_context():
    try:
        # Tester la connexion
        db.session.execute('SELECT 1')
        
        # Vérifier si les tables principales existent
        tables = db.session.execute(\"\"\"
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'users'
        \"\"\").fetchall()
        
        if not tables:
            print('INIT_REQUIRED')
        else:
            print('DB_OK')
            
    except Exception as e:
        print('INIT_REQUIRED')
" > /tmp/db_status

    DB_STATUS=$(cat /tmp/db_status)
    
    if [ "$DB_STATUS" = "INIT_REQUIRED" ]; then
        log "🔧 Initialisation de la base de données..."
        
        if [ "$ENABLE_DEMO_DATA" = "true" ]; then
            log "📝 Création des données de démonstration..."
            python src/database/init_db_improved.py
        else
            log "📋 Création des tables uniquement..."
            python -c "
from src.main_production import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Tables créées avec succès')
"
        fi
        
        log "✅ Base de données initialisée"
    else
        log "✅ Base de données déjà initialisée"
    fi
}

# Vérifier la configuration
validate_config() {
    log "🔍 Validation de la configuration finale..."
    
    python -c "
from src.config import validate_config
import sys

report = validate_config()
print(f'Statut de configuration: {report[\"status\"]}')

if report['issues']:
    print('❌ Problèmes critiques:')
    for issue in report['issues']:
        print(f'  - {issue}')
        
if report['warnings']:
    print('⚠️  Avertissements:')
    for warning in report['warnings']:
        print(f'  - {warning}')

if report['status'] == 'critical':
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        log "✅ Configuration validée"
    else
        log "❌ Configuration critique manquante"
        exit 1
    fi
}

# Fonction principale
main() {
    log "🌟 Initialisation de Nexus Réussite Backend v1.0.0"
    
    # Exécuter les vérifications
    check_env
    wait_for_db
    init_db
    validate_config
    
    log "🚀 Démarrage de l'application..."
    log "📡 API disponible sur: http://0.0.0.0:5000"
    log "📋 Documentation: http://0.0.0.0:5000/api/docs"
    log "❤️  Health check: http://0.0.0.0:5000/health"
    
    # Exécuter la commande fournie
    exec "$@"
}

# Point d'entrée
if [ "$1" = "gunicorn" ] || [ "$1" = "python" ]; then
    main "$@"
else
    # Pour les commandes personnalisées (tests, migration, etc.)
    log "🔧 Exécution de la commande personnalisée: $*"
    exec "$@"
fi
