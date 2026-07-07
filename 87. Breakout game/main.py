"""
Controles:
    Flecha Izquierda -> Mover paleta a la izquierda
    Flecha Derecha   -> Mover paleta a la derecha
    Espacio          -> Pausar / Reanudar
"""

import turtle
import time

WIDTH_SCREEN = 800
HEIGHT_SCREEN = 600
COLOR_FONDO = "black"

BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_COLORS = ["red", "orange", "yellow", "green", "cyan"]


# ---------------------------------------------------------
# Class: Paleta (Paddle)
# ---------------------------------------------------------
class Paddle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=6)
        self.penup()
        self.goto(0, -HEIGHT_SCREEN / 2 + 40)
        self.move_speed = 25

    def move_left(self):
        new_x = self.xcor() - self.move_speed
        left_limit = -WIDTH_SCREEN / 2 + 60
        if new_x < left_limit:
            new_x = left_limit
        self.setx(new_x)

    def move_right(self):
        new_x = self.xcor() + self.move_speed
        right_limit = WIDTH_SCREEN / 2 - 60
        if new_x > right_limit:
            new_x = right_limit
        self.setx(new_x)


# ---------------------------------------------------------
# Class: Ball (Ball)
# ---------------------------------------------------------
class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, -100)
        self.dx = 4
        self.dy = 4

    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1

    def restart(self):
        self.goto(0, -100)
        self.dx = 4
        self.dy = 4


# ---------------------------------------------------------
# Class: Brick (Brick)
# ---------------------------------------------------------
class Brick(turtle.Turtle):
    def __init__(self, x, y, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.penup()
        self.goto(x, y)
        self.destroyed = False

    def destroy(self):
        self.destroyed = True
        self.hideturtle()
        self.goto(2000, 2000) 


# ---------------------------------------------------------
# Class: Scoreboard
# ---------------------------------------------------------
class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, HEIGHT_SCREEN / 2 - 40)
        self.points = 0
        self.lives = 3
        self.update()

    def update(self):
        self.clear()
        self.write(
            f"Points: {self.points}    Lives: {self.lives}",
            align="center",
            font=("Courier", 18, "normal"),
        )

    def add_points(self, valor=10):
        self.points += valor
        self.update()

    def lose_live(self):
        self.lives -= 1
        self.update()

    def final_message(self, texto):
        self.goto(0, 0)
        self.write(texto, align="center", font=("Courier", 24, "bold"))


# ---------------------------------------------------------
# Class: Game
# ---------------------------------------------------------
class GameBreakout:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Breakout - Python + Turtle (POO)")
        self.screen.bgcolor(COLOR_FONDO)
        self.screen.setup(width=WIDTH_SCREEN, height=HEIGHT_SCREEN)
        self.screen.tracer(0)

        self.paddle = Paddle()
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.bricks = []
        self.paused = False
        self.is_active = True

        self.create_bricks()
        self.setup_controls()

    def create_bricks(self):
        width_Brick = 60
        height_Brick = 20
        margin_x = 10
        margin_y = 10
        start_y = HEIGHT_SCREEN / 2 - 100

        for fila in range(BRICK_ROWS):
            color = BRICK_COLORS[fila % len(BRICK_COLORS)]
            y = start_y - fila * (height_Brick + margin_y)
            for col in range(BRICK_COLUMNS):
                x = (
                    -WIDTH_SCREEN / 2
                    + margin_x
                    + width_Brick / 2
                    + col * (width_Brick + margin_x)
                )
                brick = Brick(x, y, color)
                self.bricks.append(brick)

    def setup_controls(self):
        self.screen.listen()
        self.screen.onkeypress(self.paddle.move_left, "Left")
        self.screen.onkeypress(self.paddle.move_right, "Right")
        self.screen.onkeypress(self.toggle_pause, "space")

    def toggle_pause(self):
        self.paused = not self.paused

    def paddle_collision(self):
        p = self.ball
        paddle = self.paddle
        if (
            p.ycor() <= paddle.ycor() + 15
            and p.ycor() >= paddle.ycor() - 5
            and paddle.xcor() - 55 <= p.xcor() <= paddle.xcor() + 55
            and p.dy < 0
        ):
            p.bounce_y()

    def border_collision(self):
        p = self.ball
        
        if p.xcor() >= WIDTH_SCREEN / 2 - 20 or p.xcor() <= -WIDTH_SCREEN / 2 + 20:
            p.bounce_x()
        
        if p.ycor() >= HEIGHT_SCREEN / 2 - 20:
            p.bounce_y()
        
        if p.ycor() <= -HEIGHT_SCREEN / 2 + 20:
            self.scoreboard.lose_live()
            if self.scoreboard.lives <= 0:
                self.end_game("Game Over!")
            else:
                p.restart()

    def brick_collision(self):
        p = self.ball
        for brick in self.bricks:
            if not brick.destroyed and p.distance(brick) < 30:
                brick.destroy()
                p.bounce_y()
                self.scoreboard.add_points(10)

        if all(l.destroyed for l in self.bricks):
            self.end_game("Congratulations, you won!")

    def end_game(self, message):
        self.is_active = False
        self.ball.dx = 0
        self.ball.dy = 0
        self.scoreboard.final_message(message)

    def execute(self):
        while True:
            self.screen.update()
            if self.is_active and not self.paused:
                self.ball.move()
                self.border_collision()
                self.paddle_collision()
                self.brick_collision()
            time.sleep(1 / 60)  # ~60 FPS


if __name__ == "__main__":
    game = GameBreakout()
    game.execute()