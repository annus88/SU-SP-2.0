from app import app
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session

from models.user_model import db
from models.user_model import User


@app.route("/")
def home():
    return redirect("/login")


# REGISTER

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


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            if user.role == "Student":
                return redirect("/student")

            elif user.role == "Teacher":
                return redirect("/teacher")

            elif user.role == "Admin":
                return redirect("/admin")

        flash("Invalid Credentials")

    return render_template("login.html")


# LOGOUT

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# STUDENT DASHBOARD

@app.route("/student")
def student_dashboard():

    if session.get("role") != "Student":
        return redirect("/login")

    return render_template("student_dashboard.html")


# TEACHER DASHBOARD

@app.route("/teacher")
def teacher_dashboard():

    if session.get("role") != "Teacher":
        return redirect("/login")

    return render_template("teacher_dashboard.html")


# ADMIN DASHBOARD

@app.route("/admin")
def admin_dashboard():

    if session.get("role") != "Admin":
        return redirect("/login")

    return render_template("admin_dashboard.html")


# PASSWORD RESET PAGE

@app.route("/forgot-password")
def forgot_password():

    return render_template("forgot_password.html")