from app import app
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from models.user_model import db
from models.user_model import User


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists")
            return redirect("/register")

        user = User(
            username=username,
            email=email,
            role=role
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")

        return redirect("/login")

    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")