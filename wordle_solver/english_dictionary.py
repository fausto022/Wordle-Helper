import string

class english_dictionary():
    """handles all the relevant information from an english dictionary"""    

    def __init__(self, path: str=''): 
        """Reads the dictionary from memory, and stores its contents.
        Also gets the alphabet from the string library
        """
        #TODO: Add path functionality
        self.alphabet = list(string.ascii_lowercase) # 26 letters from the english alphabet, in [chr] format

        #reads both dictionaries from memory and stores them in different variables
        with open("words_5.txt", "r") as f:
            self.word_list_1 = f.read().split("\n") 
        with open("words_5_2.txt", "r") as f:
            self.word_list_2 = f.read().split(' ')

        


