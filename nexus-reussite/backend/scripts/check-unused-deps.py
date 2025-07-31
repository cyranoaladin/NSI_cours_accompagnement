#!/usr/bin/env python3

"""
==========================================
NEXUS RÉUSSITE - UNUSED DEPENDENCIES CHECKER
==========================================
Script pour identifier et gérer les dépendances inutilisées
avec pip-unused et analyse personnalisée
"""

import argparse
import json
import os
import subprocess
from pathlib import Path
import pkg_resources


class UnusedDependencyChecker:
    """Gestionnaire pour l'analyse des dépendances inutilisées."""
    
    def __init__(self, project_root: Path, src_paths: List[str] = None):
        self.project_root = project_root
        self.src_paths = src_paths or ["src", "tests", "scripts"]
        self.requirements_files = [
            "requirements.txt",
            "requirements-production.txt", 
            "requirements-dev.txt"
        ]
        
        # Exceptions: packages qui peuvent être utilisés de manière indirecte
        self.known_indirect_deps = {
            "setuptools", "wheel", "pip", "pip-tools",  # build tools
            "gunicorn", "gevent",  # WSGI servers
            "psycopg2-binary",  # database driver
            "alembic",  # migrations (via Flask-Migrate)
            "celery", "redis",  # async tasks
            "prometheus-client",  # metrics collection
            "sentry-sdk",  # error reporting
            "safety", "bandit", "pytest", "pytest-cov",  # dev tools
            "black", "flake8", "pylint", "mypy", "isort"  # linting
        }
        
        # Extras optionnels connus
        self.known_extras = {
            "crypto": ["cryptography", "bcrypt"],
            "pdf": ["reportlab", "pillow"],
            "excel": ["openpyxl", "xlrd"],
            "security": ["safety", "bandit"],
            "performance": ["gevent", "psutil"],
            "docs": ["sphinx", "sphinx-rtd-theme"],
            "dev": ["pytest", "black", "flake8", "mypy"]
        }

    def run_pip_unused(self) -> Tuple[List[str], List[str]]:
        """Exécute pip-unused et parse les résultats."""
        print("🔍 Analyse avec pip-unused...")
        
        try:
            # Installation de pip-unused si nécessaire
            try:
                import pip_unused
            except ImportError:
                print("📥 Installation de pip-unused...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "pip-unused>=0.0.10"
                ], check=True, capture_output=True, check=False)
        
            # Exécution de pip-unused
            result = subprocess.run([
                sys.executable, "-m", "pip_unused", 
                "--exclude", ",".join(self.known_indirect_deps, check=False),
                "--verbose"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                unused_deps = []
                # Parse de la sortie pip-unused
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        unused_deps.append(line.strip())
                
                return unused_deps, []
            else:
                return [], [f"pip-unused error: {result.stderr}"]
                
        except (RuntimeError, OSError, ValueError) as e:
            return [], [f"Erreur lors de l'exécution de pip-unused: {str(e)}"]

    def analyze_imports_in_code(self) -> Set[str]:
        """Analyse les imports dans le code source."""
        print("📂 Analyse des imports dans le code source...")
        
        imported_packages = set()
        
        for src_path in self.src_paths:
            src_dir = self.project_root / src_path
            if not src_dir.exists():
                continue
                
            for py_file in src_dir.rglob("*.py"):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Recherche des imports
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('import ') or line.startswith('from '):
                            # Extract package name
                            if line.startswith('import '):
                                package = line.replace('import ', '').split('.')[0].split(' as ')[0].split(',')[0].strip()
                            elif line.startswith('from '):
                                package = line.replace('from ', '').split('.')[0].split(' import')[0].strip()
                            
                            if package and not package.startswith('.'):
                                imported_packages.add(package)
                                
                except (RuntimeError, OSError, ValueError) as e:
                    print(f"⚠️  Erreur lors de la lecture de {py_file}: {e}")
                    
        return imported_packages

    def get_installed_packages(self) -> Dict[str, str]:
        """Récupère la liste des packages installés."""
        print("📦 Récupération des packages installés...")
        
        installed = {}
        for dist in pkg_resources.working_set:
            installed[dist.project_name.lower()] = dist.version
            
        return installed

    def parse_requirements_files(self) -> Dict[str, Set[str]]:
        """Parse les fichiers requirements pour obtenir les dépendances déclarées."""
        print("📄 Analyse des fichiers requirements...")
        
        requirements = {}
        
        for req_file in self.requirements_files:
            req_path = self.project_root / req_file
            if not req_path.exists():
                continue
                
            requirements[req_file] = set()
            
            try:
                with open(req_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('-'):
                            # Extract package name
                            package = line.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].split('!')[0].split('[')[0].strip()
                            if package:
                                requirements[req_file].add(package.lower())
                                
            except (RuntimeError, OSError, ValueError) as e:
                print(f"⚠️  Erreur lors de la lecture de {req_file}: {e}")
                
        return requirements

    def categorize_unused_deps(self, unused_deps: List[str], 
                             imported_packages: Set[str], 
                             installed_packages: Dict[str, str]) -> Dict[str, List[str]]:
        """Catégorise les dépendances inutilisées."""
        print("🏷️  Catégorisation des dépendances inutilisées...")
        
        categories = {
            "truly_unused": [],  # Vraiment inutilisées
            "indirect_deps": [],  # Dépendances indirectes
            "dev_tools": [],  # Outils de développement
            "optional_extras": [],  # Extras optionnels
            "potential_issues": []  # Problèmes potentiels
        }
        
        for dep in unused_deps:
            dep_lower = dep.lower()
            
            # Vérification des dépendances indirectes connues
            if dep_lower in self.known_indirect_deps:
                categories["indirect_deps"].append(dep)
                continue
                
            # Vérification des outils de dev
            if any(dev_tool in dep_lower for dev_tool in ["test", "lint", "format", "doc", "dev"]):
                categories["dev_tools"].append(dep)
                continue
                
            # Vérification des extras optionnels
            is_extra = False
            for extra_group, packages in self.known_extras.items():
                if dep_lower in [p.lower() for p in packages]:
                    categories["optional_extras"].append(dep)
                    is_extra = True
                    break
                    
            if is_extra:
                continue
                
            # Si le package n'est pas importé dans le code
            if dep_lower not in [p.lower() for p in imported_packages]:
                categories["truly_unused"].append(dep)
            else:
                categories["potential_issues"].append(dep)
                
        return categories

    def generate_report(self, categories: Dict[str, List[str]], 
                       installed_packages: Dict[str, str],
                       output_file: str = None) -> str:
        """Génère un rapport détaillé."""
        print("📊 Génération du rapport...")
        
        report_lines = [
            "# RAPPORT D'ANALYSE DES DÉPENDANCES INUTILISÉES",
            "=" * 60,
            f"Date: {subprocess.run(['date'], capture_output=True, text=True, check=False).stdout.strip()}",
            f"Projet: {self.project_root.name}",
            f"Packages installés: {len(installed_packages)}",
            "",
            "## RÉSUMÉ",
            "-" * 20
        ]
        
        total_unused = sum(len(deps) for deps in categories.values())
        report_lines.extend([
            f"Total dépendances potentiellement inutilisées: {total_unused}",
            f"- Vraiment inutilisées: {len(categories['truly_unused'])}",
            f"- Dépendances indirectes: {len(categories['indirect_deps'])}",
            f"- Outils de développement: {len(categories['dev_tools'])}",
            f"- Extras optionnels: {len(categories['optional_extras'])}",
            f"- Problèmes potentiels: {len(categories['potential_issues'])}",
            ""
        ])
        
        # Détail par catégorie
        for category, deps in categories.items():
            if not deps:
                continue
                
            category_title = {
                "truly_unused": "🗑️  DÉPENDANCES VRAIMENT INUTILISÉES",
                "indirect_deps": "🔗 DÉPENDANCES INDIRECTES",
                "dev_tools": "🛠️  OUTILS DE DÉVELOPPEMENT",
                "optional_extras": "📦 EXTRAS OPTIONNELS",
                "potential_issues": "⚠️  PROBLÈMES POTENTIELS"
            }.get(category, category.upper())
            
            report_lines.extend([
                f"## {category_title}",
                "-" * 40
            ])
            
            for dep in sorted(deps):
                version = installed_packages.get(dep.lower(), "unknown")
                report_lines.append(f"- {dep}=={version}")
                
            report_lines.append("")
            
        # Recommandations
        report_lines.extend([
            "## RECOMMANDATIONS",
            "-" * 30,
            "",
            "### Actions immédiates:",
            "1. Vérifiez les dépendances 'vraiment inutilisées' et supprimez-les si confirmé",
            "2. Documentez les dépendances indirectes dans un commentaire",
            "3. Déplacez les outils de dev vers requirements-dev.txt si nécessaire",
            "",
            "### Commandes suggérées:",
        ])
        
        if categories["truly_unused"]:
            unused_list = " ".join(categories["truly_unused"])
            report_lines.append(f"pip uninstall {unused_list}")
            
        if categories["dev_tools"]:
            report_lines.append("# Vérifiez que ces outils sont dans requirements-dev.txt:")
            for tool in categories["dev_tools"]:
                report_lines.append(f"# - {tool}")
                
        report_content = "\n".join(report_lines)
        
        if output_file:
            output_path = self.project_root / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"📄 Rapport sauvegardé dans {output_path}")
            
        return report_content

    def run_analysis(self, output_file: str = None, verbose: bool = False) -> int:
        """Exécute l'analyse complète."""
        print("🚀 Démarrage de l'analyse des dépendances inutilisées...")
        print(f"📁 Répertoire du projet: {self.project_root}")
        
        # 1. Exécution de pip-unused
        unused_deps, errors = self.run_pip_unused()
        
        if errors:
            print("❌ Erreurs détectées:")
            for error in errors:
                print(f"   {error}")
            return 1
            
        if not unused_deps:
            print("✅ Aucune dépendance inutilisée détectée!")
            return 0
            
        print(f"🔍 {len(unused_deps)} dépendances potentiellement inutilisées trouvées")
        
        if verbose:
            print("   " + ", ".join(unused_deps))
            
        # 2. Analyse des imports dans le code
        imported_packages = self.analyze_imports_in_code()
        print(f"📂 {len(imported_packages)} packages importés dans le code")
        
        # 3. Packages installés
        installed_packages = self.get_installed_packages()
        
        # 4. Catégorisation
        categories = self.categorize_unused_deps(
            unused_deps, imported_packages, installed_packages
        )
        
        # 5. Génération du rapport
        report = self.generate_report(categories, installed_packages, output_file)
        
        if not output_file:
            print("\n" + report)
            
        # Code de sortie basé sur le nombre de dépendances vraiment inutilisées
        truly_unused_count = len(categories["truly_unused"])
        if truly_unused_count > 0:
            print(f"\n⚠️  {truly_unused_count} dépendances vraiment inutilisées trouvées")
            return 2  # Code d'avertissement
        else:
            print("\n✅ Aucune dépendance vraiment inutilisée")
            return 0


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(
        description="Analyse les dépendances Python inutilisées"
    )
    parser.add_argument(
        "--project-root", 
        type=Path, 
        default=Path.cwd(),
        help="Répertoire racine du projet"
    )
    parser.add_argument(
        "--src-paths",
        nargs="+",
        default=["src", "tests", "scripts"],
        help="Chemins des sources à analyser"
    )
    parser.add_argument(
        "--output",
        help="Fichier de sortie pour le rapport"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mode verbeux"
    )
    parser.add_argument(
        "--fail-on-unused",
        action="store_true",
        help="Échoue (exit code 1) si des dépendances inutilisées sont trouvées"
    )
    
    args = parser.parse_args()
    
    checker = UnusedDependencyChecker(
        project_root=args.project_root,
        src_paths=args.src_paths
    )
    
    exit_code = checker.run_analysis(
        output_file=args.output,
        verbose=args.verbose
    )
    
    if args.fail_on_unused and exit_code == 2:
        exit_code = 1
        
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
