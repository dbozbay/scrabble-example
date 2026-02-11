import random
import copy


class ScrabbleBoard():
    def __init__(self):
        # Scrabble boards are 15x15 generally,
        # reoresented by nested list
        self.board = [[str(i+j*15) for i in range(15)] for j in range(15)]
        self.hypo_board = self.board
        self.n_moves = 0
        self.middle = "112"  # Should start from the middle.
        self.get_words()

    def get_words(self):
        with open("scrabble_words.txt") as f:
            self.all_words = f.read().split("\n")

    def conv_idx_to_coords(self, idx):
        return (idx // 15, idx % 15)

    def letter_in_pos(self, coords):
        return self.hypo_board[coords[0]][coords[1]]

    def down(self, coords):
        return self.hypo_board[coords[0]+1][coords[1]]

    def up(self, coords):
        return self.hypo_board[coords[0]-1][coords[1]]

    def left(self, coords):
        return self.hypo_board[coords[0]][coords[1]-1]

    def right(self, coords):
        return self.hypo_board[coords[0]][coords[1]+1]

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
        for line in self.board:
            for element in line:
                if element.isalpha():
                    # adds the purple colour to the letter.
                    print(f"\033[95m    {element}\033[0m".rjust(5), end="|")
                else:
                    print(element.rjust(5), end="|")
            print("\n" + "-"*100)

    def gain_word_from_letter(self, coords):
        # This lets us see if the word is going vertically or horizontally
        # If the word is going horizontally then we should expect to see another letter left/right
        # If the word is going vertically then we should expect to see another letter up/down
        # It might go both
        words = ["", ""]
        coords_orig = list(coords).copy()
        coords = list(coords)
        if self.left(coords).isalpha() or self.right(coords).isalpha():
            # Word is horizontal
            print("Found horiz")
            while self.left(coords).isalpha():
                coords[1] = coords[1] - 1
            print(self.letter_in_pos(coords))
            words[0] += self.letter_in_pos(coords)
            while self.right(coords).isalpha():
                words[0] += self.right(coords)
                coords[1] = coords[1] + 1
                print(self.right(coords))
            pass
        coords = coords_orig
        if self.up(coords).isalpha() or self.down(coords).isalpha():
            # Word is vertical
            print("Found vertical")
            while self.up(coords).isalpha():
                print(self.up(coords))
                coords[0] = coords[0] - 1
            words[1] += self.letter_in_pos(coords)
            while self.down(coords).isalpha():
                words[1] += self.down(coords)
                coords[0] = coords[0] + 1
        return words

    def try_word(self, start: int, hor: bool, word: str) -> bool:
        word = word.upper()
        corresp_row, corresp_column = self.conv_idx_to_coords(start)
        start_coords = (corresp_row, corresp_column)
        self.hypo_board = copy.deepcopy(self.board)
        if hor:
            end_coords = (corresp_row, corresp_column + len(word))
        else:
            end_coords = (corresp_row + len(word), corresp_column)
        if max(end_coords) > 14:
            return False, "The word will go out of the board!"
        for i, char in enumerate(word):
            if hor:
                self.hypo_board[corresp_row][corresp_column + i] = char
            else:
                self.hypo_board[corresp_row + i][corresp_column] = char
        for i in range(len(word)):
            if hor:
                letter_row = corresp_row
                letter_col = corresp_column + i
            else:
                letter_row = corresp_row + i
                letter_col = corresp_column
            for neighbour in self.find_neighbours((letter_row, letter_col), start_coords, hor, end_coords):
                if neighbour.isalpha():
                    print(f"Found neighbouring {neighbour}")
                    neighbouring_words = self.gain_word_from_letter(
                        (letter_row, letter_col))
                    print(neighbouring_words)
                    validation_check = self.validation_check(
                        neighbouring_words)
                    if not validation_check[0]:
                        # This move would be illegal
                        return False, f"Invalid word found ({validation_check[1]})"
        return True, "Word is playable."

    def insert_word(self, start: int, hor: bool, word: str):
        word = word.upper()
        corresp_row, corresp_column = self.conv_idx_to_coords(start)
        for i, char in enumerate(word):
            if hor:
                self.board[corresp_row][corresp_column + i] = char
            else:
                self.board[corresp_row + i][corresp_column] = char

    def input_word(self, start: int, hor: bool, word: str):
        outcome = self.try_word(start, hor, word)
        self.display_board()
        print(outcome[0])
        if outcome[0]:
            self.insert_word(start, hor, word)
        else:
            print(outcome[1])
        scrabble_board.display_board()

    def validation_check(self, word_list: list):
        # Check all words formed are valid words
        print(f"checking words {word_list}")
        for word in word_list:
            print(f"checking {word}")
            if word not in self.all_words:
                return False, word
        return True, "words passed"


if __name__ == "__main__":
    scrabble_board = ScrabbleBoard(None)
    scrabble_board.display_board()
    # inserting alpha at the start and beta at some point.
    scrabble_board.input_word(34, True, "alpha")
    scrabble_board.input_word(50, False, "psers")
    # scrabble_board.insert_word(51, False, "lalala")
    print(scrabble_board.letter_in_pos(scrabble_board.conv_idx_to_coords(66)))
