"""
data_loader.py
──────────────
Responsable du téléchargement et du chargement des données brutes.

Le dataset Titanic contient 891 passagers avec les informations suivantes :
- PassengerId : Identifiant unique
- Survived    : 0 = décédé, 1 = survivant (notre TARGET)
- Pclass      : Classe du billet (1 = 1ère, 2 = 2ème, 3 = 3ème)
- Name        : Nom complet du passager
- Sex         : Sexe (male/female)
- Age         : Âge en années
- SibSp       : Nombre de frères/sœurs ou conjoints à bord
- Parch       : Nombre de parents ou enfants à bord
- Ticket      : Numéro de billet
- Fare        : Prix du billet
- Cabin       : Numéro de cabine
- Embarked    : Port d'embarquement (C=Cherbourg, Q=Queenstown, S=Southampton)
"""

import pandas as pd
import requests
from pathlib import Path
from loguru import logger


def download_titanic_dataset(url: str, output_path: str) -> bool:
    """
    Télécharge le dataset Titanic depuis une URL.

    Args:
        url: URL du fichier CSV à télécharger.
        output_path: Chemin local où sauvegarder le fichier.

    Returns:
        bool: True si le téléchargement a réussi.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Si le fichier existe déjà, on ne le re-télécharge pas
    if output_file.exists():
        logger.info(f"Dataset déjà présent : {output_path} — téléchargement ignoré.")
        return True

    logger.info(f"Téléchargement du dataset depuis : {url}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Lève une exception si erreur HTTP

        with open(output_file, "wb") as f:
            f.write(response.content)

        logger.success(f"Dataset téléchargé avec succès : {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors du téléchargement : {e}")
        raise


def load_data(file_path: str) -> pd.DataFrame:
    """
    Charge un fichier CSV en DataFrame pandas.

    Args:
        file_path: Chemin vers le fichier CSV.

    Returns:
        pd.DataFrame: Les données chargées.
    """
    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    logger.info(f"Chargement des données depuis : {file_path}")
    df = pd.read_csv(file_path)

    logger.info(f"Dataset chargé : {df.shape[0]} lignes × {df.shape[1]} colonnes")
    logger.info(f"Colonnes : {list(df.columns)}")

    return df


def display_data_summary(df: pd.DataFrame) -> None:
    """
    Affiche un résumé statistique du dataset pour l'exploration initiale.

    Args:
        df: Le DataFrame à analyser.
    """
    logger.info("=" * 60)
    logger.info("📊 RÉSUMÉ DU DATASET")
    logger.info("=" * 60)
    logger.info(f"Dimensions        : {df.shape[0]} lignes × {df.shape[1]} colonnes")
    logger.info(f"Mémoire utilisée  : {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

    # Valeurs manquantes
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df) * 100).round(2)
    missing_info = pd.DataFrame({
        "Valeurs manquantes": null_counts,
        "Pourcentage (%)": null_pct
    })
    missing_info = missing_info[missing_info["Valeurs manquantes"] > 0]

    if not missing_info.empty:
        logger.warning(f"Valeurs manquantes détectées :\n{missing_info.to_string()}")
    else:
        logger.info("Aucune valeur manquante détectée ✅")

    # Distribution de la cible
    if "Survived" in df.columns:
        survival_rate = df["Survived"].mean() * 100
        logger.info(f"Taux de survie    : {survival_rate:.1f}%")
        logger.info(f"Survivants        : {df['Survived'].sum()} / {len(df)}")

    logger.info("=" * 60)
