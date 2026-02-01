from abc import ABC, abstractmethod


class BasePage(ABC):
    """
    BasePage dont les autres pages héritent
    """

    @abstractmethod
    def layout(self):
        pass

    @abstractmethod
    def register_callbacks(self, app):
        pass
