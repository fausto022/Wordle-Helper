"""Handles the prompting on the terminal, collects the user's data about their game, and runs the main loop of the program"""

from typing import Match
from wordle_solver import solver

def run_guessing_loop() -> int:
    """Runs the main loop for your wordle_helper"""
    options = """1)Show me the word with maximum coverage for the current info.
2)Show me the best guess with maximum coverage for the current info.
3)Show me a list of the possible guesses.
4)Keep guessing.
?)Help.
"""
    difference = """The difference between options 1) and 2), is that the first option will try to affect as many remaining words as possible without restricting itself to possible guesses, since the word that minimizes the scope COULD contain a discarded letter.
    The second option will give you the word that reduces the scope as much as possible while matching your greens, yellows and grays, meaning that if you are aim is to get it right in the next guess, and don't care for how many words your guess will affect, this is the word you should choose.
    Note: Testing has proven this heuristic to not always be right, and sometimes using option 1) will leave you with more possible guesses than option 2), making option 2) a strictly better guess."""

    solver_instance = solver.solver("5_letter_words.txt")       
    print(f"There are {len(solver_instance.valid_words)} possible words.")
    while True:
        input("Press enter when you are ready to guess.")        
        user_greens = _guess_from_user("Input your green letters in d_c_s format: ")
        user_yellows = _guess_from_user("Input your yellow letters in d_c_s format: ")
        user_grays = _guess_from_user("And finally, input your grays in dcs format: ", enforce_format = False)
        print("Processing your data...")
        solver_instance.add_guess(user_greens, user_yellows, user_grays)
        print(f"There are {len(solver_instance.valid_words)} possible words remaining.")        
        print(options, end = '')
        while True:
            user_option = input("\n-> ")
            match user_option:
                case '1':
                    print("Option 1 selected")
                    print(f"The best word now is: {solver_instance.choose_word(True)}")
                case '2':
                    print("Option 2 selected")
                    print(f"The best guess now is: {solver_instance.choose_word(False)}")
                case '3':
                    if len(solver_instance.valid_words) > 49:
                        print("There are too many possible gueses, showing you the first 50")
                        print(solver_instance.valid_words[0:50])
                    else:
                        print(solver_instance.valid_words)
                case '4':
                    break
                case '?':
                    print(difference)
                case _:
                    print("Try again...")
    return 0

def _guess_from_user(prompt: str, enforce_format: bool = True) -> str:
    """Prompts the user for their green or yellow letters, 
    in the form ' d _ c _ _ ' or 'd_c__' 
    """
    user_input = input(prompt)    
    user_input = user_input.replace(' ', '')

    #ensure correct usage
    if enforce_format:
        valid_input = (len(user_input) == 5)
        for c in user_input:
            if c != '_' and (not c.isalpha()):
                valid_input = False
        if not valid_input:
            _guess_from_user(prompt)
    else:
        for c in user_input:
            if not c.isalpha():
                valid_input = False
    return user_input