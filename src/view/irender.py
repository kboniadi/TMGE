from abc import ABC, abstractmethod

class iRender(ABC):
    @abstractmethod
    def render(self, game_model):
        pass
