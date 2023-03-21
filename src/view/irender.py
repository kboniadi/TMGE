from abc import ABC, abstractmethod

class iRender(ABC):
    @abstractmethod
    def render(self, game_model):
        pass

    @abstractmethod
    def render_menu(self, game_model):
        pass

    @abstractmethod
    def render_gameover(self, game_model):
        pass