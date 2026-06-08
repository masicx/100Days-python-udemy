from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"

timer = ""
repetition = 0
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global repetition
    repetition = 0
    canvas.itemconfig(timer_text, text="00:00")
    label_title.config(text="Timer", fg=GREEN)
    window.after_cancel(timer)

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global repetition
    repetition += 1
    if timer != "":
        window.after_cancel(timer)
    
    if repetition % 8 == 0:
        label_title.config(text="Long Break", fg=RED)
        repetition = 0
        count_down(LONG_BREAK_MIN * 60)
    elif repetition % 2 == 0:
        label_title.config(text="Break", fg=PINK)
        count_down(SHORT_BREAK_MIN * 60)
    else:
        label_title.config(text="Work", fg=GREEN)
        count_down(WORK_MIN * 60)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    canvas.itemconfig(timer_text, text=f"{count // 60:02d}:{count % 60:02d}") # 2d means 2 digits (count)
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        window.focus()
        window.bell()
    marks = ""
    work_sessions = repetition // 2
    for _ in range(work_sessions):
        marks += CHECK_MARK
    label_check.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

label_title = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, 'bold'))
label_title.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
photo_image = PhotoImage(file=r"C:\Code\100DaysCourse\28. Pomodoro\tomato.png")
canvas.create_image(100, 112, image=photo_image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")) 
canvas.grid(column=1, row=1)

button_start = Button(text="Start", highlightthickness=0, command=start_timer)
button_start.grid(column=0, row=2)

label_check = Label(fg=GREEN, bg=YELLOW, text="")
label_check.grid(column=1, row=3)

button_reset = Button(text="Reset", highlightthickness=0, command=reset_timer)
button_reset.grid(column=2, row=2)

window.mainloop()