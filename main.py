from src.model.Tetris import Tetris
from src.model.user import User
from src.model.player import Player
from src.controller.keyboard import Keyboard
from src.listener.eventmanager import EventManagerWeak
from src.model.gameengine import GameEngine
from src.view.canvas import Canvas


def run():
    evManager = EventManagerWeak()
    gamemodel = GameEngine(evManager, Tetris())
    keyboard = Keyboard(evManager, gamemodel)
    graphics = Canvas(evManager, gamemodel)
    gamemodel.run()


if __name__ == '__main__':
    print("--------------------")
    print("--------------------")
    print("Welcome to TileGames!")
    print("Brought to you by Group 9.")
    print("--------------------")
    print("Please enter a valid username to continue: ")
    username = str(input())
    user = None
    while len(username) == 0:
        print("A valid username is any string of characters: ")
        username = str(input())
    user = User(username)
    print("--------------------")
    print("Please input the number of players (1 or 2): ")
    print("--------------------")
    num_players = int(input())
    while num_players != 1 and num_players != 2:
        print("--------------------")
        print("Please input the number of players (1 or 2): ")
        print("--------------------")
        num_players = int(input())
    players = [Player(i + 1, 0) for i in range(0, num_players)]
    user.players = players
    print("--------------------")
    print("Please input 1 or 2 to select one of the following games: ")
    print("1. Tetris")
    print("2. Candy Crush")
    print("--------------------")
    selected_game = int(input())
    while selected_game != 1 and selected_game != 2:
        print("--------------------")
        print("Please input 1 or 2 to select one of the following games: ")
        print("1. Tetris")
        print("2. Candy Crush")
        print("--------------------")
        selected_game = int(input())
    if selected_game == 1:
        user.selected_game = "tetris"
        # run_tetris()
        run()
    elif selected_game == 2:
        user.selected_game = "candy_crush"
        # run_candy_crush()

    # run game engine
    # run()
