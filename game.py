from board import ScrabbleBoard


class Scrabble():
    def __init__(self, board: ScrabbleBoard):
        pass

    def validate_input_slot(self):
        try:
            # number should be able to turn into int
            slot_int = int(self.slot)
        except:
            return False
        if slot_int > 224 or slot_int < 0:
            # number should be in board range
            return False
        return True

    def validate_hor(self):
        if self.hor_vert.lower() in ("h", "v"):
            return True

    def validate_word_input(self):
        if self.word_input.isalpha():
            # shouldn't contain any digits.
            return True

    def take_input(self, player):
        print(f"{player}'s turn.")
        slot_valid, hor_valid, word_valid = None, None, None

        while not slot_valid:
            self.slot = input("Please insert your starting point (0-224): ")
            slot_valid = self.validate_input_slot()
        while not hor_valid:
            self.hor_vert = input(
                "Please specify if the word is vertical (v) or horizontal (h): ")
            hor_valid = self.validate_hor()
        while not word_valid:
            self.word_input = input("Please enter your word: ")
            word_valid = self.validate_word_input()


if __name__ == "__main__":
    scrabble_example = Scrabble(board=None)
    scrabble_example.take_input("Talha")
