from game.domain.difficulty import Difficulty
from game.presentation.main_app import App
from game.presentation.game_over import GameOverScreen
from game.presentation.difficulty_selector import DifficultySelectorScreen
from game.game_setup import create_game_app
from game.presentation.gui import Window


def main():
    difficulty_selector = DifficultySelectorScreen()
    game_app = create_game_app(Difficulty(0))
    game_over = GameOverScreen()

    window = Window(difficulty=Difficulty(0))

    App(screens=[difficulty_selector, game_app, game_over], initial_screen=game_app, window=window)


if __name__ == "__main__":
    main()
