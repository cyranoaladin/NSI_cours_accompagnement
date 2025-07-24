"""
Service de gestion de la banque de contenu modulaire
Nexus Réussite - Content Bank Service
"""

import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from ..models.content_system import (
    ContentBrick, BrickType, Subject, TargetProfile,
    LearningStep, DocumentRequest
)

class ContentBankService:
    """Service de gestion de la banque de contenu"""

    def __init__(self, data_file: str = "content_bank.json"):
        self.data_file = data_file
        self.bricks: Dict[str, ContentBrick] = {}
        self.load_data()

    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for brick_data in data.get('bricks', []):
                        brick = ContentBrick.from_dict(brick_data)
                        self.bricks[brick.id] = brick
            except Exception as e:
                print(f"Erreur lors du chargement des données: {e}")
                self._initialize_sample_data()
        else:
            self._initialize_sample_data()

    def save_data(self):
        """Sauvegarde les données dans le fichier JSON"""
        try:
            data = {
                'bricks': [brick.to_dict() for brick in self.bricks.values()],
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")

    def _initialize_sample_data(self):
        """Initialise la banque avec des données d'exemple"""
        sample_bricks = [
            # Mathématiques - Fonctions exponentielles
            ContentBrick(
                id=str(uuid.uuid4()),
                content="""# Définition de la fonction exponentielle

La fonction exponentielle, notée exp ou e^x, est définie sur ℝ par :

**exp(x) = e^x** où e ≈ 2,718...

## Propriétés fondamentales :
- exp(0) = 1
- exp(1) = e
- exp est strictement croissante sur ℝ
- exp(x) > 0 pour tout x ∈ ℝ""",
                type=BrickType.DEFINITION,
                title="Définition de la fonction exponentielle",
                subject=Subject.MATHEMATIQUES,
                chapter="Fonctions exponentielles",
                difficulty=2,
                target_profiles=[TargetProfile.AVERAGE, TargetProfile.EXCELLENCE],
                learning_steps=[LearningStep.DISCOVERY],
                tags=["exponentielle", "définition", "propriétés"],
                prerequisites=[],
                duration_minutes=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                author_id="coach_dubois",
                author_name="M. Dubois"
            ),

            ContentBrick(
                id=str(uuid.uuid4()),
                content="""# Propriété fondamentale de l'exponentielle

Pour tous réels a et b :
**exp(a + b) = exp(a) × exp(b)**

## Conséquences :
- exp(a - b) = exp(a) / exp(b)
- exp(na) = [exp(a)]^n pour n ∈ ℤ
- exp(-x) = 1/exp(x)

Cette propriété fait de l'exponentielle un **morphisme** de (ℝ,+) vers (ℝ*₊,×).""",
                type=BrickType.THEOREME,
                title="Propriété fondamentale de l'exponentielle",
                subject=Subject.MATHEMATIQUES,
                chapter="Fonctions exponentielles",
                difficulty=3,
                target_profiles=[TargetProfile.AVERAGE, TargetProfile.EXCELLENCE],
                learning_steps=[LearningStep.TRAINING],
                tags=["exponentielle", "propriété", "morphisme"],
                prerequisites=[],
                duration_minutes=15,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                author_id="coach_dubois",
                author_name="M. Dubois"
            ),

            # NSI - Graphes
            ContentBrick(
                id=str(uuid.uuid4()),
                content="""# Définition d'un graphe en informatique

Un **graphe** G = (V, E) est une structure de données composée de :
- **V** : un ensemble de sommets (vertices/nodes)
- **E** : un ensemble d'arêtes (edges) reliant les sommets

## Types de graphes :
- **Graphe orienté** : les arêtes ont une direction
- **Graphe non orienté** : les arêtes sont bidirectionnelles
- **Graphe pondéré** : chaque arête a un poids/coût

## Représentations :
- Matrice d'adjacence
- Liste d'adjacence
- Liste d'arêtes""",
                type=BrickType.DEFINITION,
                title="Définition d'un graphe",
                subject=Subject.NSI,
                chapter="Graphes",
                difficulty=2,
                target_profiles=[TargetProfile.AVERAGE, TargetProfile.EXCELLENCE],
                learning_steps=[LearningStep.DISCOVERY],
                tags=["graphe", "structure", "données"],
                prerequisites=[],
                duration_minutes=12,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                author_id="coach_martin",
                author_name="Mme Martin"
            ),

            ContentBrick(
                id=str(uuid.uuid4()),
                content="""# Exercice : Parcours en largeur (BFS)

Soit le graphe suivant représenté par sa liste d'adjacence :
```
A: [B, C]
B: [A, D, E]
C: [A, F]
D: [B]
E: [B, F]
F: [C, E]
```

**Questions :**
1. Effectuez un parcours en largeur à partir du sommet A
2. Donnez l'ordre de visite des sommets
3. Construisez l'arbre de parcours
4. Quelle est la complexité temporelle de cet algorithme ?

**Aide :** Utilisez une file (queue) pour implémenter le BFS.""",
                type=BrickType.EXERCICE,
                title="Exercice BFS sur graphe",
                subject=Subject.NSI,
                chapter="Graphes",
                difficulty=4,
                target_profiles=[TargetProfile.EXCELLENCE],
                learning_steps=[LearningStep.TRAINING, LearningStep.DEEPENING],
                tags=["BFS", "parcours", "algorithme"],
                prerequisites=["definition_graphe"],
                duration_minutes=25,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                author_id="coach_martin",
                author_name="Mme Martin"
            )
        ]

        for brick in sample_bricks:
            self.bricks[brick.id] = brick

        self.save_data()

    def add_brick(self, brick: ContentBrick) -> str:
        """Ajoute une nouvelle brique à la banque"""
        if not brick.id:
            brick.id = str(uuid.uuid4())

        brick.created_at = datetime.now()
        brick.updated_at = datetime.now()

        self.bricks[brick.id] = brick
        self.save_data()
        return brick.id

    def get_brick(self, brick_id: str) -> Optional[ContentBrick]:
        """Récupère une brique par son ID"""
        return self.bricks.get(brick_id)

    def update_brick(self, brick_id: str, updates: Dict[str, Any]) -> bool:
        """Met à jour une brique existante"""
        if brick_id not in self.bricks:
            return False

        brick = self.bricks[brick_id]
        for key, value in updates.items():
            if hasattr(brick, key):
                setattr(brick, key, value)

        brick.updated_at = datetime.now()
        self.save_data()
        return True

    def delete_brick(self, brick_id: str) -> bool:
        """Supprime une brique de la banque"""
        if brick_id in self.bricks:
            del self.bricks[brick_id]
            self.save_data()
            return True
        return False

    def search_bricks(self,
                     subject: Optional[Subject] = None,
                     chapter: Optional[str] = None,
                     brick_type: Optional[BrickType] = None,
                     difficulty_min: Optional[int] = None,
                     difficulty_max: Optional[int] = None,
                     target_profile: Optional[TargetProfile] = None,
                     learning_step: Optional[LearningStep] = None,
                     tags: Optional[List[str]] = None,
                     limit: Optional[int] = None) -> List[ContentBrick]:
        """Recherche des briques selon des critères"""

        results = []

        for brick in self.bricks.values():
            # Filtrage par matière
            if subject and brick.subject != subject:
                continue

            # Filtrage par chapitre
            if chapter and brick.chapter.lower() != chapter.lower():
                continue

            # Filtrage par type
            if brick_type and brick.type != brick_type:
                continue

            # Filtrage par difficulté
            if difficulty_min and brick.difficulty < difficulty_min:
                continue
            if difficulty_max and brick.difficulty > difficulty_max:
                continue

            # Filtrage par profil cible
            if target_profile and target_profile not in brick.target_profiles:
                continue

            # Filtrage par étape d'apprentissage
            if learning_step and learning_step not in brick.learning_steps:
                continue

            # Filtrage par tags
            if tags:
                if not any(tag.lower() in [t.lower() for t in brick.tags] for tag in tags):
                    continue

            results.append(brick)

        # Tri par pertinence (usage_count et rating)
        results.sort(key=lambda b: (b.average_rating, b.usage_count), reverse=True)

        if limit:
            results = results[:limit]

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """Retourne des statistiques sur la banque de contenu"""
        total_bricks = len(self.bricks)

        by_subject = {}
        by_type = {}
        by_difficulty = {}

        for brick in self.bricks.values():
            # Par matière
            subject_key = brick.subject.value
            by_subject[subject_key] = by_subject.get(subject_key, 0) + 1

            # Par type
            type_key = brick.type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1

            # Par difficulté
            diff_key = f"niveau_{brick.difficulty}"
            by_difficulty[diff_key] = by_difficulty.get(diff_key, 0) + 1

        return {
            'total_bricks': total_bricks,
            'by_subject': by_subject,
            'by_type': by_type,
            'by_difficulty': by_difficulty,
            'last_updated': datetime.now().isoformat()
        }

    def increment_usage(self, brick_id: str):
        """Incrémente le compteur d'utilisation d'une brique"""
        if brick_id in self.bricks:
            self.bricks[brick_id].usage_count += 1
            self.save_data()

    def update_rating(self, brick_id: str, rating: float):
        """Met à jour la note moyenne d'une brique"""
        if brick_id in self.bricks:
            brick = self.bricks[brick_id]
            # Calcul simple de moyenne pondérée (à améliorer avec un vrai système de votes)
            brick.average_rating = (brick.average_rating + rating) / 2
            self.save_data()

