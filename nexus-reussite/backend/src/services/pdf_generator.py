import io
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from reportlab.lib.colors import Color, black, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# Imports pour la génération PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DocumentMetadata:
    """Métadonnées du document"""

    title: str
    subject: str
    author: str = "ARIA - Nexus Réussite"
    creator: str = "Nexus Réussite Platform"
    student_name: str = ""
    student_level: str = ""
    generated_at: str = ""
    document_type: str = ""
    topic: str = ""

    def __post_init__(self):
        if not self.generated_at:
            self.generated_at = datetime.now().strftime("%d/%m/%Y à %H:%M")


class NexusPDFGenerator:
    """Générateur PDF personnalisé pour Nexus Réussite"""

    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 2 * cm
        self.content_width = self.page_width - 2 * self.margin

        # Couleurs de la charte graphique Nexus
        self.colors = {
            "primary": Color(0.059, 0.090, 0.165, 1),  # #0F172A (Bleu nuit)
            "secondary": Color(0.902, 0.224, 0.275, 1),  # #E63946 (Rouge énergie)
            "accent": Color(0.118, 0.161, 0.235, 1),  # #1E293B (Bleu foncé)
            "light_gray": Color(0.941, 0.953, 0.965, 1),  # #F1F5F9
            "medium_gray": Color(0.475, 0.549, 0.635, 1),  # #798DA3
            "success": Color(0.133, 0.545, 0.133, 1),  # #228B22
            "warning": Color(1.0, 0.647, 0.0, 1),  # #FFA500
            "error": Color(0.863, 0.078, 0.235, 1),  # #DC143C
        }

        # Styles personnalisés
        self.styles = self._create_custom_styles()

    def _create_custom_styles(self):
        """Crée les styles personnalisés pour Nexus Réussite"""
        styles = getSampleStyleSheet()

        # Style pour le titre principal
        styles.add(
            ParagraphStyle(
                name="NexusTitle",
                parent=styles["Title"],
                fontSize=24,
                textColor=self.colors["primary"],
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            )
        )

        # Style pour les sous-titres
        styles.add(
            ParagraphStyle(
                name="NexusSubtitle",
                parent=styles["Heading1"],
                fontSize=18,
                textColor=self.colors["secondary"],
                spaceAfter=15,
                spaceBefore=20,
                fontName="Helvetica-Bold",
            )
        )

        # Style pour les sections
        styles.add(
            ParagraphStyle(
                name="NexusSection",
                parent=styles["Heading2"],
                fontSize=14,
                textColor=self.colors["primary"],
                spaceAfter=10,
                spaceBefore=15,
                fontName="Helvetica-Bold",
            )
        )

        # Style pour le texte normal
        styles.add(
            ParagraphStyle(
                name="NexusNormal",
                parent=styles["Normal"],
                fontSize=11,
                textColor=black,
                spaceAfter=8,
                alignment=TA_JUSTIFY,
                fontName="Helvetica",
            )
        )

        # Style pour les définitions
        styles.add(
            ParagraphStyle(
                name="NexusDefinition",
                parent=styles["Normal"],
                fontSize=11,
                textColor=self.colors["primary"],
                spaceAfter=8,
                leftIndent=20,
                fontName="Helvetica-Oblique",
                backColor=self.colors["light_gray"],
            )
        )

        # Style pour les formules
        styles.add(
            ParagraphStyle(
                name="NexusFormula",
                parent=styles["Normal"],
                fontSize=12,
                textColor=self.colors["accent"],
                spaceAfter=10,
                spaceBefore=10,
                alignment=TA_CENTER,
                fontName="Courier-Bold",
                backColor=self.colors["light_gray"],
            )
        )

        # Style pour les exemples
        styles.add(
            ParagraphStyle(
                name="NexusExample",
                parent=styles["Normal"],
                fontSize=10,
                textColor=self.colors["medium_gray"],
                spaceAfter=8,
                leftIndent=15,
                fontName="Helvetica",
                borderColor=self.colors["secondary"],
                borderWidth=1,
                borderPadding=5,
            )
        )

        # Style pour les conseils
        styles.add(
            ParagraphStyle(
                name="NexusTip",
                parent=styles["Normal"],
                fontSize=10,
                textColor=self.colors["success"],
                spaceAfter=8,
                leftIndent=15,
                fontName="Helvetica-Bold",
                backColor=Color(0.9, 1.0, 0.9, 1),
            )
        )

        # Style pour les avertissements
        styles.add(
            ParagraphStyle(
                name="NexusWarning",
                parent=styles["Normal"],
                fontSize=10,
                textColor=self.colors["warning"],
                spaceAfter=8,
                leftIndent=15,
                fontName="Helvetica-Bold",
                backColor=Color(1.0, 0.98, 0.9, 1),
            )
        )

        # Style pour le footer
        styles.add(
            ParagraphStyle(
                name="NexusFooter",
                parent=styles["Normal"],
                fontSize=8,
                textColor=self.colors["medium_gray"],
                alignment=TA_CENTER,
                fontName="Helvetica",
            )
        )

        return styles

    def _draw_header(self, canvas, doc, metadata: DocumentMetadata):
        """Dessine l'en-tête personnalisé Nexus Réussite"""
        canvas.saveState()

        # Logo et titre Nexus (simplifié)
        canvas.setFillColor(self.colors["primary"])
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(self.margin, self.page_height - self.margin, "NEXUS")

        canvas.setFillColor(self.colors["secondary"])
        canvas.setFont("Helvetica", 12)
        canvas.drawString(self.margin + 60, self.page_height - self.margin, "Réussite")

        # Ligne de séparation
        canvas.setStrokeColor(self.colors["secondary"])
        canvas.setLineWidth(2)
        canvas.line(
            self.margin,
            self.page_height - self.margin - 20,
            self.page_width - self.margin,
            self.page_height - self.margin - 20,
        )

        # Informations du document
        canvas.setFillColor(self.colors["medium_gray"])
        canvas.setFont("Helvetica", 9)

        info_y = self.page_height - self.margin - 35
        canvas.drawString(self.margin, info_y, f"Document: {metadata.document_type}")
        canvas.drawString(self.margin, info_y - 12, f"Matière: {metadata.subject}")
        if metadata.topic:
            canvas.drawString(self.margin, info_y - 24, f"Sujet: {metadata.topic}")

        # Informations étudiant (côté droit)
        if metadata.student_name:
            canvas.drawRightString(
                self.page_width - self.margin, info_y, f"Élève: {metadata.student_name}"
            )
        if metadata.student_level:
            canvas.drawRightString(
                self.page_width - self.margin,
                info_y - 12,
                f"Niveau: {metadata.student_level}",
            )
        canvas.drawRightString(
            self.page_width - self.margin,
            info_y - 24,
            f"Généré le: {metadata.generated_at}",
        )

        canvas.restoreState()

    def _draw_footer(self, canvas, doc):
        """Dessine le pied de page"""
        canvas.saveState()

        # Ligne de séparation
        canvas.setStrokeColor(self.colors["light_gray"])
        canvas.setLineWidth(1)
        canvas.line(
            self.margin,
            self.margin + 30,
            self.page_width - self.margin,
            self.margin + 30,
        )

        # Texte du footer
        canvas.setFillColor(self.colors["medium_gray"])
        canvas.setFont("Helvetica", 8)

        footer_text = (
            "Nexus Réussite - Centre Urbain Nord, Immeuble VENUS, Apt. C13, 1082 Tunis"
        )
        canvas.drawCentredText(self.page_width / 2, self.margin + 15, footer_text)

        # Numéro de page
        canvas.drawRightString(
            self.page_width - self.margin, self.margin + 15, f"Page {doc.page}"
        )

        canvas.restoreState()

    def generate_revision_sheet(
        self,
        content: Dict[str, Any],
        metadata: DocumentMetadata,
        output_path: Optional[str] = None,
    ) -> bytes:
        """Génère une fiche de révision personnalisée"""

        # Création du buffer ou fichier
        if output_path:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin + 60,
                bottomMargin=self.margin + 40,
            )
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin + 60,
                bottomMargin=self.margin + 40,
            )

        # Construction du contenu
        story = []

        # Titre principal
        story.append(
            Paragraph(content.get("title", metadata.title), self.styles["NexusTitle"])
        )
        story.append(Spacer(1, 20))

        # Objectifs d'apprentissage
        if "objectives" in content:
            story.append(
                Paragraph("🎯 Objectifs d'apprentissage", self.styles["NexusSubtitle"])
            )
            for objective in content["objectives"]:
                story.append(Paragraph(f"• {objective}", self.styles["NexusNormal"]))
            story.append(Spacer(1, 15))

        # Prérequis
        if "prerequisites" in content:
            story.append(Paragraph("📚 Prérequis", self.styles["NexusSection"]))
            for prereq in content["prerequisites"]:
                story.append(Paragraph(f"• {prereq}", self.styles["NexusNormal"]))
            story.append(Spacer(1, 15))

        # Définitions clés
        if "definitions" in content:
            story.append(Paragraph("📖 Définitions clés", self.styles["NexusSection"]))
            for term, definition in content["definitions"].items():
                story.append(
                    Paragraph(
                        f"<b>{term}:</b> {definition}", self.styles["NexusDefinition"]
                    )
                )
            story.append(Spacer(1, 15))

        # Formules importantes
        if "formulas" in content:
            story.append(
                Paragraph("🧮 Formules importantes", self.styles["NexusSection"])
            )
            for formula in content["formulas"]:
                story.append(Paragraph(formula, self.styles["NexusFormula"]))
            story.append(Spacer(1, 15))

        # Méthodes et techniques
        if "methods" in content:
            story.append(
                Paragraph("⚙️ Méthodes et techniques", self.styles["NexusSection"])
            )
            for i, method in enumerate(content["methods"], 1):
                story.append(
                    Paragraph(
                        f"<b>Méthode {i}:</b> {method}", self.styles["NexusNormal"]
                    )
                )
            story.append(Spacer(1, 15))

        # Exemples types
        if "examples" in content:
            story.append(Paragraph("💡 Exemples types", self.styles["NexusSection"]))
            for i, example in enumerate(content["examples"], 1):
                story.append(
                    Paragraph(f"<b>Exemple {i}:</b>", self.styles["NexusNormal"])
                )
                story.append(Paragraph(example, self.styles["NexusExample"]))
            story.append(Spacer(1, 15))

        # Conseils et astuces
        if "tips" in content:
            story.append(
                Paragraph("💡 Conseils et astuces", self.styles["NexusSection"])
            )
            for tip in content["tips"]:
                story.append(Paragraph(f"💡 {tip}", self.styles["NexusTip"]))
            story.append(Spacer(1, 15))

        # Points d'attention
        if "warnings" in content:
            story.append(Paragraph("⚠️ Points d'attention", self.styles["NexusSection"]))
            for warning in content["warnings"]:
                story.append(Paragraph(f"⚠️ {warning}", self.styles["NexusWarning"]))
            story.append(Spacer(1, 15))

        # Exercices d'application
        if "exercises" in content:
            story.append(
                Paragraph("📝 Exercices d'application", self.styles["NexusSection"])
            )
            for i, exercise in enumerate(content["exercises"], 1):
                story.append(
                    Paragraph(
                        f"<b>Exercice {i}:</b> {exercise}", self.styles["NexusNormal"]
                    )
                )
            story.append(Spacer(1, 15))

        # Points clés à retenir
        if "key_points" in content:
            story.append(
                Paragraph("🔑 Points clés à retenir", self.styles["NexusSection"])
            )

            # Création d'un tableau pour les points clés
            key_points_data = []
            for point in content["key_points"]:
                key_points_data.append(["✓", point])

            if key_points_data:
                key_table = Table(
                    key_points_data, colWidths=[0.5 * cm, self.content_width - 0.5 * cm]
                )
                key_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, -1), self.colors["light_gray"]),
                            ("TEXTCOLOR", (0, 0), (0, -1), self.colors["success"]),
                            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, -1), 10),
                            ("ALIGN", (0, 0), (0, -1), "CENTER"),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 5),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                            ("TOPPADDING", (0, 0), (-1, -1), 5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ]
                    )
                )
                story.append(key_table)
                story.append(Spacer(1, 15))

        # Pour aller plus loin
        if "further_reading" in content:
            story.append(
                Paragraph("📚 Pour aller plus loin", self.styles["NexusSection"])
            )
            for resource in content["further_reading"]:
                story.append(Paragraph(f"• {resource}", self.styles["NexusNormal"]))

        # Construction du PDF avec en-tête et pied de page personnalisés
        def add_page_decorations(canvas, doc):
            self._draw_header(canvas, doc, metadata)
            self._draw_footer(canvas, doc)

        doc.build(
            story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations
        )

        if output_path:
            return output_path
        else:
            buffer.seek(0)
            return buffer.getvalue()

    def generate_exercise_sheet(
        self,
        content: Dict[str, Any],
        metadata: DocumentMetadata,
        output_path: Optional[str] = None,
    ) -> bytes:
        """Génère une feuille d'exercices personnalisée"""

        # Création du buffer ou fichier
        if output_path:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin + 60,
                bottomMargin=self.margin + 40,
            )
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin + 60,
                bottomMargin=self.margin + 40,
            )

        story = []

        # Titre principal
        story.append(
            Paragraph(content.get("title", metadata.title), self.styles["NexusTitle"])
        )
        story.append(Spacer(1, 20))

        # Instructions générales
        if "instructions" in content:
            story.append(Paragraph("📋 Instructions", self.styles["NexusSection"]))
            story.append(Paragraph(content["instructions"], self.styles["NexusNormal"]))
            story.append(Spacer(1, 15))

        # Durée et barème
        info_data = []
        if "duration" in content:
            info_data.append(["⏱️ Durée:", content["duration"]])
        if "total_points" in content:
            info_data.append(["📊 Total:", f"{content['total_points']} points"])

        if info_data:
            info_table = Table(info_data, colWidths=[3 * cm, 5 * cm])
            info_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), self.colors["light_gray"]),
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            story.append(info_table)
            story.append(Spacer(1, 20))

        # Exercices
        if "exercises" in content:
            for i, exercise in enumerate(content["exercises"], 1):
                # Titre de l'exercice
                exercise_title = f"Exercice {i}"
                if "points" in exercise:
                    exercise_title += f" ({exercise['points']} points)"
                if "difficulty" in exercise:
                    difficulty_emoji = {
                        "easy": "⭐",
                        "medium": "⭐⭐",
                        "hard": "⭐⭐⭐",
                    }
                    exercise_title += (
                        f" {difficulty_emoji.get(exercise['difficulty'], '')}"
                    )

                story.append(Paragraph(exercise_title, self.styles["NexusSubtitle"]))

                # Énoncé
                if "statement" in exercise:
                    story.append(
                        Paragraph(exercise["statement"], self.styles["NexusNormal"])
                    )

                # Questions
                if "questions" in exercise:
                    for j, question in enumerate(exercise["questions"], 1):
                        question_text = f"<b>{j}.</b> {question}"
                        story.append(
                            Paragraph(question_text, self.styles["NexusNormal"])
                        )

                        # Espace pour la réponse
                        story.append(Spacer(1, 30))

                # Conseils spécifiques
                if "hints" in exercise:
                    story.append(Paragraph("💡 Conseils:", self.styles["NexusSection"]))
                    for hint in exercise["hints"]:
                        story.append(Paragraph(f"• {hint}", self.styles["NexusTip"]))

                story.append(Spacer(1, 20))

        # Construction du PDF
        def add_page_decorations(canvas, doc):
            self._draw_header(canvas, doc, metadata)
            self._draw_footer(canvas, doc)

        doc.build(
            story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations
        )

        if output_path:
            return output_path
        else:
            buffer.seek(0)
            return buffer.getvalue()

    def generate_evaluation_report(
        self,
        content: Dict[str, Any],
        metadata: DocumentMetadata,
        output_path: Optional[str] = None,
    ) -> bytes:
        """Génère un rapport d'évaluation personnalisé"""

        # Création du buffer ou fichier
        if output_path:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin + 60,
                bottomMargin=self.margin + 40,
            )
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin + 60,
                bottomMargin=self.margin + 40,
            )

        story = []

        # Titre principal
        story.append(
            Paragraph(
                content.get("title", "Rapport d'évaluation"), self.styles["NexusTitle"]
            )
        )
        story.append(Spacer(1, 20))

        # Résumé exécutif
        if "summary" in content:
            story.append(Paragraph("📊 Résumé exécuti", self.styles["NexusSubtitle"]))
            story.append(Paragraph(content["summary"], self.styles["NexusNormal"]))
            story.append(Spacer(1, 15))

        # Résultats globaux
        if "overall_results" in content:
            results = content["overall_results"]

            # Tableau des résultats
            results_data = [["Critère", "Score", "Commentaire"]]

            for criterion, data in results.items():
                score = data.get("score", "N/A")
                comment = data.get("comment", "")
                results_data.append([criterion, str(score), comment])

            results_table = Table(results_data, colWidths=[4 * cm, 2 * cm, 8 * cm])
            results_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), self.colors["primary"]),
                        ("TEXTCOLOR", (0, 0), (-1, 0), white),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("ALIGN", (1, 1), (1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("GRID", (0, 0), (-1, -1), 1, black),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )

            story.append(results_table)
            story.append(Spacer(1, 20))

        # Points forts
        if "strengths" in content:
            story.append(Paragraph("✅ Points forts", self.styles["NexusSection"]))
            for strength in content["strengths"]:
                story.append(Paragraph(f"• {strength}", self.styles["NexusTip"]))
            story.append(Spacer(1, 15))

        # Axes d'amélioration
        if "improvements" in content:
            story.append(
                Paragraph("📈 Axes d'amélioration", self.styles["NexusSection"])
            )
            for improvement in content["improvements"]:
                story.append(Paragraph(f"• {improvement}", self.styles["NexusWarning"]))
            story.append(Spacer(1, 15))

        # Recommandations
        if "recommendations" in content:
            story.append(Paragraph("🎯 Recommandations", self.styles["NexusSection"]))
            for i, recommendation in enumerate(content["recommendations"], 1):
                story.append(
                    Paragraph(
                        f"<b>{i}.</b> {recommendation}", self.styles["NexusNormal"]
                    )
                )
            story.append(Spacer(1, 15))

        # Plan d'action
        if "action_plan" in content:
            story.append(Paragraph("📋 Plan d'action", self.styles["NexusSection"]))

            action_data = [["Action", "Priorité", "Échéance"]]
            for action in content["action_plan"]:
                action_data.append(
                    [
                        action.get("description", ""),
                        action.get("priority", ""),
                        action.get("deadline", ""),
                    ]
                )

            action_table = Table(action_data, colWidths=[8 * cm, 3 * cm, 3 * cm])
            action_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), self.colors["secondary"]),
                        ("TEXTCOLOR", (0, 0), (-1, 0), white),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("ALIGN", (1, 1), (2, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("GRID", (0, 0), (-1, -1), 1, black),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )

            story.append(action_table)

        # Construction du PDF
        def add_page_decorations(canvas, doc):
            self._draw_header(canvas, doc, metadata)
            self._draw_footer(canvas, doc)

        doc.build(
            story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations
        )

        if output_path:
            return output_path
        else:
            buffer.seek(0)
            return buffer.getvalue()

    def generate_progress_report(
        self,
        student_data: Dict[str, Any],
        metadata: DocumentMetadata,
        output_path: Optional[str] = None,
    ) -> bytes:
        """Génère un rapport de progression pour les parents"""

        # Création du buffer ou fichier
        if output_path:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin + 60,
                bottomMargin=self.margin + 40,
            )
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin + 60,
                bottomMargin=self.margin + 40,
            )

        story = []

        # Titre principal
        story.append(
            Paragraph(
                f"Rapport de progression - {metadata.student_name}",
                self.styles["NexusTitle"],
            )
        )
        story.append(Spacer(1, 20))

        # Période du rapport
        if "period" in student_data:
            story.append(
                Paragraph(
                    f"Période: {student_data['period']}", self.styles["NexusSection"]
                )
            )
            story.append(Spacer(1, 10))

        # Vue d'ensemble
        if "overview" in student_data:
            story.append(Paragraph("📊 Vue d'ensemble", self.styles["NexusSubtitle"]))
            story.append(
                Paragraph(student_data["overview"], self.styles["NexusNormal"])
            )
            story.append(Spacer(1, 15))

        # Progression par matière
        if "subjects_progress" in student_data:
            story.append(
                Paragraph("📚 Progression par matière", self.styles["NexusSubtitle"])
            )

            for subject, progress in student_data["subjects_progress"].items():
                story.append(
                    Paragraph(f"<b>{subject}</b>", self.styles["NexusSection"])
                )

                # Tableau de progression
                progress_data = [["Aspect", "Note", "Évolution", "Commentaire"]]

                for aspect, data in progress.items():
                    if isinstance(data, dict):
                        evolution = data.get("evolution", "")
                        if evolution == "up":
                            evolution = "📈"
                        elif evolution == "down":
                            evolution = "📉"
                        elif evolution == "stable":
                            evolution = "➡️"

                        progress_data.append(
                            [
                                aspect,
                                str(data.get("score", "N/A")),
                                evolution,
                                data.get("comment", ""),
                            ]
                        )

                if len(progress_data) > 1:
                    progress_table = Table(
                        progress_data, colWidths=[3 * cm, 2 * cm, 2 * cm, 7 * cm]
                    )
                    progress_table.setStyle(
                        TableStyle(
                            [
                                ("BACKGROUND", (0, 0), (-1, 0), self.colors["accent"]),
                                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                                ("FONTSIZE", (0, 0), (-1, -1), 9),
                                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                                ("ALIGN", (1, 1), (2, -1), "CENTER"),
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("GRID", (0, 0), (-1, -1), 1, black),
                                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                                ("TOPPADDING", (0, 0), (-1, -1), 3),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                            ]
                        )
                    )

                    story.append(progress_table)
                    story.append(Spacer(1, 10))

        # Objectifs atteints
        if "achieved_goals" in student_data:
            story.append(
                Paragraph("🎯 Objectifs atteints", self.styles["NexusSection"])
            )
            for goal in student_data["achieved_goals"]:
                story.append(Paragraph(f"✅ {goal}", self.styles["NexusTip"]))
            story.append(Spacer(1, 15))

        # Défis à relever
        if "challenges" in student_data:
            story.append(Paragraph("🚀 Défis à relever", self.styles["NexusSection"]))
            for challenge in student_data["challenges"]:
                story.append(Paragraph(f"🎯 {challenge}", self.styles["NexusWarning"]))
            story.append(Spacer(1, 15))

        # Recommandations pour les parents
        if "parent_recommendations" in student_data:
            story.append(
                Paragraph(
                    "👨‍👩‍👧‍👦 Recommandations pour les parents",
                    self.styles["NexusSection"],
                )
            )
            for recommendation in student_data["parent_recommendations"]:
                story.append(
                    Paragraph(f"• {recommendation}", self.styles["NexusNormal"])
                )
            story.append(Spacer(1, 15))

        # Prochaines étapes
        if "next_steps" in student_data:
            story.append(Paragraph("➡️ Prochaines étapes", self.styles["NexusSection"]))
            for step in student_data["next_steps"]:
                story.append(Paragraph(f"• {step}", self.styles["NexusNormal"]))

        # Construction du PDF
        def add_page_decorations(canvas, doc):
            self._draw_header(canvas, doc, metadata)
            self._draw_footer(canvas, doc)

        doc.build(
            story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations
        )

        if output_path:
            return output_path
        else:
            buffer.seek(0)
            return buffer.getvalue()


