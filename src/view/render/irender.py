from abc import ABC, abstractmethod

class IRender(ABC):
    @abstractmethod
    def render(self, game_model):
        pass

    @abstractmethod
    def initialize(self, screen):
        pass
