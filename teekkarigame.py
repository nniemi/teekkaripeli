"""
COMP.CS.100 Programming 1


                              TEEKKARIGAME

This program is a version of the traditional game of hangman, made with
a healthy dose of teekkarihumor. The program contains 18 different
words, which can then be guessed by the user. Guessed letters show up at the
bottom half of the GUI in alphabetical order. If the user has a total of nine
wrong guesses, the user loses the game.

Everytime the user guesses a letter correctly, it will be shown in a label at
the correct position corresponding to the randomized word. The program saves
data from recent games and tracks wins and losses. The data will be shown at
the bottom of the GUI.

The user can guess letters using a virtual keyboard. When a correct letter is
guessed, that key becomes locked on the keyboard. When the user wins/loses the
whole keyboard becomes locked. A new game can be started by pressing the
reset-button. The whole program can be shut down by pressing the quit-button.

Below the guessed letters label there is a counter to indicate how many guesses
the user still has before they lose the game.


"""

from tkinter import *

# Importing randint from random library for randomizing the
# word used in the game

from random import randint

# Importing ascii_uppercase from string library for the virtual keyboard

from string import ascii_uppercase


class UserInterface:
    """
    Defines the user interface and the functions in it. Forms the graphic
    structure of the interface.
    """

    def __init__(self):

        """
        The constructor for the program. Contains the configuration for the
        whole user interface.
        """

        # Sets the mainframe for the program.
        self.__mainframe = Tk()

        # Sets a new title for the game in tkinter window.
        self.__mainframe.title("Teekkaripeli")

        # Sets a new icon for the game in tkinter window.
        self.__mainframe.iconbitmap("kuvat/tolkki.ico")

        # Creates a drop down menu, where the user can see the rules of the
        # game and all the words.
        menu = Menu(self.__mainframe)
        self.__mainframe.config(menu=menu)

        submenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Valikko", menu=submenu)
        submenu.add_command(label="Ohjeet", command=self.instructions)
        submenu.add_command(label="Sanasto", command=self.word_photo)
        submenu.add_command(label="Takaisin", command=self.back)

        # Initializes the values for the variables
        self.guesses = 0
        self.games = 0
        self.wins = 0
        self.losses = 0

        # Contains a list of images used in photo_label
        self.photos = (PhotoImage(file="kuvat/Tausta.png"),
                       PhotoImage(file="kuvat/jalat.png"),
                       PhotoImage(file="kuvat/ylaosa.png"),
                       PhotoImage(file="kuvat/paa.png"),
                       PhotoImage(file="kuvat/lakki.png"),
                       PhotoImage(file="kuvat/santtu.png"),
                       PhotoImage(file="kuvat/kurkkumopo.png"),
                       PhotoImage(file="kuvat/puuhoyla.png"),
                       PhotoImage(file="kuvat/matrixlasit.png"))

        # The image which is shown in photo_label when the user wins/loses.
        self.win_photo = PhotoImage(file="kuvat/pottiin.png")
        self.lose_photo = PhotoImage(file="kuvat/kottiin.png")

        # Defines a location of the rules image and the word image.
        self.instructs = PhotoImage(file="kuvat/ohjeet.png")
        self.word_image = PhotoImage(file="kuvat/sanasto.png")

        # A list which contains the words for the game.
        self.wordlist = ["KEIHÄS", "KARHU", "TEEKKARI", "KALJA", "TERVA",
                         "PUUHÖYLÄ", "ISÄNMAA", "KÄPY", "KATAPULTTI", "SAUNA",
                         "TALVISOTA", "MÖKKITIE", "JALOVIINA", "GAMBINA",
                         "MÄMMI", "TIILI", "ETELÄ-HERVANTA",
                         "DIPLOMI-INSINÖÖRI"]

        # A label which forms the boundaries for the "hangman".
        self.photo_label = Label(self.__mainframe)
        self.photo_label.grid(row=0, column=0, columnspan=6)
        self.photo_label.configure(image=self.photos[0])

        # A label which forms the boundaries for the correct word
        # next to the photo_label.
        self.word_label = StringVar()
        Label(self.__mainframe, textvariable=self.word_label,
              font="Helvetica 10").grid(row=0, column=5, columnspan=8, padx=15)

        # Randomizes a number between 0 and the length of the wordlist and
        # references the number to the corresponding index in self.wordlist.
        self.word_number = randint(0, len(self.wordlist) - 1)
        self.word = self.wordlist[self.word_number]

        # Replaces the letters with underscores, so that the word can
        # be guessed letter by letter.
        self.word_with_spaces = " ".join(self.word)
        self.word_label.set(" ".join("_" * len(self.word)))

        # A label which contains a text for the alphabet_label which is
        # defined below.
        self.guessed_label = Label(self.__mainframe, text="Arvatut kirjaimet:",
                                   font="Helvetica 15")
        self.guessed_label.grid(row=6, column=1, columnspan=8, pady=10)

        # Sets the boundaries for self.alphabet
        self.alphabet_label = StringVar()
        Label(self.__mainframe, textvariable=self.alphabet_label,
              font="Helvetica 10").grid(row=7, column=1, columnspan=8)

        # Replaces self.alphabet with underscores so the user can see which
        # letters they have used this round in alphabetical order.
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ-"
        self.split_alphabet = " ".join(self.alphabet)
        self.alphabet_label.set(" ".join("_" * (len(self.alphabet))))

        # Forms the boundaries for a label which shows how many guesses
        # the user has left before losing the game.
        self.guesses_left = 9
        self.guess_amount_label = Label(self.__mainframe,
                                        text=f"Yrityksiä jäljellä: {self.guesses_left}",
                                        font="Helvetica 15")
        self.guess_amount_label.grid(row=8, column=1, columnspan=8, pady=10)

        # Forms the boundaries for a label which indicates if the user has
        # lost or won the game.
        self.result_label = Label(self.__mainframe, text=None,
                                  font="Helvetica 24")
        self.result_label.grid(row=9, column=1, columnspan=8)

        # Forms the boundaries for a label which shows the
        # amount of total games.
        self.games_label = Label(self.__mainframe,
                                 text=f"Pelejä yhteensä: {self.games}",
                                 font="Helvetica 15")
        self.games_label.grid(row=10, column=1, columnspan=8)

        # Forms the boundaries for a label which shows the
        # amount of total wins.
        self.wins_label = Label(self.__mainframe, text=f"Voitot: {self.wins}",
                                font="Helvetica 15")
        self.wins_label.grid(row=11, column=2, columnspan=3, pady=10)

        # Forms the boundaries for a label which shows the
        # amount of total losses.
        self.losses_label = Label(self.__mainframe,
                                  text=f"Häviöt: {self.losses}",
                                  font="Helvetica 15")
        self.losses_label.grid(row=11, column=5, columnspan=3, pady=10)

        # Forms the keyboard which is used to operate the interface.
        # ASCII-characters are created as buttons using a for loop which also
        # saves each key as a dictionary key and a button as a dictionary value.
        # This dictionary is used later on to disable buttons after a correct
        # guess.
        self.keyboard_dict = {}

        n = 0
        for i in ascii_uppercase:
            self.keyboard_dict[i] = Button(self.__mainframe, text=i,
                                           command=lambda i=i: self.guess(i),
                                           width=6, bg="grey80")
            self.keyboard_dict[i].grid(row=1 + n // 9, column=n % 9)
            n += 1

        # String-library doesn't include non-ASCII characters,
        # such as scandinavian letters or dash, so the following lines form
        # these characters as individuals. The basic structure stays the same
        # as above.
        self.keyboard_dict["Å"] = Button(self.__mainframe, text="Å",
                                         width=6,
                                         command=lambda: self.guess("Å"),
                                         bg="grey80")
        self.keyboard_dict["Å"].grid(row=1, column=9)

        self.keyboard_dict["Ä"] = Button(self.__mainframe, text="Ä",
                                         width=6,
                                         command=lambda: self.guess("Ä"),
                                         bg="grey80")
        self.keyboard_dict["Ä"].grid(row=2, column=9)

        self.keyboard_dict["Ö"] = Button(self.__mainframe, text="Ö",
                                         width=6,
                                         command=lambda: self.guess("Ö"),
                                         bg="grey80")
        self.keyboard_dict["Ö"].grid(row=3, column=9)

        self.keyboard_dict["-"] = Button(self.__mainframe, text="-",
                                         width=6,
                                         command=lambda: self.guess("-"),
                                         bg="grey80")
        self.keyboard_dict["-"].grid(row=3, column=8)

        # Forms a button to shut down the program.
        self.quit_button = Button(self.__mainframe, text="LOPETA",
                                  font="Helvetica 15", bg="grey64", width=10,
                                  height=2,
                                  command=self.quit).grid(row=4, column=5,
                                                          columnspan=3)

        # Forms a button to start a new game.
        self.reset_button = Button(self.__mainframe, text="TYHJENNÄ",
                                   font="Helvetica 15", bg="grey64", width=10,
                                   height=2,
                                   command=self.reset).grid(row=4, column=2,
                                                            columnspan=3)

        # Starts the program.
        self.__mainframe.mainloop()

    # Defines the functionality of the instructions button in the menu.
    # Replaces the photo_label with an image where the user can read the rules.
    def instructions(self):
        self.photo_label.config(image=self.instructs)
        self.reset_button = Button(self.__mainframe, text="TAKAISIN",
                                   font="Helvetica 15", bg="grey64", width=10,
                                   height=2, command=self.reset).grid(row=4,
                                   column=2, columnspan=3)

    # Defines the functionality of the word list button in the menu.
    # Replaces the photo_label with an image where the user can see the words.
    def word_photo(self):
        self.photo_label.config(image=self.word_image)
        self.reset_button = Button(self.__mainframe, text="TAKAISIN",
                                   font="Helvetica 15", bg="grey64", width=10,
                                   height=2, command=self.reset).grid(row=4,
                                   column=2, columnspan=3)

    # Defines the functionality of the back button in the menu.
    def back(self):
        self.reset()

    def guess(self, key):

        """
        Compares the pressed key with splitted randomized words, if there is
        a match with any of the letter, sets a new value for word_label, with
        correct letters.
        :param key: str, pressed key
        """

        # Creates lists out of a given string, which are used to compare the
        # pressed key to each index on the randomized word.
        split_word = list(self.word_with_spaces)
        guessed = list(self.word_label.get())

        # Creates lists out of the given alphabet string, which can be used to
        # indicate which letters have been used.
        split_alph = list(self.split_alphabet)
        used_letters = list(self.alphabet_label.get())

        # Loops the alphabet and compares it to the key. There is a match
        # everytime, because split_alph contains all the letters given in the
        # keyboard. Replaces the underscore with the given key.
        for i in range(len(split_alph)):
            if split_alph[i] == key:
                used_letters[i] = key
            self.alphabet_label.set("".join(used_letters))

        # Loops every index of split_word and compares the given key to the
        # randomized word, if there is a match, it will replace that exact
        # underscore with the key.
        if self.word.count(key) > 0:
            for i in range(len(split_word)):

                if split_word[i] == key:
                    guessed[i] = key
                    self.keyboard_dict[key].config(state=DISABLED)
                self.word_label.set("".join(guessed))

            # If the word_label is equal to the randomized word, user will
            # win, the scoreboard updates, win image will be shown and program
            # congratulates the user. Afterwards, the keyboard is locked.
            if self.word_label.get() == self.word_with_spaces:
                self.result_label.config(text="Voitit pelin!")
                self.games += 1
                self.wins += 1
                self.games_label.config(text=f"Pelejä yhteensä:{self.games}")
                self.wins_label.config(text=f"Voitot:{self.wins}")
                self.photo_label.config(image=self.win_photo)
                self.disable_keyboard()

        else:
            # If the guessed letter is wrong program increments
            # self.guesses by one.
            self.guesses += 1
            try:
                # If the guess was wrong, the photo_label will be updated with
                # a new image.
                self.photo_label.config(image=self.photos[self.guesses])

                # Updates the guess_amount_label to show the user, how many
                # guesses they have left.
                self.guess_amount_label.config(
                    text=f"Yrityksiä jäljellä: {self.guesses_left - self.guesses}")

            except IndexError:
                # If there are more than 9 guesses, program will
                # disable the keyboard.
                self.disable_keyboard()

        # If the user guesses too many times, the user will lose the game,
        # the scoreboard will update with amount of losses, shows the
        # lose photo on photo_label and disables the keyboard.
        if self.guesses == 9:
            self.result_label.config(text="Hävisit pelin!")
            self.games += 1
            self.losses = self.games - self.wins
            self.games_label.config(text=f"Pelejä yhteensä:{self.games}")
            self.losses_label.config(text=f"Häviöt:{self.losses}")
            self.photo_label.config(image=self.lose_photo)
            self.guess_amount_label.config(text=f"Yrityksiä jäljellä: {0}")
            self.disable_keyboard()

    def disable_keyboard(self):

        """
        Disables the keyboard using the dictionary, which was created during
        assembling the buttons at __init__.
        """

        for key in self.keyboard_dict:
            self.keyboard_dict[key].config(state=DISABLED)

    def enable_keyboard(self):
        """
        Enables the keyboard again, if it is disabled.
        """

        for key in self.keyboard_dict:
            self.keyboard_dict[key].config(state=NORMAL)

    def reset(self):

        """
        Creates a new game. Resets the photo_label, sets the users guesses to
        zero, randomizes a new word, resets the result_label, clears the
        guessed letters and enables the keyboard.
        """
        self.photo_label.config(image=self.photos[0])
        self.guesses = 0
        self.word_number = randint(0, len(self.wordlist) - 1)
        self.word = self.wordlist[self.word_number]
        self.word_with_spaces = " ".join(self.word)
        self.word_label.set(" ".join("_" * len(self.word)))
        self.result_label.destroy()
        self.result_label = Label(self.__mainframe, text=None,
                                  font="Helvetica 24")
        self.result_label.grid(row=5, column=1, columnspan=9)

        self.split_alphabet = " ".join(self.alphabet)
        self.alphabet_label.set(" ".join("_" * (len(self.alphabet))))
        self.reset_button = Button(self.__mainframe,
                                   text="TYHJENNÄ", font="Helvetica 15",
                                   bg="grey64", width=10, height=2,
                                   command=self.reset).grid(
                                   row=4, column=2,
                                   columnspan=3)
        self.enable_keyboard()

    def quit(self):
        """
        Quits the program.
        """
        self.__mainframe.destroy()


def main():
    GUI = UserInterface()


if __name__ == "__main__":
    main()
