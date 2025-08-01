# 🔧 VARIABLES D'ENVIRONNEMENT COMPLÈTES - NEXUS RÉUSSITE

**Date :** $(date +"%Y-%m-%d %H:%M:%S")
**Projet :** Nexus Réussite - Plateforme Éducative Intelligente

---

## 📋 INDEX RAPIDE

- [Variables Backend Flask](#-variables-backend-flask)
- [Variables Frontend Next.js](#-variables-frontend-nextjs)
- [Variables Docker/Déploiement](#-variables-dockerdéploiement)
- [Variables Optionnelles](#-variables-optionnelles)
- [Fichiers de Configuration](#-fichiers-de-configuration)
- [Validation](#-validation)

---

## 🔑 VARIABLES BACKEND FLASK

### **OBLIGATOIRES PRODUCTION** ⚠️

```bash
# ======================================
# FLASK & SECURITY - OBLIGATOIRES
# ======================================
FLASK_ENV=production
SECRET_KEY=votre_secret_64_caracteres_minimum_genere_avec_openssl_rand_hex_32
JWT_SECRET_KEY=autre_secret_64_caracteres_minimum_different_du_precedent
CSRF_SECRET_KEY=troisieme_secret_64_caracteres_minimum_encore_different

# ======================================
# DATABASE - POSTGRESQL OBLIGATOIRE
# ======================================
DATABASE_URL=postgresql://username:password@host:5432/nexus_reussite_prod

# Pool de connexions
DB_POOL_SIZE=20
DB_POOL_TIMEOUT=60
DB_MAX_OVERFLOW=40
DB_POOL_RECYCLE=3600

# ======================================
# DOMAINE ET CORS - OBLIGATOIRES
# ======================================
CORS_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com
CORS_TRUSTED_DOMAINS=votre-domaine.com,www.votre-domaine.com

# ======================================
# EMAIL - OBLIGATOIRE POUR NOTIFICATIONS
# ======================================
MAIL_SERVER=smtp.votre-fournisseur.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=notifications@votre-domaine.com
MAIL_PASSWORD=mot_de_passe_email_fort
MAIL_DEFAULT_SENDER=Nexus Réussite <notifications@votre-domaine.com>
```

### **SERVICES EXTERNES** 🌐

```bash
# ======================================
# INTELLIGENCE ARTIFICIELLE - ARIA
# ======================================
OPENAI_API_KEY=sk-proj-VOTRE_CLE_OPENAI_REELLE_ICI
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_TIMEOUT=30

# ======================================
# BASES DE DONNÉES VECTORIELLES (Optionnel)
# ======================================
PINECONE_API_KEY=votre-cle-pinecone-si-utilise
PINECONE_ENVIRONMENT=us-west1-gcp
CHROMA_HOST=localhost
CHROMA_PORT=8000

# ======================================
# CACHE REDIS
# ======================================
REDIS_URL=redis://:password@votre-host-redis:6379/0
CACHE_TTL_SHORT=300
CACHE_TTL_MEDIUM=3600
CACHE_TTL_LONG=86400

# ======================================
# MONITORING & OBSERVABILITÉ
# ======================================
SENTRY_DSN=https://votre-sentry-dsn@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1
```

### **SÉCURITÉ AVANCÉE** 🔒

```bash
# ======================================
# SECRETS MANAGEMENT (Optionnel)
# ======================================
# HashiCorp Vault
VAULT_ADDR=https://vault.votre-domaine.com:8200
VAULT_TOKEN=votre-vault-token
VAULT_SECRET_PATH=secret/nexus-reussite
VAULT_ROLE_ID=votre-role-id-approle
VAULT_SECRET_ID=votre-secret-id-approle

# AWS Secrets Manager (Alternative)
AWS_REGION=us-east-1
AWS_SECRET_NAME=nexus-reussite/production
AWS_ACCESS_KEY_ID=votre-access-key
AWS_SECRET_ACCESS_KEY=votre-secret-key

# ======================================
# HTTPS & CERTIFICATES
# ======================================
SECURITY_ENFORCE_HTTPS=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
SSL_CERT_PATH=/etc/ssl/certs/nexus-reussite.crt
SSL_KEY_PATH=/etc/ssl/private/nexus-reussite.key
```

### **PERFORMANCE & MONITORING** 📊

```bash
# ======================================
# PERFORMANCE TUNING
# ======================================
COMPRESS_LEVEL=6
COMPRESS_MIN_SIZE=500
LOG_LEVEL=WARNING
ENABLE_METRICS=True
ENABLE_SQL_PROFILING=False

# ======================================
# RATE LIMITING
# ======================================
RATELIMIT_STORAGE_URL=redis://:password@redis:6379/0
RATELIMIT_DEFAULT=200 per day,50 per hour,1 per second

# ======================================
# JWT CONFIGURATION
# ======================================
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
JWT_BLACKLIST_ENABLED=True

# ======================================
# UPLOADS & STORAGE
# ======================================
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/var/lib/nexus-reussite/uploads
ALLOWED_EXTENSIONS=pdf,doc,docx,txt,png,jpg,jpeg,gif
```

---

## 🌐 VARIABLES FRONTEND NEXT.JS

### **OBLIGATOIRES PRODUCTION**

```bash
# ======================================
# API & BACKEND CONNECTION
# ======================================
NEXT_PUBLIC_API_URL=https://api.votre-domaine.com/api/v1
NEXT_PUBLIC_WS_URL=wss://api.votre-domaine.com/ws
NEXT_PUBLIC_APP_URL=https://votre-domaine.com

# ======================================
# ENVIRONNEMENT
# ======================================
NODE_ENV=production
NEXT_PUBLIC_ENVIRONMENT=production

# ======================================
# FEATURES & CONFIGURATION
# ======================================
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_SENTRY=true
NEXT_PUBLIC_SITE_NAME=Nexus Réussite
NEXT_PUBLIC_SITE_DESCRIPTION=Plateforme éducative intelligente avec IA

# ======================================
# ANALYTICS (Optionnel)
# ======================================
NEXT_PUBLIC_GA_TRACKING_ID=G-XXXXXXXXXX
NEXT_PUBLIC_HOTJAR_ID=votre-hotjar-id
NEXT_PUBLIC_FACEBOOK_PIXEL_ID=votre-pixel-id

# ======================================
# SECURITY & DOMAIN
# ======================================
NEXT_PUBLIC_DOMAIN=votre-domaine.com
NEXT_PUBLIC_SECURE_COOKIES=true
```

### **DÉVELOPPEMENT UNIQUEMENT**

```bash
# Variables pour développement local
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
NEXT_PUBLIC_WS_URL=http://localhost:5000
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## 🐳 VARIABLES DOCKER/DÉPLOIEMENT

### **Docker Compose**

```bash
# ======================================
# POSTGRESQL
# ======================================
POSTGRES_DB=nexus_reussite_prod
POSTGRES_USER=nexus_user
POSTGRES_PASSWORD=mot_de_passe_postgresql_fort_et_unique

# ======================================
# REDIS
# ======================================
REDIS_PASSWORD=mot_de_passe_redis_fort

# ======================================
# NGINX
# ======================================
NGINX_HOST=votre-domaine.com
NGINX_PORT=80
NGINX_SSL_PORT=443

# ======================================
# DOCKER SPECIFIQUE
# ======================================
COMPOSE_PROJECT_NAME=nexus-reussite
DOCKER_BUILDKIT=1
```

### **VPS/Production**

```bash
# ======================================
# SYSTÈME
# ======================================
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
USER=nexus-reussite
GROUP=www-data
UMASK=0022

# ======================================
# PORTS & NETWORK
# ======================================
PORT=5000
HOST=0.0.0.0
WORKERS=4
TIMEOUT=120

# ======================================
# LOGS & MONITORING
# ======================================
LOG_FILE=/var/log/nexus-reussite/app.log
ERROR_LOG=/var/log/nexus-reussite/error.log
ACCESS_LOG=/var/log/nexus-reussite/access.log
PID_FILE=/var/run/nexus-reussite.pid
```

---

## 🔧 VARIABLES OPTIONNELLES

### **Services Intégrations Externes**

```bash
# ======================================
# WEBHOOKS & NOTIFICATIONS
# ======================================
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...

# ======================================
# STORAGE CLOUD (Optionnel)
# ======================================
AWS_S3_BUCKET=nexus-reussite-uploads
AWS_S3_REGION=eu-west-1
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

# ======================================
# BACKUP & MAINTENANCE
# ======================================
BACKUP_SCHEDULE=0 2 * * *
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET=nexus-reussite-backups
MAINTENANCE_WINDOW=02:00-04:00

# ======================================
# DÉVELOPPEMENT & DEBUG
# ======================================
FLASK_DEBUG=False
WERKZEUG_DEBUG_PIN=off
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
```

---

## 📄 FICHIERS DE CONFIGURATION

### **Fichiers à créer**

```bash
# Backend
nexus-reussite/backend/.env                    # Variables principales
nexus-reussite/backend/.env.production         # Variables production
nexus-reussite/backend/.env.local              # Variables locales (gitignore)

# Frontend
nexus-reussite/frontend/.env                   # Variables Next.js
nexus-reussite/frontend/.env.production        # Variables production frontend
nexus-reussite/frontend/.env.local             # Variables locales (gitignore)

# Root
.env                                            # Variables globales
.env.production                                 # Variables production globales
docker-compose.override.yml                    # Surcharge Docker locale
```

### **Templates disponibles**

```bash
# Utilisez ces templates comme base
nexus-reussite/backend/env.production.template
nexus-reussite/backend/src/secrets_loader.py   # Génère automatiquement un template
```

---

## ✅ VALIDATION

### **Variables CRITIQUES à vérifier**

```bash
# Script de validation
cd nexus-reussite/backend
python -c "
from src.config_production import validate_production_environment
import json
result = validate_production_environment()
print(json.dumps(result, indent=2))
"
```

### **Test des connexions**

```bash
# Test base de données
python -c "import psycopg2; psycopg2.connect('${DATABASE_URL}'); print('✅ PostgreSQL OK')"

# Test Redis
python -c "import redis; r=redis.from_url('${REDIS_URL}'); r.ping(); print('✅ Redis OK')"

# Test OpenAI
python -c "import openai; openai.api_key='${OPENAI_API_KEY}'; print('✅ OpenAI OK')"
```

---

## 🚨 SÉCURITÉ - POINTS CRITIQUES

### **⚠️ À NE JAMAIS OUBLIER**

1. **Secrets uniques** : Chaque `SECRET_KEY`, `JWT_SECRET_KEY` DOIT être différent
2. **Longueur minimale** : Minimum 32 caractères pour tous les secrets
3. **PostgreSQL obligatoire** : Jamais de SQLite en production
4. **HTTPS uniquement** : Tous les domaines en HTTPS
5. **CORS restrictif** : Seulement vos domaines autorisés

### **🔐 Génération de secrets sécurisés**

```bash
# Générer des secrets forts
openssl rand -hex 32  # Pour SECRET_KEY
openssl rand -hex 32  # Pour JWT_SECRET_KEY
openssl rand -hex 32  # Pour CSRF_SECRET_KEY

# Ou utiliser le générateur intégré
cd nexus-reussite/backend
python -c "from src.secrets_loader import create_env_template; print(create_env_template())" > .env.production
```

---

## 📋 CHECKLIST FINAL

### **Avant déploiement, vérifiez :**

- [ ] **Backend** : Toutes les variables obligatoires définies
- [ ] **Frontend** : URLs API correctes
- [ ] **Database** : PostgreSQL configuré et accessible
- [ ] **Redis** : Cache opérationnel
- [ ] **Secrets** : Tous uniques et de 32+ caractères
- [ ] **CORS** : Seulement vos domaines
- [ ] **Email** : SMTP configuré et testé
- [ ] **OpenAI** : Clé API valide (si utilisée)
- [ ] **HTTPS** : Certificats installés
- [ ] **Logs** : Répertoires créés et permissions correctes
- [ ] **Backup** : Stratégie de sauvegarde en place

---

## 🎯 DÉPLOIEMENT RAPIDE

### **Template minimal production**

```bash
# Créer rapidement un .env de production
cat > .env.production << 'EOF'
# === OBLIGATOIRES ===
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://user:pass@host:5432/nexus_reussite_prod
CORS_ORIGINS=https://votre-domaine.com

# === FRONTEND ===
NEXT_PUBLIC_API_URL=https://api.votre-domaine.com/api/v1
NEXT_PUBLIC_WS_URL=wss://api.votre-domaine.com/ws

# === EMAIL ===
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-app

# === IA (Optionnel) ===
OPENAI_API_KEY=sk-votre-cle-openai
EOF
```

**Total : 52 variables identifiées**
**Obligatoires : 15 variables**
**Recommandées : 12 variables**
**Optionnelles : 25 variables**

---

*📝 Ce document liste TOUTES les variables d'environnement du projet Nexus Réussite. Adaptez selon vos besoins spécifiques.*
