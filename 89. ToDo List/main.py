from flask import Flask, jsonify, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
from datetime import datetime


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)


class ToDo(db.Model):
    __tablename__ = "to_do"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    dueDate: Mapped[str] = mapped_column(String(250), nullable=True)
    isChecked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    createdAt: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    todos = db.session.execute(db.select(ToDo)).scalars().all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    new_todo = ToDo(
        text=request.form.get("text"),
        dueDate=request.form.get("dueDate", type=str) if request.form.get("dueDate", type=str) is not None else "",
        isChecked=request.form.get("isChecked", type=bool) if request.form.get("isChecked", type=bool) is not None else False,
        createdAt=datetime.now().date().strftime("%Y-%m-%d"),
    )
    db.session.add(new_todo)
    db.session.commit()
    return redirect("/")

@app.route("/check/<int:id>", methods=["GET", "POST"])
def check(id):
    todo = db.session.get(ToDo, id)
    if todo:
        todo.isChecked = not todo.isChecked
        db.session.commit()
        if request.method == "POST":
            return jsonify({"success": True, "isChecked": todo.isChecked})
    return redirect("/")

@app.get("/delete/<int:id>")
def delete(id):
    todo = db.session.get(ToDo, id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
