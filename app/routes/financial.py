from flask import Blueprint, render_template, url_for, redirect, request
from app import db
from app.models.models import Transaction, Student
from datetime import datetime

bp = Blueprint('financial', __name__, url_prefix='/financial')

@bp.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('financial/index.html', transactions=transactions)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    students = Student.query.all()
    if request.method == 'POST':
        amount = request.form['amount']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        student_id = request.form['student_id']
        description = request.form['description']

        new_transaction = Transaction(amount=amount, date=date, student_id=student_id, description=description)
        db.session.add(new_transaction)
        db.session.commit()

        return redirect(url_for('financial.index'))
    return render_template('financial/create.html', students=students)
