from abc import ABC, abstractmethod


class BasePage(ABC):
    @abstractmethod
    def layout(self):
        pass

    @abstractmethod
    def register_callbacks(self, app):
        pass
