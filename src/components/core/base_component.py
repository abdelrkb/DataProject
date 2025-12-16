from abc import ABC, abstractmethod


class BaseComponent(ABC):

    def __init__(self, service=None):
        self.service = service

    @abstractmethod
    def layout(self):
        pass