from tkinter import *

timer = None

def count_down(count: int):
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        entry.delete("1.0", END)
    label.config(text=f"00:{count:02d}")


def start_timer():
    global timer
    if timer is not None:
        window.after_cancel(timer)

    count_down(5)

def on_text_changed(event):
    start_timer()
    words = len(entry.get("1.0", END).split())
    label_words.config(text=f"{words} Words")
    entry.edit_modified(False)

window = Tk()
window.title("Disappearing text writing app")

label = Label(text="00:05")
label.grid(column=1, row=0)

entry = Text(window, wrap="word", height=5)
entry.grid(column=1, row=1, rowspan=2)
entry.bind("<<Modified>>", on_text_changed)

label_words = Label(text="Words")
label_words.grid(column=1, row=3)

start_timer()

window.mainloop()