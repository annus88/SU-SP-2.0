from models.user_model import db

class Course(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course_name = db.Column(
        db.String(100),
        nullable=False
    )

    teacher_name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(300)
    )