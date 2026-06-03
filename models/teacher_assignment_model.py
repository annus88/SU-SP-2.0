from models.user_model import db

class TeacherAssignment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.String(500)
    )

    course_name = db.Column(
        db.String(100)
    )

    due_date = db.Column(
        db.String(50)
    )

    created_by = db.Column(
        db.String(100)
    )