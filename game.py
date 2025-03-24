# game.py
import time
import timed_game_proxy  # Correct import

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
            if isinstance(self, timed_game_proxy.TimedGameProxy) and time.time() - self.start_time > 60:
                self.determine_timed_winner()
                return

        winner = self.player1 if self.player1.score >= 100 else self.player2
        print(f"\n{winner.name} wins!")