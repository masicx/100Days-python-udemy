from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


app = Flask(__name__)
app.secret_key = "super secret key"
boostrap = Bootstrap5(app)


class LoginForm(FlaskForm):
    username = EmailField('Username', validators=[InputRequired(), Email(), Length(min=4, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=30)])
    submit = SubmitField('Log in')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "admin@email.com" and form.password.data == "12345678":
            return render_template("success.html", username=form.username.data)
        else:
            return render_template("denied.html", username=form.username.data)
    return render_template("login.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
