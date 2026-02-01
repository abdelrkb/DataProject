import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "DATA_PATH": {
        "RAW": os.path.join(BASE_DIR, "data", "raw", "covid_dataset.csv"),
        "CLEANED": os.path.join(BASE_DIR, "data", "cleaned", "covid_clean.csv"),
    },
    "GEOJSON_PATH": { 
        "REGIONS": os.path.join(BASE_DIR, "data", "geo", "regions.geojson"),
        "DEPARTEMENTS": os.path.join(BASE_DIR, "data", "geo", "departements.geojson"),
        "GUADELOUPE": os.path.join(BASE_DIR, "data", "geo", "guadeloupe.geojson"),
        "MARTINIQUE": os.path.join(BASE_DIR, "data", "geo", "martinique.geojson"),
        "GUYANE": os.path.join(BASE_DIR, "data", "geo", "guyane.geojson"),
        "REUNION": os.path.join(BASE_DIR, "data", "geo", "reunion.geojson"),
        "MAYOTTE": os.path.join(BASE_DIR, "data", "geo", "mayotte.geojson"),
    },
    "APP_HOST": "127.0.0.1",
    "APP_PORT": 8050,
    "DEBUG": True
}