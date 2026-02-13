from board import ScrabbleBoard
from input_checker import InputChecker
from letters import Letters
from player import Player
import json
import random
import copy
#  "pip install pandas" if this doesn't exist
import pandas as pd
import os


class Scrabble():
    def __init__(self, board: ScrabbleBoard, checker: InputChecker, letters_collection: Letters, log: bool = True):
        print("PLAYING SCRABBLE")

        self.board = board
        self.checker = checker
        self.letters = letters_collection
        self.log = log
        self.all_moves = []

        self.curr_player = None
        self.players = []
        self.n_players = len(self.players)  # 0
        #  player score and whatever letters they might have.
        self.save_path = None
        if log:
            self.find_unique_filename()

    def find_unique_filename(self):
        possible_fname = "logged_games/game.csv"
        i = 0
        while os.path.isfile(possible_fname):
            i += 1
            possible_fname = f"logged_games/game{i}.csv"
        self.save_path = possible_fname
        self.header = True

    def start_names(self):
        while not self.checker.validate_n_players():
            self.n_players = input(
                "How many players do you want to play [2-4]? ")
            self.checker.user_in = self.n_players
        self.n_players = int(self.n_players)
        for i in range(self.n_players):
            player_name = input(f"Please insert player {i} name: ")
            if player_name.strip() == "":
                player_name = f"Player {i+1}"
            self.players.append(Player(name=player_name))

    def take_input(self) -> str | None:
        slot_valid, hor_valid, word_valid = None, None, None

        while not slot_valid:
            print("NOTE: If trying to fill a word with existing letters,"
                  "type the full word in e.g. placing 'g' in 'e(g)g', type 'egg'")
            self.slot = input(
                "Please insert your starting point (0-224) or 'swap' to swap tiles: ").strip()
            self.checker.user_in = self.slot
            slot_valid = self.checker.validate_input_slot()
            if self.slot == "swap":
                return self.slot

        self.slot = int(self.slot)
        while not hor_valid:
            self.hor_vert = input(
                "Please specify if the word is vertical (v) or horizontal (h): ").strip()
            self.checker.user_in = self.hor_vert
            hor_valid = self.checker.validate_hor()
        self.hor_input = False if self.hor_vert == "v" else True
        while not word_valid:
            self.word_input = input("Please enter your word: ").strip()
            self.checker.user_in = self.word_input
            word_valid = self.checker.validate_word_input()

    def take_letters(self):
        # It will pick up letters based on the current player's letters
        current_player_letters = self.curr_player.letters.copy()
        # Copy is necessary as otherwise will overwrite letters
        # for all players
        self.curr_player.letters = self.letters.pick_up_letters(
            current_player_letters)

    def place_letters(self):
        for letter in self.board.req_letters:
            print(letter)
            self.curr_player.letters.remove(letter.upper())
        self.board.insert_word(self.slot, self.hor_input, self.word_input)

    def take_turn(self):
        print(f"{self.curr_player.name}'s turn")
        print(self.curr_player)
        move = self.take_input()
        #  Player can either play a word here or swap tiles
        if move == "swap":
            # Swap letters
            self.letters.replace_all_letters(
                self.curr_player.letters)
            return True
        if self.board.input_word(self.slot, self.hor_input, self.word_input):
            # Input found to be valid, but now we need to check if we have the relevant letters too
            player_letters = copy.deepcopy(self.curr_player.letters)
            for letter in self.board.req_letters:
                print(letter)
                if letter.upper() not in player_letters:
                    print(
                        f"You don't have those letters.")

                    return False
                player_letters.remove(letter)
            #  place_letters will place them on the board.
            self.place_letters()
            return True

    def play(self):
        print("starting game")
        self.start_names()
        i = 0
        while i < 15:
            self.curr_player = self.players[i % self.n_players]
            self.take_letters()
            self.board.display_board()
            if self.curr_player.letters:
                while not self.take_turn():
                    pass
                self.curr_player.score += self.board.word_score
                print(
                    f"{self.curr_player.name} is now on {self.curr_player.score} points")
                if self.log:
                    move_info = {
                        "word": [self.board.most_recent_move.word],
                        "hor": [self.board.most_recent_move.orientation],
                        "starting_position": [self.board.most_recent_move.pos]
                    }
                    mode = "w" if self.header else "a"
                    pd.DataFrame.from_dict(move_info).to_csv(
                        self.save_path, mode=mode, header=self.header, index=False)
                    self.header = False
            i += 1
        # Game has ended at this point

    def play_auto(self, moves: list):
        print("starting game")
        self.n_players = 2
        self.players = [Player("Player 1"), Player("Player 2")]
        i = 0
        while i < len(moves):
            # Probably put a bunch of
            # moves in here then can
            # check
            pass

    def get_letter(self):
        # Take a random letter from the letters list and return it
        random.shuffle(self.letters)
        return self.letters.pop()


board = ScrabbleBoard()
input_checker = InputChecker()
letters = Letters()

if __name__ == "__main__":
    scrabble_example = Scrabble(board, input_checker, letters)
    scrabble_example.play()
