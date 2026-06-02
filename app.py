from flask import Flask
from config import Config
from models.user_model import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

from routes.auth_routes import *

if __name__ == "__main__":
    app.run(debug=True)