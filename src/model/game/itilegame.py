from abc import ABC, abstractmethod

class ITileGame(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def do_pre_tick(self, time):
        pass

    @abstractmethod
    def do_post_tick(self, time):
        pass

    @abstractmethod
    def handle_left(self):
        pass

    @abstractmethod
    def handle_right(self):
        pass

    @abstractmethod
    def handle_up(self):
        pass

    @abstractmethod
    def handle_down(self):
        pass

    @abstractmethod
    def handle_space(self):
        pass

    @abstractmethod
    def check_lost(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_score(self):
        pass
