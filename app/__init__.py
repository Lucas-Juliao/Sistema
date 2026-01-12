import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.routes import students, teachers, courses, financial
app.register_blueprint(students.bp)
app.register_blueprint(teachers.bp)
app.register_blueprint(courses.bp)
app.register_blueprint(financial.bp)

from app import models
