from board import ScrabbleBoard
import json


class Scrabble():
    def __init__(self, board: ScrabbleBoard):
        print("PLAYING SCRABBLE")
        with open("game_info.json", "r") as f:
            game_info = json.load(f)
        self.score_dict = game_info["points"]
        self.curr_player = None
        self.players = []
        self.n_players = len(self.players)  # 0

    def start_names(self):
        while not self.validate_n_players():
            self.n_players = input(
                "How many players do you want to play [2-4]? ")

        for i in range(self.n_players):
            player_name = input(f"Please insert player {i} name: ")
            if player_name.strip() == "":
                self.players.append(f"Player {i+1}")
            else:
                self.players.append(player_name)
        print(self.players)

    def validate_n_players(self):
        try:
            self.n_players = int(self.n_players)
        except:
            return False
        if self.n_players < 2 or self.n_players > 4:
            return False
        return True

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

    def take_input(self):
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

    def word_score(self, player):
        total_score = 0
        for char in self.word_input:
            total_score += self.score_dict[char]
        return total_score

    def play(self):
        self.start_names()
        i = 0
        while i < 15:
            self.curr_player = self.players[i % self.n_players]
            print(f"{self.curr_player}'s turn")
            self.take_input()
            i += 1


if __name__ == "__main__":
    scrabble_example = Scrabble(board=None)
    scrabble_example.play()
