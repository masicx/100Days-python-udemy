from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

"""
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
"""
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.secret_key = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkOGYwZTg5YWU1OWZkMDRhNDViNmRmODU0ZTc2NmJiNiIsIm5iZiI6MTc4MDg5MDA3MC45OTksInN1YiI6IjZhMjYzOWQ2NmEwMzllMDVjMDllOWU1ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.QRFPpQkEBm__6qxkCcvSernk3O5TEiXE-kbJgFf55dk",
    "api-key": "d8f0e89ae59fd04a45b6df854e766bb6"
}


# CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# with app.app_context():
#     db.create_all()

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )

# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()


class MovieEditForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


class MovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    movies = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())
    ).scalars()
    return render_template("index.html", movies=movies)


@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = MovieEditForm()
    movie_to_update = db.session.execute(
        db.select(Movie).where(Movie.id == movie_id)
    ).scalar()
    if form.validate_on_submit():
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    form.rating.data = movie_to_update.rating
    form.review.data = movie_to_update.review
    return render_template("edit.html", form=form, movie=movie_to_update)


@app.route("/delete/<int:movie_id>", methods=["GET", "POST"])
def delete(movie_id):
    movie_to_delete = db.session.execute(
        db.select(Movie).where(Movie.id == movie_id)
    ).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={
                "query": movie_title,
                "include_adult": "true",
            },
            headers=headers
        )
        data = response.json()
        return render_template("select.html", movies=data["results"])
    return render_template("add.html", form=form)


@app.route("/select/<int:movie_id>", methods=["GET"])
def select(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}", 
        params={"movie_id": movie_id},
        headers=headers
    )
    data = response.json()
    movie_to_add = Movie()
    movie_to_add.title = data["title"]
    movie_to_add.year = data["release_date"]
    movie_to_add.description = data["overview"]
    movie_to_add.rating = 0
    movie_to_add.ranking = 0
    movie_to_add.review = ""
    movie_to_add.img_url = f"{MOVIE_DB_IMAGE_URL}{data["poster_path"]}"

    db.session.add(movie_to_add)
    db.session.commit()
    return redirect(url_for("edit", movie_id=movie_to_add.id))


if __name__ == "__main__":
    app.run(debug=True)
