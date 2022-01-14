from wordle_solver import english_dictionary as e_d
from enum import Enum


(gray, yellow, green) = (0, 1, 2)
class solver():
    """Provides the methods to find the optimal word, and a list of all the possible words."""
    def __init__(self, dictionary_file: str):
        self._e_d = e_d.english_dictionary(dictionary_file)
        self._greens = {0: '', 1: '', 2: '', 3: '', 4: ''}
        self._yellows = {0: [], 1: [], 2: [], 3: [], 4: []}
        self._all_yellows = set()
        self._discarded = set()
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
        if any(l not in word for l in self._all_yellows): valid_word = False
        
        return valid_word
        
    def add_guess(self, guess: list[dict[chr, int]]) -> None:
        """Process the information coming from this new guess. This function also applies different
        heuristics/inferences I came up with to further narrow the information provided by each guess.
        Automatically updates the list of valid words.
        """
        for i, t in enumerate(guess):
            l = t['l']
            col = t['c']
            if col == green:
                self._greens[i] = l
            elif col == yellow:
                self._yellows[i].append(l)
                self._all_yellows.add(l) #I'm keeping a separate list of yellows so I don't have to flatten the self._yellows list
            elif col == gray:
                self._discarded = self._discarded | set(l)

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
            if (letter not in self._greens.values()) and (letter not in self._all_yellows):
                words_it_affects = words_it_affects | words_by_letter[letter]
        return len(words_it_affects)

    def choose_word(self) -> str:
        """ 
        """
        #create a dictionary of the form {char: list[word]}, to see which letter maps to which of the remaining valid words.       
        words_x_letter = self._e_d.words_by_letter(self.valid_words)
        best_exploratory_word = max(self._e_d.words_list, key=lambda x: self._how_many_discards(words_x_letter, x))
        best_valid_word = max(self.valid_words, key=lambda x: self._how_many_discards(words_x_letter, x))        
        return best_exploratory_word, best_valid_word