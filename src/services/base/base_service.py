from src.services.base.datastore import DataStore


class BaseService:
    """
    Base service dont les autres services héritent
    """

    def __init__(self):
        self.df = DataStore.load_df()
