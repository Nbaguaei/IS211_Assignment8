# player.py
import random

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

# player_factory.py
from player import HumanPlayer, ComputerPlayer

class PlayerFactory:
    def create_player(self, player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

# timed_game_proxy.py
import time

class TimedGameProxy:
    def __init__(self, game):
        self._game = game
        self.start_time = time.time()

    def play(self):
        self._game.play()

    def determine_timed_winner(self):
        if self._game.player1.score > self._game.player2.score:
            print(f"{self._game.player1.name} wins with {self._game.player1.score} points!")
        elif self._game.player2.score > self._game.player1.score:
            print(f"{self._game.player2.name} wins with {self._game.player2.score} points!")
        else:
            print("It's a tie!")

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play(self):
        current_player = self.player1
        other_player = self.player2
        turn_score = 0

        while self.player1.score < 100 and self.player2.score < 100:
            print(f"\n{current_player.name}'s turn:")
            action = current_player.get_action(turn_score)

            if action == "roll":
                roll_value = current_player.roll()
                if roll_value == 1:
                    print("You rolled a 1! Turn score reset to 0.")
                    turn_score = 0
                    current_player, other_player = other_player, current_player
                else:
                    turn_score += roll_value
                    print(f"You rolled a {roll_value}. Turn score: {turn_score}")
            elif action == "hold":
                current_player.hold(turn_score)
                print(f"{current_player.name}'s score is now {current_player.score}.")
                turn_score = 0
                current_player, other_player = other_player, current_player
            if isinstance(self, TimedGameProxy) and time.time() - self.start_time > 60:
                self.determine_timed_winner()
                return

        winner = self.player1 if self.player1.score >= 100 else self.player2
        print(f"\n{winner.name} wins!")

# main.py
import argparse
from player_factory import PlayerFactory
from timed_game_proxy import TimedGameProxy
from game import Game

parser = argparse.ArgumentParser()
parser.add_argument("--player1", choices=["human", "computer"], required=True)
parser.add_argument("--player2", choices=["human", "computer"], required=True)
parser.add_argument("--timed", action="store_true")

args = parser.parse_args()

factory = PlayerFactory()
player1 = factory.create_player(args.player1, "Player 1")
player2 = factory.create_player(args.player2, "Player 2")

game = Game(player1, player2)

if args.timed:
    game = TimedGameProxy(game)

game.play()