#!/bin/bash

# ==========================================
# NEXUS RÉUSSITE - HASH-BASED REQUIREMENTS GENERATOR
# ==========================================
# Script pour générer requirements-hash.txt avec des hashes SHA256
# pour des installations déterministes et sécurisées

set -euo pipefail

echo "🔐 Génération des requirements avec hashes SHA256..."

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REQUIREMENTS_IN="$PROJECT_ROOT/requirements.in"
REQUIREMENTS_HASH="$PROJECT_ROOT/requirements-hash.txt"

# Vérification de l'environnement virtuel
if [[ "${VIRTUAL_ENV:-}" == "" ]]; then
    echo "❌ Erreur: Veuillez activer votre environnement virtuel"
    echo "   Commande: source .venv/bin/activate"
    exit 1
fi

# Vérification des fichiers requis
if [[ ! -f "$REQUIREMENTS_IN" ]]; then
    echo "❌ Erreur: $REQUIREMENTS_IN introuvable"
    echo "   Ce fichier définit les dépendances principales"
    exit 1
fi

# Installation de pip-tools si nécessaire
echo "📦 Vérification de pip-tools..."
if ! python -c "import pip_tools" 2>/dev/null; then
    echo "📥 Installation de pip-tools..."
    pip install "pip-tools>=7.4.0"
fi

# Nettoyage du cache pip pour éviter les versions en cache
echo "🧹 Nettoyage du cache pip..."
pip cache purge --quiet || true

# Génération des requirements avec hashes
echo "🔨 Compilation des requirements avec hashes..."
cd "$PROJECT_ROOT"

# Options pip-compile pour sécurité maximale
pip-compile \
    --generate-hashes \
    --no-emit-index-url \
    --no-emit-trusted-host \
    --resolver=backtracking \
    --upgrade \
    --verbose \
    --output-file="$REQUIREMENTS_HASH" \
    "$REQUIREMENTS_IN"

# Vérification de l'intégrité du fichier généré
if [[ ! -f "$REQUIREMENTS_HASH" ]]; then
    echo "❌ Erreur: Échec de la génération de $REQUIREMENTS_HASH"
    exit 1
fi

# Validation que les hashes sont présents
HASH_COUNT=$(grep -c "sha256:" "$REQUIREMENTS_HASH" || echo "0")
PACKAGE_COUNT=$(grep -c "==" "$REQUIREMENTS_HASH" || echo "0")

echo "📊 Statistiques du fichier généré:"
echo "   - Packages: $PACKAGE_COUNT"
echo "   - Hashes SHA256: $HASH_COUNT"

if [[ "$HASH_COUNT" -eq 0 ]]; then
    echo "⚠️  Attention: Aucun hash généré. Vérifiez la configuration pip-tools"
elif [[ "$HASH_COUNT" -lt "$PACKAGE_COUNT" ]]; then
    echo "⚠️  Attention: Certains packages n'ont pas de hash ($HASH_COUNT/$PACKAGE_COUNT)"
else
    echo "✅ Tous les packages ont des hashes SHA256"
fi

# Test d'installation en mode dry-run pour validation
echo "🧪 Test de validation des dépendances..."
if pip install --dry-run --requirement "$REQUIREMENTS_HASH" >/dev/null 2>&1; then
    echo "✅ Validation réussie: toutes les dépendances sont résolvables"
else
    echo "❌ Erreur: Problème de résolution des dépendances"
    echo "   Vérifiez les conflits potentiels dans $REQUIREMENTS_IN"
    exit 1
fi

# Génération des métadonnées
echo "📝 Génération des métadonnées..."
cat > "${REQUIREMENTS_HASH}.meta" << EOF
# Métadonnées pour requirements-hash.txt
generation_date=$(date -Iseconds)
python_version=$(python --version)
pip_version=$(pip --version)
pip_tools_version=$(pip show pip-tools | grep Version | cut -d' ' -f2)
platform=$(python -c "import platform; print(platform.platform())")
total_packages=$PACKAGE_COUNT
total_hashes=$HASH_COUNT
EOF

echo "✅ Génération terminée avec succès!"
echo ""
echo "📋 Prochaines étapes:"
echo "   1. Testez l'installation: pip install -r requirements-hash.txt"
echo "   2. Committez les fichiers: git add requirements-hash.txt requirements-hash.txt.meta"
echo "   3. Utilisez requirements-hash.txt en production pour la sécurité maximale"
echo ""
echo "🔒 Installation sécurisée:"
echo "   pip install --require-hashes -r requirements-hash.txt"
