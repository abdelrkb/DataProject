from src.utils.clean_data import clean_data
import json
from config import CONFIG


class DataStore:
    df = None
    geojson_dep = None
    geojson_reg = None

    @classmethod
    def load_df(cls, force_reload=False):
        if cls.df is None or force_reload:
            cls.df = clean_data()
        return cls.df

    @classmethod
    def load_geojson(cls):
        if cls.geojson_dep is None:
            with open(CONFIG["GEOJSON_PATH"]["DEPARTEMENTS"], encoding="utf-8") as f:
                cls.geojson_dep = json.load(f)
        if cls.geojson_reg is None:
            with open(CONFIG["GEOJSON_PATH"]["REGIONS"], encoding="utf-8") as f:
                cls.geojson_reg = json.load(f)

        return cls.geojson_dep, cls.geojson_reg
