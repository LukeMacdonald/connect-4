from utils import PlayerColour


class Player:
    def __init__(self, name: str, colour: PlayerColour, tokens: list):
        self.name = name
        self.colour = colour
        self.tokens = tokens
    def remove_token(self):
        return self.tokens.pop(0)
