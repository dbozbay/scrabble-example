#  Should probably add some tests here, will save time over time.
#  Some typical games
#  Some extreme plays
import os
import json
from board import Move


#  Perhaps we would have a speed game where these moves are automatically inserted.


def save_game_instance(moves_file: str):
    from game import Scrabble
    from board import ScrabbleBoard
    from letters import Letters
    from input_checker import InputChecker
    import pandas as pd

    # To save final board after moves
    scrabble_board = ScrabbleBoard()
    input_checker = InputChecker()
    letters = Letters()
    scrabble_game = Scrabble(scrabble_board, input_checker, letters)

    df = pd.read_csv(moves_file)
    moves = []
    for idx, row in df.iterrows():
        move_conv = Move(row["starting_position"], row["hor"], row["word"])
        moves.append(move_conv)
    scrabble_game.play_auto(moves)
    scrabble_game.save_board_json()


def test_board():
    from game import Scrabble
    from board import ScrabbleBoard
    from letters import Letters
    from input_checker import InputChecker
    import pandas as pd

    # To save final board after moves

    # df = pd.read_csv("logged_games/game1/edge_game.csv")
    # moves = []
    # for idx, row in df.iterrows():
    #     move_conv = Move(row["starting_position"], row["hor"], row["word"])
    #     moves.append(move_conv)
    # scrabble_game.play_auto(moves)
    # scrabble_game.save_board_json()

    # To check final board (known) is consistent with moves
    testing_folder = "testing_games"
    for folder in os.listdir(testing_folder):
        scrabble_board = ScrabbleBoard("scrabble_words_for_testing.txt")
        input_checker = InputChecker()
        letters = Letters()
        scrabble_game = Scrabble(scrabble_board, input_checker, letters)
        print(folder)
        for file in os.listdir(testing_folder + "/" + folder):
            print(file)
            fpath = testing_folder + "/" + folder + "/" + file
            print(fpath)
            if file.endswith(".csv"):
                df = pd.read_csv(fpath)
            if file.endswith(".json"):
                with open(fpath, "r") as f:
                    expected_board = json.load(f)
        moves = []
        for idx, row in df.iterrows():
            move_conv = Move(row["starting_position"],
                             row["hor"], row["word"])
            moves.append(move_conv)
        scrabble_game.play_auto(moves)
        assert scrabble_game.board.board == expected_board
