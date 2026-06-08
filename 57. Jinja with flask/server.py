from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/")
def home():
    response_json = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
    return render_template("index.html", posts=response_json)

# @app.route("/guess/<name>")
# def guess(name):
#     gender = requests.get("https://api.genderize.io/?name=" + name).json()["gender"]
#     age_response = requests.get("https://api.agify.io/?name=" + name).json()
#     age = age = 0 if age_response["age"] is None else age_response["age"]
#     name = name.title()
#     return render_template("guess.html", name=name, age=age, gender=gender)

@app.route("/blog/<int:number>")
def get_blog(number):
    response_json = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
    post = [post for post in response_json if post["id"] == number][0]
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)