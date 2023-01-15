from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import mysql.connector as mys
from time import time
import threading
import collections
from tkinter.simpledialog import askstring

# Window dimensions
WIDTH = 1024
HEIGHT = 720

# Key States
USED = "#242424"
CORRECT = "#0f4200"
EXISTS_IN_WORD = "#887400"

DEBUG = True

running = True

tries = 0

wordlist_data = []
# Setting up MySQL
db = mys.connect(user="root", password="batman", host="localhost")
cursor = db.cursor()
cursor.execute("create database if not exists cs;")
cursor.execute("use cs;")
cursor.execute("create table if not exists scores(name varchar(100), time_taken varchar(10), score decimal(5, 2));")

username = askstring("Username", "What is your name?")

# Setting up Tkinter
root = Tk()
root.geometry("{}x{}".format(WIDTH, HEIGHT))
root.title("Wordle")
root.configure(background="#000000")

keylist = []
labels_list = []

main_frame = Frame(root)
timer_frame = Frame(root)

user_input = Entry(root, width=5, bg="black", fg="white", font=("JetBrains Mono", 27, "bold"))
user_input.place(relx=0.4, rely=0.9)

random_word = ""

score = 0

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
    letter_count = list(collections.Counter(random_word).values())
    while any([i > 1 for i in letter_count]):
        random_word = random.choice(wordlist_data)
        letter_count = list(collections.Counter(random_word).values())

    empty = Label(main_frame, text="", bg="#000000", height=3)
    title = Label(main_frame, text="Wordle", font=("JetBrains Mono", 27, "bold"), bg="#000000", fg="white")
    empty.grid(row=0, column=0)
    title.place(x=350, y=5)

    # Backup plan
    # random_word_list = list(random_word)
    # while True:
    #     for (idx, _) in enumerate(random_word_list):
    #         letter = random_word_list.pop(idx)
    #         if letter in random_word_list:
    #             random_word = random.choice(wordlist_data)
    #             break
    #     break

    # Inputted words
    for i in range(6):
        tmp_label = []
        for j in range(5):
            tmp_label.append(Label(main_frame, text="", font=("JetBrains Mono", 27, "bold"), bg="#1f1f1f", fg="white", width=2, height=1))
            tmp_label[j].config(anchor=CENTER)
            tmp_label[j].grid(row=len(labels_list) + 1, column=j, pady=(15, 0), padx=(0, 15))
            tmp_label[0].grid(padx=(WIDTH - 1020, 15))
        # Appending to the main list of inputted words.
        labels_list.append(tmp_label)


    # Keypad
    for i in range(7):
        tmp = []
        for j in range(4):
            tmp.append(Label(main_frame, text=inverse_keymap[(i, j)], font=("JetBrains Mono", 27), bg="#666666", fg="white", width=2, height=1))
            tmp[j].config(anchor=CENTER)
            tmp[j].grid(row=i + 1, column=j+5, pady=(15, 0), padx=(0, 15))
            tmp[0].grid(padx=(WIDTH // 4, 15))

        keylist.append(tmp)

def add_word(self):
    global labels_list
    global user_input
    global tries
    global wordlist_data

    try:

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
            
            messagebox.showinfo("You won")
            exit()

            return

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
                    update_keyboard(user_input.get()[i].upper(), EXISTS_IN_WORD)
                else:
                    tmp_label[i].config(text=user_input.get()[i].upper())
                    tmp_label[i].config(bg="#1f1f1f")
                    update_keyboard(user_input.get()[i].upper(), USED)

            # labels_list.append(tmp_label)
            tries += 1

        if tries >= 6:
            messagebox.info("You're out of tries!")
            exit()

        # Clearing the input
        user_input.delete(0, 'end')

    except:
        exit()

def exit():
    global username
    global time_elapsed_str
    global db
    global cursor
    global running

    if running:
        score = ((6 - tries) / 6) * 100
        cursor.execute("insert into scores values('{}', '{}', {})".format(username, time_elapsed_str, score))
        db.commit()

    running = False



def update_keyboard(letter, state):
    global user_input
    global keylist
    global keymap

    r, c = keymap[letter]

    keylist[r][c].config(bg = state)

def update_timer():
    global running
    global time_elapsed_str

    start_time = time()
    timer_label = Label(root, text="00:00:00", font=("JetBrains Mono", 27), bg="#000000", fg="white")
    timer_label.place(x = 390, y = 570)
    hrs = 0
    mins = 0
    seconds = 0

    while True:
        seconds = int(time() - start_time)
        time_elapsed_str = "{:02d}:{:02d}:{:02d}".format(hrs, mins, seconds)
        timer_label.config(text = time_elapsed_str)
        if seconds >= 60:
            mins += 1
            seconds = 0
            start_time = time()

        if mins >= 60:
            mins = 0
            hrs += 1
            seconds = 0
            start_time = time()

        if running == False:
            break

if __name__ == "__main__":
    init()
    if DEBUG:
        print(random_word)
    user_input.focus_set()
    main_frame.config(bg="#000000")
    timer_frame.config(bg="#000000")
    main_frame.pack()
    # timer_frame.pack()
    # Binding a callback function to the Enter/Return key
    root.bind("<Return>", add_word)
    timer_thread = threading.Thread(target=update_timer)
    timer_thread.start()
    root.mainloop()
    running = False
    timer_thread.join()