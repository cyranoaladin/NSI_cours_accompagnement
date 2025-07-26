#!/usr/bin/env python3
"""
Nexus Réussite Flask Server Startup Script
Simple script to start the Flask development server
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Configuration des variables d'environnement
os.environ.setdefault("FLASK_ENV", "development")
os.environ.setdefault("PYTHONPATH", str(src_path))

if __name__ == "__main__":
    try:
        # Import après configuration du path
        import main_production
        
        # Configuration par défaut
        host = os.environ.get("FLASK_HOST", "127.0.0.1")
        port = int(os.environ.get("FLASK_PORT", 5000))
        debug = os.environ.get("FLASK_ENV", "development") == "development"
        
        print("🚀 Starting Nexus Réussite Backend Server...")
        print(f"📁 Source path: {src_path}")
        print(f"🌐 Server: http://{host}:{port}")
        print(f"🔧 Debug mode: {debug}")
        print(f"📋 Health check: http://{host}:{port}/health")
        print("=" * 50)
        
        # Création et lancement de l'application
        app = main_production.create_default_app()
        app.run(host=host, port=port, debug=debug)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.lock")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
