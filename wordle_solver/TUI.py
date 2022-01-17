"""Handles the prompting on the terminal, collects the user's data about their game, and runs the main loop of the program"""

import curses
import threading
import time
from random import choice

from wordle_solver.solver import solver #it's the only class in the module, so I'm importing it directly :)

#renamings
(down, up) = (-1, 1)
(left, right) = (-1, 1)
(gray, yellow, green) = (0, 1, 2)

def isLetter(key: int) -> bool:
    return (ord('A') <= key <= ord('Z') or ord('a') <= key <= ord('z'))

class guess:    
    def __init__(self, window: 'curses._CursesWindow', y: int, x: int) -> None:        
        self._pWindow = window #assign parent window
        self._y = y            #assign the position in the parent window
        self._x = x            #assign the position in the parent window
        self.letters = [{'l': '_', 'c': 0} for _ in range(5)]
        self.pos = 0

    def redraw_letter(self, pos: int = None) -> None:
        """Redraws the letter in the specified position at its corresponding screen position, 
        redraws the currently highlighted letter if pos is empty"""
        if pos == None:
            pos = self.pos
        self._pWindow.addch(self._y, (self._x + pos*2), self.pos_l(pos),  self.l_color(pos) | curses.A_UNDERLINE)
        
    def display_word(self) -> None:
        """Displays the resulting word"""        
        for i, _ in enumerate(self.letters):
            self.redraw_letter(i)

    def l_color(self, pos: int = None) -> int:
        """Returns the color_pair of a specified position, returns the color_pair of the 
        currently highlighted letter if pos is empty"""
        if pos == None:
            pos = self.pos
        return curses.color_pair(self.letters[pos]['c'])
    
    def pos_l(self, pos: int = None) -> chr:
        """Returns the letter in a specified position, returns the currently highlighted letter if pos is empty"""
        if pos == None:
            pos = self.pos
        return self.letters[pos]['l']

    def pos_coord_x(self) -> int:
        """Returns the cursor screen row according to the current position"""
        return (self._x + self.pos * 2)        

    def next(self, dir: int, wrapping) -> None:
        """Move the cursor to the next position"""
        if wrapping:
            self.pos = (self.pos + dir) % 5
        else:
            self.pos = max(0, min(self.pos + dir, 4))

    def change_l_col(self, dir, pos: int = None) -> int:
        """Change the color of the specified position by one, changes the color the currently highlited letter if pos is empty"""
        if pos == None:
            pos = self.pos
        new_col = (self.letters[pos]['c'] + dir) % 3
        self.letters[self.pos]['c'] = new_col
        return new_col

    def set_l_color(self, color: int, pos: int = None):
        """Sets the color of the specified position to a specific one, changes the color the 
        currently highlited letter if pos is empty"""
        if pos == None:
            pos = self.pos
        c = -1
        while c != color:
            c = self.change_l_col(1, pos)

    def change_l(self, l: chr, pos: int = None) -> None:
        """Change the letter of the currently highlighted position"""
        if pos == None:
            pos = self.pos 
        self.letters[self.pos]['l'] = l 

    def translate_to(self, y: int, x: int)-> None:
        """Moves the guess to another point on the window."""
        self._y = y
        self._x = x

    def translate_up(self, i: int = 1) -> None:
        """Moves the guess one line closer to the top edge."""
        for _ in range(i):
            self.translate_to(self._y - 1, self._x)
        

