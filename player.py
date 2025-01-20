from utils import PlayerColour


class Player:
    def __init__(self, name: str, colour: PlayerColour, tokens: list):
        self.name = name
        self.colour = colour
        self.tokens = tokens

    def __str__(self):
        name = f"Name: {self.name}"
        colour = f"Color: {self.colour.name}"
        total_tokens = f"Tokens Left: {len(self.tokens)}"
        return f"{name}\n{colour}\n{total_tokens}"

    def to_dict(self):
        return {
            "name": self.name,
        }

    def remove_token(self):
        return self.tokens.pop(0)

    def has_tokens(self):
        return len(self.tokens) > 0
