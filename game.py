from board import ScrabbleBoard
from input_checker import InputChecker
from letters import Letters
import json
import random


class Scrabble():
    def __init__(self, board: ScrabbleBoard, checker: InputChecker):
        print("PLAYING SCRABBLE")
        with open("game_info.json", "r") as f:
            game_info = json.load(f)
        self.board = board
        self.checker = checker
        self.score_dict = game_info["points"]
        self.curr_player = None
        self.players = []
        self.n_players = len(self.players)  # 0

    def start_names(self):
        while not self.checker.validate_n_players():
            self.n_players = input(
                "How many players do you want to play [2-4]? ")
            self.checker.user_in = self.n_players
        self.n_players = int(self.n_players)
        for i in range(self.n_players):
            player_name = input(f"Please insert player {i} name: ")
            if player_name.strip() == "":
                self.players.append(f"Player {i+1}")
            else:
                self.players.append(player_name)
        print(self.players)

    def take_input(self):
        slot_valid, hor_valid, word_valid = None, None, None

        while not slot_valid:
            self.slot = input("Please insert your starting point (0-224): ")
            self.checker.user_in = self.slot
            slot_valid = self.checker.validate_input_slot()
        while not hor_valid:
            self.hor_vert = input(
                "Please specify if the word is vertical (v) or horizontal (h): ")
            self.checker.user_in = self.hor_vert
            hor_valid = self.checker.validate_hor()
        while not word_valid:
            self.word_input = input("Please enter your word: ")
            self.checker.user_in = self.word_input
            word_valid = self.checker.validate_word_input()

    def word_score(self, player):
        total_score = 0
        for char in self.word_input:
            total_score += self.score_dict[char]
        return total_score

    def play(self):
        print("starting game")
        self.start_names()
        i = 0
        while i < 15:
            self.curr_player = self.players[i % self.n_players]
            print(f"{self.curr_player}'s turn")
            self.take_input()
            i += 1

    def get_letter(self):
        # Take a random letter from the letters list and return it
        random.shuffle(self.letters)
        return self.letters.pop()


board = ScrabbleBoard()
input_checker = InputChecker()

if __name__ == "__main__":
    scrabble_example = Scrabble(board, input_checker)
    scrabble_example.play()
