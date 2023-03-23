from abc import ABC, abstractmethod


class IRender(ABC):
    @abstractmethod
    def initialize(self, screen):
        pass

    @abstractmethod
    def render(self, game_model):
        pass
