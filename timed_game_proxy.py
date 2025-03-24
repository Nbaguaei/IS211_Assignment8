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