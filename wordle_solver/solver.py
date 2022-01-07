from wordle_solver import english_dictionary as e_d
from enum import Enum



class solver():
    """Provides the methods to find the optimal word, and a list of all the possible words."""

    def __init__(self, dictionary_file: str): #TODO: add path functionality.
        self._e_d = e_d.english_dictionary(dictionary_file)
        self._greens = {0: '', 1: '', 2: '', 3: '', 4: ''}
        self._yellows = {0: [], 1: [], 2: [], 3: [], 4: []}
        self._discarded = []
        self.valid_words = self._e_d.words_list

    def _is_valid(self, word) -> bool:
        """Given a word, checks if it could be a possible correct answer."""
        valid_word = True
        for i, l in enumerate(word):
            # for the word to be valid, all letters have to be valid.
            if self._greens[i] != '':
                valid_letter = (l == self._greens[i])
            else:
                valid_letter = l not in self._yellows[i] and l not in self._discarded
            valid_word = valid_word and valid_letter
        
        for yellows_list in self._yellows.values():
            if any(l not in word for l in yellows_list): valid_word = False
        
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
        self.valid_words = [word for word in self.valid_words if self._is_valid(word)]
    
    def _how_many_discards(self, words_by_letter: dict[chr: list[str]],word: str) -> int:
        """Using the words_x_letter info, this function tells you how useful guessing a word would be, 
        based on how much its letters appear in the remaining possible words.
        """
        words_it_affects = set()
        for letter in word:
            has_yellow = False
            if any(letter in yellows_list for yellows_list in self._yellows.values()): has_yellow = True
            #TODO: optimize 'cus wtf
            if letter not in self._greens.values() and has_yellow == False:
                words_it_affects = words_it_affects | words_by_letter[letter]
        return len(words_it_affects)

    def choose_word(self, any_word: bool = True) -> str:
        """ 
        """
        # TODO: rethink the working of this function.
        # For if you want to print BOTH best words (the valid and the non valid) you would have to run this function TWICE, which is not optimal.

        #create a dictionary of the form {char: list[word]}, to see which letter maps to which of the remaining valid words.        
        words_x_letter = self._e_d.words_by_letter(self.valid_words)
        
        if any_word:
            words_to_choose_from = self._e_d.words_list
        else:
            words_to_choose_from = self.valid_words
        best_word = max(words_to_choose_from, key=lambda x: self._how_many_discards(words_x_letter, x))
        print(f"Affects {self._how_many_discards(words_x_letter, best_word)} words.")
        return best_word

    