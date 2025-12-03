import pandas as pd
from config import CONFIG

def get_raw_data() -> pd.DataFrame:
    """
    Charge le dataset brut depuis data/raw/.
    Retourne un DataFrame Pandas.
    """
    raw_path = CONFIG["DATA_PATH"]["RAW"]
    df = pd.read_csv(raw_path, sep=",", low_memory=False)

    return df
