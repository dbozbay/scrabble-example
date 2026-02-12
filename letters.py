import random


class Letter():
    def __init__(self):
        pass


class Letters():
    def __init__(self, tile_collection: dict = None, max_letters_on_hand: int = 7):
        self.max_letters_on_hand = max_letters_on_hand
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
        self.pickup_tiles = [tile
                             for tile in self.tiles for i in range(self.tiles[tile])]
        print(self.pickup_tiles)

    def pick_up_letters(self, current_letters: list):
        print(f"current letters: {current_letters}")
        while len(current_letters) < self.max_letters_on_hand and self.pickup_tiles:
            random.shuffle(self.pickup_tiles)
            current_letters.append(self.pickup_tiles.pop())
        return current_letters

    def get_word_score(self, word):
        total_score = 0
        for char in word:
            total_score += self.score_dict[char]
        return total_score

    def replace_all_letters(self, current_letters: list):
        # Give all letters back to pile, and grab some new ones
        number_of_letters = len(current_letters)
        for i in range(number_of_letters):
            # take each letter out of current letters and put in pickup tiles
            self.pickup_tiles.append(current_letters.pop())
        return self.pick_up_letters(current_letters=current_letters)

    def show_current_letters(self, letters: list):
        print(letters)
