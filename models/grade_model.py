from models.user_model import db

class Grade(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        nullable=False
    )

    course_name = db.Column(
        db.String(100),
        nullable=False
    )

    marks = db.Column(
        db.Integer,
        nullable=False
    )

    grade = db.Column(
        db.String(5),
        nullable=False
    )

    remarks = db.Column(
        db.String(300)
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )