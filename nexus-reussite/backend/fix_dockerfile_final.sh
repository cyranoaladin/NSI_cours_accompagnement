#!/bin/bash

# Script de correction du Dockerfile
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend

# Sauvegarder l'ancien fichier
mv Dockerfile.production Dockerfile.production.backup

# Renommer le nouveau fichier propre
mv Dockerfile.production.clean Dockerfile.production

echo "✅ Dockerfile.production corrigé et nettoyé !"
