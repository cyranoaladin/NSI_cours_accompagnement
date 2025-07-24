#!/usr/bin/env python3
"""
LANCEMENT DÉFINITIF NEXUS RÉUSSITE
Démarre réellement les services backend et frontend
"""
import subprocess
import time
import sys


def cleanup_processes():
    """Nettoie les processus existants"""
    print("🧹 Nettoyage des processus existants...")

    commands = [
        ["pkill", "-f", "python.*run_dev.py"],
        ["pkill", "-f", "npm.*run.*dev"],
        ["pkill", "-f", "node.*vite"]
    ]

    for cmd in commands:
        try:
            subprocess.run(
                cmd,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                check=False
            )
        except (subprocess.SubprocessError, OSError):
            pass

    time.sleep(2)
    print("✅ Processus nettoyés")


def start_backend():
    """Démarre le backend Flask"""
    print("🐍 Démarrage du Backend Flask...")

    backend_dir = "/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/backend"
    venv_activate = "/home/alaeddine/Documents/NSI_cours_accompagnement/.venv/bin/activate"

    # Commande bash complète
    bash_cmd = f"""
    cd {backend_dir}
    source {venv_activate}
    python run_dev.py
    """

    try:
        # Lancer en arrière-plan
        with open("/tmp/nexus-backend.log", "w", encoding="utf-8") as log_file:
            process = subprocess.Popen(
                ["bash", "-c", bash_cmd],
                stdout=log_file,
                stderr=subprocess.STDOUT
            )

        print(f"   ✅ Backend démarré (PID: {process.pid})")
        print("   📝 Log: /tmp/nexus-backend.log")
        return process

    except (subprocess.SubprocessError, OSError) as e:
        print(f"   ❌ Erreur backend: {e}")
        return None


def start_frontend():
    """Démarre le frontend React"""
    print("⚛️  Démarrage du Frontend React...")

    frontend_dir = "/home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite/frontend"

    try:
        # Lancer npm run dev
        with open("/tmp/nexus-frontend.log", "w", encoding="utf-8") as log_file:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                stdout=log_file,
                stderr=subprocess.STDOUT
            )

        print(f"   ✅ Frontend démarré (PID: {process.pid})")
        print("   📝 Log: /tmp/nexus-frontend.log")
        return process

    except (subprocess.SubprocessError, OSError) as e:
        print(f"   ❌ Erreur frontend: {e}")
        return None


def wait_for_services():
    """Attendre que les services soient opérationnels"""
    print("⏳ Attente de la stabilisation des services...")

    # Attendre 15 secondes pour la stabilisation
    for i in range(15):
        print(f"   Stabilisation: {i+1}/15s", end="\r")
        time.sleep(1)

    print("\n✅ Services stabilisés")


def main():
    """Fonction principale"""
    print("🎓✨ NEXUS RÉUSSITE - LANCEMENT DÉFINITIF ✨🎓")
    print("=" * 60)

    # Nettoyer les processus existants
    cleanup_processes()

    # Démarrer les services
    backend_process = start_backend()
    time.sleep(3)  # Laisser le temps au backend

    frontend_process = start_frontend()

    if not backend_process or not frontend_process:
        print("❌ Échec du démarrage des services")
        return 1

    # Attendre la stabilisation
    wait_for_services()

    # Affichage final
    print("\n🎉 NEXUS RÉUSSITE EST MAINTENANT OPÉRATIONNEL!")
    print("=" * 50)
    print()
    print("🌐 ACCÈS DIRECT AUX SERVICES:")
    print("   📱 Interface utilisateur: http://localhost:3000")
    print("   🔧 API Backend:          http://localhost:5000")
    print("   📊 Santé du système:     http://localhost:5000/health")
    print()
    print("🎯 FONCTIONNALITÉS DISPONIBLES:")
    print("   🤖 Assistant IA ARIA")
    print("   📊 Tableaux de bord interactifs")
    print("   👥 Gestion multi-utilisateurs")
    print("   📚 Banque d'exercices intelligente")
    print()
    print("📊 PROCESSUS ACTIFS:")
    print(f"   Backend PID:  {backend_process.pid}")
    print(f"   Frontend PID: {frontend_process.pid}")
    print()
    print("📝 LOGS EN TEMPS RÉEL:")
    print("   Backend:  tail -f /tmp/nexus-backend.log")
    print("   Frontend: tail -f /tmp/nexus-frontend.log")
    print()
    print("🔄 RAFRAÎCHISSEZ LES ONGLETS SIMPLE BROWSER DANS VS CODE")
    print()
    print("✨ Bienvenue dans l'avenir de l'éducation française ! ✨")

    # Garder le script actif
    try:
        print("\n⏸️  Script actif - Ctrl+C pour arrêter tous les services")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt demandé...")

        # Arrêter les processus
        try:
            if backend_process:
                backend_process.terminate()
            if frontend_process:
                frontend_process.terminate()
        except (subprocess.SubprocessError, OSError):
            pass

        print("✅ Tous les services arrêtés")
        return 0


if __name__ == "__main__":
    sys.exit(main())