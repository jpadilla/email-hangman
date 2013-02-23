import random


class Hangman(object):

    def __init__(self, word):
        self.word = word
        self.length = len(self.word.strip())
        self.keys = ['_' for x in xrange(self.length)]
        self.insert_random(self.length)

    def insert_random(self, length):
        randint = random.randint

        # 3 hints
        if length >= 7:
            hint = 3
        else:
            hint = 1

        for x in xrange(hint):
            a = randint(1, length - 1)
            self.keys[a - 1] = self.word[a - 1]


def generate_ascii(mistakes):
    if mistakes == 1:
        ascii_message = """
        ___________
        |         |
        |         0
        |
        |
        |
        |
        __
        """
    elif mistakes == 2:
        ascii_message = """
        ___________
        |         |
        |         0
        |         |
        |
        |
        |
        __
        """
    elif mistakes == 3:
        ascii_message = """
        ___________
        |         |
        |         0
        |        /|
        |
        |
        |
        __
        """
    elif mistakes == 4:
        ascii_message = """
        ___________
        |         |
        |         0
        |        /|\\
        |
        |
        |
        __
        """
    elif mistakes == 5:
        ascii_message = """
        ___________
        |         |
        |         0
        |        /|\\
        |        /
        |
        |
        __
        """
    elif mistakes == 6:
        ascii_message = """
        ___________
        |         |
        |         0
        |        /|\\
        |        / \\
        |
        |
        __
        """
    else:
        ascii_message = """
        ___________
        |         |
        |
        |
        |
        |
        |
        __
        """

    return ascii_message
