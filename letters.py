import random


class Letter():
    def __init__(self):
        pass


class Letters():
    def __init__(self, tile_collection: dict = None, max_letters_on_hand: int = 7):
        self.letters_on_hand = []
        if tile_collection:
            self.tiles = tile_collection
        # Otherwise, use default tile numbers
        self.tiles = {
            "A": 9, "B": 2, "C": 2, "D": 4, "E": 12,
            "F": 2, "G": 3, "H": 2, "I": 9, "J": 1,
            "K": 1, "L": 4, "M": 2, "N": 6, "O": 8,
            "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6,
            "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1
        }

    def pick_up_letters(self):
        while len(self.letters_on_hand) < 7:
