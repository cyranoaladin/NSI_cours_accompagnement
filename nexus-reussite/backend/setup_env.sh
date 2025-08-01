#!/bin/bash

# ==============================================
# NEXUS RÉUSSITE - Configuration Environnement
# ==============================================
# Script pour configurer l'environnement de développement backend

set -e  # Arrêter si une commande échoue

echo "🚀 Configuration de l'environnement Nexus Réussite Backend"
echo "==========================================================="

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier si Python 3 est installé
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé. Veuillez l'installer d'abord.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 détecté${NC}"

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Création de l'environnement virtuel...${NC}"
    python3 -m venv venv
else
    echo -e "${GREEN}✅ Environnement virtuel existant${NC}"
fi

# Activer l'environnement virtuel
echo -e "${YELLOW}🔄 Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

# Mettre à jour pip
echo -e "${YELLOW}🔧 Mise à jour de pip...${NC}"
python -m pip install --upgrade pip

# Installer les dépendances
echo -e "${YELLOW}📚 Installation des dépendances...${NC}"
python -m pip install -r requirements.txt

# Vérifier l'installation de Flask
echo -e "${YELLOW}🧪 Vérification de l'installation Flask...${NC}"
python -c "import flask; print('Flask version:', flask.__version__)" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Flask installé avec succès${NC}"
else
    echo -e "${RED}❌ Problème avec l'installation Flask${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Configuration terminée avec succès !${NC}"
echo ""
echo "Pour activer l'environnement manuellement :"
echo -e "${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "Pour lancer le serveur de développement :"
echo -e "${YELLOW}python src/main_simple.py${NC}"
echo ""
echo "Adresses importantes :"
echo "  🌐 Backend API: http://localhost:5000"
echo "  📱 Frontend: http://localhost:3000"
