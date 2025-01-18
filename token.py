from utils import PlayerColour


class Token:
    def __init__(self, colour: PlayerColour, placed: bool):
        self.colour = colour
        self.placed = placed

    def __str__(self):
        if self.colour == PlayerColour.RED:
            return "R"
        return "Y"
