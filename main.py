from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import mysql.connector as mys

# Window dimensions
WIDTH = 1024
HEIGHT = 720

# Key States
USED = "#242424"
CORRECT = "#0f4200"

tries = 0

wordlist_data = []

# Setting up Tkinter
root = Tk()
root.geometry("{}x{}".format(WIDTH, HEIGHT))
root.title("Wordle")
root.configure(background="#000000")

keylist = []
labels_list = []

user_input = Entry(root, width=5, bg="black", fg="white", font=("JetBrains Mono", 27, "bold"))
user_input.place(relx=0.4, rely=0.9)

random_word = ""

keymap = {
    "A": (0, 0),
    "B": (0, 1),
    "C": (0, 2),
    "D": (0, 3),
    "E": (1, 0),
    "F": (1, 1),
    "G": (1, 2),
    "H": (1, 3),
    "I": (2, 0),
    "J": (2, 1),
    "K": (2, 2),
    "L": (2, 3),
    "M": (3, 0),
    "N": (3, 1),
    "O": (3, 2),
    "P": (3, 3),
    "Q": (4, 0),
    "R": (4, 1),
    "S": (4, 2),
    "T": (4, 3),
    "U": (5, 0),
    "V": (5, 1),
    "W": (5, 2),
    "X": (5, 3),
    " ": (6, 0),
    "Y": (6, 1),
    "Z": (6, 2),
    "": (6, 3)
}

inverse_keymap = {v: k for k, v in keymap.items()}

def init():
    global random_word
    global labels_list
    global wordlist_data
    global keylist
    global inverse_keymap

    # Picking a random word from the wordlist
    with open("wordlist.txt", "r") as f:
        for i in f:
            wordlist_data.append(i)

    for i in range(len(wordlist_data)):
        wordlist_data[i] = wordlist_data[i].strip("\n")

    random_word = random.choice(wordlist_data)

    for i in range(6):
        tmp_label = []
        for j in range(5):
            tmp_label.append(Label(root, text="", font=("JetBrains Mono", 27, "bold"), bg="#1f1f1f", fg="white", width=2, height=1))
            tmp_label[j].config(anchor=CENTER)
            tmp_label[j].grid(row=len(labels_list), column=j, pady=(15, 0), padx=(0, 15))
            tmp_label[0].grid(padx=(WIDTH - 900, 15))
        # Appending to the main list of inputted words.
        labels_list.append(tmp_label)

    current_char = 65

    for i in range(7):
        tmp = []
        for j in range(4):
            tmp.append(Label(text=inverse_keymap[(i, j)], font=("JetBrains Mono", 27), bg="#666666", fg="white", width=2, height=1))
            tmp[j].config(anchor=CENTER)
            tmp[j].grid(row=i, column=j+5, pady=(15, 0), padx=(0, 15))
            tmp[0].grid(padx=(WIDTH // 4, 15))

            current_char += 1
        keylist.append(tmp)

def add_word(self):
    global labels_list
    global user_input
    global tries
    global wordlist_data

    tmp_label = labels_list[tries]

    # Checking the size of the inputted word
    if len(user_input.get()) != 5:
        messagebox.showwarning("", "Word must be 5 letters long")

    elif user_input.get() not in wordlist_data:
        messagebox.showwarning("", "Word not in word list")

    # Checking if the inputted word is right
    elif user_input.get() == random_word:
        for i in range(5):
            tmp_label[i].config(text=user_input.get()[i].upper())
            tmp_label[i].config(bg="#0f4200")
    else:
        for i in range(5):
            # Appending characters to display with colours
            if user_input.get()[i] in random_word and i == random_word.index(user_input.get()[i]):
                tmp_label[i].config(text=user_input.get()[i].upper())
                tmp_label[i].config(bg="#0f4200")
                update_keyboard(user_input.get()[i].upper(), CORRECT)

            elif user_input.get()[i] in random_word:
                tmp_label[i].config(text=user_input.get()[i].upper())
                tmp_label[i].config(bg="#887400")
                update_keyboard(user_input.get()[i].upper(), USED)
            else:
                tmp_label[i].config(text=user_input.get()[i].upper())
                tmp_label[i].config(bg="#1f1f1f")
                update_keyboard(user_input.get()[i].upper(), USED)

        # labels_list.append(tmp_label)
        tries += 1

    # Clearing the input
    user_input.delete(0, 'end')

def update_keyboard(letter, state):
    global user_input
    global keylist
    global keymap

    r, c = keymap[letter]

    keylist[r][c].config(bg = state)

    print(letter)
    print(f"{r = }, {c = }")

if __name__ == "__main__":
    init()
    print(random_word)
    user_input.focus_set()
    # Binding a callback function to the return key
    root.bind("<Return>", add_word)
    root.mainloop()