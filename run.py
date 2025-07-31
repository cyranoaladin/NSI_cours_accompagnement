#!/usr/bin/env python3
"""
Script de lancement simplifié pour Nexus Réussite
Usage:
  python run.py dev      # Mode développement
  python run.py prod     # Mode production
  python run.py build    # Build seulement
"""

import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("🎯 Nexus Réussite - Lanceur Simplifié")
        print("Usage:")
        print("  python run.py dev      # Mode développement")
        print("  python run.py prod     # Mode production")
        print("  python run.py build    # Build frontend seulement")
        return

    mode = sys.argv[1].lower()
    script_dir = Path(__file__).parent / "scripts"

    if mode == "dev":
        subprocess.run([sys.executable, str(script_dir / "dev_launcher.py")])
    elif mode == "prod":
        subprocess.run([sys.executable, str(script_dir / "production_launcher.py")] + sys.argv[2:])
    elif mode == "build":
        subprocess.run([sys.executable, str(script_dir / "production_launcher.py"), "--skip-build"] + ["--port", "8000"])
    else:
        print(f"❌ Mode '{mode}' non reconnu")
        print("Modes disponibles: dev, prod, build")

if __name__ == "__main__":
    main()
