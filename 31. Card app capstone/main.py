from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = None
word_text = None
title_text = None
current_card = {}
#-------------------- Data ----------------------#
try:
    csv = pandas.read_csv("data/german_words_to_learn.csv")
except FileNotFoundError:
    csv = pandas.read_csv("data/german_words.csv")
to_learn = csv.to_dict(orient="records")
image = None
after = None

def next_card():
    global current_card
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text="German", fill="black")
    canvas.itemconfig(word_text, text=current_card["German"], fill="black")
    canvas.itemconfig(image, image=card_front_image)
    global after
    if after:
        window.after_cancel(after)
    after = window.after(3000, flip_card)

def is_known():
    if len(to_learn) > 0:
        to_learn.remove(current_card)
    data_frame = pandas.DataFrame(to_learn)
    data_frame.to_csv("data/german_words_to_learn.csv", index=False)
    next_card()

# ------------------- Counter ----------------------#
def flip_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(image, image=card_back_image)
    


# ------------------- Setup UI ----------------------#
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
after = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
image = canvas.create_image(400, 263, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

title_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

unknown_image = PhotoImage(file="images/wrong.png")
button_unknown = Button(image=unknown_image, highlightthickness=0, command=next_card)
button_unknown.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
button_right = Button(image=right_image, highlightthickness=0, command=is_known)
button_right.grid(column=1, row=1)

next_card()

window.mainloop()