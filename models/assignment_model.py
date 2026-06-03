from models.user_model import db

class Assignment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    teacher_assignment_id = db.Column(
        db.Integer,
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    file_name = db.Column(
        db.String(300)
    )

    status = db.Column(
        db.String(50),
        default="Pending Review"
    )

    marks = db.Column(
        db.Integer,
        default=0
    )

    grade = db.Column(
        db.String(5)
    )

    feedback = db.Column(
        db.String(500)
    )