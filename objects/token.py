from objects.enums import PlayerColour


class Token:
    def __init__(self, colour: PlayerColour, placed: bool):
        self.colour = colour

    def __str__(self):
        if self.colour == PlayerColour.RED:
            return "R"
        return "Y"

    def to_dict(self):
        return {"colour": self.colour.name}

    @staticmethod
    def token_from_dict(data):
        if data["colour"] == PlayerColour.RED.name:
            return PlayerColour.RED
        return PlayerColour.YELLOW
