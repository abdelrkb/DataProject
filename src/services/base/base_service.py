from src.services.base.datastore import DataStore


class BaseService:
    def __init__(self):
        self.df = DataStore.load()
