

#  Should probably add some tests here, will save time over time.
#  Some typical games
#  Some extreme plays


class Move():
    def __init__(self, pos: int, orientation: bool, word: str):
        pass

    def update(self, pos: int, orientation: bool, word: str):
        self.pos = pos
        self.orientation = orientation
        self.word = word

#  Perhaps we would have a speed game where these moves are automatically inserted.


if __name__ == "__main__":
    from game import Scrabble
    from board import ScrabbleBoard
    from player import Player
    from letters import Letters
    from input_checker import InputChecker

    scrabble_board = ScrabbleBoard()
    input_checker = InputChecker()
    letters = Letters()
    scrabble_game = Scrabble(scrabble_board, input_checker, letters)
