import pandas as pd
from config import CONFIG
from src.utils.get_data import get_raw_data
from pathlib import Path


def clean_data(save=True):
    """
    Nettoie les données brutes COVID et retourne un DataFrame propre.
    """
    df = get_raw_data()

    cols_to_drop = [
        "R",
        "TO",
        "cv_dose1",
        "tx_pos",
        "tx_incid",
        "pos_7j",
        "pos",
        "reg_rea",
        "reg_incid_rea",
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors="ignore")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["dep", "date"])
    df = df[df["dep"] != "00"]

    df["taux_mortalite"] = df["dchosp"] / (df["hosp"] + 1) * 100
    df["taux_rea"] = df["rea"] / (df["hosp"] + 1) * 100

    if save:
        output_path: Path = CONFIG["DATA_PATH"]["CLEANED"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

    return df
