#!/usr/bin/env python3
"""
Script de lancement production pour Nexus Réussite
Usage: python production_launcher.py [--port PORT] [--host HOST]
"""

import subprocess
import sys
import os
import argparse
import time
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")

    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        return False

    # Vérifier Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Node.js non trouvé")
            return False
        print(f"✅ Node.js {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Node.js non installé")
        return False

    print("✅ Dépendances OK")
    return True

def build_frontend():
    """Build le frontend React"""
    print("🏗️ Build du frontend...")

    frontend_dir = Path(__file__).parent.parent / "frontend"
    if not frontend_dir.exists():
        print("❌ Dossier frontend non trouvé")
        return False

    # Installer les dépendances si nécessaire
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installation des dépendances frontend...")
        result = subprocess.run(['npm', 'install'], cwd=frontend_dir)
        if result.returncode != 0:
            print("❌ Échec installation npm")
            return False

    # Build production
    result = subprocess.run(['npm', 'run', 'build'], cwd=frontend_dir)
    if result.returncode != 0:
        print("❌ Échec build frontend")
        return False

    print("✅ Frontend buildé avec succès")
    return True

def setup_backend():
    """Configure l'environnement backend"""
    print("🐍 Configuration du backend...")

    backend_dir = Path(__file__).parent.parent / "backend"
    if not backend_dir.exists():
        print("❌ Dossier backend non trouvé")
        return False

    # Vérifier l'environnement virtuel
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("📦 Création de l'environnement virtuel...")
        result = subprocess.run([sys.executable, '-m', 'venv', 'venv'], cwd=backend_dir)
        if result.returncode != 0:
            print("❌ Échec création venv")
            return False

    # Activer et installer les dépendances
    pip_path = venv_dir / "bin" / "pip"
    if not pip_path.exists():
        pip_path = venv_dir / "Scripts" / "pip.exe"  # Windows

    if pip_path.exists():
        print("📦 Installation des dépendances Python...")
        result = subprocess.run([str(pip_path), 'install', '-r', 'requirements.txt'], cwd=backend_dir)
        if result.returncode != 0:
            print("❌ Échec installation pip")
            return False

    print("✅ Backend configuré avec succès")
    return True

def start_production_server(host="0.0.0.0", port=5000):
    """Lance le serveur en mode production"""
    print(f"🚀 Démarrage du serveur sur {host}:{port}...")

    backend_dir = Path(__file__).parent.parent / "backend"

    # Utiliser gunicorn si disponible, sinon Flask dev server
    venv_dir = backend_dir / "venv"
    python_path = venv_dir / "bin" / "python"
    if not python_path.exists():
        python_path = venv_dir / "Scripts" / "python.exe"  # Windows

    if not python_path.exists():
        python_path = sys.executable

    # Variables d'environnement
    env = os.environ.copy()
    env['FLASK_ENV'] = 'production'
    env['FLASK_DEBUG'] = 'False'

    try:
        # Essayer avec gunicorn
        cmd = [str(python_path), '-m', 'gunicorn', '--bind', f'{host}:{port}', 'src.main:app']
        print(f"🌟 Commande: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=backend_dir, env=env)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur")
    except Exception as e:
        print(f"❌ Erreur serveur: {e}")
        # Fallback vers Flask dev server
        try:
            cmd = [str(python_path), 'src/main.py']
            subprocess.run(cmd, cwd=backend_dir, env=env)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du serveur")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Lanceur de production Nexus Réussite")
    parser.add_argument('--host', default='0.0.0.0', help='Adresse IP du serveur')
    parser.add_argument('--port', type=int, default=5000, help='Port du serveur')
    parser.add_argument('--skip-build', action='store_true', help='Ignorer le build frontend')

    args = parser.parse_args()

    print("🎯 Nexus Réussite - Lanceur Production")
    print("=" * 50)

    # Étapes de démarrage
    if not check_dependencies():
        sys.exit(1)

    if not setup_backend():
        sys.exit(1)

    if not args.skip_build:
        if not build_frontend():
            sys.exit(1)

    print("\n✅ Prêt pour la production !")
    print(f"🌐 Serveur disponible sur: http://{args.host}:{args.port}")
    print("🔄 Ctrl+C pour arrêter\n")

    time.sleep(2)
    start_production_server(args.host, args.port)

if __name__ == "__main__":
    main()
