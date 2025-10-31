from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('dashboard.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/users')
def users():
    return render_template('users.html')

@main_bp.route('/settings')
def settings():
    return render_template('settings.html')
