from src.utils.clean_data import clean_data


class DataStore:
    df = None

    @classmethod
    def load(cls, force_reload=False):
        if cls.df is None or force_reload:
            cls.df = clean_data()
        return cls.df
