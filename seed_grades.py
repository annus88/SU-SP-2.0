from app import app
from models.user_model import db
from models.grade_model import Grade

with app.app_context():

    g = Grade(
        student_id=1,
        course_name="Software Quality Assurance",
        marks=88,
        grade="A"
    )

    db.session.add(g)

    db.session.commit()