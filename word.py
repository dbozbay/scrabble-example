import json


class Word():
    def __init__(self, word, start_pos, orientation):
        self.word = word
        self.start_pos = start_pos
        self.orientation = orientation
        self.new = True

    def load_score(self):
        with open("game_info.json", "r") as f:
            game_info = json.load(f)
            self.score_dict = game_info["points"]

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
