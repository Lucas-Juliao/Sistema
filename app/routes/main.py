from flask import Blueprint, render_template, redirect, url_for, session
from .auth import login_required
from app.database import get_db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.menu'))
    return redirect(url_for('auth.login'))

@main_bp.route('/menu')
@login_required
def menu():
    days = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
    today_idx = datetime.now().weekday()
    today_str = days[today_idx]

    db = get_db()
    # Busca a agenda dos professores para o dia de hoje
    schedules = db.execute('''
        SELECT s.*, p.name as teacher_name
        FROM schedules s
        JOIN people p ON s.teacher_id = p.id
        WHERE s.day_of_week = ?
        ORDER BY s.start_time
    ''', (today_str,)).fetchall()
    db.close()

    return render_template('menu.html', schedules=schedules, today=today_str.capitalize())

@main_bp.route('/people')
@login_required
def people():
    db = get_db()
    people_list = db.execute('SELECT * FROM people ORDER BY name').fetchall()
    db.close()
    return render_template('people.html', people=people_list)

@main_bp.route('/people/add', methods=['POST'])
@login_required
def add_person():
    from flask import request
    name = request.form.get('name')
    type = request.form.get('type')
    email = request.form.get('email')
    phone = request.form.get('phone')
    birth_date = request.form.get('birth_date')
    has_guardian = 1 if request.form.get('has_guardian') else 0
    guardian_name = request.form.get('guardian_name')
    guardian_phone = request.form.get('guardian_phone')

    if name and type:
        db = get_db()
        db.execute('''
            INSERT INTO people (name, type, email, phone, birth_date, has_guardian, guardian_name, guardian_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, type, email, phone, birth_date, has_guardian, guardian_name, guardian_phone))
        db.commit()
        db.close()

    return redirect(url_for('main.people'))

@main_bp.route('/people/edit/<int:id>', methods=['POST'])
@login_required
def edit_person(id):
    from flask import request
    name = request.form.get('name')
    type = request.form.get('type')
    email = request.form.get('email')
    phone = request.form.get('phone')
    birth_date = request.form.get('birth_date')
    has_guardian = 1 if request.form.get('has_guardian') else 0
    guardian_name = request.form.get('guardian_name')
    guardian_phone = request.form.get('guardian_phone')

    if name and type:
        db = get_db()
        db.execute('''
            UPDATE people
            SET name = ?, type = ?, email = ?, phone = ?, birth_date = ?, has_guardian = ?, guardian_name = ?, guardian_phone = ?
            WHERE id = ?
        ''', (name, type, email, phone, birth_date, has_guardian, guardian_name, guardian_phone, id))
        db.commit()
        db.close()

    return redirect(url_for('main.people'))

@main_bp.route('/people/delete/<int:id>')
@login_required
def delete_person(id):
    db = get_db()
    db.execute('DELETE FROM people WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('main.people'))

@main_bp.route('/courses')
@login_required
def courses():
    db = get_db()
    courses_list = db.execute('''
        SELECT c.*, p.name as teacher_name
        FROM courses c
        LEFT JOIN people p ON c.teacher_id = p.id
        ORDER BY c.name
    ''').fetchall()
    teachers = db.execute("SELECT * FROM people WHERE type = 'teacher' ORDER BY name").fetchall()
    db.close()
    return render_template('courses.html', courses=courses_list, teachers=teachers)

@main_bp.route('/courses/add', methods=['POST'])
@login_required
def add_course():
    from flask import request
    name = request.form.get('name')
    workload = request.form.get('workload')
    teacher_id = request.form.get('teacher_id')

    if name:
        db = get_db()
        db.execute('INSERT INTO courses (name, workload, teacher_id) VALUES (?, ?, ?)',
                   (name, workload, teacher_id or None))
        db.commit()
        db.close()

    return redirect(url_for('main.courses'))

@main_bp.route('/courses/edit/<int:id>', methods=['POST'])
@login_required
def edit_course(id):
    from flask import request
    name = request.form.get('name')
    workload = request.form.get('workload')
    teacher_id = request.form.get('teacher_id')

    if name:
        db = get_db()
        db.execute('UPDATE courses SET name = ?, workload = ?, teacher_id = ? WHERE id = ?',
                   (name, workload, teacher_id or None, id))
        db.commit()
        db.close()

    return redirect(url_for('main.courses'))

@main_bp.route('/courses/delete/<int:id>')
@login_required
def delete_course(id):
    db = get_db()
    db.execute('DELETE FROM courses WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('main.courses'))

@main_bp.route('/schedule')
@login_required
def schedule():
    db = get_db()
    schedules_list = db.execute('''
        SELECT s.*, p.name as teacher_name
        FROM schedules s
        JOIN people p ON s.teacher_id = p.id
        ORDER BY CASE s.day_of_week
            WHEN 'segunda-feira' THEN 1
            WHEN 'terça-feira' THEN 2
            WHEN 'quarta-feira' THEN 3
            WHEN 'quinta-feira' THEN 4
            WHEN 'sexta-feira' THEN 5
            WHEN 'sábado' THEN 6
            WHEN 'domingo' THEN 7
        END, s.start_time
    ''').fetchall()
    teachers = db.execute("SELECT * FROM people WHERE type = 'teacher' ORDER BY name").fetchall()
    db.close()
    return render_template('schedule.html', schedules=schedules_list, teachers=teachers)

@main_bp.route('/schedule/add', methods=['POST'])
@login_required
def add_schedule():
    from flask import request
    teacher_id = request.form.get('teacher_id')
    day_of_week = request.form.get('day_of_week')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    course_name = request.form.get('course_name')
    room = request.form.get('room')

    if teacher_id and day_of_week and start_time and end_time:
        db = get_db()
        db.execute('''
            INSERT INTO schedules (teacher_id, day_of_week, start_time, end_time, course_name, room)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (teacher_id, day_of_week, start_time, end_time, course_name, room))
        db.commit()
        db.close()

    return redirect(url_for('main.schedule'))

