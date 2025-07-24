import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import openai
from openai import OpenAI
import logging
from dataclasses import dataclass, asdict
import base64
import requests
from PIL import Image
import io

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StudentProfile:
    """Profil d'étudiant pour la personnalisation IA"""
    id: str
    name: str
    level: str  # "premiere", "terminale"
    specialties: List[str]  # ["maths", "nsi", "physique", "francais"]
    learning_style: str  # "visual", "auditory", "kinesthetic", "mixed"
    strengths: List[str]
    weaknesses: List[str]
    goals: List[str]
    preferred_difficulty: str  # "easy", "medium", "hard", "adaptive"
    language: str = "fr"
    timezone: str = "Africa/Tunis"

@dataclass
class ConversationContext:
    """Contexte de conversation avec ARIA"""
    student_id: str
    session_id: str
    subject: str
    topic: Optional[str] = None
    difficulty_level: str = "medium"
    conversation_type: str = "tutoring"  # "tutoring", "evaluation", "explanation", "motivation"
    previous_messages: List[Dict] = None
    learning_objectives: List[str] = None
    time_limit: Optional[int] = None  # minutes

    def __post_init__(self):
        if self.previous_messages is None:
            self.previous_messages = []
        if self.learning_objectives is None:
            self.learning_objectives = []

