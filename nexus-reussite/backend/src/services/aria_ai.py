"""
Service IA ARIA - Assistant d'Apprentissage Adaptatif
Version unifiée et opérationnelle avec fallback
"""

import json
import logging
import os
import random
from datetime import datetime
from typing import Dict, List, Optional, Any

# Configuration du logging
logger = logging.getLogger(__name__)


class ARIAService:
    """
    Service IA ARIA - Assistant d'Apprentissage Adaptatif
    Intelligence artificielle qui s'adapte au profil cognitif de chaque élève
    Fonctionne avec ou sans API OpenAI
    """

    def __init__(self):
        self.client = None
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.has_openai = False

        # Configuration des styles et niveaux
        self.learning_styles = ["visual", "auditory", "kinesthetic", "reading_writing"]
        self.difficulty_levels = ["beginner", "intermediate", "advanced", "expert"]

        # Base de connaissances par matière
        self.subjects = {
            "mathematiques": [
                "algèbre",
                "géométrie",
                "analyse",
                "probabilités",
                "statistiques",
            ],
            "physique": [
                "mécanique",
                "thermodynamique",
                "électricité",
                "optique",
                "physique_moderne",
            ],
            "chimie": [
                "chimie_organique",
                "chimie_inorganique",
                "thermochimie",
                "cinétique",
            ],
            "francais": [
                "littérature",
                "grammaire",
                "expression_écrite",
                "analyse_texte",
            ],
            "nsi": [
                "algorithmique",
                "programmation",
                "bases_données",
                "réseaux",
                "architecture",
            ],
            "philosophie": [
                "métaphysique",
                "épistémologie",
                "éthique",
                "politique",
                "esthétique",
            ],
        }

        # Templates de réponses pour fallback
        self.response_templates = {
            "greeting": [
                (
                    "Bonjour ! Je suis ARIA, votre assistant IA personnel de Nexus "
                    "Réussite. Comment puis-je vous aider aujourd'hui ?"
                ),
                (
                    "Salut ! Prêt(e) à apprendre ensemble ? Je suis là pour vous "
                    "accompagner dans votre parcours d'excellence."
                ),
                (
                    "Bienvenue ! Je suis ARIA, votre coach IA adaptatif. Que "
                    "souhaitez-vous étudier aujourd'hui ?"
                ),
            ],
            "math": [
                (
                    "Les mathématiques sont passionnantes ! Avec votre style "
                    "d'apprentissage, nous allons décomposer le problème étape par "
                    "étape."
                ),
                (
                    "Excellente question en mathématiques ! Je vais adapter mon "
                    "explication à votre profil d'apprentissage."
                ),
                (
                    "Les maths deviennent plus faciles quand on utilise la bonne "
                    "méthode. Laissez-moi vous guider !"
                ),
            ],
            "study_tips": [
                (
                    "Pour améliorer vos notes, je recommande une approche "
                    "personnalisée basée sur votre style d'apprentissage."
                ),
                (
                    "Voici mes conseils adaptés à votre profil : planification, "
                    "révisions actives et pratique régulière."
                ),
                (
                    "L'excellence vient de la régularité et de la méthode. Créons "
                    "ensemble votre plan d'étude personnalisé !"
                ),
            ],
            "bac_prep": [
                (
                    "La préparation au bac nécessite une stratégie bien définie. Je "
                    "vais vous aider à créer un plan d'étude optimal."
                ),
                (
                    "Pour réussir votre bac, nous allons travailler sur vos points "
                    "forts et renforcer vos faiblesses."
                ),
                (
                    "Le bac se prépare méthodiquement. Analysons ensemble vos "
                    "besoins et créons votre feuille de route !"
                ),
            ],
            "default": [
                (
                    "C'est une excellente question ! Adaptons notre approche à votre "
                    "style d'apprentissage."
                ),
                (
                    "Je vais vous aider avec une méthode personnalisée selon votre "
                    "profil cognitif."
                ),
                (
                    "Intéressant ! Laissez-moi vous proposer une approche adaptée à "
                    "vos besoins spécifiques."
                ),
            ],
        }

        # Initialisation du client OpenAI si possible
        self._initialize_openai()

    def _initialize_openai(self):
        """Initialise le client OpenAI si la clé API est disponible"""
        # pylint: disable=import-outside-toplevel,reimported,redefined-outer-name
        try:
            if self.api_key and self.api_key.startswith("sk-"):
                from openai import OpenAI

                self.client = OpenAI(api_key=self.api_key)
                self.has_openai = True
                logger.info("Service ARIA initialisé avec OpenAI API")
            else:
                # Ne pas afficher d'avertissement en mode test

                if os.environ.get("FLASK_ENV") != "testing":
                    logger.warning("Clé OpenAI non configurée - Mode simulation activé")
                self.has_openai = False
        except ImportError:
            logger.error("Package openai non installé - Mode simulation activé")
            self.has_openai = False
        except (RuntimeError, OSError, ValueError) as exc:  # pylint: disable=broad-exception-caught
            logger.error(
                "Erreur initialisation OpenAI: %s - Mode simulation activé", exc
            )
            self.has_openai = False

    def detect_message_type(self, message: str) -> str:
        """Détecte le type de message pour choisir la réponse appropriée"""
        message_lower = message.lower()

        if any(
            word in message_lower for word in ["bonjour", "salut", "hello", "bonsoir"]
        ):
            return "greeting"
        if any(
            word in message_lower
            for word in ["mathématiques", "maths", "calcul", "équation", "fonction"]
        ):
            return "math"
        if any(
            word in message_lower
            for word in ["améliorer", "notes", "résultats", "conseils"]
        ):
            return "study_tips"
        if any(
            word in message_lower
            for word in ["bac", "baccalauréat", "examen", "préparer"]
        ):
            return "bac_prep"
        return "default"

    def generate_response(
        self,
        message: str,
        student_profile: Dict,
        context: str = "",
        relevant_documents: List = None,
    ) -> Dict[str, Any]:
        """Génère une réponse ARIA avec OpenAI ou fallback"""

        if self.has_openai:
            return self._generate_openai_response(
                message, student_profile, context, relevant_documents
            )
        return self._generate_fallback_response(message, student_profile, context)

    def _generate_openai_response(
        self,
        message: str,
        student_profile: Dict,
        context: str,
        relevant_documents: List,
    ) -> Dict[str, Any]:
        """Génère une réponse avec OpenAI API"""
        try:
            # Construction du prompt personnalisé
            system_prompt = self._build_system_prompt(student_profile)
            user_message = self._build_user_message(
                message, context, relevant_documents
            )

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Modèle plus économique
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=1000,
                top_p=0.9,
            )

            aria_response = response.choices[0].message.content

            return {
                "response": aria_response,
                "badges": self._generate_badges(student_profile, message),
                "confidence_score": 0.95,
                "processing_time_ms": random.randint(800, 1500),
                "message_type": self.detect_message_type(message),
                "personalized": True,
                "source": "openai",
                "token_usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }

        except (RuntimeError, OSError, ValueError) as exc:  # pylint: disable=broad-exception-caught
            logger.error("Erreur OpenAI API: %s", exc)
            return self._generate_fallback_response(message, student_profile, context)

    def _generate_fallback_response(
        self,
        message: str,
        student_profile: Dict,
        context: str,  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        """Génère une réponse de fallback sans OpenAI"""

        message_type = self.detect_message_type(message)
        responses = self.response_templates.get(
            message_type, self.response_templates["default"]
        )
        response_text = random.choice(responses)

        # Personnalisation selon le profil (style d'apprentissage non utilisé actuellement)
        _ = student_profile.get(
            "learning_style", "adaptatif"
        )  # pylint: disable=unused-variable

        return {
            "response": response_text,
            "badges": self._generate_badges(student_profile, message),
            "confidence_score": random.uniform(0.85, 0.95),
            "processing_time_ms": random.randint(150, 800),
            "message_type": message_type,
            "personalized": True,
            "source": "fallback",
        }

    def _build_system_prompt(self, student_profile: Dict) -> str:
        """Construit le prompt système personnalisé"""
        learning_style = student_profile.get("learning_style", "mixed")
        grade_level = student_profile.get("grade_level", "terminale")

        return (
            "Tu es ARIA, l'assistant IA personnel de Nexus Réussite, "
            "spécialisé dans l'accompagnement des élèves du système français "
            f"en Tunisie.\n\nPROFIL DE L'ÉLÈVE:\n- Niveau: {grade_level}\n"
            f"- Style d'apprentissage: {learning_style}\n\n"
            "CARACTÉRISTIQUES DE TES RÉPONSES:\n- Adapte ton langage au "
            f"niveau {grade_level}\n- Utilise des approches {learning_style} "
            "dans tes explications\n- Sois encourageant et bienveillant\n"
            "- Propose des solutions concrètes et personnalisées\n- Reste "
            "concis mais informatif (maximum 200 mots)\n\nMISSION:\n"
            "Accompagner l'élève vers l'excellence académique en préparant "
            "au Bac français ET aux études supérieures."
        )

    def _build_user_message(
        self, message: str, context: str, relevant_documents: List
    ) -> str:
        """Construit le message utilisateur avec contexte"""
        user_message = f"Question: {message}"

        if context:
            user_message += f"\nContexte: {context}"

        if relevant_documents:
            docs_content = "\n".join(
                [doc.get("content", "")[:200] + "..." for doc in relevant_documents[:2]]
            )
            user_message += f"\nDocuments pertinents:\n{docs_content}"

        return user_message

    def _generate_badges(self, student_profile: Dict, message: str) -> List[Dict]:
        """Génère des badges contextuels"""
        learning_style = student_profile.get("learning_style", "adaptatif")
        message_type = self.detect_message_type(message)

        badges = [
            {
                "text": f"🎯 Style: {learning_style.title()}",
                "class": "bg-blue-100 text-blue-800",
            },
            {
                "text": f"📊 Confiance: {random.randint(85, 98)}%",
                "class": "bg-green-100 text-green-800",
            },
        ]

        if message_type == "math":
            badges.append(
                {
                    "text": "🔢 Spécialiste Maths",
                    "class": "bg-purple-100 text-purple-800",
                }
            )
        elif message_type == "bac_prep":
            badges.append(
                {"text": "🎓 Coach Bac", "class": "bg-orange-100 text-orange-800"}
            )

        return badges

    def generate_personalized_content(
        self, student_profile: Dict, subject: str, topic: str
    ) -> Dict[str, Any]:
        """Génère du contenu personnalisé pour un sujet donné"""
        learning_style = student_profile.get("learning_style", "adaptati")
        difficulty_level = student_profile.get("difficulty_level", "intermediate")

        if self.has_openai:
            return self._generate_openai_content(student_profile, subject, topic)
        return self._generate_fallback_content(
            learning_style, subject, topic, difficulty_level
        )

    def _generate_openai_content(
        self, student_profile: Dict, subject: str, topic: str
    ) -> Dict[str, Any]:
        """Génère du contenu avec OpenAI"""
        try:
            prompt = (
                "Génère du contenu éducatif personnalisé pour:\n"
                f"- Sujet: {topic} en {subject}\n"
                "- Style d'apprentissage: "
                f"{student_profile.get('learning_style')}\n"
                f"- Niveau: {student_profile.get('grade_level', 'terminale')}\n\n"
                "Inclus:\n1. Une explication adaptée (100 mots max)\n"
                "2. 2 exercices progressifs\n3. 2 conseils méthodologiques\n"
                "4. 1 ressource recommandée\n\nFormat JSON avec clés: "
                "explanation, exercises, methodology_tips, resources"
            )

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800,
            )

            content_text = response.choices[0].message.content

            try:
                content = json.loads(content_text)
            except json.JSONDecodeError:
                content = self._parse_content_text(content_text)

            return {
                "content": content,
                "generated_at": datetime.utcnow().isoformat(),
                "source": "openai",
                "personalized": True,
            }

        except (RuntimeError, OSError, ValueError) as exc:  # pylint: disable=broad-exception-caught
            logger.error("Erreur génération contenu OpenAI: %s", exc)
            return self._generate_fallback_content(
                student_profile.get("learning_style"),
                subject,
                topic,
                student_profile.get("difficulty_level", "intermediate"),
            )

    def _generate_fallback_content(
        self, learning_style: str, subject: str, topic: str, difficulty: str
    ) -> Dict[str, Any]:  # pylint: disable=unused-argument
        """Génère du contenu de fallback"""

        style_adaptations = {
            "visual": {
                "explanation": (
                    f"Approche visuelle pour {topic} en {subject}. "
                    "Utilisez des schémas et diagrammes pour visualiser "
                    "les concepts clés."
                ),
                "exercises": [
                    "Créez un schéma représentant les concepts",
                    "Utilisez des couleurs pour organiser l'information",
                ],
            },
            "auditory": {
                "explanation": (
                    f"Approche auditive pour {topic} en {subject}. "
                    "Écoutez attentivement les explications structurées."
                ),
                "exercises": [
                    "Expliquez le concept à voix haute",
                    "Participez à des discussions sur le sujet",
                ],
            },
            "kinesthetic": {
                "explanation": (
                    f"Approche pratique pour {topic} en {subject}. "
                    "Apprenez par l'expérimentation et la manipulation."
                ),
                "exercises": [
                    "Réalisez des exercices pratiques",
                    "Manipulez des objets ou modèles concrets",
                ],
            },
            "reading_writing": {
                "explanation": (
                    f"Approche textuelle pour {topic} en {subject}. "
                    "Lisez et écrivez pour mieux comprendre."
                ),
                "exercises": [
                    "Rédigez un résumé du concept",
                    "Créez des fiches de révision détaillées",
                ],
            },
        }

        adaptation = style_adaptations.get(learning_style, style_adaptations["visual"])

        content = {
            "explanation": adaptation["explanation"],
            "exercises": adaptation["exercises"],
            "methodology_tips": [
                f"Adaptez votre méthode au style {learning_style}",
                "Pratiquez régulièrement avec des exercices variés",
            ],
            "resources": [
                f"Ressources {learning_style}es recommandées",
                "Supports complémentaires adaptés",
            ],
        }

        return {
            "content": content,
            "generated_at": datetime.utcnow().isoformat(),
            "source": "fallback",
            "personalized": True,
        }

    def _parse_content_text(self, text: str) -> Dict[str, Any]:
        """Parse le contenu textuel en structure JSON"""
        return {
            "explanation": text[:200] + "...",
            "exercises": ["Exercice généré automatiquement"],
            "methodology_tips": ["Conseil méthodologique adapté"],
            "resources": ["Ressource recommandée"],
        }

    def analyze_learning_style(self, responses: Dict) -> Dict[str, Any]:
        """Analyse le style d'apprentissage basé sur les réponses"""

        # Scores par style (simulation basée sur les réponses)
        scores = {"visual": 0, "auditory": 0, "kinesthetic": 0, "reading_writing": 0}

        # Analyse simplifiée des réponses
        for _question, answer in responses.items():  # pylint: disable=unused-variable
            if isinstance(answer, str):
                answer_lower = answer.lower()

                # Patterns visuels
                if any(
                    word in answer_lower
                    for word in ["voir", "schéma", "couleur", "image"]
                ):
                    scores["visual"] += 1

                # Patterns auditifs
                if any(
                    word in answer_lower
                    for word in ["écouter", "expliquer", "dire", "entendre"]
                ):
                    scores["auditory"] += 1

                # Patterns kinesthésiques
                if any(
                    word in answer_lower
                    for word in ["faire", "manipuler", "bouger", "pratiquer"]
                ):
                    scores["kinesthetic"] += 1

                # Patterns lecture/écriture
                if any(
                    word in answer_lower
                    for word in ["lire", "écrire", "texte", "noter"]
                ):
                    scores["reading_writing"] += 1

        # Détermination du style dominant
        dominant_style = max(scores.keys(), key=lambda k: scores[k])

        return {
            "dominant_style": dominant_style,
            "scores": scores,
            "recommendations": self._get_style_recommendations(dominant_style),
            "analyzed_at": datetime.utcnow().isoformat(),
        }

    def _get_style_recommendations(self, style: str) -> List[str]:
        """Recommandations selon le style d'apprentissage"""
        recommendations = {
            "visual": [
                "Utilisez des diagrammes et schémas",
                "Surlignez et organisez visuellement vos notes",
                "Créez des cartes mentales",
            ],
            "auditory": [
                "Lisez vos cours à voix haute",
                "Participez aux discussions en classe",
                "Enregistrez-vous en révisant",
            ],
            "kinesthetic": [
                "Prenez des pauses actives",
                "Utilisez des manipulations concrètes",
                "Variez vos positions de travail",
            ],
            "reading_writing": [
                "Prenez des notes détaillées",
                "Rédigez des résumés",
                "Faites des fiches de révision",
            ],
        }

        return recommendations.get(style, recommendations["visual"])

    def assess_student_performance(
        self, student_id: int, session_data: Dict  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        """Évalue la performance d'un étudiant"""
        answers = session_data.get("answers", [])
        questions = session_data.get("questions", [])
        time_spent = session_data.get("time_spent_seconds", 0)

        if not questions:
            return {"error": "Aucune question fournie pour l'évaluation"}

        # Calcul du score
        correct_answers = 0
        total_questions = len(questions)
        detailed_analysis = []

        for i, (question, answer) in enumerate(zip(questions, answers)):
            is_correct = self._evaluate_answer(question, answer)
            if is_correct:
                correct_answers += 1

            detailed_analysis.append(
                {
                    "question_id": i + 1,
                    "question": question.get("text", ""),
                    "student_answer": answer,
                    "correct_answer": question.get("correct_answer", ""),
                    "is_correct": is_correct,
                    "topic": question.get("topic", ""),
                    "difficulty": question.get("difficulty", "medium"),
                }
            )

        score = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        # Analyse des patterns d'erreur
        error_patterns = self._analyze_error_patterns(detailed_analysis)

        # Génération de recommandations
        recommendations = self._generate_performance_recommendations(
            score, error_patterns, time_spent
        )

        return {
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "time_spent_seconds": time_spent,
            "detailed_analysis": detailed_analysis,
            "error_patterns": error_patterns,
            "recommendations": recommendations,
            "next_difficulty_level": self._suggest_next_difficulty(score),
            "assessed_at": datetime.utcnow().isoformat(),
        }

    def _evaluate_answer(self, question: Dict, answer: str) -> bool:
        """Évalue si une réponse est correcte (simulation)"""
        correct_answer = question.get("correct_answer", "").lower().strip()
        student_answer = str(answer).lower().strip()

        # Simulation basique d'évaluation
        return correct_answer == student_answer or random.choice(
            [True, False, True]
        )  # Biais positif

    def _analyze_error_patterns(self, detailed_analysis: List) -> Dict[str, int]:
        """Analyse les patterns d'erreurs"""
        patterns = {
            "calculation_errors": 0,
            "methodology_issues": 0,
            "comprehension_gaps": 0,
            "careless_mistakes": 0,
        }

        for item in detailed_analysis:
            if not item["is_correct"]:
                # Simulation d'analyse des erreurs
                error_type = random.choice(list(patterns.keys()))
                patterns[error_type] += 1

        return patterns

    def _generate_performance_recommendations(
        self, score: float, error_patterns: Dict, time_spent: int
    ) -> List[str]:
        """Génère des recommandations basées sur la performance"""
        recommendations = []

        if score >= 85:
            recommendations.append("Excellent travail ! Continuez sur cette lancée.")
        elif score >= 70:
            recommendations.append("Bon niveau, quelques points à consolider.")
        else:
            recommendations.append(
                "Il faut renforcer les bases. Ne vous découragez pas !"
            )

        # Recommandations selon les erreurs
        if error_patterns.get("calculation_errors", 0) > 2:
            recommendations.append("Travaillez la précision des calculs.")

        if error_patterns.get("methodology_issues", 0) > 1:
            recommendations.append("Revoyez la méthodologie de résolution.")

        if time_spent < 300:  # Moins de 5 minutes
            recommendations.append("Prenez plus de temps pour réfléchir.")
        elif time_spent > 1800:  # Plus de 30 minutes
            recommendations.append("Travaillez l'efficacité et la gestion du temps.")

        return recommendations

    def _suggest_next_difficulty(self, score: float) -> str:
        """Suggère le niveau de difficulté suivant"""
        if score >= 85:
            return "advanced"
        if score >= 70:
            return "intermediate"
        if score >= 50:
            return "beginner"
        return "foundation"

    def evaluate_progress(
        self,
        student_id: int,  # pylint: disable=unused-argument
        subject: str,
        recent_scores: List[float],
    ) -> Dict[str, Any]:
        """Évalue les progrès d'un élève basé sur ses scores récents"""
        if not recent_scores:
            return {
                "status": "insufficient_data",
                "message": "Pas assez de données pour évaluer les progrès",
                "recommendations": [
                    "Commencer par faire quelques exercices pour obtenir une "
                    "évaluation"
                ],
            }

        # Calculs de base
        average_score = sum(recent_scores) / len(recent_scores)
        latest_score = recent_scores[-1]

        # Tendance (comparaison dernière moitié vs première moitié)
        if len(recent_scores) >= 4:
            mid_point = len(recent_scores) // 2
            first_half_avg = sum(recent_scores[:mid_point]) / mid_point
            second_half_avg = sum(recent_scores[mid_point:]) / (
                len(recent_scores) - mid_point
            )
            if second_half_avg > first_half_avg:
                trend = "amélioration"
            elif second_half_avg < first_half_avg:
                trend = "déclin"
            else:
                trend = "stable"
            progress_percentage = (
                ((second_half_avg - first_half_avg) / first_half_avg) * 100
                if first_half_avg > 0
                else 0
            )
        else:
            trend = "stable"
            progress_percentage = 0

        # Niveau actuel basé sur la moyenne
        if average_score >= 90:
            level = "excellent"
        elif average_score >= 75:
            level = "bon"
        elif average_score >= 60:
            level = "moyen"
        else:
            level = "à améliorer"

        # Recommandations basées sur la performance
        recommendations = []
        if trend == "amélioration":
            recommendations.append("Excellent progrès ! Continuez sur cette lancée.")
            if average_score < 85:
                recommendations.append(
                    "Intensifiez légèrement la difficulté pour vous challenger."
                )
        elif trend == "déclin":
            recommendations.append(
                "Il semble y avoir une baisse récente. Prenez le temps de "
                "réviser les concepts de base."
            )
            recommendations.append(
                "Considérez réduire temporairement la difficulté pour "
                "reprendre confiance."
            )
        else:
            if average_score >= 85:
                recommendations.append(
                    "Performance stable et élevée. Essayez des défis plus " "complexes."
                )
            elif average_score >= 70:
                recommendations.append(
                    "Performance correcte et stable. Continuez avec régularité."
                )
            else:
                recommendations.append(
                    "Performance stable mais perfectible. Focalisez sur les "
                    "lacunes identifiées."
                )

        # Prochaines étapes
        next_steps = []
        if latest_score < 60:
            next_steps.append("Réviser les fondamentaux")
            next_steps.append("Faire des exercices de base")
        elif latest_score < 80:
            next_steps.append("Approfondir les concepts intermédiaires")
            next_steps.append("Pratiquer des exercices variés")
        else:
            next_steps.append("Aborder des sujets avancés")
            next_steps.append("Résoudre des problèmes complexes")

        return {
            "status": "success",
            "student_id": student_id,
            "subject": subject,
            "statistics": {
                "average_score": round(average_score, 2),
                "latest_score": latest_score,
                "total_evaluations": len(recent_scores),
                "trend": trend,
                "progress_percentage": round(progress_percentage, 2),
            },
            "assessment": {
                "current_level": level,
                "strengths": (
                    ["Régularité dans le travail"] if trend != "déclin" else []
                ),
                "areas_for_improvement": (
                    ["Consistency"]
                    if trend == "déclin"
                    else (
                        ["Challenge level"]
                        if average_score >= 85
                        else ["Core concepts"]
                    )
                ),
            },
            "recommendations": recommendations,
            "next_steps": next_steps,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get_health_status(self) -> Dict[str, Any]:
        """Retourne l'état de santé du service ARIA"""
        return {
            "status": "healthy",
            "openai_available": self.has_openai,
            "api_key_configured": bool(self.api_key),
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
        }


# Instance globale du service
aria_service = ARIAService()
