#!/usr/bin/env python3
"""
Lancement complet en parallèle - Nexus Réussite
"""
import sys
import time
import signal
import subprocess
import socket
import urllib.request
from pathlib import Path


class NexusLauncher:
    """Gestionnaire de lancement des services Nexus Réussite"""

    def __init__(self):
        """Initialise le lanceur"""
        self.backend_process = None
        self.frontend_process = None
        self.project_root = Path(
            "/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite"
        )
    def cleanup(self, signum=None, frame=None):
        """Arrêt propre des services
        
        Args:
            signum: Numéro du signal (inutilisé)
            frame: Frame d'exécution (inutilisé)
        """
        # Les paramètres signum et frame sont requis par signal.signal
        # mais ne sont pas utilisés dans cette implémentation
        del signum, frame  # Supprime l'avertissement unused-argument

        print("\n🛑 Arrêt des services Nexus Réussite...")

        if self.backend_process:
            print("   Arrêt du backend...")
            self.backend_process.terminate()

        if self.frontend_process:
            print("   Arrêt du frontend...")
            self.frontend_process.terminate()

        print("✅ Tous les services arrêtés")
        sys.exit(0)
    def start_backend(self):
        """Démarre le backend Flask
        
        Returns:
            bool: True si démarrage réussi, False sinon
        """
        print("🐍 Démarrage du backend...")

        backend_dir = self.project_root / "backend"
        venv_activate = self.project_root.parent / ".venv" / "bin" / "activate"

        # Script bash pour activer venv et lancer
        bash_command = f"""
        source {venv_activate}
        cd {backend_dir}
        python run_dev.py
        """

        try:
            self.backend_process = subprocess.Popen(
                ["bash", "-c", bash_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            print(f"✅ Backend démarré (PID: {self.backend_process.pid})")
            return True

        except (subprocess.SubprocessError, OSError) as e:
            print(f"❌ Erreur backend: {e}")
            return False
    def start_frontend(self):
        """Démarre le frontend React
        
        Returns:
            bool: True si démarrage réussi, False sinon
        """
        print("⚛️  Démarrage du frontend...")

        frontend_dir = self.project_root / "frontend"

        try:
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            print(f"✅ Frontend démarré (PID: {self.frontend_process.pid})")
            return True

        except (subprocess.SubprocessError, OSError) as e:
            print(f"❌ Erreur frontend: {e}")
            return False
    def wait_for_services(self):
        """Attendre que les services soient prêts"""
        print("⏳ Attente des services...")

        # Attendre le backend
        for i in range(30):
            try:
                urllib.request.urlopen(
                    "http://localhost:5000/health", timeout=1
                )
                print("✅ Backend opérationnel")
                break
            except (urllib.error.URLError, OSError):
                time.sleep(1)
                if i % 5 == 0:
                    print(f"   Backend: tentative {i+1}/30...")

        # Attendre le frontend
        for i in range(30):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', 3000))
                sock.close()

                if result == 0:
                    print("✅ Frontend opérationnel")
                    break
            except OSError:
                pass

            time.sleep(1)
            if i % 5 == 0:
                print(f"   Frontend: tentative {i+1}/30...")
                
    def run(self):
        """Lancement principal
        
        Returns:
            int: Code de retour (0 = succès, 1 = échec)
        """
        print("🎓✨ NEXUS RÉUSSITE - LANCEMENT COMPLET ✨🎓")
        print("=" * 60)

        # Gestionnaire de signaux
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

        # Démarrer les services
        backend_ok = self.start_backend()
        time.sleep(2)  # Laisser le temps au backend

        frontend_ok = self.start_frontend()

        if not backend_ok or not frontend_ok:
            print("❌ Échec du démarrage")
            return 1

        # Attendre que les services soient prêts
        self.wait_for_services()

        # Affichage final
        print("\n🎉 NEXUS RÉUSSITE EST OPÉRATIONNEL!")
        print("=" * 40)
        print()
        print("🌐 ACCÈS DIRECT:")
        print("   📱 Interface: http://localhost:3000")
        print("   🔧 API:       http://localhost:5000")
        print("   📊 Santé:     http://localhost:5000/health")
        print()
        print("🎯 FONCTIONNALITÉS:")
        print("   🤖 Assistant IA ARIA")
        print("   📊 Tableaux de bord interactifs")
        print("   👥 Gestion multi-utilisateurs")
        print("   📚 Banque d'exercices")
        print()
        print("⏸️  Pour arrêter: Ctrl+C")
        print()
        print("✨ Bienvenue dans l'avenir de l'éducation ! ✨")

        try:
            # Attendre les processus
            if self.backend_process and self.frontend_process:
                self.backend_process.wait()
                self.frontend_process.wait()
        except KeyboardInterrupt:
            self.cleanup()

        return 0


def main():
    """Point d'entrée principal
    
    Returns:
        int: Code de retour
    """
    launcher = NexusLauncher()
    return launcher.run()


if __name__ == "__main__":
    sys.exit(main())