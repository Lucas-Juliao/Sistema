from flask import Blueprint, render_template, redirect, url_for, session
from .auth import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.menu'))
    return redirect(url_for('auth.login'))

@main_bp.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@main_bp.route('/people')
@login_required
def people():
    return render_template('people.html')

@main_bp.route('/courses')
@login_required
def courses():
    return render_template('courses.html')

@main_bp.route('/schedule')
@login_required
def schedule():
    return render_template('schedule.html')

@main_bp.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html')

@main_bp.route('/finance')
@login_required
def finance():
    return render_template('finance.html')
