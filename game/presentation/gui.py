from game.domain.difficulty import selected_difficulty

class Window:
    def __init__(self, width: int = 500):
        self.width = selected_difficulty.difficulty_values()["window_width"]
        self.height = selected_difficulty.difficulty_values()["window_height"]


running_window = Window() #Manually altering window resolution is not recommended