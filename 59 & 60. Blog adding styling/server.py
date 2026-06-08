from flask import Flask, render_template, request
import requests
import smtplib

BLOG_API = "https://api.npoint.io/c094062ae0badad27a81"

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get(BLOG_API)
    posts = response.json()
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def post(post_id):
    response = requests.get(BLOG_API)
    post = [post for post in response.json() if post["id"] == post_id][0]
    return render_template("post.html", post=post)

@app.route("/about")
def about():
    return render_template("about.html")

@app.get("/contact")
def contact():
    return render_template("contact.html")

@app.post("/contact")
def contact_post():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    print(name, email, phone, message)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("masicx@gmail.com", "ktqs lfhj tjml diux")
    server.sendmail("masicx@gmail.com", email, f"Subject: New message from {name} \n\n {message} {phone}")
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)