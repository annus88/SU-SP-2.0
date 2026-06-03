from flask import Flask
from config import Config

from models.user_model import db
from models.user_model import User
from models.course_model import Course
from models.assignment_model import Assignment
from models.grade_model import Grade
from models.teacher_assignment_model import TeacherAssignment
from models.enrollment_model import Enrollment

import os

app = Flask(__name__)

app.config.from_object(Config)

UPLOAD_FOLDER = "uploads/student_submissions"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

with app.app_context():
    db.create_all()

from routes.auth_routes import *

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )