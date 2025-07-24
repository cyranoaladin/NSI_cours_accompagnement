#!/usr/bin/env python3
"""
Démarrage direct du frontend Nexus Réussite
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("⚛️  DÉMARRAGE DIRECT DU FRONTEND NEXUS RÉUSSITE")
    print("=" * 50)
    
    # Changer vers le répertoire frontend
    frontend_dir = Path("/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/frontend")
    os.chdir(frontend_dir)
    
    print("📦 Vérification de Node.js...")
    
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ Node.js {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("❌ Node.js non trouvé")
        return 1
    
    print("🔧 Démarrage du serveur de développement...")
    print(f"   Répertoire: {frontend_dir}")
    print()
    print("🎯 Frontend sera disponible sur: http://localhost:3000")
    print("⏸️  Pour arrêter: Ctrl+C")
    print()
    
    # Exécuter npm run dev
    try:
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du frontend par l'utilisateur")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
