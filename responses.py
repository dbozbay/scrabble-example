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


class Response():
    def __init__(self, message: str = None, prefix: str = None, colour=bcolors.OKBLUE, status: bool = True):
        print("PEWWWW")
        self.colour = colour  #  By default
        self.message = message
        self.prefix = prefix
        self.ending = bcolors.ENDC
        self.status = status
        if None not in (self.colour, self.message, self.prefix, self.ending):
            self.full_msg = self.colour + self.prefix + " " + self.message + self.ending

    def display_response(self):
        self.full_msg = self.colour + self.prefix + " " + self.message + self.ending
        print(self.full_msg)


class Mistake(Response):
    def __init__(self, message: str):
        super().__init__(message, prefix="OH NO!", colour=bcolors.FAIL)


class Instruction(Response):
    def __init__(self, message: str):
        super().__init__(message, prefix="Instruction:",
                         colour=bcolors.OKGREEN)


class Note(Response):
    def __init__(self, message: str):
        super().__init__(message, prefix="NOTE:", colour=bcolors.OKCYAN)


class Question(Response):
    def __init__(self, message: str):
        super().__init__(message, prefix="Instruction:",
                         colour=bcolors.OKBLUE)
