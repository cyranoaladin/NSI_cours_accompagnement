"""
Utilitaires de validation pour Nexus Réussite
"""

import re
from typing import Any, Dict, List, Optional

from email_validator import EmailNotValidError
from email_validator import validate_email as _validate_email


def validate_email(email: str) -> bool:
    """
    Valide le format d'un email

    Args:
        email: Adresse email à valider

    Returns:
        bool: True si valide
    """
    try:
        if not email or not isinstance(email, str):
            return False

        # Utiliser email-validator pour une validation robuste
        validated_email = _validate_email(email.strip())
        return True

    except EmailNotValidError:
        return False
    except Exception:
        return False


def validate_password(password: str) -> bool:
    """
    Valide la force d'un mot de passe

    Critères:
    - Au moins 8 caractères
    - Au moins une majuscule
    - Au moins une minuscule
    - Au moins un chiffre
    - Au moins un caractère spécial (optionnel mais recommandé)

    Args:
        password: Mot de passe à valider

    Returns:
        bool: True si valide
    """
    if not password or not isinstance(password, str):
        return False

    # Longueur minimale
    if len(password) < 8:
        return False

    # Au moins une majuscule
    if not re.search(r"[A-Z]", password):
        return False

    # Au moins une minuscule
    if not re.search(r"[a-z]", password):
        return False

    # Au moins un chiffre
    if not re.search(r"\d", password):
        return False

    return True


def validate_phone_number(phone: str, country_code: str = "TN") -> bool:
    """
    Valide un numéro de téléphone

    Args:
        phone: Numéro de téléphone
        country_code: Code pays (par défaut TN pour Tunisie)

    Returns:
        bool: True si valide
    """
    if not phone or not isinstance(phone, str):
        return False

    # Nettoyer le numéro
    phone = re.sub(r"[^\d+]", "", phone)

    if country_code == "TN":
        # Format tunisien: +216 ou 216 ou 0 suivi de 8 chiffres
        patterns = [
            r"^\+216[2-9]\d{7}$",  # Format international +216 XX XXX XXX
            r"^216[2-9]\d{7}$",  # Format sans + : 216 XX XXX XXX
            r"^0[2-9]\d{7}$",  # Format national : 0X XXX XXX
        ]

        return any(re.match(pattern, phone) for pattern in patterns)

    # Validation générique pour d'autres pays
    return len(phone) >= 8 and len(phone) <= 15


def validate_name(name: str, min_length: int = 2, max_length: int = 50) -> bool:
    """
    Valide un nom (prénom/nom)

    Args:
        name: Nom à valider
        min_length: Longueur minimale
        max_length: Longueur maximale

    Returns:
        bool: True si valide
    """
    if not name or not isinstance(name, str):
        return False

    name = name.strip()

    # Vérifier la longueur
    if len(name) < min_length or len(name) > max_length:
        return False

    # Vérifier que le nom contient seulement des lettres, espaces, tirets et apostrophes
    if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", name):
        return False

    return True


def validate_grade_level(grade: str) -> bool:
    """
    Valide un niveau scolaire

    Args:
        grade: Niveau scolaire

    Returns:
        bool: True si valide
    """
    valid_grades = [
        "seconde",
        "premiere",
        "terminale",
        "2nde",
        "1ere",
        "term",
        "cp",
        "ce1",
        "ce2",
        "cm1",
        "cm2",
        "6eme",
        "5eme",
        "4eme",
        "3eme",
    ]

    return grade and grade.lower() in valid_grades


def validate_subject(subject: str) -> bool:
    """
    Valide une matière scolaire

    Args:
        subject: Matière à valider

    Returns:
        bool: True si valide
    """
    valid_subjects = [
        "mathematiques",
        "maths",
        "francais",
        "anglais",
        "espagnol",
        "histoire",
        "geographie",
        "sciences",
        "physique",
        "chimie",
        "biologie",
        "svt",
        "philosophie",
        "economie",
        "droit",
        "informatique",
        "nsi",
        "ses",
        "litterature",
        "latin",
        "grec",
    ]

    return subject and subject.lower() in valid_subjects


def validate_json_structure(data: Any, required_fields: List[str]) -> Dict[str, Any]:
    """
    Valide la structure d'un objet JSON

    Args:
        data: Données à valider
        required_fields: Champs obligatoires

    Returns:
        dict: Résultat de validation avec erreurs
    """
    result = {"valid": True, "errors": [], "warnings": []}

    if not isinstance(data, dict):
        result["valid"] = False
        result["errors"].append("Les données doivent être un objet JSON")
        return result

    # Vérifier les champs obligatoires
    for field in required_fields:
        if field not in data:
            result["valid"] = False
            result["errors"].append(f"Champ obligatoire manquant: {field}")
        elif data[field] is None or data[field] == "":
            result["warnings"].append(f"Champ vide: {field}")

    return result


