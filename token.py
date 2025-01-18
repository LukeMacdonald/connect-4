from utils import PlayerColour


class Token:
    def __init__(self, colour: PlayerColour, placed: bool):
        self.colour = colour
        self.placed = placed

    def get_color(self):
        return self.colour
