# main.py
import argparse
import time
from player_factory import PlayerFactory
from timed_game_proxy import TimedGameProxy
from player import Player, HumanPlayer, ComputerPlayer
import random

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