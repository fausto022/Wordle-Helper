"""Handles the prompting on the terminal, as well as collecting the user's data about their game"""

import string

def char_from_user(prompt: str) -> chr:
    """Ask the user for a character for an alphabetic character, can be empty."""
    user_input = input(prompt).lower()
    if user_input.isalpha() and len(user_input) == 1 or user_input == '':
        return user_input
    else:
        return char_from_user(prompt)

def list_of_chars_from_user(prompt: str) -> list[chr]:
    """Prompts the user for a list of alphabetic characters in the form 'xyabzd', can be empty"""
    user_input = input(prompt)
    if user_input == '':
        return []
    elif not user_input.isalpha():
        list_of_chars_from_user(prompt)

    return [char for char in user_input]

def dict_of_greens_from_user(prompt: str) -> dict[int: chr]:
    """Prompts the user for their green letters, in the form ' d _ c _ _ ' or 'd_c__' """
    user_input = input(prompt)    
    user_input = user_input.replace(' ', '')

    #ensure correct usage
    valid_input = True
    for c in user_input:
        if c != '_' or not c.isAlpha():
            valid_input = False
    if not (valid_input and len(user_input) == 5):
            dict_of_greens_from_user(prompt)

    #return the data in the appropiate format
    return_dict = {0:'', 1:'', 2:'', 3:'', 4:''}
    for k, letra in enumerate(user_input):
        if letra.isalpha():
            return_dict[k] = letra
    return return_dict