import sys
from game.presentation.main_app import App


def main(new_width, new_height, new_difficulty_value):
    App(new_width, new_height, new_difficulty_value)


if __name__ == "__main__":
    new_width = int(sys.argv[1]) if len(sys.argv) > 1 else None
    new_height = int(sys.argv[2]) if len(sys.argv) > 2 else None
    new_difficulty_value = int(sys.argv[3]) if len(sys.argv) > 3 else None

    main(new_width, new_height, new_difficulty_value)