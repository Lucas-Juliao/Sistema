from flask import Blueprint, render_template, url_for, redirect, request
from app import db
from app.models.models import User, Teacher
from datetime import datetime
from werkzeug.security import generate_password_hash

bp = Blueprint('teachers', __name__, url_prefix='/teachers')

@bp.route('/')
def index():
    teachers = Teacher.query.all()
    return render_template('teachers/index.html', teachers=teachers)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()

        new_user = User(username=username, email=email, password=password, is_teacher=True)
        db.session.add(new_user)
        db.session.commit()

        new_teacher = Teacher(user_id=new_user.id, hire_date=hire_date)
        db.session.add(new_teacher)
        db.session.commit()

        return redirect(url_for('teachers.index'))
    return render_template('teachers/create.html')
