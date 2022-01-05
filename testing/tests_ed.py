import unittest

from wordle_solver import solver, english_dictionary as ed

class ed_loading_test_long_dict(unittest.TestCase):
    def setUp(self):
        self.english_dict = ed.english_dictionary("5_letter_words_ver.2.txt")

    def test_first_word(self):
        self.assertEqual(self.english_dict.words_list[0], "aahed")

    def test_length(self):
        self.assertEqual(len(self.english_dict.words_list), 12478)

class ed_methods_test_26_dict(unittest.TestCase):
    def setUp(self):
        self.english_dict = ed.english_dictionary("5_letter_words_26_words.txt")

    def test_words_by_letter(self):
        words_by_letter = self.english_dict.words_by_letter()
        
        self.assertEqual(words_by_letter['a'], {"admen", "bandy", "darcy", "haver", "ideas", "jarps", "kulas", "ratch", "saute", "ulema", "waist"})
        self.assertEqual(words_by_letter['b'], {"bandy", "xebec"})
        self.assertEqual(words_by_letter['c'], {"coxed", "ratch", "xebec"})
        self.assertEqual(words_by_letter['d'], {"admen", "bandy", "coxed", "darcy", "edges"})
        self.assertEqual(words_by_letter['e'], {"admen", "coxed", "edges", "ideas", "lunet", "ozzie", "quine", "saute", "ulema", "xebec"})
        self.assertEqual(words_by_letter['f'], {"foins"})
        self.assertEqual(words_by_letter['g'], {})

if __name__ == "__main__":
    unittest.main()