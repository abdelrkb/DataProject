from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CONFIG = {
    "DATA_PATH": {
        "RAW": BASE_DIR / "data" / "raw" / "covid_dataset.csv",
        "CLEANED": BASE_DIR / "data" / "cleaned" / "covid_clean.csv",
    },
    "APP_HOST": "127.0.0.1",
    "APP_PORT": 8050,
    "DEBUG": True,
}