#!/usr/bin/env python3
"""
Démarrage direct du backend Nexus Réussite
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 DÉMARRAGE DIRECT DU BACKEND NEXUS RÉUSSITE")
    print("=" * 50)
    
    # Changer vers le répertoire backend
    backend_dir = Path("/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend")
    os.chdir(backend_dir)
    
    # Activer l'environnement virtuel et démarrer
    venv_path = backend_dir.parent.parent / ".venv" / "bin" / "activate"
    
    if not venv_path.exists():
        print("❌ Environnement virtuel non trouvé")
        return 1
        
    print("🐍 Activation de l'environnement virtuel...")
    print(f"   Path: {venv_path}")
    
    # Commandes à exécuter
    commands = [
        f"source {venv_path}",
        "cd " + str(backend_dir),
        "python run_dev.py"
    ]
    
    # Créer le script bash
    bash_script = " && ".join(commands)
    
    print("🔧 Commande d'exécution:")
    print(f"   {bash_script}")
    print()
    print("🎯 Backend sera disponible sur: http://localhost:5000")
    print("⏸️  Pour arrêter: Ctrl+C")
    print()
    
    # Exécuter
    try:
        subprocess.run(["bash", "-c", bash_script], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du backend par l'utilisateur")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
