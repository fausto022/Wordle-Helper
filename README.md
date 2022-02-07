# Wordle-Helper
Wordle-Helper is my first approach at making a 100% application with PYTHON.

Started out as a way of helping you solve the popular "Wordle" game.
It makes use of the CURSES library to give the user a quick, easy and lightweight TUI to input your guesses, and displays which word the user should input next.

The interface will display two words, one "exploratory", one "correct", and will cycle the possible words in the middle of the screen.

"exploratory" means the given word won't take into consideration whether it contains any discarded letter or not, but strives to give the user the most possible
amount of info when the word is inputted in the game.

"correct" means the given word won't contain any discarded letters, will contain all green letters in their corresponding positions, and won't have any yellow letters
in a position that has already been discarded, making this word a possible correct guess.

For example, if the world of the day was "Fever", all you'd have to do is input the words into Wordle, and input the results in the program so it will lead your guesses

![Demonstration of the program in action](https://media4.giphy.com/media/4eVB6OMMQ2dZZmpI4f/giphy.gif?cid=790b761183fb759269d37ca5a1fda3e9ecd7717d02c06706&rid=giphy.gif&ct=g)