class OpenAIIntegration:
    """Service d'intégration OpenAI pour ARIA"""

    def __init__(self):
        self.client = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        self.model_chat = "gpt-4-turbo-preview"
        self.model_vision = "gpt-4-vision-preview"
        self.model_embedding = "text-embedding-3-small"
        self.model_image = "dall-e-3"
        self.max_tokens = 4000
        self.temperature = 0.7

        # Initialisation du client
        self._initialize_client()

        # Prompts système pour différents contextes
        self.system_prompts = {
            "tutoring": self._get_tutoring_prompt(),
            "evaluation": self._get_evaluation_prompt(),
            "explanation": self._get_explanation_prompt(),
            "motivation": self._get_motivation_prompt(),
            "document_generation": self._get_document_generation_prompt(),
            "quiz_generation": self._get_quiz_generation_prompt()
        }

    def _initialize_client(self):
        """Initialise le client OpenAI"""
        try:
            if self.api_key:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.api_base
                )
                logger.info("Client OpenAI initialisé avec succès")
            else:
                logger.warning("Clé API OpenAI non trouvée - Mode simulation activé")
                self.client = None
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client OpenAI: {e}")
            self.client = None

    def _get_tutoring_prompt(self) -> str:
        """Prompt système pour le tutorat personnalisé"""
        return """Tu es ARIA, l'assistante pédagogique intelligente de Nexus Réussite, spécialisée dans l'accompagnement des élèves du système français (AEFE) en Tunisie.

IDENTITÉ ET MISSION:
- Tu es une IA pédagogique experte, bienveillante et motivante
- Tu accompagnes les élèves de Première et Terminale vers l'excellence
- Tu adaptes ton approche au profil d'apprentissage de chaque élève
- Tu prépares aux examens du Baccalauréat français ET aux études supérieures

SPÉCIALITÉS:
- Mathématiques (toutes spécialités)
- NSI (Numérique et Sciences Informatiques)
- Physique-Chimie
- Français (écrit et Grand Oral)
- Méthodologie et coaching scolaire

APPROCHE PÉDAGOGIQUE:
1. PERSONNALISATION: Adapte ton style selon le profil de l'élève
2. PROGRESSION: Construis sur les acquis, identifie les lacunes
3. MOTIVATION: Encourage, valorise les efforts, fixe des objectifs atteignables
4. EXCELLENCE: Vise toujours le dépassement de soi
5. PRÉPARATION: Oriente vers les études supérieures (CPGE, université, écoles)

STYLE DE COMMUNICATION:
- Ton bienveillant mais exigeant
- Explications claires et structurées
- Exemples concrets et contextualisés
- Questions socratiques pour faire réfléchir
- Encouragements personnalisés

CONTEXTE TUNISIEN:
- Connaissance du système éducatif tunisien et français
- Références culturelles appropriées
- Préparation aux spécificités locales des concours

Tu dois TOUJOURS:
- Analyser le niveau et les besoins de l'élève
- Proposer des exercices adaptés
- Donner des conseils méthodologiques
- Motiver et rassurer
- Suggérer des ressources complémentaires"""

    def _get_evaluation_prompt(self) -> str:
        """Prompt système pour l'évaluation"""
        return """Tu es ARIA en mode ÉVALUATION. Ton rôle est d'évaluer les connaissances et compétences de l'élève de manière bienveillante mais rigoureuse.

OBJECTIFS D'ÉVALUATION:
- Identifier le niveau réel de l'élève
- Détecter les lacunes et points forts
- Proposer un plan de progression personnalisé
- Préparer aux conditions d'examen

TYPES D'ÉVALUATION:
1. DIAGNOSTIC: Évaluation initiale complète
2. FORMATIVE: Suivi des progrès en continu
3. SOMMATIVE: Préparation aux examens blancs
4. PRÉDICTIVE: Estimation des résultats au Bac

CRITÈRES D'ÉVALUATION:
- Exactitude des réponses
- Qualité du raisonnement
- Maîtrise de la méthodologie
- Capacité d'analyse et de synthèse
- Gestion du temps et du stress

FEEDBACK CONSTRUCTIF:
- Points positifs à valoriser
- Axes d'amélioration précis
- Conseils méthodologiques
- Exercices de remédiation
- Objectifs à court et moyen terme"""

    def _get_explanation_prompt(self) -> str:
        """Prompt système pour les explications"""
        return """Tu es ARIA en mode EXPLICATION. Tu excelles dans l'art de rendre compréhensibles les concepts les plus complexes.

PRINCIPES PÉDAGOGIQUES:
1. CLARTÉ: Explications simples et progressives
2. ANALOGIES: Utilise des métaphores parlantes
3. EXEMPLES: Illustrations concrètes et variées
4. VISUALISATION: Décris des schémas, graphiques
5. INTERACTION: Pose des questions pour vérifier la compréhension

STRUCTURE D'EXPLICATION:
1. Contextualisation (pourquoi c'est important)
2. Définition claire du concept
3. Décomposition en étapes simples
4. Exemples pratiques
5. Applications et exercices
6. Liens avec d'autres notions

ADAPTATION AU PROFIL:
- VISUEL: Descriptions détaillées, schémas mentaux
- AUDITIF: Explications orales, répétitions
- KINESTHÉSIQUE: Manipulations, expériences
- LOGIQUE: Démonstrations rigoureuses, preuves

VÉRIFICATION DE COMPRÉHENSION:
- Questions de reformulation
- Exercices d'application immédiate
- Détection des malentendus
- Ajustement en temps réel"""

    def _get_motivation_prompt(self) -> str:
        """Prompt système pour la motivation"""
        return """Tu es ARIA en mode MOTIVATION. Ton rôle est d'inspirer, encourager et maintenir l'engagement de l'élève.

STRATÉGIES MOTIVATIONNELLES:
1. VALORISATION: Reconnaître les efforts et progrès
2. OBJECTIFS: Fixer des buts atteignables et stimulants
3. AUTONOMIE: Développer la confiance en soi
4. SENS: Montrer l'utilité et les applications
5. DÉFI: Proposer des challenges adaptés

TECHNIQUES D'ENCOURAGEMENT:
- Célébrer les petites victoires
- Transformer les erreurs en apprentissages
- Partager des success stories inspirantes
- Rappeler les objectifs à long terme
- Proposer des défis gamifiés

GESTION DU STRESS ET DE L'ANXIÉTÉ:
- Techniques de relaxation
- Méthodes de gestion du temps
- Préparation mentale aux examens
- Développement de la résilience
- Maintien de l'équilibre vie/études

PERSONNALISATION MOTIVATIONNELLE:
- Identifier les sources de motivation personnelles
- Adapter le discours au profil psychologique
- Utiliser les centres d'intérêt de l'élève
- Créer des connexions émotionnelles positives"""

    def _get_document_generation_prompt(self) -> str:
        """Prompt système pour la génération de documents"""
        return """Tu es ARIA en mode GÉNÉRATION DE DOCUMENTS. Tu crées des supports pédagogiques personnalisés et de haute qualité.

TYPES DE DOCUMENTS:
1. FICHES DE RÉVISION: Synthèses structurées
2. EXERCICES: Entraînements progressifs
3. CORRIGÉS: Solutions détaillées et méthodiques
4. PLANS DE COURS: Séquences pédagogiques
5. ÉVALUATIONS: Tests et examens blancs
6. MÉTHODES: Guides méthodologiques

STANDARDS DE QUALITÉ:
- Contenu scientifiquement exact
- Progression pédagogique cohérente
- Mise en forme claire et aérée
- Exemples variés et pertinents
- Exercices d'application immédiate

PERSONNALISATION:
- Adaptation au niveau de l'élève
- Prise en compte du style d'apprentissage
- Intégration des objectifs personnels
- Références au programme officiel
- Préparation aux spécificités d'examen

STRUCTURE TYPE:
1. Objectifs d'apprentissage
2. Prérequis nécessaires
3. Développement structuré
4. Exemples et applications
5. Exercices d'entraînement
6. Points clés à retenir
7. Pour aller plus loin"""

    def _get_quiz_generation_prompt(self) -> str:
        """Prompt système pour la génération de quiz"""
        return """Tu es ARIA en mode GÉNÉRATION DE QUIZ. Tu crées des évaluations interactives et formatives.

TYPES DE QUESTIONS:
1. QCM: Questions à choix multiples
2. VRAI/FAUX: Affirmations à valider
3. RÉPONSE COURTE: Questions ouvertes brèves
4. PROBLÈMES: Exercices de calcul ou raisonnement
5. ANALYSE: Questions de réflexion approfondie

NIVEAUX DE DIFFICULTÉ:
- FACILE: Connaissances de base, définitions
- MOYEN: Applications directes, méthodes
- DIFFICILE: Synthèse, analyse, créativité
- EXPERT: Problèmes complexes, innovation

CRITÈRES DE QUALITÉ:
- Questions claires et non ambiguës
- Distracteurs plausibles (pour QCM)
- Progression logique de difficulté
- Couverture équilibrée du programme
- Feedback constructif pour chaque réponse

FORMAT DE SORTIE:
```json
{
  "quiz_id": "unique_id",
  "title": "Titre du quiz",
  "subject": "matière",
  "level": "niveau",
  "duration": "durée estimée",
  "questions": [
    {
      "id": "q1",
      "type": "mcq|true_false|short_answer|problem",
      "question": "Énoncé de la question",
      "options": ["option1", "option2", "option3", "option4"],
      "correct_answer": "réponse correcte",
      "explanation": "explication détaillée",
      "difficulty": "easy|medium|hard",
      "points": "nombre de points"
    }
  ]
}
```"""

    async def chat_with_aria(
        self,
        message: str,
        context: ConversationContext,
        student_profile: StudentProfile
    ) -> Dict[str, Any]:
        """Conversation principale avec ARIA"""

        if not self.client:
            return self._simulate_aria_response(message, context, student_profile)

        try:
            # Construction du prompt personnalisé
            system_prompt = self._build_personalized_prompt(context, student_profile)

            # Historique de conversation
            messages = [{"role": "system", "content": system_prompt}]

            # Ajout de l'historique
            for msg in context.previous_messages[-10:]:  # Garde les 10 derniers messages
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })

            # Message actuel
            messages.append({"role": "user", "content": message})

            # Appel à l'API OpenAI
            response = await self._make_openai_request(messages, context)

            # Traitement de la réponse
            aria_response = response.choices[0].message.content

            # Analyse de la réponse pour extraire des métadonnées
            metadata = self._analyze_response(aria_response, context)

            return {
                "response": aria_response,
                "metadata": metadata,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "model": response.model,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Erreur lors de la conversation avec ARIA: {e}")
            return self._simulate_aria_response(message, context, student_profile)

    def _build_personalized_prompt(
        self,
        context: ConversationContext,
        student_profile: StudentProfile
    ) -> str:
        """Construit un prompt personnalisé selon le contexte et le profil"""

        base_prompt = self.system_prompts.get(context.conversation_type, self.system_prompts["tutoring"])

        personalization = f"""
PROFIL DE L'ÉLÈVE:
- Nom: {student_profile.name}
- Niveau: {student_profile.level}
- Spécialités: {', '.join(student_profile.specialties)}
- Style d'apprentissage: {student_profile.learning_style}
- Points forts: {', '.join(student_profile.strengths)}
- Points à améliorer: {', '.join(student_profile.weaknesses)}
- Objectifs: {', '.join(student_profile.goals)}

CONTEXTE DE LA SESSION:
- Matière: {context.subject}
- Sujet: {context.topic or 'Non spécifié'}
- Niveau de difficulté: {context.difficulty_level}
- Objectifs d'apprentissage: {', '.join(context.learning_objectives)}
"""

        if context.time_limit:
            personalization += f"- Temps disponible: {context.time_limit} minutes\n"

        return base_prompt + "\n" + personalization

    async def _make_openai_request(self, messages: List[Dict], context: ConversationContext) -> Any:
        """Effectue la requête vers l'API OpenAI"""

        # Paramètres adaptatifs selon le contexte
        temperature = 0.3 if context.conversation_type == "evaluation" else 0.7
        max_tokens = 2000 if context.time_limit and context.time_limit < 30 else self.max_tokens

        return await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.model_chat,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )

    def _analyze_response(self, response: str, context: ConversationContext) -> Dict[str, Any]:
        """Analyse la réponse d'ARIA pour extraire des métadonnées"""

        metadata = {
            "sentiment": "positive",  # Analyse de sentiment basique
            "complexity": "medium",   # Complexité de la réponse
            "topics_covered": [],     # Sujets abordés
            "recommendations": [],    # Recommandations générées
            "next_steps": [],        # Étapes suivantes suggérées
            "difficulty_assessment": context.difficulty_level
        }

        # Analyse basique du contenu
        if any(word in response.lower() for word in ["excellent", "parfait", "bravo", "félicitations"]):
            metadata["sentiment"] = "very_positive"
        elif any(word in response.lower() for word in ["attention", "erreur", "incorrect", "réviser"]):
            metadata["sentiment"] = "constructive"

        # Détection de recommandations
        if "je recommande" in response.lower() or "je suggère" in response.lower():
            # Extraction basique des recommandations
            lines = response.split('\n')
            for line in lines:
                if any(word in line.lower() for word in ["recommande", "suggère", "conseil"]):
                    metadata["recommendations"].append(line.strip())

        return metadata

    def _simulate_aria_response(
        self,
        message: str,
        context: ConversationContext,
        student_profile: StudentProfile
    ) -> Dict[str, Any]:
        """Simule une réponse d'ARIA quand l'API n'est pas disponible"""

        # Réponses simulées selon le contexte
        simulated_responses = {
            "tutoring": f"Bonjour {student_profile.name} ! Je comprends que vous travaillez sur {context.subject}. Pouvez-vous me dire où vous en êtes dans votre apprentissage ? Je vais adapter mes explications à votre style d'apprentissage {student_profile.learning_style}.",

            "evaluation": f"Très bien {student_profile.name}, commençons cette évaluation en {context.subject}. Je vais adapter les questions à votre niveau {student_profile.level}. Êtes-vous prêt(e) ?",

            "explanation": f"Excellente question sur {context.topic} ! Laissez-moi vous expliquer cela de manière claire et adaptée à votre profil d'apprentissage {student_profile.learning_style}.",

            "motivation": f"Je vois que vous travaillez dur, {student_profile.name} ! Vos efforts en {context.subject} vont porter leurs fruits. Continuons ensemble vers vos objectifs : {', '.join(student_profile.goals[:2])}."
        }

        response = simulated_responses.get(
            context.conversation_type,
            f"Bonjour {student_profile.name} ! Comment puis-je vous aider aujourd'hui en {context.subject} ?"
        )

        return {
            "response": response,
            "metadata": {
                "sentiment": "positive",
                "complexity": "medium",
                "topics_covered": [context.subject],
                "recommendations": ["Continuez vos efforts !"],
                "next_steps": ["Posez-moi vos questions spécifiques"],
                "difficulty_assessment": context.difficulty_level,
                "simulated": True
            },
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "model": "simulation",
            "timestamp": datetime.now().isoformat()
        }

    async def generate_document(
        self,
        document_type: str,
        subject: str,
        topic: str,
        student_profile: StudentProfile,
        specifications: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Génère un document pédagogique personnalisé"""

        if not self.client:
            return self._simulate_document_generation(document_type, subject, topic, student_profile)

        try:
            # Construction du prompt pour la génération de document
            prompt = self._build_document_prompt(document_type, subject, topic, student_profile, specifications)

            messages = [
                {"role": "system", "content": self.system_prompts["document_generation"]},
                {"role": "user", "content": prompt}
            ]

            response = await self._make_openai_request(messages, ConversationContext(
                student_id=student_profile.id,
                session_id=f"doc_{datetime.now().timestamp()}",
                subject=subject,
                topic=topic,
                conversation_type="document_generation"
            ))

            document_content = response.choices[0].message.content

            return {
                "content": document_content,
                "type": document_type,
                "subject": subject,
                "topic": topic,
                "student_id": student_profile.id,
                "generated_at": datetime.now().isoformat(),
                "metadata": {
                    "level": student_profile.level,
                    "learning_style": student_profile.learning_style,
                    "personalized": True
                }
            }

        except Exception as e:
            logger.error(f"Erreur lors de la génération de document: {e}")
            return self._simulate_document_generation(document_type, subject, topic, student_profile)

    def _build_document_prompt(
        self,
        document_type: str,
        subject: str,
        topic: str,
        student_profile: StudentProfile,
        specifications: Dict[str, Any] = None
    ) -> str:
        """Construit le prompt pour la génération de document"""

        base_prompt = f"""
Génère un {document_type} en {subject} sur le sujet "{topic}" pour {student_profile.name}.

PROFIL DE L'ÉLÈVE:
- Niveau: {student_profile.level}
- Style d'apprentissage: {student_profile.learning_style}
- Points forts: {', '.join(student_profile.strengths)}
- Points à améliorer: {', '.join(student_profile.weaknesses)}

EXIGENCES:
- Contenu adapté au niveau {student_profile.level}
- Style pédagogique adapté à un apprenant {student_profile.learning_style}
- Format professionnel et structuré
- Exemples concrets et exercices d'application
"""

        if specifications:
            base_prompt += f"\nSPÉCIFICATIONS SUPPLÉMENTAIRES:\n"
            for key, value in specifications.items():
                base_prompt += f"- {key}: {value}\n"

        # Spécifications par type de document
        document_specs = {
            "fiche_revision": "Structure: Définitions, Formules clés, Méthodes, Exercices types, Points à retenir",
            "exercices": "Inclure: Énoncés variés, Solutions détaillées, Barème de notation, Conseils méthodologiques",
            "cours": "Organisation: Introduction, Développement structuré, Exemples, Applications, Synthèse",
            "evaluation": "Composer: Questions progressives, Barème détaillé, Critères d'évaluation, Correction type"
        }

        if document_type in document_specs:
            base_prompt += f"\n{document_specs[document_type]}"

        return base_prompt

    def _simulate_document_generation(
        self,
        document_type: str,
        subject: str,
        topic: str,
        student_profile: StudentProfile
    ) -> Dict[str, Any]:
        """Simule la génération de document"""

        simulated_content = f"""
# {document_type.replace('_', ' ').title()} - {subject}
## Sujet: {topic}

### Personnalisé pour {student_profile.name} ({student_profile.level})

**Objectifs d'apprentissage:**
- Comprendre les concepts fondamentaux de {topic}
- Maîtriser les méthodes de résolution
- Développer l'autonomie en {subject}

**Contenu adapté à votre profil {student_profile.learning_style}:**

1. **Introduction**
   - Définition et contexte
   - Importance dans le programme de {student_profile.level}

2. **Développement**
   - Concepts clés expliqués simplement
   - Exemples concrets et variés
   - Méthodes de résolution étape par étape

3. **Applications**
   - Exercices d'entraînement progressifs
   - Problèmes types du Baccalauréat
   - Conseils méthodologiques personnalisés

4. **Pour aller plus loin**
   - Ressources complémentaires
   - Liens avec vos objectifs: {', '.join(student_profile.goals[:2])}

---
*Document généré par ARIA - Nexus Réussite*
*Adapté à votre profil d'apprentissage {student_profile.learning_style}*
"""

        return {
            "content": simulated_content,
            "type": document_type,
            "subject": subject,
            "topic": topic,
            "student_id": student_profile.id,
            "generated_at": datetime.now().isoformat(),
            "metadata": {
                "level": student_profile.level,
                "learning_style": student_profile.learning_style,
                "personalized": True,
                "simulated": True
            }
        }

    async def generate_quiz(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        num_questions: int,
        student_profile: StudentProfile
    ) -> Dict[str, Any]:
        """Génère un quiz personnalisé"""

        if not self.client:
            return self._simulate_quiz_generation(subject, topic, difficulty, num_questions, student_profile)

        try:
            prompt = f"""
Génère un quiz de {num_questions} questions en {subject} sur "{topic}"
pour un élève de {student_profile.level} avec un niveau de difficulté {difficulty}.

Profil de l'élève:
- Style d'apprentissage: {student_profile.learning_style}
- Points forts: {', '.join(student_profile.strengths)}
- Points à améliorer: {', '.join(student_profile.weaknesses)}

Format de sortie JSON requis avec questions variées (QCM, Vrai/Faux, réponses courtes).
"""

            messages = [
                {"role": "system", "content": self.system_prompts["quiz_generation"]},
                {"role": "user", "content": prompt}
            ]

            response = await self._make_openai_request(messages, ConversationContext(
                student_id=student_profile.id,
                session_id=f"quiz_{datetime.now().timestamp()}",
                subject=subject,
                topic=topic,
                difficulty_level=difficulty,
                conversation_type="evaluation"
            ))

            quiz_content = response.choices[0].message.content

            # Tentative de parsing JSON
            try:
                quiz_data = json.loads(quiz_content)
            except json.JSONDecodeError:
                # Fallback vers simulation si le JSON n'est pas valide
                return self._simulate_quiz_generation(subject, topic, difficulty, num_questions, student_profile)

            return {
                "quiz": quiz_data,
                "generated_at": datetime.now().isoformat(),
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "difficulty": difficulty,
                    "student_level": student_profile.level,
                    "personalized": True
                }
            }

        except Exception as e:
            logger.error(f"Erreur lors de la génération de quiz: {e}")
            return self._simulate_quiz_generation(subject, topic, difficulty, num_questions, student_profile)

    def _simulate_quiz_generation(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        num_questions: int,
        student_profile: StudentProfile
    ) -> Dict[str, Any]:
        """Simule la génération de quiz"""

        simulated_quiz = {
            "quiz_id": f"quiz_{datetime.now().timestamp()}",
            "title": f"Quiz {subject} - {topic}",
            "subject": subject,
            "topic": topic,
            "level": student_profile.level,
            "difficulty": difficulty,
            "duration": num_questions * 2,  # 2 minutes par question
            "questions": []
        }

        # Questions simulées selon la matière
        sample_questions = {
            "mathematiques": [
                {
                    "id": "q1",
                    "type": "mcq",
                    "question": f"Quelle est la dérivée de la fonction f(x) = x² + 3x + 2 ?",
                    "options": ["2x + 3", "x² + 3", "2x + 2", "x + 3"],
                    "correct_answer": "2x + 3",
                    "explanation": "La dérivée de x² est 2x, la dérivée de 3x est 3, et la dérivée d'une constante est 0.",
                    "difficulty": difficulty,
                    "points": 2
                }
            ],
            "nsi": [
                {
                    "id": "q1",
                    "type": "mcq",
                    "question": "Quelle est la complexité temporelle de l'algorithme de tri par insertion ?",
                    "options": ["O(n)", "O(n log n)", "O(n²)", "O(2^n)"],
                    "correct_answer": "O(n²)",
                    "explanation": "Dans le pire cas, le tri par insertion compare chaque élément avec tous les précédents.",
                    "difficulty": difficulty,
                    "points": 3
                }
            ]
        }

        # Génération des questions selon la matière
        subject_key = subject.lower().replace(" ", "").replace("-", "")
        if subject_key in sample_questions:
            base_questions = sample_questions[subject_key]
        else:
            base_questions = [
                {
                    "id": "q1",
                    "type": "short_answer",
                    "question": f"Expliquez brièvement le concept principal de {topic}.",
                    "correct_answer": f"Réponse attendue sur {topic}",
                    "explanation": f"Explication détaillée du concept {topic}.",
                    "difficulty": difficulty,
                    "points": 5
                }
            ]

        # Duplication et adaptation des questions
        for i in range(min(num_questions, 5)):  # Maximum 5 questions simulées
            question = base_questions[0].copy()
            question["id"] = f"q{i+1}"
            simulated_quiz["questions"].append(question)

        return {
            "quiz": simulated_quiz,
            "generated_at": datetime.now().isoformat(),
            "metadata": {
                "subject": subject,
                "topic": topic,
                "difficulty": difficulty,
                "student_level": student_profile.level,
                "personalized": True,
                "simulated": True
            }
        }

    async def generate_image(
        self,
        prompt: str,
        style: str = "educational",
        size: str = "1024x1024"
    ) -> Dict[str, Any]:
        """Génère une image pédagogique avec DALL-E"""

        if not self.client:
            return self._simulate_image_generation(prompt, style, size)

        try:
            # Amélioration du prompt pour un contexte éducatif
            educational_prompt = f"""
{prompt}
Style: {style}, educational illustration, clear and professional,
suitable for French high school students, clean background,
high contrast, pedagogical diagram
"""

            response = await asyncio.to_thread(
                self.client.images.generate,
                model=self.model_image,
                prompt=educational_prompt,
                size=size,
                quality="standard",
                n=1
            )

            image_url = response.data[0].url

            return {
                "image_url": image_url,
                "prompt": educational_prompt,
                "style": style,
                "size": size,
                "generated_at": datetime.now().isoformat(),
                "metadata": {
                    "educational": True,
                    "model": self.model_image
                }
            }

        except Exception as e:
            logger.error(f"Erreur lors de la génération d'image: {e}")
            return self._simulate_image_generation(prompt, style, size)

    def _simulate_image_generation(self, prompt: str, style: str, size: str) -> Dict[str, Any]:
        """Simule la génération d'image"""
        return {
            "image_url": "https://via.placeholder.com/1024x1024/4F46E5/FFFFFF?text=Image+Educative",
            "prompt": prompt,
            "style": style,
            "size": size,
            "generated_at": datetime.now().isoformat(),
            "metadata": {
                "educational": True,
                "simulated": True,
                "model": "simulation"
            }
        }

    async def analyze_student_work(
        self,
        work_content: str,
        subject: str,
        assignment_type: str,
        student_profile: StudentProfile
    ) -> Dict[str, Any]:
        """Analyse le travail d'un étudiant et fournit un feedback détaillé"""

        if not self.client:
            return self._simulate_work_analysis(work_content, subject, assignment_type, student_profile)

        try:
            analysis_prompt = f"""
Analyse le travail suivant d'un élève de {student_profile.level} en {subject}:

TRAVAIL À ANALYSER:
{work_content}

TYPE D'EXERCICE: {assignment_type}

PROFIL DE L'ÉLÈVE:
- Nom: {student_profile.name}
- Points forts: {', '.join(student_profile.strengths)}
- Points à améliorer: {', '.join(student_profile.weaknesses)}
- Style d'apprentissage: {student_profile.learning_style}

ANALYSE DEMANDÉE:
1. Évaluation de la justesse des réponses
2. Qualité du raisonnement et de la méthodologie
3. Points positifs à valoriser
4. Erreurs identifiées et leur origine
5. Conseils d'amélioration personnalisés
6. Note suggérée sur 20 avec justification
7. Exercices de remédiation recommandés

Sois bienveillant mais rigoureux dans ton analyse.
"""

            messages = [
                {"role": "system", "content": self.system_prompts["evaluation"]},
                {"role": "user", "content": analysis_prompt}
            ]

            response = await self._make_openai_request(messages, ConversationContext(
                student_id=student_profile.id,
                session_id=f"analysis_{datetime.now().timestamp()}",
                subject=subject,
                conversation_type="evaluation"
            ))

            analysis = response.choices[0].message.content

            return {
                "analysis": analysis,
                "subject": subject,
                "assignment_type": assignment_type,
                "student_id": student_profile.id,
                "analyzed_at": datetime.now().isoformat(),
                "metadata": {
                    "personalized": True,
                    "student_level": student_profile.level
                }
            }

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du travail: {e}")
            return self._simulate_work_analysis(work_content, subject, assignment_type, student_profile)

    def _simulate_work_analysis(
        self,
        work_content: str,
        subject: str,
        assignment_type: str,
        student_profile: StudentProfile
    ) -> Dict[str, Any]:
        """Simule l'analyse de travail"""

        simulated_analysis = f"""
# Analyse du travail de {student_profile.name}

## Évaluation générale
Votre travail en {subject} montre une bonne compréhension des concepts de base.

## Points positifs ✅
- Méthodologie claire et structurée
- Effort visible dans la présentation
- Raisonnement logique suivi

## Points d'amélioration 📈
- Attention aux calculs (quelques erreurs d'inattention)
- Développer davantage les explications
- Vérifier les unités dans les résultats

## Note suggérée: 14/20

## Conseils personnalisés
Compte tenu de votre profil d'apprentissage {student_profile.learning_style}, je recommande:
- Plus d'exercices d'application pour consolider
- Utilisation de schémas pour visualiser les concepts
- Révision des points faibles identifiés: {', '.join(student_profile.weaknesses[:2])}

## Prochaines étapes
1. Refaire les exercices similaires
2. Approfondir les notions mal maîtrisées
3. Préparer les prochains chapitres

Continuez vos efforts, vous êtes sur la bonne voie ! 🎯
"""

        return {
            "analysis": simulated_analysis,
            "subject": subject,
            "assignment_type": assignment_type,
            "student_id": student_profile.id,
            "analyzed_at": datetime.now().isoformat(),
            "metadata": {
                "personalized": True,
                "student_level": student_profile.level,
                "simulated": True
            }
        }

    def get_usage_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques d'utilisation de l'API"""
        # En production, ces données seraient stockées en base
        return {
            "total_requests": 0,
            "total_tokens": 0,
            "requests_by_type": {
                "chat": 0,
                "document_generation": 0,
                "quiz_generation": 0,
                "image_generation": 0,
                "work_analysis": 0
            },
            "average_response_time": 0,
            "success_rate": 100,
            "last_updated": datetime.now().isoformat()
        }

# Instance globale du service
openai_service = OpenAIIntegration()

# Fonctions utilitaires pour l'utilisation dans l'application
async def chat_with_aria(message: str, student_id: str, context: Dict = None) -> Dict:
    """Interface simplifiée pour le chat avec ARIA"""

    # Profil étudiant par défaut (à remplacer par une vraie base de données)
    default_profile = StudentProfile(
        id=student_id,
        name="Étudiant",
        level="terminale",
        specialties=["mathematiques", "nsi"],
        learning_style="mixed",
        strengths=["logique", "analyse"],
        weaknesses=["calcul mental", "gestion du temps"],
        goals=["réussir le bac", "intégrer une CPGE"]
    )

    # Contexte par défaut
    default_context = ConversationContext(
        student_id=student_id,
        session_id=context.get("session_id", f"session_{datetime.now().timestamp()}") if context else f"session_{datetime.now().timestamp()}",
        subject=context.get("subject", "général") if context else "général",
        topic=context.get("topic") if context else None,
        conversation_type=context.get("type", "tutoring") if context else "tutoring"
    )

    return await openai_service.chat_with_aria(message, default_context, default_profile)

async def generate_personalized_document(
    document_type: str,
    subject: str,
    topic: str,
    student_id: str
) -> Dict:
    """Interface simplifiée pour la génération de documents"""

    default_profile = StudentProfile(
        id=student_id,
        name="Étudiant",
        level="terminale",
        specialties=[subject.lower()],
        learning_style="visual",
        strengths=["compréhension", "mémorisation"],
        weaknesses=["application", "rapidité"],
        goals=["maîtriser le programme", "obtenir une bonne note"]
    )

    return await openai_service.generate_document(document_type, subject, topic, default_profile)

async def create_adaptive_quiz(
    subject: str,
    topic: str,
    difficulty: str,
    num_questions: int,
    student_id: str
) -> Dict:
    """Interface simplifiée pour la génération de quiz"""

    default_profile = StudentProfile(
        id=student_id,
        name="Étudiant",
        level="terminale",
        specialties=[subject.lower()],
        learning_style="mixed",
        strengths=["raisonnement"],
        weaknesses=["rapidité"],
        goals=["progresser", "réussir"]
    )

    return await openai_service.generate_quiz(subject, topic, difficulty, num_questions, default_profile)