class guessing_interface:    
    def __init__(self, y: int = 0, x: int = 0) -> None:
        #init the new window and basic members
        self.length = 24
        self.width = 27
        self._y = int(self.length * 5/6)
        self._x = int((self.width/2) - 4.5)
        self._window = curses.newwin(self.length, self.width, y, x)
        self._guess = guess(self._window, self._y, self._x)
        self._past_guesses = []
        self._guesses_left = True

        #Create an instance of our solver
        self._solver = solver()

        #set the properties        
        self._window.box()

        #draw the initial elements
        self._blank_prompt()

        #finally refresh the window
        self._window.refresh()

        #Create a couple windows to display information
        self._exploratory_guess = curses.newwin(1, 24, 1, 1)
        self._display_message(self._exploratory_guess, "Exploratory: aurei.")

        self._valid_guess = curses.newwin(1, 24, 2, 1)
        self._display_message(self._valid_guess, "Correct: arise.")

        self._number_of_left = curses.newwin(1, 11, self.length-2, self.width-12)
        self._display_message(self._number_of_left, "left: " + str(len(self._solver.answers)))

        #create a separate window for the threaded display
        self.possibles_display = curses.newwin(1, 24, 7, 1)
        #create a thread to show random words in the middle of the screens
        self.randoms_thread = threading.Thread(target = self._display_random_timed, args=[self.possibles_display])
        self.randoms_thread.daemon = True
        self.randoms_thread.start()


    def _blank_prompt(self) -> None:
        """Erases the cursor and sets everything back to white and updates the internal structure's guess to a new one."""
        self._window.addstr(self._y-1, self._x, "#          ") #erases the old cursor
        self._window.addstr(self._y+1, self._x, "#          ") #erases the old cursor
        self._window.addstr(self._y, self._x, "_ _ _ _ _")
        self._guess = guess(self._window, self._y, self._x)
        self._window.refresh()

    def move_cursor(self, dir: int = 0, wrapping: bool = True) -> None:
        """Moves the cursor graphic while also modifying the necessary class members,
        dir = 0 will repaint the cursor without moving it"""
        #erase current cursor        
        self._window.addch(self._y - 1, self._guess.pos_coord_x(), ' ')
        self._window.addch(self._y + 1, self._guess.pos_coord_x(), ' ')        
        #draw the new cursor
        self._guess.next(dir, wrapping)
        cursor_x = self._guess.pos_coord_x()
        self._window.addch(self._y - 1, cursor_x, '#', self._guess.l_color())
        self._window.addch(self._y + 1, cursor_x, '#', self._guess.l_color())

    def change_color(self, dir) -> None:
        #change the color
        self._guess.change_l_col(dir)
        #redraw the letter        
        self._guess.redraw_letter()
        self.move_cursor()

    def _submit_guess(self) -> None:        
        if not any('_' == t['l'] for t in self._guess.letters):
            #Update the solver
            self._solver.add_guess(self._guess.letters)
            words_left = len(self._solver.answers)
            self._number_of_left.clear()
            print(len(str(len(self._solver.answers))))
            self._display_message(self._number_of_left, "left: " + str(len(self._solver.answers)), x=4-len(str(len(self._solver.answers))))

            if words_left > 1:
                #You're still going
                #display the new words
                best_exploratory, best_valid = self._solver.choose_word()
                self._display_message(self._exploratory_guess, "Exploratory: " + best_exploratory + '.')
                self._display_message(self._valid_guess, "Correct: " + best_valid + '.')                
            else:
                self._guesses_left = False
                self._clear_screen(self.possibles_display)
                self._clear_screen(self._exploratory_guess)
                self._clear_screen(self._valid_guess)
                if words_left == 0:
                    #You lost :(
                    defeat_msg = "No more guessing :("
                    for i, ch in enumerate(defeat_msg):
                        self._window.addch(7, int((self.width - len(defeat_msg)) / 2) + i, ch, curses.color_pair(i % 3))
                    self._window.addstr(self._y-1, self._x, "# # # # #")
                    self._window.addstr(self._y+1, self._x, "# # # # #")
                elif words_left == 1:
                    #You won!
                    _, best_valid = self._solver.choose_word()
                    word_to_show = ''
                    for ch in best_valid:
                        word_to_show = word_to_show + ch + ' '
                    self._window.addstr(self._y-1, self._x, "! ! ! ! !")
                    self._window.addstr(self._y+1, self._x, "! ! ! ! !")
                    victory_msg = "!!!You won!!!"
                    for i, ch in enumerate(victory_msg):
                        self._window.addch(7, int((self.width - len(victory_msg)) / 2) + i, ch, curses.color_pair(i % 3))
                    self._window.addstr(self._y, self._x, word_to_show[:-1], curses.color_pair(green))
                    self._window.refresh()
                    

            #Only create a new prompt if we are not at the last guess
            if len(self._past_guesses) < 5 and self._guesses_left:
                self._past_guesses.append(self._guess)
                for past_guess in self._past_guesses:
                    past_guess.translate_up(2)
                    past_guess.display_word()
                    self._blank_prompt()
            else:
                #You've reached your last guess
                self._guesses_left = False

    def manage_input(self, key: int) -> None:
        if self._guesses_left:
            if isLetter(key):
                self._guess.change_l(chr(key).lower())
                self._guess.redraw_letter()
                self.move_cursor(right, False)
            elif key == curses.KEY_RIGHT:
                self.move_cursor(right)
            elif key == curses.KEY_LEFT:
                self.move_cursor(left)
            elif key == curses.KEY_UP:
                self.change_color(up)
            elif key == curses.KEY_DOWN:
                self.change_color(down)
            elif key == 8 or key == curses.KEY_BACKSPACE: #had to hardcode my own backspace key because curses wasn't detecting correctly
                self._guess.change_l('_')
                self._guess.set_l_color(gray)
                self._guess.redraw_letter()
            elif key == 13 or key == curses.KEY_ENTER: #had to hardcode my own enter key because curses wasn't detecting correctly
                self._submit_guess()                    
            self._window.refresh()

    def _display_message(self, screen: 'curses._CursesWindow', message: str, y: int = 0, x: int = 0) -> None:
        screen.addstr(y, x, message)
        screen.refresh()

    def _clear_screen(self, screen: 'curses._CursesWindow') -> None:
        screen.clear()
        screen.refresh()

    def _display_random_timed(self, screen: 'curses._CursesWindow') -> None:
        while True:
            if len(self._solver.answers) > 1:
                self._display_message(screen, choice(self._solver.answers), x = int(self.width/2 - 3))
                time.sleep(1)
            else:
                break


def main(screen: 'curses._CursesWindow'):
    #curses settings
    curses.initscr()
    curses.start_color()
    curses.resize_term(24, 27) #resize the terminal so it fits our windows nicely
    curses.curs_set(0) #make cursor invisible
    curses.raw() #disable special inputs like enter/return
 
    #init colors
    curses.init_color(21, 156, 3, 4)
    curses.init_pair(green, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(yellow, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    terminal_y, terminal_x = screen.getmaxyx()
    guessing_window = guessing_interface()

    #run the main loop
    while True:
        key = screen.getch()
        if key == 3: #if ctrl+c is pressed, quit.
            break
        else:
            guessing_window.manage_input(key)
    curses.endwin()

curses.wrapper(main)