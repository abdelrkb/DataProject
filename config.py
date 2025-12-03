import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "DATA_PATH": {
        "RAW": os.path.join(BASE_DIR, "data", "raw", "covid_dataset.csv"),
        "CLEANED": os.path.join(BASE_DIR, "data", "cleaned", "covid_clean.csv"),
    }
}
