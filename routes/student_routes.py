from models.teacher_assignment_model import TeacherAssignment

@app.route("/assignment")
def assignment_page():

    assignments = TeacherAssignment.query.all()

    return render_template(
        "assignment_page.html",
        assignments=assignments
    )