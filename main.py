from src.controller.keyboard import Keyboard
from src.listener.eventmanager import EventManagerWeak
from src.model.GameEngine import GameEngine
from src.view.canvas import Canvas


def run():
    evManager = EventManagerWeak()
    gamemodel = GameEngine(evManager)
    keyboard = Keyboard(evManager, gamemodel)
    graphics = Canvas(evManager, gamemodel)
    gamemodel.run()


if __name__ == '__main__':
    run()
