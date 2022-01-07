"""Entry point script for wordle_solver"""

import sys

from wordle_solver import TUI


def main():    
    TUI.run_guessing_loop()

if __name__ == "__main__":
    sys.exit(int(main() or 0))