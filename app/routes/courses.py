from flask import Blueprint, render_template, url_for, redirect, request
from app import db
from app.models.models import Course, Teacher

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/')
def index():
    courses = Course.query.all()
    return render_template('courses/index.html', courses=courses)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    teachers = Teacher.query.all()
    if request.method == 'POST':
        name = request.form['name']
        teacher_id = request.form['teacher_id']

        new_course = Course(name=name, teacher_id=teacher_id)
        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('courses.index'))
    return render_template('courses/create.html', teachers=teachers)
