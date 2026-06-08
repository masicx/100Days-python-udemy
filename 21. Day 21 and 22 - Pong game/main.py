from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("My Pong Game")
screen.tracer(0)

l_paddle = Paddle([-360, 0])
r_paddle = Paddle([360, 0])
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(r_paddle.up, "Up")
screen.onkeypress(r_paddle.down, "Down")
screen.onkeypress(l_paddle.up, "w")
screen.onkeypress(l_paddle.down, "s")
game_speed = 0.1

game_is_on = True
while game_is_on:
    time.sleep(game_speed)
    screen.update()
    ball.move()

    # Detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()
    
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.increase_l_score()

    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.increase_r_score()

    # Detect collision with paddle
    if ball.distance(r_paddle) < 50 and ball.xcor() > 330 or ball.distance(l_paddle) < 50 and ball.xcor() < -330:

        ball.bounce_x()

screen.exitonclick()