@main_bp.route('/schedule/edit/<int:id>', methods=['POST'])
@login_required
def edit_schedule(id):
    from flask import request
    teacher_id = request.form.get('teacher_id')
    day_of_week = request.form.get('day_of_week')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    course_name = request.form.get('course_name')
    room = request.form.get('room')

    if teacher_id and day_of_week and start_time and end_time:
        db = get_db()
        db.execute('''
            UPDATE schedules
            SET teacher_id = ?, day_of_week = ?, start_time = ?, end_time = ?, course_name = ?, room = ?
            WHERE id = ?
        ''', (teacher_id, day_of_week, start_time, end_time, course_name, room, id))
        db.commit()
        db.close()

    return redirect(url_for('main.schedule'))

@main_bp.route('/schedule/delete/<int:id>')
@login_required
def delete_schedule(id):
    db = get_db()
    db.execute('DELETE FROM schedules WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('main.schedule'))

@main_bp.route('/attendance')
@login_required
def attendance():
    db = get_db()
    # Pega todas as presenças registradas
    attendances = db.execute('''
        SELECT a.*, p.name as student_name, s.course_name, t.name as teacher_name
        FROM attendance a
        JOIN people p ON a.student_id = p.id
        JOIN schedules s ON a.schedule_id = s.id
        JOIN people t ON s.teacher_id = t.id
        ORDER BY a.date DESC
    ''').fetchall()

    # Dados para o formulário de adição
    students = db.execute("SELECT * FROM people WHERE type = 'student' ORDER BY name").fetchall()
    schedules = db.execute('''
        SELECT s.*, p.name as teacher_name
        FROM schedules s
        JOIN people p ON s.teacher_id = p.id
    ''').fetchall()

    db.close()
    return render_template('attendance.html', attendances=attendances, students=students, schedules=schedules)

@main_bp.route('/attendance/add', methods=['POST'])
@login_required
def add_attendance():
    from flask import request
    schedule_id = request.form.get('schedule_id')
    student_id = request.form.get('student_id')
    date = request.form.get('date')
    status = request.form.get('status')

    if schedule_id and student_id and date and status:
        db = get_db()
        db.execute('''
            INSERT INTO attendance (schedule_id, student_id, date, status)
            VALUES (?, ?, ?, ?)
        ''', (schedule_id, student_id, date, status))
        db.commit()
        db.close()

    return redirect(url_for('main.attendance'))

@main_bp.route('/attendance/delete/<int:id>')
@login_required
def delete_attendance(id):
    db = get_db()
    db.execute('DELETE FROM attendance WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('main.attendance'))

@main_bp.route('/finance')
@login_required
def finance():
    db = get_db()
    transactions = db.execute('SELECT * FROM finance ORDER BY date DESC').fetchall()

    # Cálculos simples
    total_receita = db.execute("SELECT SUM(amount) FROM finance WHERE type = 'receita'").fetchone()[0] or 0
    total_despesa = db.execute("SELECT SUM(amount) FROM finance WHERE type = 'despesa'").fetchone()[0] or 0
    saldo = total_receita - total_despesa

    db.close()
    return render_template('finance.html',
                           transactions=transactions,
                           total_receita=total_receita,
                           total_despesa=total_despesa,
                           saldo=saldo)

@main_bp.route('/finance/add', methods=['POST'])
@login_required
def add_transaction():
    from flask import request
    description = request.form.get('description')
    amount = request.form.get('amount')
    type = request.form.get('type')
    date = request.form.get('date')
    status = request.form.get('status')

    if description and amount and type and date:
        db = get_db()
        db.execute('''
            INSERT INTO finance (description, amount, type, date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (description, amount, type, date, status))
        db.commit()
        db.close()

    return redirect(url_for('main.finance'))

@main_bp.route('/finance/delete/<int:id>')
@login_required
def delete_transaction(id):
    db = get_db()
    db.execute('DELETE FROM finance WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('main.finance'))
