import random
from game.player import Player
from game.mansion import rooms
from game.character import characters
from game.weapon import weapons

# Main game engine that controls the overall gameplay loop and logic
class GameEngine:
    def __init__(self, num_players=3):
        # Randomly generate the solution (truth) of the murder: who, where, with what
        self.solution = {
            "character": random.choice(characters),
            "weapon": random.choice(weapons),
            "room": random.choice(rooms)
        }
        print(f"[DEBUG] Correct Answer is :{self.solution}")

        # Remove the solution cards and shuffle the rest to distribute among players
        all_cards = characters + weapons + rooms
        truth_cards = list(self.solution.values())
        remaining = [card for card in all_cards if card not in truth_cards]
        random.shuffle(remaining)

        # Initialize players and deal cards equally
        self.num_players = num_players
        self.hands = [remaining[i::num_players] for i in range(num_players)]
        self.players = [
            Player(i, self.hands[i]) for i in range(num_players)
        ]

    # Start the main game loop: manage player turns and handle actions
    def start(self):
        print("Welcome to Cluedo Game!")
        turn = 0
        while True:
            if not any(p.active for p in self.players):
                print("\n💀 All players are eliminated. Game over.")
                print(f"The correct answer was: {self.solution}")
                break

            player_index = turn % self.num_players
            player = self.players[player_index]

            if not player.active:
                turn += 1
                continue

            print(f"\n🎲 Player {player.id}'s turn.")
            print(f"You are currently in: {player.current_room if player.current_room else 'None'}")
            action = input("Enter 'move', 'suggest', 'accuse', or 'notebook': ").strip().lower()

            # Handle player actions
            if action == "move":
                self.move_room(player_index)
            elif action == "suggest":
                self.make_suggestion(player_index)
            elif action == "accuse":
                self.make_accusation(player_index)
            elif action == "notebook":
                self.show_notebook(player_index)
            else:
                print("Invalid input.")
            turn += 1

    # Display the player's current notebook (their clue tracking)
    def show_notebook(self, player_index):
        player = self.players[player_index]
        print(f"\n📒 Player {player.id}'s Notebook:")
        for card in characters + weapons + rooms:
            status = player.notebook.get(card, "Unknown")
            print(f"  {card}: {status}")

    # Let the player move into a room
    def move_room(self, player_index):
        player = self.players[player_index]
        print(f"Available rooms: {rooms}")
        room = input(f"Player {player.id}, enter room name to move: ").strip()
        if room in rooms:
            player.current_room = room
            print(f"Player {player.id} moved to {room}.")
        else:
            print("Invalid Room!")

    # Allow the player to make a suggestion (guess the 3 components)
    def make_suggestion(self, player_index):
        player = self.players[player_index]
        if not player.current_room:
            print("You must move to a room before making a suggestion!")
            return

        print(f"Player {player.id}'s Suggestion:")
        char = input(f"Suggest a character {characters}: ").strip()
        weap = input(f"Suggest a weapon {weapons}: ").strip()
        suggestion = {
            "character": char,
            "weapon": weap,
            "room": player.current_room
        }
        print(f"Player {player.id} suggests: {suggestion}")
        self.refute_suggestion(player_index, suggestion)

    # Check if other players can refute the suggestion
    def refute_suggestion(self, suggesting_player_index, suggestion):
        suggesting_player = self.players[suggesting_player_index]

        for i in range(1, self.num_players):
            check_index = (suggesting_player_index + i) % self.num_players
            refuter = self.players[check_index]
            if not refuter.active:
                continue

            matches = [card for card in suggestion.values() if card in refuter.hand]
            if matches:
                shown = random.choice(matches)
                suggesting_player.notebook[shown] = f"Player {refuter.id}"
                return {
                    "refuter_id": refuter.id,
                    "shown_card": shown
                }

            # No one refuted
            for card in suggestion.values():
                if suggesting_player.notebook.get(card, "Unknown") == "Unknown":
                    suggesting_player.notebook[card] = "MAYBE (no one refuted)"

            return {
                "refuter_id": None,
                "shown_card": None
            }


    # Let the player make an accusation (final guess)
    def make_accusation(self, player_index):
        player = self.players[player_index]
        print(f"Player {player.id} is making an accusation!")
        char = input(f"Who is the murderer? {characters}: ").strip()
        weap = input(f"What is the weapon? {weapons}: ").strip()
        room = input(f"In which room? {rooms}: ").strip()
        accusation = {
            "character": char,
            "weapon": weap,
            "room": room
        }
        if accusation == self.solution:
            print(f"\n🎉 Player {player.id} made a correct accusation and WINS the game!")
            print(f"✔️ The solution was: {self.solution}")
            exit()
        else:
            print(f"❌ Player {player.id} made a wrong accusation and is eliminated.")
            player.active = False
