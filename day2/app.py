from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# zadefinujeme si nasu Flask aplikaciu
app = Flask(__name__)

# toto by mal byt nejaky nahodny string,
# pouziva sa na sifrovanie sessionov:
app.config["SECRET_KEY"] = "nieco"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

from models import *

db.create_all()

@app.route("/")
def index():
    posts = Post.query.order_by(Post.created.desc()).limit(20).all()
    return render_template("index.html", posts=posts)


@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    if "name" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        post = Post()
        post.code = request.form.get("code")
        post.text = request.form.get("text")
        post.user_id = session["id"]
        post.created = datetime.now()

        db.session.add(post)
        db.session.commit()

        return redirect("/")

    return render_template("new_post.html")


@app.route("/logout")
def logout():
    del session["name"]
    del session["id"]
    return "si odhlaseny."


@app.route("/login", methods=["GET", "POST"])
def login():
    if "name" in session:
        return redirect("/")

    error = False

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                session["name"] = user.name
                session["id"] = user.id
                return redirect("/")
            else:
                error = "Email alebo heslo je nespravne."
        else:
            error = "Email alebo heslo je nespravne."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if password != password2:
            error = "Hesla nie su rovnake."
        elif len(password) < 6:
            error = "Heslo je kratke."
        else:
            user = User()
            user.name = name
            user.email = email
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            session["name"] = name
            session["id"] = user.id
            return redirect("/")

    return render_template("register.html", error=error)
