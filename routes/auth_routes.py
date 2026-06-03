from app import app
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session
from models.course_model import Course
from models.assignment_model import Assignment
from models.teacher_assignment_model import TeacherAssignment
from models.grade_model import Grade
from models.enrollment_model import Enrollment

from models.user_model import db
from models.user_model import User

from werkzeug.utils import secure_filename
import os

def calculate_grade(marks):

    marks = int(marks)

    if marks >= 85:
        return "A"

    elif marks >= 70:
        return "B"

    elif marks >= 60:
        return "C"

    elif marks >= 50:
        return "D"

    return "F"

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
            flash("Email already exists", "danger")
            return redirect("/register")

        user = User(
            username=username,
            email=email,
            role=role
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful", "success")

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

        flash("Invalid Email or Password", "danger")

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

# Student Module

@app.route("/profile")
def profile():

    if session.get("role") != "Student":
        return redirect("/login")

    user = User.query.get(
        session["user_id"]
    )

    return render_template(
        "profile.html",
        username=user.username,
        email=user.email
    )

@app.route("/courses")
def courses():

    data = Course.query.all()

    return render_template(
        "courses.html",
        courses=data
    )

@app.route("/assignment")
def assignment():

    assignments = TeacherAssignment.query.all()

    student_submissions = Assignment.query.filter_by(
        student_id=session["user_id"]
    ).all()

    return render_template(
        "assignment.html",
        assignments=assignments,
        student_submissions=student_submissions
    )

@app.route("/status")
def status():

    assignments = Assignment.query.filter_by(
        student_id=session["user_id"]
    ).all()

    return render_template(
        "status.html",
        assignments=assignments
    )

@app.route("/grades")
def grades():

    grades = Grade.query.filter_by(
        student_id=session["user_id"]
    ).all()

    total_points = 0

    total_courses = len(grades)

    for g in grades:

        if g.grade == "A":
            total_points += 4.0

        elif g.grade == "B":
            total_points += 3.0

        elif g.grade == "C":
            total_points += 2.0

        elif g.grade == "D":
            total_points += 1.0

    gpa = 0

    if total_courses > 0:
        gpa = round(
            total_points / total_courses,
            2
        )

    return render_template(
        "grades.html",
        grades=grades,
        gpa=gpa
    )

# Teacher Module

@app.route(
    "/teacher/create_assignment",
    methods=["GET", "POST"]
)
def create_assignment():

    if request.method == "POST":

        assignment = TeacherAssignment()

        assignment.title = request.form["title"]

        assignment.description = request.form["description"]

        assignment.course_name = request.form["course_name"]

        assignment.due_date = request.form["due_date"]

        assignment.created_by = session.get(
            "username",
            "Teacher"
        )

        db.session.add(assignment)

        db.session.commit()

        return redirect(
            "/teacher/create_assignment"
        )

    assignments = TeacherAssignment.query.all()

    return render_template(
        "create_assignment.html",
        assignments=assignments
    )

@app.route(
"/teacher/edit_assignment/<int:id>",
methods=["GET","POST"]
)
def edit_assignment(id):

    assignment = TeacherAssignment.query.get(id)

    if request.method=="POST":

        assignment.title = request.form["title"]

        assignment.description = request.form["description"]

        assignment.due_date = request.form["due_date"]

        db.session.commit()

        return redirect("/teacher/assignments")

    return render_template(
        "edit_assignment.html",
        assignment=assignment
    )

@app.route("/teacher/review")
def review_submissions():

    submissions = Assignment.query.all()

    return render_template(
        "review_submissions.html",
        submissions=submissions
    )

@app.route("/teacher/grade/<int:id>", methods=["GET", "POST"])
def grade_assignment(id):

    assignment = Assignment.query.get_or_404(id)

    if request.method == "POST":

        # SAFE INPUT EXTRACTION
        marks = request.form.get("marks")
        feedback = request.form.get("feedback")

        # VALIDATION (IMPORTANT)
        if not marks:
            flash("Marks are required", "danger")
            return redirect(f"/teacher/grade/{id}")

        marks = int(marks)

        # AUTO GRADE CALCULATION
        if marks >= 85:
            calculated_grade = "A"
        elif marks >= 70:
            calculated_grade = "B"
        elif marks >= 60:
            calculated_grade = "C"
        elif marks >= 50:
            calculated_grade = "D"
        else:
            calculated_grade = "F"

        # UPDATE ASSIGNMENT
        assignment.status = "Graded"
        assignment.marks = marks
        assignment.grade = calculated_grade
        assignment.feedback = feedback

        # SAVE INTO GRADE TABLE (NO DUPLICATES)
        grade = Grade.query.filter_by(
            student_id=assignment.student_id,
            course_name="Software Quality Assurance"
        ).first()

        if not grade:
            grade = Grade()
            grade.student_id = assignment.student_id
            grade.course_name = "Software Quality Assurance"
            db.session.add(grade)

        grade.marks = marks
        grade.grade = calculated_grade
        grade.remarks = feedback

        db.session.commit()

        flash("Graded successfully", "success")

        return redirect("/teacher/review")

    return render_template(
        "grade_assignment.html",
        assignment=assignment
    )

@app.route(
    "/teacher/courses",
    methods=["GET","POST"]
)
def teacher_courses():

    if request.method == "POST":

        course = Course()

        course.course_name = request.form["course_name"]

        course.teacher_name = session["username"]

        course.description = request.form["description"]

        db.session.add(course)

        db.session.commit()

    courses = Course.query.all()

    return render_template(
        "teacher_courses.html",
        courses=courses
    )

@app.route(
"/submit_assignment/<int:id>",
methods=["GET", "POST"]
)
def submit_assignment(id):

    teacher_assignment = TeacherAssignment.query.get_or_404(id)

    # ALWAYS define existing first (prevents crash)
    existing = Assignment.query.filter_by(
        teacher_assignment_id=id,
        student_id=session["user_id"]
    ).first()

    if request.method == "POST":

        # Prevent duplicate submission
        if existing:
            flash(
                "You already submitted this assignment",
                "warning"
            )
            return redirect("/assignment")

        file = request.files.get("assignment_file")

        filename = None

        if file:
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        submission = Assignment()

        submission.teacher_assignment_id = id
        submission.student_id = session["user_id"]
        submission.title = teacher_assignment.title
        submission.file_name = filename
        submission.status = "Submitted"

        db.session.add(submission)
        db.session.commit()

        flash("Assignment submitted successfully", "success")

        return redirect("/assignment")

    return render_template(
        "submit_assignment.html",
        assignment=teacher_assignment
    )

@app.route("/enroll_course/<int:id>")
def enroll_course(id):

    course = Course.query.get_or_404(id)

    existing = Enrollment.query.filter_by(
        student_id=session["user_id"],
        course_id=id
    ).first()

    if existing:
        flash(
            "Already enrolled",
            "warning"
        )

        return redirect("/courses")

    enrollment = Enrollment()

    enrollment.student_id = session["user_id"]

    enrollment.student_name = session["username"]

    enrollment.course_id = course.id

    enrollment.course_name = course.course_name

    db.session.add(enrollment)

    db.session.commit()

    flash(
        "Course enrolled successfully",
        "success"
    )

    return redirect("/courses")

@app.route("/teacher/enrollments")
def teacher_enrollments():

    enrollments = Enrollment.query.all()

    return render_template(
        "teacher_enrollments.html",
        enrollments=enrollments
    )

#ADMIN MODULES

#Manage Users (View + Delete Users)
@app.route("/admin/users")
def manage_users():

    if session.get("role") != "Admin":
        return redirect("/login")

    users = User.query.filter(
        User.role != "Admin"
    ).all()

    return render_template(
        "manage_users.html",
        users=users
    )


@app.route("/admin/delete_user/<int:id>")
def delete_user(id):

    if session.get("role") != "Admin":
        return redirect("/login")

    user = User.query.get(id)

    if user and user.role != "Admin":
        db.session.delete(user)
        db.session.commit()

    return redirect("/admin/users")



#Assign Roles (Change Role Only)
@app.route(
    "/admin/roles",
    methods=["GET", "POST"]
)
def assign_roles():

    if session.get("role") != "Admin":
        return redirect("/login")

    if request.method == "POST":

        user_id = request.form["user_id"]

        new_role = request.form["role"]

        user = User.query.get(user_id)

        if user:
            user.role = new_role
            db.session.commit()

    users = User.query.filter(
        User.role != "Admin"
    ).all()

    return render_template(
        "assign_roles.html",
        users=users
    )

@app.route("/admin/monitor")
def system_monitor():

    total_users = User.query.count()

    total_students = User.query.filter_by(
        role="Student"
    ).count()

    total_teachers = User.query.filter_by(
        role="Teacher"
    ).count()

    total_courses = Course.query.count()

    total_assignments = TeacherAssignment.query.count()

    total_enrollments = Enrollment.query.count()

    return render_template(
        "system_monitor.html",
        total_users=total_users,
        total_students=total_students,
        total_teachers=total_teachers,
        total_courses=total_courses,
        total_assignments=total_assignments,
        total_enrollments=total_enrollments
    )

@app.route("/admin/reports")
def reports():

    enrollments = Enrollment.query.all()

    grades = Grade.query.all()

    assignments = Assignment.query.all()

    return render_template(
        "reports.html",
        enrollments=enrollments,
        grades=grades,
        assignments=assignments
    )