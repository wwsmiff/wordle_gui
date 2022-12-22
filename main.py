from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

# Window dimensions
WIDTH = 1024
HEIGHT = 720

tries = 0

wordlist_data = []

# Setting up Tkinter
root = Tk()
root.geometry("{}x{}".format(WIDTH, HEIGHT))
root.title("Wordle")
root.configure(background="#000000")

# Creating separate frames
words_frame = Frame(root, width=WIDTH//2, height=HEIGHT, bg="black")
keys_frame = Frame(root, width=WIDTH//2, height=HEIGHT, bg="black")

labels_list = []

user_input = Entry(root, width=5, bg="black", fg="white", font=("JetBrains Mono", 27, "bold"))
user_input.place(relx=0.4, rely=0.9)

random_word = ""

def init():
    global random_word
    global labels_list
    global wordlist_data

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
            elif user_input.get()[i] in random_word:
                tmp_label[i].config(text=user_input.get()[i].upper())
                tmp_label[i].config(bg="#887400")
            else:
                tmp_label[i].config(text=user_input.get()[i].upper())
                tmp_label[i].config(bg="#1f1f1f")

        # Appending to the main list of inputted words.
        labels_list.append(tmp_label)
        tries += 1

    # Clearing the input
    user_input.delete(0, 'end')

def update_keyboard():
    global user_input

    keylist = []
    current_char = 65
    for i in range(6):
        tmp = []
        for j in range(4):
            tmp.append(Label(text=chr(current_char), font=("JetBrains Mono", 27), bg="#666666", fg="white", width=2, height=1))
            tmp[j].config(anchor=CENTER)
            tmp[j].grid(row=i, column=j+5, pady=(15, 0), padx=(0, 15))
            keylist.append(tmp)
            current_char += 1
            tmp[0].grid(padx=(WIDTH // 4, 15))

    for i in range(len(user_input.get())):
        if user_input.get()[i] in random_word and i == random_word.index(user_input.get()[i]):
            for x in keylist:
                for y in x:
                    if y['text'] == user_input.get()[i]:
                        y.config(bg="#0f4200")

if __name__ == "__main__":
    init()
    print(random_word)
    user_input.focus_set()
    update_keyboard()
    # Binding a callback function to the return key
    root.bind("<Return>", add_word)
    root.mainloop()