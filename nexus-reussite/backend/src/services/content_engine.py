"""
Moteur d'assemblage intelligent pour la génération de contenu personnalisé
Nexus Réussite - Content Assembly Engine
"""

import json
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid
from ..models.content_system import (
    ContentBrick, BrickType, Subject, TargetProfile,
    LearningStep, DocumentRequest, GeneratedDocument
)
from .content_bank import ContentBankService

class ContentAssemblyEngine:
    """Moteur d'assemblage intelligent pour la génération de contenu personnalisé"""

    def __init__(self, content_bank: ContentBankService):
        self.content_bank = content_bank
        self.document_templates = self._load_document_templates()

    def _load_document_templates(self) -> Dict[str, Dict[str, Any]]:
        """Charge les templates de documents disponibles"""
        return {
            "fiche_revision": {
                "name": "Fiche de Révision",
                "structure": [
                    {"type": BrickType.DEFINITION, "count": 2, "required": True},
                    {"type": BrickType.THEOREME, "count": 1, "required": True},
                    {"type": BrickType.EXEMPLE, "count": 2, "required": True},
                    {"type": BrickType.CONSEIL_METHODE, "count": 1, "required": False},
                    {"type": BrickType.EXERCICE, "count": 3, "required": True}
                ],
                "estimated_duration": 45
            },
            "exercices_entrainement": {
                "name": "Série d'Exercices d'Entraînement",
                "structure": [
                    {"type": BrickType.DEFINITION, "count": 1, "required": False},
                    {"type": BrickType.EXERCICE, "count": 5, "required": True},
                    {"type": BrickType.CORRECTION, "count": 3, "required": True},
                    {"type": BrickType.CONSEIL_METHODE, "count": 2, "required": True}
                ],
                "estimated_duration": 60
            },
            "cours_complet": {
                "name": "Cours Complet",
                "structure": [
                    {"type": BrickType.DEFINITION, "count": 3, "required": True},
                    {"type": BrickType.THEOREME, "count": 2, "required": True},
                    {"type": BrickType.PROPRIETE, "count": 2, "required": False},
                    {"type": BrickType.EXEMPLE, "count": 4, "required": True},
                    {"type": BrickType.HISTOIRE_SCIENCES, "count": 1, "required": False},
                    {"type": BrickType.EXERCICE, "count": 2, "required": True},
                    {"type": BrickType.CONSEIL_METHODE, "count": 2, "required": True}
                ],
                "estimated_duration": 90
            },
            "evaluation_diagnostique": {
                "name": "Évaluation Diagnostique",
                "structure": [
                    {"type": BrickType.EXERCICE, "count": 8, "required": True},
                    {"type": BrickType.CORRECTION, "count": 8, "required": True}
                ],
                "estimated_duration": 120
            },
            "fiche_methode": {
                "name": "Fiche Méthode",
                "structure": [
                    {"type": BrickType.DEFINITION, "count": 1, "required": True},
                    {"type": BrickType.CONSEIL_METHODE, "count": 4, "required": True},
                    {"type": BrickType.EXEMPLE, "count": 3, "required": True},
                    {"type": BrickType.EXERCICE, "count": 2, "required": True}
                ],
                "estimated_duration": 30
            }
        }

    def generate_document(self, request: DocumentRequest) -> GeneratedDocument:
        """Génère un document personnalisé selon la requête"""
        start_time = datetime.now()

        # Validation de la requête
        if request.document_type not in self.document_templates:
            raise ValueError(f"Type de document non supporté: {request.document_type}")

        template = self.document_templates[request.document_type]

        # Sélection des briques de contenu
        selected_bricks = self._select_content_bricks(request, template)

        # Assemblage du contenu
        content_html, content_markdown = self._assemble_content(
            selected_bricks, template, request
        )

        # Calcul des métriques
        generation_time = (datetime.now() - start_time).total_seconds() * 1000
        estimated_duration = self._calculate_estimated_duration(selected_bricks)
        difficulty_level = self._calculate_difficulty_level(selected_bricks)

        # Création du document généré
        document = GeneratedDocument(
            id=str(uuid.uuid4()),
            request=request,
            bricks_used=[brick.id for brick in selected_bricks],
            content_html=content_html,
            content_markdown=content_markdown,
            title=self._generate_title(request, template),
            estimated_duration=estimated_duration,
            difficulty_level=difficulty_level,
            generated_at=datetime.now(),
            generation_time_ms=int(generation_time),
            template_used=request.document_type
        )

        # Mise à jour des statistiques d'utilisation
        for brick in selected_bricks:
            self.content_bank.increment_usage(brick.id)

        return document

    def _select_content_bricks(self, request: DocumentRequest, template: Dict[str, Any]) -> List[ContentBrick]:
        """Sélectionne les briques de contenu appropriées pour la requête"""
        selected_bricks = []

        for brick_spec in template["structure"]:
            brick_type = brick_spec["type"]
            count = brick_spec["count"]
            required = brick_spec["required"]

            # Recherche des briques candidates
            candidates = self.content_bank.search_bricks(
                subject=request.subject,
                chapter=request.chapter,
                brick_type=brick_type,
                difficulty_min=request.difficulty_range[0],
                difficulty_max=request.difficulty_range[1],
                target_profile=request.student_profile,
                learning_step=request.learning_step,
                tags=request.specific_topics if request.specific_topics else None
            )

            # Filtrage des sujets à exclure
            if request.exclude_topics:
                candidates = [
                    brick for brick in candidates
                    if not any(topic.lower() in [tag.lower() for tag in brick.tags]
                             for topic in request.exclude_topics)
                ]

            # Sélection intelligente
            if candidates:
                # Tri par pertinence (rating, usage, difficulté adaptée)
                candidates = self._rank_candidates(candidates, request)

                # Sélection du nombre requis
                selected_count = min(count, len(candidates))
                selected = candidates[:selected_count]
                selected_bricks.extend(selected)
            elif required:
                # Si aucune brique trouvée pour un type requis, on cherche plus largement
                fallback_candidates = self.content_bank.search_bricks(
                    subject=request.subject,
                    brick_type=brick_type,
                    target_profile=request.student_profile
                )
                if fallback_candidates:
                    selected_count = min(count, len(fallback_candidates))
                    selected = fallback_candidates[:selected_count]
                    selected_bricks.extend(selected)

        return selected_bricks

    def _rank_candidates(self, candidates: List[ContentBrick], request: DocumentRequest) -> List[ContentBrick]:
        """Classe les candidats par pertinence pour la requête"""
        def calculate_score(brick: ContentBrick) -> float:
            score = 0.0

            # Score basé sur la note moyenne
            score += brick.average_rating * 2

            # Score basé sur l'usage (popularité)
            score += min(brick.usage_count / 10, 2)  # Plafonné à 2 points

            # Score basé sur l'adéquation de difficulté
            target_difficulty = sum(request.difficulty_range) / 2
            difficulty_diff = abs(brick.difficulty - target_difficulty)
            score += max(0, 3 - difficulty_diff)  # Plus proche = meilleur score

            # Score basé sur les tags correspondants
            if request.specific_topics:
                matching_tags = sum(1 for topic in request.specific_topics
                                  if any(topic.lower() in tag.lower() for tag in brick.tags))
                score += matching_tags * 1.5

            # Score basé sur l'étape d'apprentissage
            if request.learning_step in brick.learning_steps:
                score += 2

            # Score basé sur le profil cible
            if request.student_profile in brick.target_profiles:
                score += 1.5

            return score

        # Tri par score décroissant
        candidates.sort(key=calculate_score, reverse=True)
        return candidates

    def _assemble_content(self, bricks: List[ContentBrick], template: Dict[str, Any],
                         request: DocumentRequest) -> Tuple[str, str]:
        """Assemble le contenu des briques sélectionnées"""

        # Organisation des briques par type
        bricks_by_type = {}
        for brick in bricks:
            if brick.type not in bricks_by_type:
                bricks_by_type[brick.type] = []
            bricks_by_type[brick.type].append(brick)

        # Construction du contenu selon la structure du template
        content_sections = []

        # En-tête du document
        header = f"""# {self._generate_title(request, template)}

**Matière :** {request.subject.value.title()}
**Chapitre :** {request.chapter}
**Niveau :** {request.student_profile.value.title()}
**Durée estimée :** {self._calculate_estimated_duration(bricks)} minutes
**Généré le :** {datetime.now().strftime("%d/%m/%Y à %H:%M")}

---

"""
        content_sections.append(header)

        # Assemblage selon la structure du template
        section_order = {
            BrickType.DEFINITION: "## 📚 Définitions et Concepts",
            BrickType.THEOREME: "## 🎯 Théorèmes et Propriétés",
            BrickType.PROPRIETE: "## ⚡ Propriétés Importantes",
            BrickType.EXEMPLE: "## 💡 Exemples et Applications",
            BrickType.EXERCICE: "## 📝 Exercices d'Application",
            BrickType.CORRECTION: "## ✅ Corrections Détaillées",
            BrickType.CONSEIL_METHODE: "## 🔧 Conseils Méthodologiques",
            BrickType.HISTOIRE_SCIENCES: "## 🏛️ Contexte Historique",
            BrickType.SCHEMA: "## 📊 Schémas et Diagrammes",
            BrickType.FORMULE: "## 🧮 Formulaire"
        }

        for brick_type, section_title in section_order.items():
            if brick_type in bricks_by_type:
                content_sections.append(f"\n{section_title}\n")

                for i, brick in enumerate(bricks_by_type[brick_type], 1):
                    if len(bricks_by_type[brick_type]) > 1:
                        content_sections.append(f"\n### {i}. {brick.title}\n")
                    else:
                        content_sections.append(f"\n### {brick.title}\n")

                    content_sections.append(brick.content)
                    content_sections.append("\n")

        # Pied de page
        footer = f"""
---

**Document généré automatiquement par Nexus Réussite**
*Système de personnalisation pédagogique - Version 1.0*

**Briques utilisées :** {len(bricks)} éléments pédagogiques
**Auteurs contributeurs :** {', '.join(set(brick.author_name for brick in bricks))}

Pour toute question, contactez votre coach Nexus Réussite.
"""
        content_sections.append(footer)

        # Assemblage final
        content_markdown = "\n".join(content_sections)

        # Conversion en HTML (simplifiée)
        content_html = self._markdown_to_html(content_markdown)

        return content_html, content_markdown

    def _markdown_to_html(self, markdown_content: str) -> str:
        """Conversion basique Markdown vers HTML"""
        html = markdown_content

        # Conversion des titres
        html = html.replace("# ", "<h1>").replace("\n", "</h1>\n", 1)
        html = html.replace("## ", "<h2>").replace("\n", "</h2>\n")
        html = html.replace("### ", "<h3>").replace("\n", "</h3>\n")

        # Conversion du gras
        import re
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

        # Conversion des listes
        html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)

        # Conversion des paragraphes
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        for p in paragraphs:
            if p.strip() and not p.startswith('<'):
                html_paragraphs.append(f'<p>{p.strip()}</p>')
            else:
                html_paragraphs.append(p)

        return '\n'.join(html_paragraphs)

    def _generate_title(self, request: DocumentRequest, template: Dict[str, Any]) -> str:
        """Génère un titre pour le document"""
        base_title = template["name"]
        return f"{base_title} - {request.chapter} ({request.subject.value.title()})"

    def _calculate_estimated_duration(self, bricks: List[ContentBrick]) -> int:
        """Calcule la durée estimée du document"""
        return sum(brick.duration_minutes for brick in bricks)

    def _calculate_difficulty_level(self, bricks: List[ContentBrick]) -> float:
        """Calcule le niveau de difficulté moyen du document"""
        if not bricks:
            return 1.0
        return sum(brick.difficulty for brick in bricks) / len(bricks)

    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Retourne la liste des templates disponibles"""
        return self.document_templates

    def suggest_document_type(self, student_profile: TargetProfile,
                            learning_step: LearningStep) -> str:
        """Suggère un type de document selon le profil et l'étape d'apprentissage"""

        suggestions = {
            (TargetProfile.STRUGGLING, LearningStep.DISCOVERY): "cours_complet",
            (TargetProfile.STRUGGLING, LearningStep.TRAINING): "fiche_methode",
            (TargetProfile.STRUGGLING, LearningStep.REVISION): "fiche_revision",

            (TargetProfile.AVERAGE, LearningStep.DISCOVERY): "cours_complet",
            (TargetProfile.AVERAGE, LearningStep.TRAINING): "exercices_entrainement",
            (TargetProfile.AVERAGE, LearningStep.REVISION): "fiche_revision",
            (TargetProfile.AVERAGE, LearningStep.EVALUATION): "evaluation_diagnostique",

            (TargetProfile.EXCELLENCE, LearningStep.TRAINING): "exercices_entrainement",
            (TargetProfile.EXCELLENCE, LearningStep.DEEPENING): "exercices_entrainement",
            (TargetProfile.EXCELLENCE, LearningStep.EVALUATION): "evaluation_diagnostique",
        }

        return suggestions.get((student_profile, learning_step), "fiche_revision")

    def analyze_content_gaps(self, subject: Subject, chapter: str) -> Dict[str, Any]:
        """Analyse les lacunes dans le contenu disponible"""

        all_bricks = self.content_bank.search_bricks(subject=subject, chapter=chapter)

        # Analyse par type de brique
        type_counts = {}
        for brick_type in BrickType:
            type_counts[brick_type.value] = len([
                b for b in all_bricks if b.type == brick_type
            ])

        # Analyse par niveau de difficulté
        difficulty_counts = {i: 0 for i in range(1, 6)}
        for brick in all_bricks:
            difficulty_counts[brick.difficulty] += 1

        # Analyse par profil cible
        profile_counts = {}
        for profile in TargetProfile:
            profile_counts[profile.value] = len([
                b for b in all_bricks
                if profile in b.target_profiles
            ])

        # Identification des lacunes
        gaps = []

        # Lacunes par type
        for brick_type, count in type_counts.items():
            if count < 2:  # Seuil minimum
                gaps.append(f"Manque de contenu de type '{brick_type}'")

        # Lacunes par difficulté
        for difficulty, count in difficulty_counts.items():
            if count == 0:
                gaps.append(f"Aucun contenu de niveau {difficulty}")

        return {
            "total_bricks": len(all_bricks),
            "by_type": type_counts,
            "by_difficulty": difficulty_counts,
            "by_profile": profile_counts,
            "identified_gaps": gaps,
            "coverage_score": min(100, (len(all_bricks) / 20) * 100)  # Score sur 20 briques minimum
        }


# Instance globale pour compatibilité avec les imports existants
from .content_bank import ContentBankService
content_engine = ContentAssemblyEngine(ContentBankService())

