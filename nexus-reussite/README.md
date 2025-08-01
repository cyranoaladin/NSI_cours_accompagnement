# 🎓 Nexus Réussite - Plateforme Éducative NSI

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture Technique](#architecture-technique)
3. [Technologies Utilisées](#technologies-utilisées)
4. [Structure du Projet](#structure-du-projet)
5. [Configuration VPS](#configuration-vps)
6. [Configuration Base de Données](#configuration-base-de-données)
7. [Agent IA ARIA](#agent-ia-aria)
8. [Authentification et Sécurité](#authentification-et-sécurité)
9. [Déploiement Production](#déploiement-production)
10. [Monitoring et Maintenance](#monitoring-et-maintenance)
11. [API Documentation](#api-documentation)
12. [Troubleshooting](#troubleshooting)

---

## 🌟 Vue d'ensemble

### Description
Nexus Réussite est une plateforme éducative révolutionnaire dédiée à l'enseignement de la NSI (Numérique et Sciences Informatiques). Elle combine intelligence artificielle, suivi personnalisé et contenus pédagogiques interactifs pour accompagner les étudiants de Première et Terminale vers l'excellence.

### Fonctionnalités Principales
- 🤖 **Assistant IA ARIA** - Intelligence artificielle conversationnelle
- 📚 **Cours NSI Complets** - Programme Première et Terminale
- 👥 **Multi-rôles** - Étudiants, Parents, Enseignants, Administrateurs
- 📊 **Suivi Personnalisé** - Analytics et progression en temps réel
- 🎯 **Évaluations** - Quiz, TP et examens blancs
- 💬 **Communication** - WebSocket temps réel
- 📱 **Responsive** - Compatible mobile, tablet, desktop

---

## 🏗️ Architecture Technique

### Architecture Globale

```
┌─────────────────────────────────────────────────────────────┐
│                    NEXUS RÉUSSITE                           │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Next.js 14)     │  Backend (Flask)               │
│  ┌─────────────────────┐   │  ┌─────────────────────────┐   │
│  │ React Components    │   │  │ API REST                │   │
│  │ Zustand Store       │   │  │ Authentication          │   │
│  │ Tailwind CSS        │   │  │ Business Logic          │   │
│  │ WebSocket Client    │   │  │ WebSocket Server        │   │
│  └─────────────────────┘   │  └─────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    Services Externes                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ PostgreSQL  │ │ Agent ARIA  │ │ Redis Cache │          │
│  │ Database    │ │ (OpenAI)    │ │             │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Microservices

```
Internet
    │
    ▼
┌─────────────┐
│   Nginx     │ ← Reverse Proxy / Load Balancer
│  (Port 80)  │
└─────────────┘
    │
    ├── Frontend (Next.js) ─── Port 3000
    ├── Backend API (Flask) ── Port 5000
    ├── WebSocket Server ───── Port 8080
    └── Agent ARIA ──────────── Port 5001
```

---

## 🛠️ Technologies Utilisées

### Frontend Stack
```json
{
  "framework": "Next.js 14.0.4",
  "language": "JavaScript/TypeScript",
  "ui_library": "React 18.2.0",
  "styling": "Tailwind CSS 3.4.0",
  "components": "Shadcn/ui + Radix UI",
  "state_management": "Zustand 4.4.7",
  "forms": "React Hook Form 7.48.2",
  "validation": "Zod 3.22.4",
  "http_client": "Axios 1.6.2",
  "websocket": "Socket.io-client 4.7.4",
  "animations": "Framer Motion 10.16.16",
  "charts": "Recharts 2.8.0",
  "testing": "Vitest 1.1.0 + Testing Library"
}
```

### Backend Stack
```json
{
  "framework": "Flask 3.1.1",
  "language": "Python 3.12",
  "database_orm": "SQLAlchemy 3.1.1",
  "migrations": "Alembic 1.16.4",
  "authentication": "Flask-JWT-Extended 4.7.1",
  "cors": "Flask-CORS 6.0.1",
  "websocket": "Flask-SocketIO",
  "validation": "Pydantic 2.10.1",
  "security": "Flask-Talisman",
  "rate_limiting": "Flask-Limiter",
  "monitoring": "Sentry SDK 2.34.1",
  "logging": "Structlog 25.4.0",
  "server": "Gunicorn 23.0.0"
}
```

### Infrastructure
```json
{
  "database": "PostgreSQL 15+",
  "cache": "Redis 7+",
  "web_server": "Nginx 1.22+",
  "container": "Docker + Docker Compose",
  "process_manager": "PM2",
  "ssl": "Let's Encrypt (Certbot)",
  "monitoring": "Prometheus + Grafana",
  "logging": "ELK Stack (Elasticsearch, Logstash, Kibana)"
}
```

### Services IA
```json
{
  "ai_provider": "OpenAI GPT-4",
  "ai_framework": "LangChain",
  "vector_database": "Pinecone/Weaviate",
  "embeddings": "OpenAI Embeddings",
  "speech": "OpenAI Whisper",
  "text_to_speech": "ElevenLabs/OpenAI TTS"
}
```

---

## 📁 Structure du Projet

### Arborescence Complète

```
nexus-reussite/
├── 📁 frontend/                    # Application Next.js
│   ├── 📁 src/
│   │   ├── 📁 app/                 # App Router Next.js 14
│   │   │   ├── 📄 layout.tsx       # Layout racine
│   │   │   ├── 📄 page.tsx         # Page d'accueil
│   │   │   ├── 📁 auth/            # Pages d'authentification
│   │   │   │   ├── 📁 login/
│   │   │   │   └── 📁 register/
│   │   │   └── 📁 dashboard/       # Pages dashboard
│   │   │       ├── 📄 page.tsx     # Dashboard générique
│   │   │       ├── 📁 student/     # Dashboard étudiant
│   │   │       ├── 📁 parent/      # Dashboard parent
│   │   │       ├── 📁 teacher/     # Dashboard enseignant
│   │   │       └── 📁 admin/       # Dashboard admin
│   │   ├── 📁 components/          # Composants React
│   │   │   ├── 📄 Header.jsx       # Header unifié
│   │   │   ├── 📄 LandingPage.jsx  # Page d'accueil
│   │   │   ├── 📄 StudentDashboard.jsx
│   │   │   ├── 📄 ARIAAgent.jsx    # Interface Agent IA
│   │   │   ├── 📁 ui/              # Composants UI (Shadcn)
│   │   │   └── 📁 Dashboard/
│   │   ├── 📁 stores/              # State Management (Zustand)
│   │   │   ├── 📄 authStore.js     # Authentification
│   │   │   ├── 📄 contentStore.js  # Contenu pédagogique
│   │   │   └── 📄 appStore.js      # État global
│   │   ├── 📁 services/            # Services API
│   │   │   ├── 📄 api.js           # Client HTTP
│   │   │   └── 📄 websocket.js     # WebSocket
│   │   ├── 📁 hooks/               # Hooks personnalisés
│   │   ├── 📁 utils/               # Utilitaires
│   │   └── 📁 lib/                 # Configuration
│   ├── 📁 public/                  # Assets statiques
│   │   ├── 🖼️ logo_nexus-reussite.png
│   │   └── 📄 favicon.ico
│   ├── 📄 package.json             # Dépendances Node.js
│   ├── 📄 next.config.mjs          # Configuration Next.js
│   ├── 📄 tailwind.config.js       # Configuration Tailwind
│   └── 📄 Dockerfile               # Container Frontend
│
├── 📁 backend/                     # Application Flask
│   ├── 📁 src/
│   │   ├── 📄 app.py               # Application principale
│   │   ├── 📄 config.py            # Configuration
│   │   ├── 📁 models/              # Modèles SQLAlchemy
│   │   │   ├── 📄 base.py          # Modèle de base
│   │   │   ├── 📄 user.py          # Utilisateurs
│   │   │   ├── 📄 content_system.py # Contenu pédagogique
│   │   │   └── 📁 schemas/         # Schémas Pydantic
│   │   ├── 📁 routes/              # Routes API
│   │   │   ├── 📄 auth.py          # Authentification
│   │   │   ├── 📄 users.py         # Gestion utilisateurs
│   │   │   ├── 📄 content.py       # Contenu pédagogique
│   │   │   ├── 📄 aria.py          # Agent IA
│   │   │   └── 📄 websocket.py     # WebSocket
│   │   ├── 📁 services/            # Logique métier
│   │   │   ├── 📄 auth_service.py  # Service d'authentification
│   │   │   ├── 📄 user_service.py  # Service utilisateurs
│   │   │   ├── 📄 aria_ai.py       # Service IA
│   │   │   └── 📄 content_service.py
│   │   ├── 📁 middleware/          # Middleware
│   │   │   ├── 📄 security.py      # Sécurité
│   │   │   └── 📄 cors_enhanced.py # CORS
│   │   ├── 📁 utils/               # Utilitaires
│   │   └── 📁 database_scripts/    # Scripts DB
│   ├── 📄 requirements.txt         # Dépendances Python
│   ├── 📄 requirements.in          # Dépendances source
│   ├── 📄 alembic.ini             # Configuration migrations
│   └── 📄 Dockerfile              # Container Backend
│
├── 📁 database/                   # Configuration DB
│   ├── 📄 init.sql               # Script d'initialisation
│   ├── 📄 schema.sql             # Schéma de base
│   └── 📁 migrations/            # Migrations Alembic
│
├── 📁 ai-agent/                  # Service Agent ARIA
│   ├── 📄 aria_main.py          # Service principal
│   ├── 📄 conversation.py       # Gestion conversations
│   ├── 📄 knowledge_base.py     # Base de connaissances
│   └── 📄 requirements.txt      # Dépendances IA
│
├── 📁 nginx/                    # Configuration Nginx
│   ├── 📄 nginx.conf           # Configuration principale
│   ├── 📄 ssl.conf             # Configuration SSL
│   └── 📄 sites-available/     # Sites virtuels
│
├── 📁 docker/                  # Configuration Docker
│   ├── 📄 docker-compose.yml   # Orchestration
│   ├── 📄 docker-compose.prod.yml # Production
│   └── 📁 scripts/            # Scripts de déploiement
│
├── 📁 docs/                   # Documentation
│   ├── 📄 API.md             # Documentation API
│   ├── 📄 DEPLOYMENT.md      # Guide de déploiement
│   └── 📄 ARCHITECTURE.md    # Architecture détaillée
│
├── 📄 docker-compose.yml     # Développement
├── 📄 .env.example          # Variables d'environnement
└── 📄 README.md             # Ce fichier
```

---

## 🖥️ Configuration VPS

### Prérequis Serveur

#### Spécifications Minimales
```yaml
CPU: 2 vCPU (4 vCPU recommandé)
RAM: 4 GB (8 GB recommandé)
Stockage: 50 GB SSD (100 GB recommandé)
Bande passante: 100 Mbps
OS: Ubuntu 22.04 LTS / Debian 12
```

#### Spécifications Production
```yaml
CPU: 4-8 vCPU
RAM: 16-32 GB
Stockage: 200-500 GB SSD NVMe
Bande passante: 1 Gbps
Load Balancer: Recommandé pour > 1000 utilisateurs
CDN: CloudFlare ou AWS CloudFront
```

### Installation Initiale

#### 1. Mise à jour du système
```bash
# Connexion au serveur
ssh root@your-server-ip

# Mise à jour des paquets
apt update && apt upgrade -y

# Installation des outils de base
apt install -y curl wget git vim htop unzip software-properties-common
```

#### 2. Création utilisateur non-root
```bash
# Créer utilisateur
adduser nexusadmin
usermod -aG sudo nexusadmin

# Configuration SSH pour le nouvel utilisateur
mkdir -p /home/nexusadmin/.ssh
cp ~/.ssh/authorized_keys /home/nexusadmin/.ssh/
chown -R nexusadmin:nexusadmin /home/nexusadmin/.ssh
chmod 700 /home/nexusadmin/.ssh
chmod 600 /home/nexusadmin/.ssh/authorized_keys
```

#### 3. Configuration du pare-feu
```bash
# Installation UFW
apt install -y ufw

# Configuration des règles
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 5432/tcp  # PostgreSQL (seulement si accès externe nécessaire)
ufw allow 6379/tcp  # Redis (seulement si accès externe nécessaire)

# Activation
ufw enable
```

### Installation Docker

```bash
# Installation Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Ajout utilisateur au groupe docker
usermod -aG docker nexusadmin

# Installation Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Vérification
docker --version
docker-compose --version
```

### Installation Node.js et Python

```bash
# Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

# Python 3.12
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# Vérification
node --version
npm --version
python3.12 --version
```

### Installation Nginx

```bash
# Installation
apt install -y nginx

# Démarrage et activation
systemctl start nginx
systemctl enable nginx

# Test
curl http://localhost
```

---

## 🗄️ Configuration Base de Données

### Installation PostgreSQL

#### Installation sur Ubuntu
```bash
# Installation PostgreSQL 15
apt install -y postgresql postgresql-contrib postgresql-client

# Démarrage et activation
systemctl start postgresql
systemctl enable postgresql

# Vérification
sudo -u postgres psql -c "SELECT version();"
```

#### Configuration PostgreSQL

```bash
# Connexion en tant qu'utilisateur postgres
sudo -u postgres psql

-- Dans psql
-- Création de la base de données
CREATE DATABASE nexus_reussite;

-- Création de l'utilisateur
CREATE USER nexus_user WITH PASSWORD 'votre_mot_de_passe_securise';

-- Attribution des privilèges
GRANT ALL PRIVILEGES ON DATABASE nexus_reussite TO nexus_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO nexus_user;

-- Configuration des permissions
ALTER USER nexus_user CREATEDB;

-- Quitter psql
\q
```

#### Configuration avancée PostgreSQL

```bash
# Édition du fichier de configuration
sudo vim /etc/postgresql/15/main/postgresql.conf
```

```ini
# /etc/postgresql/15/main/postgresql.conf

# Connexions
listen_addresses = 'localhost'  # ou '*' pour accès externe
port = 5432
max_connections = 200

# Mémoire
shared_buffers = 256MB          # 25% de la RAM
effective_cache_size = 1GB      # 75% de la RAM
work_mem = 4MB
maintenance_work_mem = 64MB

# Logging
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'all'
log_min_duration_statement = 1000  # Log requêtes > 1s

# Performance
checkpoint_segments = 32
checkpoint_completion_target = 0.7
wal_buffers = 16MB

# Sécurité
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

```bash
# Configuration des accès
sudo vim /etc/postgresql/15/main/pg_hba.conf
```

```ini
# /etc/postgresql/15/main/pg_hba.conf

# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
local   all             all                                     peer
host    nexus_reussite  nexus_user      127.0.0.1/32           md5
host    nexus_reussite  nexus_user      ::1/128                md5

# Pour accès externe (si nécessaire)
# host    nexus_reussite  nexus_user      0.0.0.0/0              md5
```

```bash
# Redémarrage PostgreSQL
sudo systemctl restart postgresql
```

### Schéma de Base de Données

#### Structure des Tables Principales

```sql
-- Utilisateurs
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'parent', 'teacher', 'admin')),
    phone VARCHAR(20),
    date_of_birth DATE,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profils étudiants
CREATE TABLE student_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    class_level VARCHAR(20) NOT NULL CHECK (class_level IN ('premiere', 'terminale')),
    school_name VARCHAR(200),
    parent_id INTEGER REFERENCES users(id),
    academic_year VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contenu pédagogique
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    level VARCHAR(20) NOT NULL,
    category VARCHAR(50),
    content JSONB,
    is_published BOOLEAN DEFAULT FALSE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Progression des étudiants
CREATE TABLE student_progress (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    progress_percentage INTEGER DEFAULT 0,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    UNIQUE(student_id, course_id)
);

-- Évaluations
CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id),
    title VARCHAR(200) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('quiz', 'tp', 'exam', 'project')),
    questions JSONB,
    max_score INTEGER,
    time_limit INTEGER, -- en minutes
    is_published BOOLEAN DEFAULT FALSE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Résultats des évaluations
CREATE TABLE assessment_results (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER REFERENCES assessments(id),
    student_id INTEGER REFERENCES users(id),
    answers JSONB,
    score INTEGER,
    max_score INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    graded_by INTEGER REFERENCES users(id),
    feedback TEXT
);

-- Sessions IA ARIA
CREATE TABLE aria_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    context JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages IA ARIA
CREATE TABLE aria_messages (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) REFERENCES aria_sessions(session_id),
    message_type VARCHAR(20) NOT NULL CHECK (message_type IN ('user', 'assistant')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tokens d'authentification
CREATE TABLE auth_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    token_type VARCHAR(20) NOT NULL CHECK (token_type IN ('access', 'refresh', 'reset')),
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les performances
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_student_progress_student_id ON student_progress(student_id);
CREATE INDEX idx_student_progress_course_id ON student_progress(course_id);
CREATE INDEX idx_assessment_results_student_id ON assessment_results(student_id);
CREATE INDEX idx_aria_sessions_user_id ON aria_sessions(user_id);
CREATE INDEX idx_aria_messages_session_id ON aria_messages(session_id);
CREATE INDEX idx_auth_tokens_user_id ON auth_tokens(user_id);
CREATE INDEX idx_auth_tokens_token_hash ON auth_tokens(token_hash);
```

### Installation Redis

```bash
# Installation Redis
apt install -y redis-server

# Configuration Redis
sudo vim /etc/redis/redis.conf
```

```ini
# /etc/redis/redis.conf

# Sécurité
bind 127.0.0.1
port 6379
requirepass votre_mot_de_passe_redis_securise

# Mémoire
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistance
save 900 1
save 300 10
save 60 10000

# Logs
loglevel notice
logfile /var/log/redis/redis-server.log
```

```bash
# Redémarrage Redis
sudo systemctl restart redis-server
sudo systemctl enable redis-server

# Test
redis-cli ping
```

---

## 🤖 Agent IA ARIA

### Architecture Agent IA

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent ARIA                               │
├─────────────────────────────────────────────────────────────┤
│  Conversation Manager  │  Knowledge Base  │  Context Store  │
│  ┌─────────────────┐   │  ┌─────────────┐ │ ┌─────────────┐ │
│  │ Session Handler │   │  │ NSI Content │ │ │ User Context│ │
│  │ Message Router  │   │  │ Embeddings  │ │ │ Chat History│ │
│  │ Response Gen.   │   │  │ Vector DB   │ │ │ Preferences │ │
│  └─────────────────┘   │  └─────────────┘ │ └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    External Services                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ OpenAI API  │ │ Vector DB   │ │ Text-to-    │          │
│  │ GPT-4       │ │ (Pinecone)  │ │ Speech      │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Configuration Agent IA

#### 1. Installation des dépendances IA

```bash
# Création du service IA
mkdir -p /opt/nexus-reussite/ai-agent
cd /opt/nexus-reussite/ai-agent

# Environnement virtuel Python
python3.12 -m venv venv
source venv/bin/activate

# Installation des dépendances
pip install -r requirements.txt
```

#### requirements.txt pour l'Agent IA
```txt
# AI et NLP
openai==1.12.0
langchain==0.1.10
langchain-openai==0.0.8
langchain-community==0.0.25

# Vector Database
pinecone-client==3.0.3
chromadb==0.4.22
sentence-transformers==2.5.1

# Framework Web
fastapi==0.109.2
uvicorn==0.27.1
websockets==12.0

# Base de données
asyncpg==0.29.0
redis==5.0.1

# Utilitaires
pydantic==2.6.1
python-dotenv==1.0.1
structlog==25.4.0
python-multipart==0.0.9

# Monitoring
prometheus-client==0.20.0
```

#### 2. Service Principal ARIA

```python
# ai-agent/aria_main.py

import asyncio
import logging
import os
from typing import Dict, List, Optional
from datetime import datetime

import openai
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis.asyncio as redis
import asyncpg
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

# Configuration
class ARIAConfig:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Paramètres IA
    MODEL_NAME = "gpt-4-turbo-preview"
    MAX_TOKENS = 2048
    TEMPERATURE = 0.7
    MAX_CONTEXT_LENGTH = 10

# Modèles Pydantic
class ChatMessage(BaseModel):
    user_id: int
    session_id: str
    message: str
    message_type: str = "user"

class ARIAResponse(BaseModel):
    session_id: str
    response: str
    confidence: float
    sources: List[str] = []
    metadata: Dict = {}

# Service Principal ARIA
class ARIAService:
    def __init__(self):
        self.config = ARIAConfig()
        self.app = FastAPI(title="ARIA Agent", version="1.0.0")
        self.setup_middleware()
        self.setup_routes()

        # Connexions
        self.redis = None
        self.db_pool = None
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.active_connections: Dict[str, WebSocket] = {}

    def setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000", "https://nexusreussite.academy"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    async def startup(self):
        """Initialisation des services"""
        try:
            # Redis
            self.redis = redis.from_url(self.config.REDIS_URL)

            # PostgreSQL
            self.db_pool = await asyncpg.create_pool(self.config.DATABASE_URL)

            # OpenAI
            openai.api_key = self.config.OPENAI_API_KEY
            self.llm = ChatOpenAI(
                model_name=self.config.MODEL_NAME,
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS
            )

            # Embeddings et Vector Store
            self.embeddings = OpenAIEmbeddings()
            # Initialiser Pinecone ici

            logging.info("ARIA Service démarré avec succès")

        except Exception as e:
            logging.error(f"Erreur lors du démarrage ARIA: {e}")
            raise

    async def shutdown(self):
        """Nettoyage des ressources"""
        if self.redis:
            await self.redis.close()
        if self.db_pool:
            await self.db_pool.close()

    def setup_routes(self):
        @self.app.on_event("startup")
        async def startup_event():
            await self.startup()

        @self.app.on_event("shutdown")
        async def shutdown_event():
            await self.shutdown()

        @self.app.websocket("/ws/{session_id}")
        async def websocket_endpoint(websocket: WebSocket, session_id: str):
            await self.handle_websocket(websocket, session_id)

        @self.app.post("/chat", response_model=ARIAResponse)
        async def chat_endpoint(message: ChatMessage):
            return await self.process_message(message)

        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "timestamp": datetime.utcnow()}

    async def handle_websocket(self, websocket: WebSocket, session_id: str):
        """Gestion des connexions WebSocket"""
        await websocket.accept()
        self.active_connections[session_id] = websocket

        try:
            while True:
                data = await websocket.receive_json()
                message = ChatMessage(**data, session_id=session_id)

                # Traitement du message
                response = await self.process_message(message)

                # Envoi de la réponse
                await websocket.send_json(response.dict())

        except WebSocketDisconnect:
            del self.active_connections[session_id]
        except Exception as e:
            logging.error(f"Erreur WebSocket pour session {session_id}: {e}")
            await websocket.close()

    async def process_message(self, message: ChatMessage) -> ARIAResponse:
        """Traitement principal des messages"""
        try:
            # 1. Récupération du contexte utilisateur
            user_context = await self.get_user_context(message.user_id)

            # 2. Récupération de l'historique de conversation
            chat_history = await self.get_chat_history(message.session_id)

            # 3. Recherche dans la base de connaissances
            relevant_docs = await self.search_knowledge_base(message.message)

            # 4. Construction du prompt contextualisé
            prompt = await self.build_contextualized_prompt(
                message.message, user_context, relevant_docs, chat_history
            )

            # 5. Génération de la réponse IA
            ai_response = await self.generate_ai_response(prompt)

            # 6. Sauvegarde de la conversation
            await self.save_conversation(message, ai_response)

            return ARIAResponse(
                session_id=message.session_id,
                response=ai_response["content"],
                confidence=ai_response["confidence"],
                sources=ai_response["sources"],
                metadata=ai_response["metadata"]
            )

        except Exception as e:
            logging.error(f"Erreur lors du traitement du message: {e}")
            return ARIAResponse(
                session_id=message.session_id,
                response="Je rencontre une difficulté technique. Pouvez-vous reformuler votre question ?",
                confidence=0.0,
                sources=[],
                metadata={"error": str(e)}
            )

    async def get_user_context(self, user_id: int) -> Dict:
        """Récupération du contexte utilisateur"""
        async with self.db_pool.acquire() as conn:
            # Informations utilisateur
            user_info = await conn.fetchrow(
                "SELECT role, first_name, last_name FROM users WHERE id = $1",
                user_id
            )

            # Profil étudiant si applicable
            student_profile = None
            if user_info and user_info['role'] == 'student':
                student_profile = await conn.fetchrow(
                    "SELECT class_level, school_name FROM student_profiles WHERE user_id = $1",
                    user_id
                )

            # Progression récente
            recent_progress = await conn.fetch(
                """
                SELECT c.title, sp.progress_percentage, sp.last_accessed
                FROM student_progress sp
                JOIN courses c ON sp.course_id = c.id
                WHERE sp.student_id = $1
                ORDER BY sp.last_accessed DESC
                LIMIT 5
                """,
                user_id
            )

            return {
                "user_info": dict(user_info) if user_info else {},
                "student_profile": dict(student_profile) if student_profile else {},
                "recent_progress": [dict(row) for row in recent_progress]
            }

    async def get_chat_history(self, session_id: str) -> List[Dict]:
        """Récupération de l'historique de conversation"""
        async with self.db_pool.acquire() as conn:
            messages = await conn.fetch(
                """
                SELECT message_type, content, created_at
                FROM aria_messages
                WHERE session_id = $1
                ORDER BY created_at DESC
                LIMIT $2
                """,
                session_id, self.config.MAX_CONTEXT_LENGTH
            )

            return [dict(msg) for msg in reversed(messages)]

    async def search_knowledge_base(self, query: str) -> List[Dict]:
        """Recherche dans la base de connaissances NSI"""
        try:
            # Embedding de la requête
            query_embedding = await self.embeddings.aembed_query(query)

            # Recherche vectorielle (à implémenter avec Pinecone)
            # results = self.vectorstore.similarity_search(query, k=5)

            # Pour l'instant, recherche simple dans la base
            async with self.db_pool.acquire() as conn:
                courses = await conn.fetch(
                    """
                    SELECT title, description, content, level
                    FROM courses
                    WHERE is_published = true
                    AND (title ILIKE $1 OR description ILIKE $1)
                    LIMIT 3
                    """,
                    f"%{query}%"
                )

                return [dict(course) for course in courses]

        except Exception as e:
            logging.error(f"Erreur recherche base de connaissances: {e}")
            return []

    async def build_contextualized_prompt(
        self,
        message: str,
        user_context: Dict,
        relevant_docs: List[Dict],
        chat_history: List[Dict]
    ) -> str:
        """Construction du prompt contextualisé"""

        # Contexte utilisateur
        user_role = user_context.get("user_info", {}).get("role", "student")
        user_name = user_context.get("user_info", {}).get("first_name", "")
        class_level = user_context.get("student_profile", {}).get("class_level", "")

        # Historique récent
        history_text = ""
        if chat_history:
            history_text = "\n".join([
                f"{msg['message_type']}: {msg['content']}"
                for msg in chat_history[-3:]  # 3 derniers messages
            ])

        # Documents pertinents
        docs_text = ""
        if relevant_docs:
            docs_text = "\n".join([
                f"Cours: {doc['title']} - {doc['description']}"
                for doc in relevant_docs[:2]  # 2 documents les plus pertinents
            ])

        prompt = f"""
Tu es ARIA, l'assistant IA spécialisé en NSI (Numérique et Sciences Informatiques) de la plateforme Nexus Réussite.

CONTEXTE UTILISATEUR:
- Nom: {user_name}
- Rôle: {user_role}
- Niveau: {class_level}

HISTORIQUE RÉCENT:
{history_text}

DOCUMENTS PERTINENTS:
{docs_text}

INSTRUCTIONS:
1. Réponds de manière pédagogique et bienveillante
2. Adapte ton niveau au profil de l'utilisateur
3. Utilise des exemples concrets en NSI
4. Propose des exercices pratiques si pertinent
5. Reste dans le domaine de la NSI et de l'informatique
6. Si tu ne sais pas, dis-le clairement

QUESTION DE L'UTILISATEUR:
{message}

RÉPONSE:
"""

        return prompt

    async def generate_ai_response(self, prompt: str) -> Dict:
        """Génération de la réponse IA"""
        try:
            response = await self.llm.agenerate([[{"content": prompt, "role": "user"}]])

            ai_content = response.generations[0][0].text

            return {
                "content": ai_content,
                "confidence": 0.9,  # À calculer basé sur la réponse
                "sources": [],  # À extraire des documents utilisés
                "metadata": {
                    "model": self.config.MODEL_NAME,
                    "tokens_used": len(prompt.split()) + len(ai_content.split())
                }
            }

        except Exception as e:
            logging.error(f"Erreur génération IA: {e}")
            raise

    async def save_conversation(self, message: ChatMessage, ai_response: Dict):
        """Sauvegarde de la conversation"""
        async with self.db_pool.acquire() as conn:
            # Message utilisateur
            await conn.execute(
                """
                INSERT INTO aria_messages (session_id, message_type, content, metadata)
                VALUES ($1, $2, $3, $4)
                """,
                message.session_id, "user", message.message, {}
            )

            # Réponse IA
            await conn.execute(
                """
                INSERT INTO aria_messages (session_id, message_type, content, metadata)
                VALUES ($1, $2, $3, $4)
                """,
                message.session_id, "assistant", ai_response["content"], ai_response["metadata"]
            )

            # Mise à jour session
            await conn.execute(
                """
                UPDATE aria_sessions
                SET last_interaction = CURRENT_TIMESTAMP
                WHERE session_id = $1
                """,
                message.session_id
            )

# Point d'entrée
if __name__ == "__main__":
    import uvicorn

    aria_service = ARIAService()

    uvicorn.run(
        aria_service.app,
        host="0.0.0.0",
        port=5001,
        log_level="info"
    )
```

#### 3. Configuration des Variables d'Environnement

```bash
# /opt/nexus-reussite/ai-agent/.env

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key

# Vector Database (Pinecone)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-west1-gcp

# Base de données
DATABASE_URL=postgresql://nexus_user:password@localhost:5432/nexus_reussite
REDIS_URL=redis://:password@localhost:6379

# Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
```

#### 4. Service Systemd pour ARIA

```bash
# /etc/systemd/system/aria-agent.service

[Unit]
Description=ARIA AI Agent for Nexus Réussite
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=nexusadmin
WorkingDirectory=/opt/nexus-reussite/ai-agent
Environment=PATH=/opt/nexus-reussite/ai-agent/venv/bin
ExecStart=/opt/nexus-reussite/ai-agent/venv/bin/python aria_main.py
Restart=always
RestartSec=10

# Logs
StandardOutput=journal
StandardError=journal

# Sécurité
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/nexus-reussite/ai-agent

[Install]
WantedBy=multi-user.target
```

```bash
# Activation du service
sudo systemctl daemon-reload
sudo systemctl enable aria-agent
sudo systemctl start aria-agent

# Vérification
sudo systemctl status aria-agent
```

---

## 🔐 Authentification et Sécurité

### Architecture d'Authentification

```
┌─────────────────────────────────────────────────────────────┐
│                 Authentification JWT                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend           │  Backend           │  Database        │
│  ┌─────────────┐    │  ┌─────────────┐   │ ┌─────────────┐  │
│  │ Auth Store  │◄──►│  │ Auth Service│◄─►│ │ Users Table │  │
│  │ (Zustand)   │    │  │ JWT Handler │   │ │ Tokens Table│  │
│  │ Token Cache │    │  │ Middleware  │   │ │             │  │
│  └─────────────┘    │  └─────────────┘   │ └─────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                     Security Layers                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Rate Limit  │ │ CORS        │ │ HTTPS/SSL   │           │
│  │ Helmet      │ │ CSRF        │ │ Security    │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Configuration JWT Backend

```python
# backend/src/services/auth_service.py

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
import hashlib

class AuthService:
    def __init__(self, secret_key: str, db_pool):
        self.secret_key = secret_key
        self.db_pool = db_pool
        self.algorithm = "HS256"

        # Durées des tokens
        self.access_token_expire = timedelta(hours=1)
        self.refresh_token_expire = timedelta(days=30)
        self.reset_token_expire = timedelta(hours=1)

    async def register_user(self, user_data: Dict) -> Dict:
        """Inscription d'un nouvel utilisateur"""
        try:
            # Validation des données
            if not self._validate_user_data(user_data):
                return {"success": False, "error": "Données invalides"}

            # Vérification email unique
            if await self._email_exists(user_data["email"]):
                return {"success": False, "error": "Email déjà utilisé"}

            # Hachage du mot de passe
            password_hash = self._hash_password(user_data["password"])

            # Insertion en base
            async with self.db_pool.acquire() as conn:
                user_id = await conn.fetchval(
                    """
                    INSERT INTO users (email, password_hash, first_name, last_name, role, phone)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                    """,
                    user_data["email"],
                    password_hash,
                    user_data["first_name"],
                    user_data["last_name"],
                    user_data["role"],
                    user_data.get("phone")
                )

                # Création du profil étudiant si nécessaire
                if user_data["role"] == "student":
                    await conn.execute(
                        """
                        INSERT INTO student_profiles (user_id, class_level)
                        VALUES ($1, $2)
                        """,
                        user_id,
                        user_data.get("class_level", "premiere")
                    )

            return {
                "success": True,
                "user_id": user_id,
                "message": "Utilisateur créé avec succès"
            }

        except Exception as e:
            return {"success": False, "error": f"Erreur lors de l'inscription: {str(e)}"}

    async def authenticate_user(self, email: str, password: str) -> Dict:
        """Authentification utilisateur"""
        try:
            async with self.db_pool.acquire() as conn:
                user = await conn.fetchrow(
                    """
                    SELECT id, email, password_hash, first_name, last_name, role, is_active
                    FROM users
                    WHERE email = $1
                    """,
                    email
                )

                if not user:
                    return {"success": False, "error": "Utilisateur non trouvé"}

                if not user["is_active"]:
                    return {"success": False, "error": "Compte désactivé"}

                # Vérification du mot de passe
                if not self._verify_password(password, user["password_hash"]):
                    return {"success": False, "error": "Mot de passe incorrect"}

                # Génération des tokens
                access_token = self._generate_access_token(user)
                refresh_token = self._generate_refresh_token(user["id"])

                # Sauvegarde du refresh token
                await self._save_refresh_token(user["id"], refresh_token)

                return {
                    "success": True,
                    "user": {
                        "id": user["id"],
                        "email": user["email"],
                        "firstName": user["first_name"],
                        "lastName": user["last_name"],
                        "role": user["role"]
                    },
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }

        except Exception as e:
            return {"success": False, "error": f"Erreur d'authentification: {str(e)}"}

    def _generate_access_token(self, user: Dict) -> str:
        """Génération du token d'accès"""
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.utcnow() + self.access_token_expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def _generate_refresh_token(self, user_id: int) -> str:
        """Génération du token de rafraîchissement"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + self.refresh_token_expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": secrets.token_urlsafe(32)  # Unique token ID
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    async def _save_refresh_token(self, user_id: int, token: str):
        """Sauvegarde du refresh token en base"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO auth_tokens (user_id, token_hash, token_type, expires_at)
                VALUES ($1, $2, $3, $4)
                """,
                user_id,
                token_hash,
                "refresh",
                datetime.utcnow() + self.refresh_token_expire
            )

    def verify_token(self, token: str) -> Optional[Dict]:
        """Vérification d'un token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def _hash_password(self, password: str) -> str:
        """Hachage du mot de passe"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Vérification du mot de passe"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def _validate_user_data(self, data: Dict) -> bool:
        """Validation des données utilisateur"""
        required_fields = ["email", "password", "first_name", "last_name", "role"]

        for field in required_fields:
            if not data.get(field):
                return False

        # Validation email
        import re
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, data["email"]):
            return False

        # Validation mot de passe
        if len(data["password"]) < 8:
            return False

        # Validation rôle
        valid_roles = ["student", "parent", "teacher", "admin"]
        if data["role"] not in valid_roles:
            return False

        return True

    async def _email_exists(self, email: str) -> bool:
        """Vérification si l'email existe déjà"""
        async with self.db_pool.acquire() as conn:
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM users WHERE email = $1",
                email
            )
            return count > 0
```

### Middleware de Sécurité

```python
# backend/src/middleware/security.py

from functools import wraps
from flask import request, jsonify, g
from services.auth_service import AuthService
import time
from collections import defaultdict
import logging

# Rate Limiting
class RateLimiter:
    def __init__(self):
        self.clients = defaultdict(list)
        self.limits = {
            "login": {"requests": 5, "window": 300},  # 5 tentatives par 5 minutes
            "register": {"requests": 3, "window": 3600},  # 3 inscriptions par heure
            "api": {"requests": 100, "window": 60},  # 100 requêtes par minute
            "chat": {"requests": 20, "window": 60}  # 20 messages IA par minute
        }

    def is_allowed(self, client_ip: str, endpoint: str) -> bool:
        now = time.time()
        limit_config = self.limits.get(endpoint, self.limits["api"])

        # Nettoyage des anciennes requêtes
        self.clients[client_ip] = [
            timestamp for timestamp in self.clients[client_ip]
            if now - timestamp < limit_config["window"]
        ]

        # Vérification de la limite
        if len(self.clients[client_ip]) >= limit_config["requests"]:
            return False

        # Ajout de la requête actuelle
        self.clients[client_ip].append(now)
        return True

rate_limiter = RateLimiter()

def require_auth(f):
    """Décorateur pour les routes nécessitant une authentification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Récupération du token depuis l'en-tête Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Format de token invalide'}), 401

        if not token:
            return jsonify({'error': 'Token manquant'}), 401

        # Vérification du token
        auth_service = AuthService(current_app.config['SECRET_KEY'], db_pool)
        payload = auth_service.verify_token(token)

        if not payload:
            return jsonify({'error': 'Token invalide ou expiré'}), 401

        # Stockage des informations utilisateur dans g
        g.current_user = payload

        return f(*args, **kwargs)

    return decorated_function

def require_role(required_role):
    """Décorateur pour vérifier le rôle utilisateur"""
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated_function(*args, **kwargs):
            if g.current_user.get('role') != required_role:
                return jsonify({'error': 'Accès non autorisé'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def rate_limit(endpoint_type="api"):
    """Décorateur pour la limitation de débit"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

            if not rate_limiter.is_allowed(client_ip, endpoint_type):
                return jsonify({
                    'error': 'Trop de requêtes',
                    'message': 'Veuillez patienter avant de réessayer'
                }), 429

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Middleware de sécurité global
def setup_security_middleware(app):
    """Configuration des middleware de sécurité"""

    @app.before_request
    def security_headers():
        # Headers de sécurité
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        # Headers de sécurité
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Logging des requêtes
        duration = time.time() - g.start_time
        logging.info(f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s")

        return response
```

### Configuration SSL/HTTPS

```bash
# Installation Certbot pour Let's Encrypt
apt install -y certbot python3-certbot-nginx

# Génération des certificats SSL
certbot --nginx -d nexusreussite.academy -d www.nexusreussite.academy

# Renouvellement automatique
crontab -e
# Ajouter la ligne suivante:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Configuration Nginx avec SSL

```nginx
# /etc/nginx/sites-available/nexus-reussite

# Redirection HTTP vers HTTPS
server {
    listen 80;
    server_name nexusreussite.academy www.nexusreussite.academy;
    return 301 https://$server_name$request_uri;
}

# Configuration HTTPS
server {
    listen 443 ssl http2;
    server_name nexusreussite.academy www.nexusreussite.academy;

    # Certificats SSL
    ssl_certificate /etc/letsencrypt/live/nexusreussite.academy/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nexusreussite.academy/privkey.pem;

    # Configuration SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Headers de sécurité
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";

    # Taille maximale des uploads
    client_max_body_size 50M;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Frontend Next.js
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # API Backend Flask
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout pour les requêtes IA
        proxy_read_timeout 300s;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
    }

    # WebSocket pour les notifications temps réel
    location /ws/ {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Agent IA ARIA
    location /aria/ {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout étendu pour l'IA
        proxy_read_timeout 600s;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
    }

    # Assets statiques avec cache
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri @nextjs;
    }

    location @nextjs {
        proxy_pass http://localhost:3000;
    }

    # Logs
    access_log /var/log/nginx/nexus-reussite.access.log;
    error_log /var/log/nginx/nexus-reussite.error.log;
}
```

---

## 🚀 Déploiement Production

### Docker Compose Production

```yaml
# docker-compose.prod.yml

version: '3.8'

services:
  # Base de données PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: nexus-postgres
    environment:
      POSTGRES_DB: nexus_reussite
      POSTGRES_USER: nexus_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - nexus-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nexus_user -d nexus_reussite"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Cache Redis
  redis:
    image: redis:7-alpine
    container_name: nexus-redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped
    networks:
      - nexus-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Backend Flask API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: nexus-backend
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://nexus_user:${POSTGRES_PASSWORD}@postgres:5432/nexus_reussite
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/logs:/app/logs
    ports:
      - "5000:5000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - nexus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend Next.js
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: nexus-frontend
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
      - NEXT_PUBLIC_WS_URL=${NEXT_PUBLIC_WS_URL}
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - nexus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Agent IA ARIA
  aria-agent:
    build:
      context: ./ai-agent
      dockerfile: Dockerfile
    container_name: nexus-aria
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - PINECONE_ENVIRONMENT=${PINECONE_ENVIRONMENT}
      - DATABASE_URL=postgresql://nexus_user:${POSTGRES_PASSWORD}@postgres:5432/nexus_reussite
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
    ports:
      - "5001:5001"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - nexus-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: nexus-nginx
    volumes:
      - ./nginx/nginx.prod.conf:/etc/nginx/nginx.conf
      - ./nginx/sites-available:/etc/nginx/sites-available
      - /etc/letsencrypt:/etc/letsencrypt:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - frontend
      - backend
      - aria-agent
    restart: unless-stopped
    networks:
      - nexus-network

volumes:
  postgres_data:
  redis_data:

networks:
  nexus-network:
    driver: bridge
```

### Variables d'Environnement Production

```bash
# .env.production

# Base de données
POSTGRES_PASSWORD=your_secure_postgres_password_here
DATABASE_URL=postgresql://nexus_user:your_secure_postgres_password_here@localhost:5432/nexus_reussite

# Redis
REDIS_PASSWORD=your_secure_redis_password_here
REDIS_URL=redis://:your_secure_redis_password_here@localhost:6379

# Sécurité
SECRET_KEY=your_super_secret_key_for_flask_sessions_min_32_chars
JWT_SECRET_KEY=your_jwt_secret_key_for_token_signing_min_32_chars

# IA
OPENAI_API_KEY=sk-your-openai-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=us-west1-gcp

# URLs
NEXT_PUBLIC_API_URL=https://nexusreussite.academy/api
NEXT_PUBLIC_WS_URL=wss://nexusreussite.academy/ws
DOMAIN=nexusreussite.academy

# Email (pour les notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring
SENTRY_DSN=your-sentry-dsn-for-error-tracking

# Environnement
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Script de Déploiement

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "🚀 Déploiement Nexus Réussite - Production"

# Variables
PROJECT_DIR="/opt/nexus-reussite"
BACKUP_DIR="/opt/nexus-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifications préalables
check_requirements() {
    log_info "Vérification des prérequis..."

    # Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé"
        exit 1
    fi

    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé"
        exit 1
    fi

    # Variables d'environnement
    if [ ! -f ".env.production" ]; then
        log_error "Fichier .env.production manquant"
        exit 1
    fi

    log_info "Prérequis OK"
}

# Sauvegarde de la base de données
backup_database() {
    log_info "Sauvegarde de la base de données..."

    mkdir -p $BACKUP_DIR

    # Export PostgreSQL
    docker exec nexus-postgres pg_dump -U nexus_user nexus_reussite > $BACKUP_DIR/db_backup_$DATE.sql

    # Compression
    gzip $BACKUP_DIR/db_backup_$DATE.sql

    log_info "Sauvegarde terminée: $BACKUP_DIR/db_backup_$DATE.sql.gz"
}

# Arrêt des services
stop_services() {
    log_info "Arrêt des services..."

    if [ -f "docker-compose.prod.yml" ]; then
        docker-compose -f docker-compose.prod.yml down
    fi

    log_info "Services arrêtés"
}

# Construction des images
build_images() {
    log_info "Construction des images Docker..."

    # Backend
    log_info "Construction de l'image backend..."
    docker build -t nexus-backend:latest ./backend

    # Frontend
    log_info "Construction de l'image frontend..."
    docker build -t nexus-frontend:latest ./frontend

    # Agent IA
    log_info "Construction de l'image ARIA..."
    docker build -t nexus-aria:latest ./ai-agent

    log_info "Images construites avec succès"
}

# Migrations de base de données
run_migrations() {
    log_info "Exécution des migrations..."

    # Démarrage temporaire de PostgreSQL
    docker-compose -f docker-compose.prod.yml up -d postgres redis

    # Attente que PostgreSQL soit prêt
    sleep 10

    # Exécution des migrations Alembic
    docker run --rm --network nexus-reussite_nexus-network \
        -e DATABASE_URL="postgresql://nexus_user:${POSTGRES_PASSWORD}@postgres:5432/nexus_reussite" \
        nexus-backend:latest \
        alembic upgrade head

    log_info "Migrations terminées"
}

# Démarrage des services
start_services() {
    log_info "Démarrage des services..."

    # Chargement des variables d'environnement
    export $(cat .env.production | xargs)

    # Démarrage avec Docker Compose
    docker-compose -f docker-compose.prod.yml up -d

    log_info "Services démarrés"
}

# Vérification de la santé des services
health_check() {
    log_info "Vérification de la santé des services..."

    # Attente du démarrage
    sleep 30

    # Vérification PostgreSQL
    if docker exec nexus-postgres pg_isready -U nexus_user -d nexus_reussite; then
        log_info "✅ PostgreSQL OK"
    else
        log_error "❌ PostgreSQL KO"
        exit 1
    fi

    # Vérification Redis
    if docker exec nexus-redis redis-cli ping | grep -q PONG; then
        log_info "✅ Redis OK"
    else
        log_error "❌ Redis KO"
        exit 1
    fi

    # Vérification Backend
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        log_info "✅ Backend OK"
    else
        log_error "❌ Backend KO"
        exit 1
    fi

    # Vérification Frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_info "✅ Frontend OK"
    else
        log_error "❌ Frontend KO"
        exit 1
    fi

    # Vérification Agent IA
    if curl -f http://localhost:5001/health > /dev/null 2>&1; then
        log_info "✅ Agent ARIA OK"
    else
        log_error "❌ Agent ARIA KO"
        exit 1
    fi

    log_info "Tous les services sont opérationnels ✅"
}

# Nettoyage des anciennes images
cleanup() {
    log_info "Nettoyage des anciennes images..."

    docker image prune -f
    docker system prune -f

    log_info "Nettoyage terminé"
}

# Fonction principale
main() {
    log_info "Début du déploiement..."

    cd $PROJECT_DIR

    check_requirements
    backup_database
    stop_services
    build_images
    run_migrations
    start_services
    health_check
    cleanup

    log_info "🎉 Déploiement terminé avec succès!"
    log_info "🌐 Application disponible sur: https://$DOMAIN"
}

# Gestion des erreurs
trap 'log_error "Erreur lors du déploiement à la ligne $LINENO"' ERR

# Exécution
main "$@"
```

### Monitoring et Logs

#### Configuration Prometheus

```yaml
# monitoring/prometheus.yml

global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'nexus-backend'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'

  - job_name: 'nexus-aria'
    static_configs:
      - targets: ['localhost:5001']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']

  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']
```

#### Configuration Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Nexus Réussite - Monitoring",
    "panels": [
      {
        "title": "Requêtes par seconde",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Temps de réponse moyen",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Utilisation CPU",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "CPU Usage %"
          }
        ]
      },
      {
        "title": "Utilisation Mémoire",
        "type": "graph",
        "targets": [
          {
            "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
            "legendFormat": "Memory Usage %"
          }
        ]
      }
    ]
  }
}
```

---

## 📚 API Documentation

### Endpoints d'Authentification

#### POST /api/auth/register
```json
{
  "description": "Inscription d'un nouvel utilisateur",
  "request": {
    "email": "student@example.com",
    "password": "motdepasse123",
    "firstName": "Jean",
    "lastName": "Dupont",
    "role": "student",
    "phone": "+33123456789",
    "classLevel": "terminale"
  },
  "response": {
    "success": true,
    "message": "Utilisateur créé avec succès",
    "userId": 123
  }
}
```

#### POST /api/auth/login
```json
{
  "description": "Connexion utilisateur",
  "request": {
    "email": "student@example.com",
    "password": "motdepasse123"
  },
  "response": {
    "success": true,
    "user": {
      "id": 123,
      "email": "student@example.com",
      "firstName": "Jean",
      "lastName": "Dupont",
      "role": "student"
    },
    "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### Endpoints de Contenu

#### GET /api/courses
```json
{
  "description": "Liste des cours disponibles",
  "parameters": {
    "level": "premiere|terminale",
    "category": "algorithmique|programmation|reseaux|donnees",
    "page": 1,
    "limit": 10
  },
  "response": {
    "courses": [
      {
        "id": 1,
        "title": "Introduction aux algorithmes",
        "description": "Cours d'introduction aux algorithmes de tri et de recherche",
        "level": "premiere",
        "category": "algorithmique",
        "duration": 120,
        "isPublished": true
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 45,
      "pages": 5
    }
  }
}
```

#### GET /api/courses/{id}
```json
{
  "description": "Détails d'un cours spécifique",
  "response": {
    "id": 1,
    "title": "Introduction aux algorithmes",
    "description": "Cours complet sur les algorithmes...",
    "level": "premiere",
    "category": "algorithmique",
    "content": {
      "chapters": [
        {
          "id": 1,
          "title": "Les algorithmes de tri",
          "sections": [
            {
              "id": 1,
              "title": "Tri par sélection",
              "content": "Le tri par sélection...",
              "examples": [],
              "exercises": []
            }
          ]
        }
      ]
    },
    "prerequisites": ["Bases de la programmation"],
    "objectives": ["Comprendre les algorithmes de tri"],
    "estimatedTime": 120
  }
}
```

### Endpoints Agent IA

#### POST /api/aria/chat
```json
{
  "description": "Conversation avec l'agent IA ARIA",
  "request": {
    "sessionId": "session_123",
    "message": "Peux-tu m'expliquer le tri par insertion ?",
    "context": {
      "currentCourse": "algorithmes-tri",
      "userLevel": "premiere"
    }
  },
  "response": {
    "sessionId": "session_123",
    "response": "Le tri par insertion est un algorithme de tri simple...",
    "confidence": 0.95,
    "sources": [
      "Cours: Algorithmes de tri",
      "Exercice: Implémentation tri insertion"
    ],
    "metadata": {
      "responseTime": 1.2,
      "tokensUsed": 156
    }
  }
}
```

#### WebSocket /ws/aria/{sessionId}
```json
{
  "description": "Connexion WebSocket pour chat temps réel",
  "messages": {
    "user_message": {
      "type": "user_message",
      "content": "Comment implémenter un tri rapide ?",
      "timestamp": "2025-01-31T15:30:00Z"
    },
    "ai_response": {
      "type": "ai_response",
      "content": "Le tri rapide (quicksort) est un algorithme...",
      "confidence": 0.92,
      "sources": ["Cours algorithmique avancée"],
      "timestamp": "2025-01-31T15:30:02Z"
    },
    "typing_indicator": {
      "type": "typing",
      "isTyping": true
    }
  }
}
```

---

## 🔧 Troubleshooting

### Problèmes Courants

#### 1. Erreur de Connexion Base de Données
```bash
# Symptômes
FATAL: password authentication failed for user "nexus_user"

# Solutions
# Vérifier les credentials
psql -U nexus_user -d nexus_reussite -h localhost

# Réinitialiser le mot de passe
sudo -u postgres psql
ALTER USER nexus_user PASSWORD 'nouveau_mot_de_passe';

# Vérifier pg_hba.conf
sudo vim /etc/postgresql/15/main/pg_hba.conf
```

#### 2. Erreur Agent IA - API Key
```bash
# Symptômes
openai.error.AuthenticationError: Incorrect API key provided

# Solutions
# Vérifier la clé API
echo $OPENAI_API_KEY

# Tester la clé
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Régénérer la clé sur OpenAI Dashboard
```

#### 3. Erreur SSL/HTTPS
```bash
# Symptômes
SSL certificate problem: unable to get local issuer certificate

# Solutions
# Renouveler les certificats
certbot renew

# Vérifier la configuration Nginx
nginx -t

# Redémarrer Nginx
systemctl restart nginx
```

#### 4. Performance Lente
```bash
# Diagnostic
# Vérifier l'utilisation des ressources
htop
df -h
free -h

# Vérifier les logs
tail -f /var/log/nginx/nexus-reussite.error.log
docker logs nexus-backend
docker logs nexus-postgres

# Optimisations PostgreSQL
# Augmenter shared_buffers
# Optimiser les requêtes lentes
# Ajouter des index
```

### Scripts de Maintenance

#### Script de Sauvegarde Automatique
```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/opt/nexus-backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Sauvegarde base de données
docker exec nexus-postgres pg_dump -U nexus_user nexus_reussite | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Sauvegarde uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /opt/nexus-reussite/backend/uploads/

# Nettoyage anciennes sauvegardes
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Sauvegarde terminée: $DATE"
```

#### Script de Monitoring
```bash
#!/bin/bash
# scripts/health_check.sh

SERVICES=("nexus-postgres" "nexus-redis" "nexus-backend" "nexus-frontend" "nexus-aria")
FAILED_SERVICES=()

for service in "${SERVICES[@]}"; do
    if ! docker ps | grep -q $service; then
        FAILED_SERVICES+=($service)
    fi
done

if [ ${#FAILED_SERVICES[@]} -gt 0 ]; then
    echo "Services en panne: ${FAILED_SERVICES[*]}"
    # Envoyer notification (email, Slack, etc.)
    exit 1
else
    echo "Tous les services sont opérationnels"
    exit 0
fi
```

---

## 📞 Support et Maintenance

### Contacts Techniques
- **Développeur Principal**: [votre-email@domain.com]
- **Support Infrastructure**: [admin@domain.com]
- **Urgences 24/7**: [+33 X XX XX XX XX]

### Procédures d'Urgence

#### Restauration Complète
```bash
# 1. Arrêter tous les services
docker-compose -f docker-compose.prod.yml down

# 2. Restaurer la base de données
gunzip -c /opt/nexus-backups/db_YYYYMMDD_HHMMSS.sql.gz | \
docker exec -i nexus-postgres psql -U nexus_user nexus_reussite

# 3. Restaurer les uploads
tar -xzf /opt/nexus-backups/uploads_YYYYMMDD_HHMMSS.tar.gz -C /

# 4. Redémarrer les services
docker-compose -f docker-compose.prod.yml up -d
```

#### Mise à Jour d'Urgence
```bash
# Déploiement rapide sans interruption
./scripts/deploy.sh --quick --no-backup
```

---

**🎓 Cette documentation complète vous donne tous les éléments nécessaires pour configurer, déployer et maintenir la plateforme Nexus Réussite en production. Pour toute question spécifique, n'hésitez pas à consulter les logs ou contacter le support technique.**
