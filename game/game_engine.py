import random
from game.mansion import rooms
from game.character import characters
from game.weapon import weapons

class GameEngine:
    def __init__(self):
        self.solution = {
            "character": random.choice(characters),
            "weapon": random.choice(weapons),
            "room": random.choice(rooms)
        }
        self.current_room = random.choice(rooms)
        print(f"[DEBUG] Correct Answer is :{self.solution}")

    def start(self):
        print("Welcome to Cluedo Game!")
        while True:
            print(f"\nYou are now in the {self.current_room}")
            action = input("Enter 'move' to change room or 'suggest' to make a suggestion: ")
            if action == "move":
                self.move_room()
            elif action == "suggest":
                self.make_suggestion()
            else:
                print("Invalid.")

    def move_room(self):
        print(f"Available rooms: {rooms}")
        room = input("Enter room name to move: ")
        if room in rooms:
            self.current_room = room
        else:
            print("Invalid Room!")

    def make_suggestion(self):
        char = input(f"Who is the MURDER {characters}: ")
        weap = input(f"What weapon he/she used? {weapons}: ")
        guess = {"character": char, "weapon": weap, "room": self.current_room}
        if guess == self.solution:
            print("Correct")
            exit()
        else:
            print("Wrong guess. Keep playing!")
