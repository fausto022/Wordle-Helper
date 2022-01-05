import unittest
from wordle_solver.solver import solver

class word_choosing(unittest.TestCase):
    def setUp(self):
        self.main_solver = solver("5_letter_words_ver.2.txt")

    def test_choose_word_1(self):
        self.assertEqual(self.main_solver.choose_word(), )

if __name__ == '__main__':
    unittest.main()
