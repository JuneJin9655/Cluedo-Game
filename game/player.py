from game.character import characters
from game.weapon import weapons
from game.mansion import rooms

# Represents a player in the Cluedo game
class Player:
    def __init__(self, player_id, hand):
        self.id = player_id
        self.hand = hand
        self.notebook = {}
        self.active = True
        self.current_room = None

        self.notebook = {}
        all_cards = characters + weapons + rooms
        for card in all_cards:
            self.notebook[card] = "Unknown"

        for card in hand:
            self.notebook[card] = f"OWNED (Player {self.id})"

    # Checks which cards in the player's hand can refute a suggestion
    def can_refute(self, suggestion):
        return [card for card in suggestion.values() if card in self.hand]
