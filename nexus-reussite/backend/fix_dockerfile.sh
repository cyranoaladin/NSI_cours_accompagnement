#!/bin/bash

cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend
rm -f Dockerfile.production
mv Dockerfile.production.new Dockerfile.production
echo "✅ Dockerfile.production corrigé !"
