import string

class words():
    """handles all the relevant information from an english dictionary."""

    def __init__(self):
        """Reads the dictionary from memory, and stores its contents.
        Also gets the alphabet from the string library.
        """
        #TODO: Add path functionality.
        self._alphabet = string.ascii_lowercase # 26 letters from the english alphabet, in [chr] format.

        #Reads a dictionary from memory.
        with open("data/5_letters_allowed.txt", "r") as f:
            self.allowed = f.read().split('\n')

        with open("data/5_letters_answers.txt", "r") as f:
            self.answers = f.read().split('\n')

    def answers_by_letter(self, words: list[str] = None) -> dict[chr: set()]:
        """Takes in a list of words, and returns a dictonary mapping each letter of the alphabet to a set
        of the words in the list that contain that letter.
        """
        if not words:
            words = self.words_list
        words_by_letter = dict.fromkeys(self._alphabet, set())
        for word in words:
            for letter in word:
                words_by_letter[letter] = words_by_letter[letter] | {word}
        return words_by_letter