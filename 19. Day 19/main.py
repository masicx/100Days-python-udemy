import random
from turtle import Turtle, Screen

screen = Screen()
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
is_race_on = False

screen.setup(500, 400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
turtles = []
for turtle_index in range(0, 6):
    new_turtle = Turtle("turtle")
    new_turtle.color(COLORS[turtle_index])
    new_turtle.penup()
    new_turtle.goto(-230, -100 + turtle_index * 30)
    turtles.append(new_turtle)

is_race_on = True
winning_color = ""

while is_race_on:
    for turtle in turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.color()
            break
        rand_distance = random.randint(0,10)
        turtle.forward(rand_distance)

if winning_color == user_bet:
    print("You win!")
else:
    print(f"You failed, the winner is {winning_color}")
screen.exitonclick()
