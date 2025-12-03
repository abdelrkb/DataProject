import sys
import os
import pandas as pd
from config import CONFIG
from src.utils.get_data import get_raw_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

def clean_data():
    """
    Nettoie les données brutes COVID, supprime les colonnes inutiles
    et sauvegarde le fichier nettoyé dans data/cleaned/.
    """
    df = get_raw_data()

    cols_to_drop = [
        "R", "TO", "cv_dose1", "tx_pos", "tx_incid", "pos_7j",
        "pos", "reg_rea", "reg_incid_rea"
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors="ignore")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["dep", "date"])
    df = df[df["dep"] != "00"]

    df["taux_mortalite"] = df["dchosp"] / (df["hosp"] + 1) * 100
    df["taux_rea"] = df["rea"] / (df["hosp"] + 1) * 100

    output_dir = os.path.dirname(CONFIG["DATA_PATH"]["CLEANED"])
    os.makedirs(output_dir, exist_ok=True)

    df.to_csv(CONFIG["DATA_PATH"]["CLEANED"], sep=",", index=False, encoding="utf-8")
    return df

if __name__ == "__main__":
    clean_data()
