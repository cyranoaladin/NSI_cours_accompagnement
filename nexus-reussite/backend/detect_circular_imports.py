#!/usr/bin/env python3
"""
Script pour détecter les imports circulaires dans le projet Nexus Réussite
"""

import ast
import os
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Set, Tuple


class ImportAnalyzer:
    """Analyse les imports d'un projet Python pour détecter les cycles"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.imports = defaultdict(set)  # module -> set of imported modules
        self.modules = set()

    def extract_imports_from_file(self, file_path: Path) -> Set[str]:
        """Extrait les imports d'un fichier Python"""
        imports = set()

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
            return imports

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)

        return imports

    def get_module_name(self, file_path: Path) -> str:
        """Convertit un chemin de fichier en nom de module"""
        relative_path = file_path.relative_to(self.root_dir)
        module_parts = list(relative_path.parts)

        # Remplacer __init__.py par le nom du package
        if module_parts[-1] == "__init__.py":
            module_parts = module_parts[:-1]
        else:
            # Retirer l'extension .py
            module_parts[-1] = module_parts[-1].replace(".py", "")

        return ".".join(module_parts)

    def is_local_import(self, import_name: str) -> bool:
        """Vérifie si un import est local au projet"""
        return import_name.startswith("src") or import_name.startswith(".")

    def normalize_import(self, import_name: str, current_module: str) -> str:
        """Normalise un nom d'import relatif"""
        if import_name.startswith("."):
            # Import relatif
            current_parts = current_module.split(".")

            # Compter les points pour remonter dans l'arborescence
            dots = 0
            for char in import_name:
                if char == ".":
                    dots += 1
                else:
                    break

            # Partir du module courant et remonter
            if dots == 1:
                # Import relatif simple (. = même package)
                base_parts = (
                    current_parts[:-1] if len(current_parts) > 1 else current_parts
                )
            else:
                # Import relatif multiple (.. = package parent, etc.)
                base_parts = (
                    current_parts[: -(dots - 1)]
                    if len(current_parts) >= dots - 1
                    else []
                )

            # Ajouter la partie après les points
            rest = import_name[dots:]
            if rest:
                base_parts.append(rest)

            return ".".join(base_parts)

        return import_name

    def analyze_project(self):
        """Analyse tous les fichiers Python du projet"""
        for file_path in self.root_dir.rglob("*.py"):
            # Ignorer les fichiers de test et __pycache__
            if "__pycache__" in str(file_path) or file_path.name.startswith("test_"):
                continue

            module_name = self.get_module_name(file_path)
            self.modules.add(module_name)

            imports = self.extract_imports_from_file(file_path)

            for import_name in imports:
                if self.is_local_import(import_name):
                    normalized = self.normalize_import(import_name, module_name)
                    self.imports[module_name].add(normalized)

    def find_cycles(self) -> List[List[str]]:
        """Détecte les cycles dans le graphe d'imports"""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(module: str, path: List[str]) -> bool:
            visited.add(module)
            rec_stack.add(module)
            path.append(module)

            for imported_module in self.imports.get(module, set()):
                if imported_module not in self.modules:
                    continue

                if imported_module in rec_stack:
                    # Cycle détecté
                    cycle_start = path.index(imported_module)
                    cycle = path[cycle_start:] + [imported_module]
                    cycles.append(cycle)
                    return True

                if imported_module not in visited:
                    if dfs(imported_module, path.copy()):
                        return True

            rec_stack.remove(module)
            return False

        for module in self.modules:
            if module not in visited:
                dfs(module, [])

        return cycles

    def get_dependency_stats(self) -> Dict[str, int]:
        """Obtient des statistiques sur les dépendances"""
        stats = {
            "total_modules": len(self.modules),
            "total_imports": sum(len(imports) for imports in self.imports.values()),
            "modules_with_imports": len([m for m in self.modules if self.imports[m]]),
            "max_imports": max(
                (len(imports) for imports in self.imports.values()), default=0
            ),
        }

        return stats

    def get_most_imported_modules(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Trouve les modules les plus importés"""
        import_count = defaultdict(int)

        for module_imports in self.imports.values():
            for imported in module_imports:
                if imported in self.modules:
                    import_count[imported] += 1

        return sorted(import_count.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def get_heaviest_importers(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Trouve les modules qui importent le plus"""
        return sorted(
            [(module, len(imports)) for module, imports in self.imports.items()],
            key=lambda x: x[1],
            reverse=True,
        )[:top_n]


def main():
    """Fonction principale"""
    project_root = Path(__file__).parent / "src"

    if not project_root.exists():
        print(f"❌ Le répertoire {project_root} n'existe pas")
        sys.exit(1)

    print("🔍 Analyse des imports circulaires - Nexus Réussite")
    print("=" * 60)

    analyzer = ImportAnalyzer(project_root)
    analyzer.analyze_project()

    # Statistiques générales
    stats = analyzer.get_dependency_stats()
    print(f"\n📊 Statistiques générales:")
    print(f"  • Modules analysés: {stats['total_modules']}")
    print(f"  • Total imports locaux: {stats['total_imports']}")
    print(f"  • Modules avec imports: {stats['modules_with_imports']}")
    print(f"  • Maximum imports par module: {stats['max_imports']}")

    # Modules les plus importés
    print(f"\n🎯 Modules les plus importés:")
    for module, count in analyzer.get_most_imported_modules(5):
        print(f"  • {module}: {count} fois")

    # Modules qui importent le plus
    print(f"\n📦 Modules avec le plus d'imports:")
    for module, count in analyzer.get_heaviest_importers(5):
        print(f"  • {module}: {count} imports")

    # Détection des cycles
    cycles = analyzer.find_cycles()

    if cycles:
        print(f"\n⚠️  IMPORTS CIRCULAIRES DÉTECTÉS ({len(cycles)} cycles):")
        for i, cycle in enumerate(cycles, 1):
            print(f"\n  Cycle {i}:")
            for j, module in enumerate(cycle):
                if j < len(cycle) - 1:
                    print(f"    {module} → {cycle[j+1]}")

        print(f"\n💡 Recommandations pour résoudre les imports circulaires:")
        print(f"  1. Utiliser l'injection de dépendances")
        print(f"  2. Déplacer les imports dans les fonctions")
        print(f"  3. Créer un module séparé pour les interfaces/abstractions")
        print(f"  4. Revoir l'architecture des modules")
    else:
        print(f"\n✅ Aucun import circulaire détecté!")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
