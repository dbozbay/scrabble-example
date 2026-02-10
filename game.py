from board import ScrabbleBoard

n_turns = 0
max_turns = 10

while n_turns < max_turns:
    n_turns += 1
    if n_turns % 2:
        user_input = input("Player 1: ")
    else:
        user_input = input("Player 2: ")


class Scrabble():
    def __init__(self, board: ScrabbleBoard):
        pass

    def validate_input_slot(slot_input: str):
        try:
            # number should be able to turn into int
            slot_int = int(slot_input)
        except:
            return False
        if slot_int > 224 or slot_int < 0:
            # number should be in board range
            return False
        return True

    def validate_hor(hor_input: str):
        if hor_input.lower() in ("h", "v"):
            return True

    def validate_word_input(word_input: str):
        if word_input.isalpha():
            # shouldn't contain any digits.
            return True

    def turn(self, player):
        print(f"{player}'s turn.")
        slot = input("Please insert your starting point (0-224): ")
        hor_vert = input(
            "Please specify if the word is vertical (v) or horizontal (h): ")
        word_input = input("Please enter your word: ")
