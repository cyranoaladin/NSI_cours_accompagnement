#!/usr/bin/env python3
"""
Script de lancement développement pour Nexus Réussite
Usage: python dev_launcher.py
"""

import subprocess
import sys
import os
import threading
import time
from pathlib import Path

def run_backend():
    """Lance le backend Flask en mode développement"""
    print("🐍 Démarrage du backend Flask...")

    backend_dir = Path(__file__).parent.parent / "backend"
    venv_dir = backend_dir / "venv"
    python_path = venv_dir / "bin" / "python"

    if not python_path.exists():
        python_path = venv_dir / "Scripts" / "python.exe"  # Windows

    if not python_path.exists():
        python_path = sys.executable

    env = os.environ.copy()
    env['FLASK_ENV'] = 'development'
    env['FLASK_DEBUG'] = 'True'

    try:
        cmd = [str(python_path), 'src/main.py']
        subprocess.run(cmd, cwd=backend_dir, env=env)
    except KeyboardInterrupt:
        print("\n🛑 Backend arrêté")

def run_frontend():
    """Lance le frontend React en mode développement"""
    print("⚛️ Démarrage du frontend React...")

    frontend_dir = Path(__file__).parent.parent / "frontend"

    # Installer les dépendances si nécessaire
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installation des dépendances frontend...")
        subprocess.run(['npm', 'install'], cwd=frontend_dir)

    try:
        subprocess.run(['npm', 'run', 'dev'], cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Frontend arrêté")

def main():
    """Fonction principale"""
    print("🎯 Nexus Réussite - Mode Développement")
    print("=" * 50)
    print("🚀 Lancement du backend et frontend...")
    print("📱 Frontend: http://localhost:3000")
    print("🔗 Backend: http://localhost:5000")
    print("🔄 Ctrl+C pour arrêter\n")

    # Lancer backend et frontend en parallèle
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)

    backend_thread.daemon = True
    frontend_thread.daemon = True

    backend_thread.start()
    time.sleep(2)  # Laisser le backend démarrer
    frontend_thread.start()

    try:
        # Attendre que les threads se terminent
        backend_thread.join()
        frontend_thread.join()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de tous les services")

if __name__ == "__main__":
    main()
