from objects.player_colour import PlayerColour


class Token:
    def __init__(self, colour: PlayerColour, placed: bool):
        self.colour = colour

    def __str__(self):
        if self.colour == PlayerColour.RED:
            return "R"
        return "Y"

    def to_dict(self):
        return {"colour": self.colour.name}
