from app import app
from models.user_model import db
from models.course_model import Course

with app.app_context():
    c1 = Course(
        course_name="Software Quality Assurance",
        teacher_name="Safoora"
    )

    c2 = Course(
        course_name="Web Engineering",
        teacher_name="Ali"
    )

    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()

    print("Courses added successfully!")