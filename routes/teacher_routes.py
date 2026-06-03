from models.teacher_assignment_model import TeacherAssignment

@app.route(
"/teacher/create_assignment",
methods=["GET","POST"]
)
def create_assignment():

    if request.method=="POST":

        obj = TeacherAssignment()

        obj.title = request.form["title"]

        obj.description = request.form["description"]

        obj.course_name = request.form["course_name"]

        obj.due_date = request.form["due_date"]

        db.session.add(obj)

        db.session.commit()

        return redirect(
            "/teacher/create_assignment"
        )

    return render_template(
        "create_assignment.html"
    )