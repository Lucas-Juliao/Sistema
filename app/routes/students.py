from flask import Blueprint, render_template, url_for, redirect, request
from app import db
from app.models.models import User, Student
from datetime import datetime
from werkzeug.security import generate_password_hash

bp = Blueprint('students', __name__, url_prefix='/students')

@bp.route('/')
def index():
    students = Student.query.all()
    return render_template('students/index.html', students=students)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        enrollment_date = datetime.strptime(request.form['enrollment_date'], '%Y-%m-%d').date()

        new_user = User(username=username, email=email, password=password, is_student=True)
        db.session.add(new_user)
        db.session.commit()

        new_student = Student(user_id=new_user.id, enrollment_date=enrollment_date)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('students.index'))
    return render_template('students/create.html')