# Instance globale du générateur PDF
pdf_generator = NexusPDFGenerator()


# Fonctions utilitaires
def create_revision_sheet_pdf(
    content: Dict, student_name: str, subject: str, topic: str
) -> bytes:
    """Crée une fiche de révision PDF"""
    metadata = DocumentMetadata(
        title=f"Fiche de révision - {topic}",
        subject=subject,
        student_name=student_name,
        student_level="Terminale",
        document_type="Fiche de révision",
        topic=topic,
    )

    return pdf_generator.generate_revision_sheet(content, metadata)


def create_exercise_sheet_pdf(
    content: Dict, student_name: str, subject: str, topic: str
) -> bytes:
    """Crée une feuille d'exercices PDF"""
    metadata = DocumentMetadata(
        title=f"Exercices - {topic}",
        subject=subject,
        student_name=student_name,
        student_level="Terminale",
        document_type="Feuille d'exercices",
        topic=topic,
    )

    return pdf_generator.generate_exercise_sheet(content, metadata)


def create_evaluation_report_pdf(
    content: Dict, student_name: str, subject: str
) -> bytes:
    """Crée un rapport d'évaluation PDF"""
    metadata = DocumentMetadata(
        title="Rapport d'évaluation",
        subject=subject,
        student_name=student_name,
        student_level="Terminale",
        document_type="Rapport d'évaluation",
    )

    return pdf_generator.generate_evaluation_report(content, metadata)


def create_progress_report_pdf(student_data: Dict, student_name: str) -> bytes:
    """Crée un rapport de progression PDF"""
    metadata = DocumentMetadata(
        title="Rapport de progression",
        subject="Toutes matières",
        student_name=student_name,
        student_level="Terminale",
        document_type="Rapport de progression",
    )

    return pdf_generator.generate_progress_report(student_data, metadata)
