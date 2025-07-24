# Dockerfile pour Nexus Réussite Backend
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 5000

# Commande de santé
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Commande par défaut
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "src.main:app"]

