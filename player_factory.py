import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def roll(self):
        roll_value = random.randint(1, 6)
        return roll_value

    def hold(self, turn_score):
        self.score += turn_score

class HumanPlayer(Player):
    def get_action(self, turn_score):
        while True:
            action = input(f"{self.name}, roll or hold? ").lower()
            if action in ("roll", "hold"):
                return action
            else:
                print("Invalid input. Please enter 'roll' or 'hold'.")

class ComputerPlayer(Player):
    def get_action(self, turn_score):
        hold_target = min(25, 100 - self.score)
        if turn_score < hold_target:
            return "roll"
        else:
            return "hold"

class PlayerFactory:
    def create_player(self, player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")