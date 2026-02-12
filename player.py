class Player():
    def __init__(self, name: str = "", score: int = 0, letters: list = []):
        self.name = name
        self.score = score
        self.letters = letters

    def __str__(self):
        # Ideally each person should not be able to see the other person's letters.
        return f"""
        Player: {self.name}
        Score : {self.score}
        Letters: {self.letters}
        """
