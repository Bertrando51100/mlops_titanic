"""
config_loader.py
────────────────
Charge et valide la configuration du projet depuis le fichier YAML.
Ce module est importé par tous les autres modules du projet pour
accéder aux paramètres de configuration de manière centralisée.
"""

import yaml
from pathlib import Path
from loguru import logger


def load_config(config_path: str = "configs/config.yaml") -> dict:
    """
    Charge la configuration depuis un fichier YAML.

    Args:
        config_path: Chemin vers le fichier de configuration.

    Returns:
        dict: Configuration complète du projet.

    Raises:
        FileNotFoundError: Si le fichier de configuration n'existe pas.
        yaml.YAMLError: Si le fichier YAML est mal formaté.
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(
            f"Fichier de configuration introuvable : {config_path}\n"
            f"Assurez-vous d'être dans le répertoire racine du projet."
        )

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logger.debug(f"Configuration chargée depuis : {config_path}")
    return config


def get_project_root() -> Path:
    """
    Retourne le chemin absolu vers la racine du projet.
    Utile pour construire des chemins absolus depuis n'importe quel module.
    """
    return Path(__file__).parent.parent
