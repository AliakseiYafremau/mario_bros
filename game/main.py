import sys
from game.presentation.main_app import App


def main(new_width: int, new_height: int, new_difficulty_value: int, points: int, seconds_alive: int):
    App(new_width=new_width,
        new_height=new_height,
        new_difficulty_value=new_difficulty_value,
        points=points,
        seconds_alive=seconds_alive)


if __name__ == "__main__":
    new_width = int(sys.argv[1]) if len(sys.argv) > 1 else None
    new_height = int(sys.argv[2]) if len(sys.argv) > 2 else None
    new_difficulty_value = int(sys.argv[3]) if len(sys.argv) > 3 else None
    points = int(sys.argv[4]) if len(sys.argv) > 4 else None
    seconds_alive = int(sys.argv[5]) if len(sys.argv) > 5 else None

    main(new_width, new_height, new_difficulty_value, points, seconds_alive)