def validate_file_upload(file_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données d'un fichier uploadé

    Args:
        file_data: Informations du fichier

    Returns:
        dict: Résultat de validation
    """
    result = {"valid": True, "errors": [], "warnings": []}

    # Vérifier la présence du fichier
    if not file_data or "filename" not in file_data:
        result["valid"] = False
        result["errors"].append("Aucun fichier fourni")
        return result

    filename = file_data.get("filename", "")
    file_size = file_data.get("size", 0)
    content_type = file_data.get("content_type", "")

    # Vérifier l'extension
    allowed_extensions = {
        "pdf",
        "doc",
        "docx",
        "txt",
        "rtf",
        "jpg",
        "jpeg",
        "png",
        "gif",
        "webp",
        "mp4",
        "avi",
        "mov",
        "wmv",
        "mp3",
        "wav",
        "ogg",
    }

    if "." in filename:
        extension = filename.rsplit(".", 1)[1].lower()
        if extension not in allowed_extensions:
            result["valid"] = False
            result["errors"].append(f"Extension de fichier non autorisée: {extension}")
    else:
        result["warnings"].append("Fichier sans extension")

    # Vérifier la taille (16MB max)
    max_size = 16 * 1024 * 1024  # 16MB
    if file_size > max_size:
        result["valid"] = False
        result["errors"].append(
            f"Fichier trop volumineux: {file_size} bytes (max: {max_size})"
        )

    # Vérifier le type MIME
    allowed_mime_types = {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "video/mp4",
        "video/quicktime",
        "audio/mpeg",
        "audio/wav",
    }

    if content_type and content_type not in allowed_mime_types:
        result["warnings"].append(f"Type MIME inhabituel: {content_type}")

    return result


def sanitize_html_input(html_content: str) -> str:
    """
    Sanitise le contenu HTML pour éviter les injections XSS

    Args:
        html_content: Contenu HTML à nettoyer

    Returns:
        str: Contenu nettoyé
    """
    if not html_content:
        return ""

    # Liste des balises autorisées (très restrictive)
    allowed_tags = {
        "p",
        "br",
        "strong",
        "em",
        "u",
        "ol",
        "ul",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
    }

    # Supprimer les balises script et style
    html_content = re.sub(
        r"<(script|style)[^>]*>.*?</\1>",
        "",
        html_content,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Supprimer les attributs JavaScript
    html_content = re.sub(
        r'\s*on\w+\s*=\s*["\'][^"\']*["\']', "", html_content, flags=re.IGNORECASE
    )

    # Supprimer les liens javascript:
    html_content = re.sub(
        r'href\s*=\s*["\']javascript:[^"\']*["\']',
        "",
        html_content,
        flags=re.IGNORECASE,
    )

    return html_content


def validate_url(url: str, allowed_schemes: List[str] = None) -> bool:
    """
    Valide une URL

    Args:
        url: URL à valider
        allowed_schemes: Schémas autorisés (http, https par défaut)

    Returns:
        bool: True si valide
    """
    if not url or not isinstance(url, str):
        return False

    if allowed_schemes is None:
        allowed_schemes = ["http", "https"]

    # Pattern pour validation d'URL
    url_pattern = re.compile(
        r"^https?://"  # Schéma http ou https
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # Domaine
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # IP
        r"(?::\d+)?"  # Port optionnel
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return bool(url_pattern.match(url))


class ValidationError(Exception):
    """
    Exception personnalisée pour les erreurs de validation
    """

    def __init__(self, message: str, field: str = None, code: str = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code or "VALIDATION_ERROR"

    def to_dict(self):
        return {"error": self.message, "field": self.field, "code": self.code}


def validate_student_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données d'un étudiant

    Args:
        data: Données de l'étudiant

    Returns:
        dict: Résultat de validation
    """
    result = validate_json_structure(
        data, ["first_name", "last_name", "email", "grade_level"]
    )

    if not result["valid"]:
        return result

    # Validations spécifiques
    if not validate_name(data.get("first_name", "")):
        result["valid"] = False
        result["errors"].append("Prénom invalide")

    if not validate_name(data.get("last_name", "")):
        result["valid"] = False
        result["errors"].append("Nom invalide")

    if not validate_email(data.get("email", "")):
        result["valid"] = False
        result["errors"].append("Email invalide")

    if not validate_grade_level(data.get("grade_level", "")):
        result["valid"] = False
        result["errors"].append("Niveau scolaire invalide")

    # Validations optionnelles
    if data.get("phone") and not validate_phone_number(data["phone"]):
        result["warnings"].append("Numéro de téléphone invalide")

    return result


def validate_teacher_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données d'un enseignant

    Args:
        data: Données de l'enseignant

    Returns:
        dict: Résultat de validation
    """
    result = validate_json_structure(
        data, ["first_name", "last_name", "email", "subjects"]
    )

    if not result["valid"]:
        return result

    # Validations spécifiques
    if not validate_name(data.get("first_name", "")):
        result["valid"] = False
        result["errors"].append("Prénom invalide")

    if not validate_name(data.get("last_name", "")):
        result["valid"] = False
        result["errors"].append("Nom invalide")

    if not validate_email(data.get("email", "")):
        result["valid"] = False
        result["errors"].append("Email invalide")

    # Valider les matières
    subjects = data.get("subjects", [])
    if not isinstance(subjects, list) or not subjects:
        result["valid"] = False
        result["errors"].append("Au moins une matière doit être spécifiée")

    return result
