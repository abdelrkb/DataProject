from abc import ABC, abstractmethod
from src.services.reference_service import ReferenceService


class BaseComponent(ABC):
    def __init__(self, service=None):
        self.service = service
        self.reference_service = ReferenceService()
        self.regions = self.reference_service.available_regions()
        self.departements = self.reference_service.available_dep()

    def cid(self, name: str) -> str:
        """
        Génère un ID unique pour le composant
        """
        return f"{self.__class__.__name__}-{name}"

    @abstractmethod
    def layout(self):
        pass
