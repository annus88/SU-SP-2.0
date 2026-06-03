from models.user_model import db

class Enrollment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        nullable=False
    )

    student_name = db.Column(
        db.String(100),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        nullable=False
    )

    course_name = db.Column(
        db.String(100),
        nullable=False
    )