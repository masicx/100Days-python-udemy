from turtle import Turtle, Screen, colormode
import random
# from turtle import * # This will import all the functions from the turtle module, 
#                        but it's not recommended to use this approach as it can lead to conflicts with other functions in your code.
# import turtle as t # This will import the turtle module and give it an alias 't', which can be used to access its functions.

# COLORS = ['DarkOrchid', 'LightSeaGreen', 'CornFlowerBlue', 'Orange', 'SlateGray', 'SeaGreen', 'Gray']
DIRECTIONS = [0, 90, 180, 270]

def draw_shape(sides):
    angle = 360 / sides
    for _ in range(sides):
        tim.forward(100)
        tim.right(angle)

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

tim = Turtle()
tim.speed(10)
tim.pensize(5)
colormode(255) # This sets the color mode to 255, allowing you to use RGB values for colors.


# tim.shape("circle")
# tim.color("blue")
# draw a dashed line
# for _ in range(15):
#     tim.penup()
#     tim.forward(5)
#     tim.pendown()
#     tim.forward(10)

# for index in range(3, 9):
#     draw_shape(index)
#     tim.color(random.choice(COLORS))

screen = Screen()

for _ in range(200):
    tim.color(random_color())
    tim.forward(30)
    tim.setheading(random.choice(DIRECTIONS))

screen.exitonclick()