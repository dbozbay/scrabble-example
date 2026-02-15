import random
import copy
from word import Word
import json
from test_game import Move


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ScrabbleBoard():
    def __init__(self):
        # Scrabble boards are 15x15 generally,
        # reoresented by nested list
        self.board = [[str(i+j*15) for i in range(15)] for j in range(15)]
        self.hypo_board = self.board
        self.n_moves = 0
        self.middle = "112"  # Should start from the middle.
        self.mid_point = self.conv_idx_to_coords(int(self.middle))
        self.get_words()
        self.unique_words_found = []
        self.word_score = 0
        self.most_recent_move = Move(None, None, None)

    def get_words(self):
        with open("scrabble_words.txt") as f:
            self.all_words = f.read().split("\n")

    def conv_idx_to_coords(self, idx: int) -> tuple:
        return (idx // 15, idx % 15)

    def conv_coords_to_idx(self, coords: tuple) -> int:
        return coords[0]*15 + coords[1]

    def letter_in_pos(self, coords):
        return self.hypo_board[coords[0]][coords[1]]

    def down(self, coords):
        if self.down_edge(coords):
            return "999"
        return self.hypo_board[coords[0]+1][coords[1]]

    def up(self, coords):
        if self.up_edge(coords):
            return "999"
        return self.hypo_board[coords[0]-1][coords[1]]

    def left(self, coords):
        if self.left_edge(coords):
            return "999"
        return self.hypo_board[coords[0]][coords[1]-1]

    def right(self, coords):
        if self.right_edge(coords):
            return "999"
        return self.hypo_board[coords[0]][coords[1]+1]

    #  Edges checked so that no
    # accidental going outside list range.
    def right_edge(self, coords):
        if coords[1] == 14:
            return True
        return False

    def left_edge(self, coords):
        if coords[1] == 0:
            return True
        return False

    def up_edge(self, coords):
        if coords[0] == 0:
            return True
        return False

    def down_edge(self, coords):
        if coords[0] == 14:
            return True
        return False

    # def neighbouring_valid_coords(self, coords) -> list:
    #     coord_values = []
    #     row, col = coords[0],  coords[1]
    #     for i in [-1, 1]:
    #         for j in [-1, 1]:
    #             proposed_row = row + i
    #             proposed_col = col + j
    #             if proposed_col == -1 or proposed_row == 15:
    #                 continue
    #             if proposed_row == -1 or proposed_row == 15:
    #                 continue
    #             coord_values.append()

    def find_neighbours(self, coords: tuple, start: tuple, hor: bool, end: tuple) -> list:
        if max(coords) < 14 and min(coords) > 0:
            if coords == start:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.up(coords),
                        self.left(coords)
                    ]
                else:
                    return [
                        self.right(coords),
                        self.left(coords),
                        self.up(coords)
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.up(coords),
                        self.right(coords)
                    ]
                else:
                    return [
                        self.down(coords),
                        self.left(coords),
                        self.right(coords)
                    ]
            else:
                if hor:
                    return [self.down(coords),
                            self.up(coords),
                            ]
                else:
                    return [
                        self.right(coords),
                        self.left(coords)
                    ]
        elif coords[0] == 0 and coords[1] != 0:
            # The tile is placed in the top row so coords[0]-1 would no longer be possible.
            if coords == start:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.left(coords),
                    ]
                else:
                    return [
                        self.right(coords),
                        self.left(coords),
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.right(coords)
                    ]
                else:
                    return [
                        self.right(coords),
                        self.left(coords),
                        self.down(coords),
                    ]
            else:
                if hor:
                    return [self.down(coords)
                            ]
                else:
                    return [
                        self.right(coords),
                        self.left(coords),
                    ]
        elif coords[0] != 0 and coords[1] == 0:
            # The tile is placed in the left most edge,
            # so coords[1] -1 would now be impossible.
            if coords == start:
                if hor:
                    return [
                        self.down(coords),
                        self.up(coords),
                    ]
                else:
                    return [
                        self.right(coords),
                        self.up(coords)
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.up(coords),
                        self.right(coords),
                    ]
                else:
                    return [
                        self.right(coords),
                        self.down(coords),
                    ]
            else:
                if hor:
                    return [self.down(coords),
                            self.up(coords),
                            ]
                else:
                    return [
                        self.right(coords),
                    ]
        elif coords[0] == 14 and coords[1] != 14:
            # On the bottom row of the board, but not in a corner.
            # Now coords[0]+1 would be impossible.
            if coords == start:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.up(coords),
                        self.left(coords),
                    ]
                else:
                    return [
                        self.right(coords),
                        self.left(coords),
                        self.up(coords)
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.up(coords),
                        self.right(coords)
                    ]
                else:
                    return [
                        self.right(coords),
                        self.left(coords),
                    ]
            else:
                if hor:
                    return [
                        self.up(coords),
                    ]
                else:
                    return [
                        self.right(coords),
                        self.left(coords),
                    ]
        elif coords[0] != 14 and coords[1] == 14:
            # Now on the right edge, this means
            # coords[1]+1 will be impossible
            if coords == start:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.up(coords),
                        self.left(coords),
                    ]
                else:
                    return [
                        self.left(coords),
                        self.up(coords)
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.up(coords),
                    ]
                else:
                    return [
                        self.left(coords),
                        self.down(coords),
                    ]
            else:
                if hor:
                    return [self.down(coords),
                            self.up(coords),
                            ]
                else:
                    return [
                        self.left(coords),
                    ]
        # Can consider corners now
        elif coords[0] == 14 and coords[1] == 0:
            # Now coords[0]+1, coords[1]-1 impossible
            if coords == start:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.up(coords),
                    ]
                else:
                    return [
                        self.right(coords),
                        self.up(coords)
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.up(coords),
                        self.right(coords)
                    ]
                else:
                    return [
                        self.right(coords),
                    ]
            else:
                if hor:
                    return [
                        self.up(coords),
                    ]
                else:
                    return [
                        self.right(coords),
                    ]
        elif coords[0] == 14 and coords[1] == 14:
            if coords == start:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.up(coords),
                        self.left(coords),
                    ]
                else:
                    return [
                        self.left(coords),
                        self.up(coords)
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.up(coords),
                    ]
                else:
                    return [
                        self.left(coords),
                    ]
            else:
                if hor:
                    return [
                        self.up(coords),
                    ]
                else:
                    return [
                        self.left(coords),
                    ]
        elif coords[0] == 0 and coords[1] == 14:
            if coords == start:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.left(coords),
                    ]
                else:
                    return [
                        self.left(coords),
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords)
                    ]
                else:
                    return [
                        self.left(coords),
                        self.down(coords),
                    ]
            else:
                if hor:
                    return [self.down(coords)
                            ]
                else:
                    return [
                        self.left(coords),
                    ]
        else:
            # This is 0,0, top right corner. no -1 anywhere.
            if coords == start:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords)
                    ]
                else:
                    return [
                        self.right(coords),
                    ]
            elif coords == end:
                # 3 possible touch points at the start and at the end
                if hor:
                    return [
                        self.down(coords),
                        self.right(coords)
                    ]
                else:
                    return [
                        self.right(coords),
                        self.down(coords),
                    ]
            else:
                if hor:
                    return [self.down(coords)
                            ]
                else:
                    return [
                        self.right(coords),
                    ]

    def display_board(self):
        print("\n"*4)
        for line in self.board:
            for element in line:
                if element.isalpha():
                    # adds the purple colour to the letter.
                    print(f"\033[95m    {element}\033[0m".rjust(5), end="|")
                else:
                    print(element.rjust(5), end="|")
            print("\n" + "-"*100)
        print("\n"*4)

    def gain_word_from_letter(self, coords):
        # This lets us see if the word is going vertically or horizontally
        # If the word is going horizontally then we should expect to see another letter left/right
        # If the word is going vertically then we should expect to see another letter up/down
        # It might go both ways
        words = ["", ""]
        coords_orig = list(coords).copy()
        coords = list(coords)
        word_coords = []
        if self.left(coords).isalpha() or self.right(coords).isalpha():
            while self.left(coords).isalpha():
                coords[1] = coords[1] - 1
            word_coords.append(coords.copy())
            words[0] += self.letter_in_pos(coords)
            while self.right(coords).isalpha():
                words[0] += self.right(coords)
                coords[1] = coords[1] + 1
            pass

        coords = coords_orig
        if self.up(coords).isalpha() or self.down(coords).isalpha():
            # Word is vertical
            while self.up(coords).isalpha():
                coords[0] = coords[0] - 1
            word_coords.append(coords.copy())
            words[1] += self.letter_in_pos(coords)
            while self.down(coords).isalpha():
                words[1] += self.down(coords)
                coords[0] = coords[0] + 1
        return [words, word_coords, [True, False]]

    def try_word(self, start: int, hor: bool, word: str) -> bool:
        self.hor = hor
        word = word.upper()
        self.req_letters = []
        all_additional_words = []
        found_some_neighbours = False
        passes_through_middle = False

        # Say for example "NOTEBOOK"
        corresp_row, corresp_column = self.conv_idx_to_coords(start)
        start_coords = (corresp_row, corresp_column)
        self.hypo_board = copy.deepcopy(self.board)
        if hor:
            end_coords = (corresp_row, corresp_column + len(word)-1)
        else:
            end_coords = (corresp_row + len(word)-1, corresp_column)
        if max(end_coords) > 14:
            return False, f"The word will go out of the board! {end_coords}"
        for i, char in enumerate(word):
            #  We need to check for overlaps
            if hor:
                board_idx = (corresp_row, corresp_column + i)
            else:
                board_idx = (corresp_row + i, corresp_column)
            if board_idx == self.mid_point:
                passes_through_middle = True
            selected_board_piece = self.hypo_board[board_idx[0]][board_idx[1]]
            if selected_board_piece != char and selected_board_piece.isalpha():
                return False, "Overlapping an original letter"
            if selected_board_piece != char:
                self.req_letters.append(char)
            # Now we know that this has to come from our hand.
            self.hypo_board[board_idx[0]][board_idx[1]] = char
        for i in range(len(word)):
            if hor:
                letter_row = corresp_row
                letter_col = corresp_column + i
            else:
                letter_row = corresp_row + i
                letter_col = corresp_column
            for neighbour in self.find_neighbours((letter_row, letter_col), start_coords, hor, end_coords):
                if neighbour.isalpha():
                    neighbouring_words_all_info = self.gain_word_from_letter(
                        (letter_row, letter_col))
                    found_some_neighbours = True
                    validation_check = self.validation_check(
                        neighbouring_words_all_info[0])
                    if not validation_check[0]:
                        # This move would be illegal
                        return False, f"Invalid word found ({validation_check[1]})"
                    additional_words = self.turn_to_words(
                        neighbouring_words_all_info)
                    #  Check for uniqueness. If not unique, add them to the set of words
                    all_additional_words.extend(additional_words)

        if not found_some_neighbours and not passes_through_middle:
            return False, "Word is unconnected"
        #  Point system needs fixing
        current_word = Word(word=word, start_pos=start, orientation=hor)
        self.word_score = current_word.get_score_unique()
        self.unique_words_found.append(current_word)

        self.check_words_for_uniqueness(all_additional_words)
        for added_word in all_additional_words:
            # That means this is fresh.
            if added_word.new:
                self.unique_words_found.append(added_word)
                word_score = added_word.get_score_unique()
                print(f"{word_score} points for {added_word.word}")
                self.word_score += added_word.get_score_unique()
        return True, "Word is playable.", self.word_score

    def turn_to_words(self, collection_of_words: list[list]) -> list[Word]:
        """


        :param self: the scrabble board
        :param collection_of_words: a list of lists which look like [[words] [positions] [orientations]]
        :type collection_of_words: list[list]
        """
        words_list = []
        for i in range(len(collection_of_words[0])):
            words_list.append(self.turn_to_word(
                collection_of_words[0][i], self.conv_coords_to_idx(collection_of_words[1][i]), collection_of_words[2][i]))
        return words_list

    def turn_to_word(self, word, start_pos, orientation) -> Word:
        return Word(word, start_pos, orientation)

    def add_to_unique_words(self, word: Word):
        self.unique_words_found.append(word)

    def check_words_for_uniqueness(self, checking_words: list[Word]):
        for checking_word in checking_words:
            self.check_word_for_uniqueness(checking_word)

    def check_word_for_uniqueness(self, checking_word: Word):
        if checking_word == "":
            checking_word.new = False
        for word in self.unique_words_found:
            if word.word == checking_word.word and word.start_pos == checking_word.start_pos and word.orientation == checking_word.orientation:
                checking_word.new = False
        return True

    def insert_word(self, start: int, hor: bool, word: str):
        word = word.upper()
        corresp_row, corresp_column = self.conv_idx_to_coords(start)
        for i, char in enumerate(word):
            if hor:
                self.board[corresp_row][corresp_column + i] = char
            else:
                self.board[corresp_row + i][corresp_column] = char
        self.most_recent_move.update(pos=start, orientation=hor, word=word)

    def input_word(self, start: int, hor: bool, word: str):
        outcome = self.try_word(start, hor, word)
        if outcome[0]:
            # self.insert_word(start, hor, word)
            return True
        else:
            print(outcome[1])
            return False

    def validation_check(self, word_list: list):
        # Check all words formed are valid words
        for word in word_list:
            if word not in self.all_words:
                return False, word
        return True, "words passed"


if __name__ == "__main__":
    scrabble_board = ScrabbleBoard()
    scrabble_board.display_board()
    # inserting alpha at the start and beta at some point.
    scrabble_board.input_word(110, True, "alpha")
    scrabble_board.input_word(67, False, "peters")
    # scrabble_board.insert_word(51, False, "lalala")
    print(scrabble_board.letter_in_pos(scrabble_board.conv_idx_to_coords(66)))
