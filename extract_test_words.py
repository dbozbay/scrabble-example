import os
import pandas as pd


def extract_test_words():
    testing_folder = "testing_games"
    all_words = ""
    for folder in os.listdir(testing_folder):
        print(folder)
        for file in os.listdir(testing_folder + "/" + folder):
            print(file)
            fpath = testing_folder + "/" + folder + "/" + file
            print(fpath)
            if file.endswith(".csv"):
                df = pd.read_csv(fpath)
                all_words += df["word"].to_string(index=None)
        all_words += "\n"
    all_words = "\n".join([i.strip() for i in all_words.split("\n")])
    with open("scrabble_words_for_testing.txt", "w") as f:
        f.write(all_words)


extract_test_words()
