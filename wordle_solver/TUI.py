"""Handles the prompting on the terminal, collects the user's data about their game, and runs the main loop of the program"""

from wordle_solver.solver import solver #it's the only class in the module, so I'm importing it directly :)
import curses

#renamings
(down, up) = (-1, 1)
(left, right) = (-1, 1)
(gray, yellow, green) = (0, 1, 2)

def isLetter(key: int) -> bool:
    return (ord('A') <= key <= ord('Z') or ord('a') <= key <= ord('z'))

class curses_message:
    def __init__(self, window: 'curses._CursesWindow', y: int, x: int, message: str = '') -> None:
        self._pWindow = window #assign parent window
        self._message = list(message) #as a list because we need to modify it in the future
        self._y = y            #assign the position in the parent window
        self._x = x            #assign the position in the parent window

    def translate_to(self, y: int, x: int)-> None:
        """Moves the guess to another point on the window."""
        self._y = y
        self._x = x

    def draw_message(self) -> None:
        """Displays the message in its current position"""
        #This function won't be used very much but it's still nice to have, even if for debugging purposes
        self._pWindow.addstr(self._message)

class guess(curses_message):    
    def __init__(self, window: 'curses._CursesWindow', y: int, x: int) -> None:
        super().__init__(window, y, x)
        self.letters = [{'l': '_', 'c': 0} for _ in range(5)]
        self.pos = 0

    def redraw_letter(self, pos: int = None) -> None:
        """Redraws the letter in the specified position at its corresponding screen position, redraws the currently highlighted letter if pos is empty"""
        if pos == None:
            pos = self.pos
        self._pWindow.addch(self._y, (self._x + pos*2), self.pos_l(pos),  self.l_color(pos) | curses.A_UNDERLINE)
        
    def display_word(self) -> None:
        """Displays the resulting word"""        
        for i, _ in enumerate(self.letters):
            self.redraw_letter(i)

    def l_color(self, pos: int = None) -> int:
        """Returns the color_pair of a specified position, returns the color_pair of the currently highlighted letter if pos is empty"""
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
        """Change the color of the specified position, changes the color the currently highlited letter if pos is empty"""
        if pos == None:
            pos = self.pos
        new_col = (self.letters[pos]['c'] + dir) % 3
        self.letters[self.pos]['c'] = new_col
        return new_col

    def set_l_color(self, color: int, pos: int = None):
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

    def translate_up(self, i: int = 1) -> None:
        """Moves the guess one line closer to the top edge."""
        for _ in range(i):
            super().translate_to(self._y - 1, self._x)
        

class guessing_interface:    
    def __init__(self, y: int = 0, x: int = 0) -> None:
        #init the new window and basic members
        self.length = 24
        self.width = 27
        self._y = int(self.length * 5/6)
        self._x = int((self.width/2) - 5)
        self._window = curses.newwin(24, 26, y, x)
        self._guess = guess(self._window, self._y, self._x)
        self._past_guesses = []

        #Create an instance of our solver
        self._solver = solver("5_letter_words.txt")

        #set the properties        
        self._window.box()

        #draw the initial elements
        self._blank_prompt()

        #finally refresh the window
        self._window.refresh()

        #Create a couple windows to display information
        self._exploratory_guess = curses.newwin(1, 24, 1, 1)
        self._exploratory_guess.addstr("Exploratory: stoae.")
        self._exploratory_guess.refresh()
        self._valid_guess = curses.newwin(1, 24, 2, 1)
        self._valid_guess.addstr("Correct: stoae.")
        self._valid_guess.refresh()

    def _blank_prompt(self) -> None: 
        self._window.addstr(self._y-1, self._x, "#          ") #erases the old cursor
        self._window.addstr(self._y+1, self._x, "#          ") #erases the old cursor
        self._window.addstr(self._y, self._x, "_ _ _ _ _ ")
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

            #display the new words
            best_exploratory, best_valid = self._solver.choose_word()            
            self._exploratory_guess.addstr(0, 0, "Exploratory: " + best_exploratory + '.')
            self._valid_guess.addstr(0, 0, "Correct: " + best_valid + '.')
            self._exploratory_guess.refresh()
            self._valid_guess.refresh()

            #Only create a new prompt if we are not at the last guess
            if len(self._past_guesses) < 6:
                self._past_guesses.append(self._guess)
                for past_guess in self._past_guesses:
                    past_guess.translate_up(2)
                    past_guess.display_word()
                    self._blank_prompt()
            else:
                self._window.addstr(self._y-1, self._x, "          ") #erases the old cursor
                self._window.addstr(self._y+1, self._x, "          ") #erases the old cursor            

    def manage_input(self, key: int) -> None:
        if len(self._past_guesses) < 6:
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

def main(screen: 'curses._CursesWindow'):
    #curses settings
    curses.initscr()
    curses.start_color()
    curses.resize_term(24, 26) #resize the terminal so it fits our windows nicely
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
            #screen.addch(int(terminal_y/2), int(terminal_x/2), key)
            guessing_window.manage_input(key)  

    curses.endwin()

curses.wrapper(main)