from src.services.core.datastore import DataStore

class BaseService:

    def __init__(self):
        self.df = DataStore.load()