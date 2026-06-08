import tkinter

def button_clicked():
    label_kilometers["text"] = round(float(entry.get()) * 1.609, 2)

window = tkinter.Tk()
window.title("My First GUI Program")
window.config(padx=20, pady=20)

# Label
my_label = tkinter.Label(text='Is equal to')
my_label.grid(column=0, row=1)

# Entry
entry = tkinter.Entry(width=20)
entry.grid(column=1, row=0)

label_miles = tkinter.Label(text='Miles')
label_miles.grid(column=2, row=0)

label_kilometers = tkinter.Label(text='0')
label_kilometers.grid(column=1, row=1)

label_km = tkinter.Label(text='Km')
label_km.grid(column=2, row=1)

# Button
button = tkinter.Button(text='Click Me')
button["command"] = button_clicked
button.grid(column=1, row=2)

window.mainloop()