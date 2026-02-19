

class Word:
    def __init__(self, word, start_pos, orientation):
        self.word = word
        self.start_pos = start_pos
        self.orientation = orientation
        self.new = True
        self.score_dict = {
            "A": 1,
            "B": 3,
            "C": 3,
            "D": 3,
            "E": 1,
            "F": 4,
            "G": 3,
            "H": 4,
            "I": 1,
            "J": 8,
            "K": 5,
            "L": 2,
            "M": 3,
            "N": 1,
            "O": 1,
            "P": 3,
            "Q": 10,
            "R": 1,
            "S": 1,
            "T": 1,
            "U": 1,
            "V": 4,
            "W": 4,
            "X": 8,
            "Y": 4,
            "Z": 10,
        }

    def __str__(self):
        return f"word: {self.word}, start: {self.start_pos}, orientation: {self.orientation}"

    def get_score(self) -> int:
        # TODO: Try and incorporate 2x letter, 3x word tiles etc
        #  By combining placed points.
        total_score = 0
        for char in self.word:
            total_score += self.score_dict[char]
        return total_score

    def get_score_unique(self) -> int:
        if self.new:
            return self.get_score()
        return 0
