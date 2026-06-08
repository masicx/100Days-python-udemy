# with open(r"C:\Code\100DaysCourse\25. Working with csv and the pandas library\weather_data.csv", "r") as file:
#     data = file.readlines()

# import csv
# with open(r"C:\Code\100DaysCourse\25. Working with csv and the pandas library\weather_data.csv", "r") as file:
#     data = csv.reader(file)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))

# print(temperatures)

# import pandas

# data = pandas.read_csv(r"C:\Code\100DaysCourse\25. Working with csv and the pandas library\weather_data.csv")
# print(data["temp"])

# temp_list = data["temp"].to_list()
# print(len(temp_list))

# print(data["temp"].mean())
# print(data["temp"].max())

# Get data in columns
# print(data["condition"])
# print(data.condition)

# Get data in rows
# print(data[data.day == "Monday"])
# print(data[data.temp == data.temp.max()])

# monday = data[data.day == "Monday"]
# print(monday.condition)
# print(monday.temp * 1.8 + 32)

# Create a dataframe from scratch
# data_dict = {
#     "students": ["Amy", "James", "Angela"],
#     "scores": [76, 56, 65]
# }
# data = pandas.DataFrame(data_dict)
# data.to_csv(r"C:\Code\100DaysCourse\25. Working with csv and the pandas library\new_data.csv")

# data = pandas.read_csv(r"C:\Code\100DaysCourse\25. Working with csv and the pandas library\Squirrel_Data.csv")
# grey_squirrels_count = len(data[data["Primary Fur Color"] == "Gray"])
# red_squirrels_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
# black_squirrels_count = len(data[data["Primary Fur Color"] == "Black"])

# data_dict = {
#     "Fur Color": ["Gray", "Cinnamon", "Black"],
#     "Count": [grey_squirrels_count, red_squirrels_count, black_squirrels_count]
# }

# df = pandas.DataFrame(data_dict)
# df.to_csv(r"C:\Code\100DaysCourse\25. Working with csv and the pandas library\squirrel_count.csv")

import turtle
import pandas

states_data = pandas.read_csv(r"C:\Code\100DaysCourse\25. Working with csv and the pandas library\50_states.csv")

screen = turtle.Screen()
screen.title("U.S. States Game")
image = r"C:\Code\100DaysCourse\25. Working with csv and the pandas library\blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

def get_mouse_click_coor(x, y):
    print(x, y)

turtle.onscreenclick(get_mouse_click_coor)

guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 Guess the State", 
                                    prompt="What's another state's name?").title()
    
    if answer_state == "Exit":
        break
    state = states_data[states_data["state"] == answer_state]
    if state.empty:
        print("Not found")
    else:
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(state.x.item(), state.y.item())
        t.write(answer_state)
        guessed_states.append(answer_state)

