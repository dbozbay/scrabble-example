

class InputChecker():
    def __init__(self, initial_in: str = None):
        self.user_in = initial_in
        pass

    def validate_input_slot(self):
        try:
            # number should be able to turn into int
            slot_int = int(self.user_in)
        except:
            return False
        if slot_int > 224 or slot_int < 0:
            # number should be in board range
            return False
        return True

    def validate_hor(self):
        if self.user_in.lower() in ("h", "v"):
            return True

    def validate_word_input(self):
        if self.user_in.isalpha():
            # shouldn't contain any digits.
            return True

    def validate_n_players(self):
        try:
            self.n_players = int(self.user_in)
        except:
            return False
        if self.n_players < 2 or self.n_players > 4:
            return False
        return True
