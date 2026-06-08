from flask import Flask
import random

app = Flask(__name__)

def make_bold(func):
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper

def make_emphasis(func):
    def wrapper():
        return f"<em>{func()}</em>"
    return wrapper

def make_underline(func):
    def wrapper():
        return f"<u>{func()}</u>"
    return wrapper

@app.route("/")
@make_bold
@make_emphasis
@make_underline
def hello():    
    return "<h1>Guess a number between 0 and 9</h1><br><img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'>"

random_number = random.randint(0, 9)

@app.route("/<int:guess>")
def guess_number(guess):
    if guess > random_number:
        return "<h1 style='color: red'>Too high, try again!</h1><br><img src='https://i.giphy.com/3o6ZtaO9BZHcOjmErm.webp'>"
    elif guess < random_number:
        return "<h1 style='color: blue'>Too low, try again!</h1><br><img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>"
    else:
        return "<h1 style='color: green'>You found me!</h1><br><img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>"


@app.route("/bye")
def bye():
    return "Goodbye, World!"

@app.route("/greet/<name>/<int:age>")
def greet(name, age):
    return f"Hello there {name}!, you are {age} years old."

if __name__ == "__main__":
    app.run(debug=True)