from wordle_solver import english_dictionary as e_d
from wordle_solver import lists
from enum import Enum



class wordle_solver():
    """Provides the methods to find the optimal word, and a list of all the possible words."""

    def __init__(self, path: str=''): #TODO: add path functionality.
        self._e_d = e_d.english_dictionary()
        self._greens = {1: '', 2: '', 3: '', 4: '', 5: ''}
        self._yellows = {1: [], 2: [], 3: [], 4: [], 5: []}
        self._discarded = []
        self._valid_words = self._e_d.words_list

    def is_valid(self, word) -> bool:
        """Given a word, checks if it could be a possible correct answer."""
        valid_word = True
        for i, l in enumerate(word):
            # for the word to be valid, all letters have to be valid.
            if self._greens[i] != '':
                valid_letter = (l == self._greens[i])
            else:
                valid_letter = l not in self._yellows[i] and l not in self._discarded
            valid_word = valid_word and valid_letter 
        return valid_word
        
    def add_guess(self, greens: str, yellows: str, grays: str) -> None:
        """Process the information coming from this new guess. This function also applies different
        heuristics/inferences I came up with to further narrow the information provided by each guess.
        Automatically updates the list of valid words.
        """
        #TODO: Implement heuristics/inferences.
        #TODO: Explain said heuristics/inferences in the README.
        for k, l in enumerate(greens):
            if l != '_':self._greens[k] = l
        for k, l in enumerate(yellows):
            if l != '_':self._yellows[k].append(l)
        self._discarded = self._discarded + list(grays)
        self._filter_words()

    def _filter_words(self) -> None:
        """Update the list of all valid words with the current information."""
        self._valid_words = [word for word in self._valid_words if self.is_valid(word)]

    def choose_word(self, valid_words: bool = None) -> str:
        """ 
        """
        # TODO: rethink the working of this function.
        # For if you want to print BOTH best words (the valid and the non valid) you would have to run this function TWICE, which is not optimal.
        if valid_words:valid_words = self._valid_words
        words_x_letter = self._e_d.words_by_letter(valid_words)
        best_word = max(words_x_letter.keys(), key=lambda x: words_x_letter[x])
        return best_word