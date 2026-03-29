import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

DATABASE = 'instance/safira.db'

def get_db():
    if not os.path.exists('instance'):
        os.makedirs('instance')
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    cursor = db.cursor()

    # Tabela de Usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')

    # Criar usuário administrador se não existir
    cursor.execute("SELECT * FROM users WHERE username = 'adm'")
    if not cursor.fetchone():
        password_hash = generate_password_hash('adm')
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ('adm', password_hash))

    # Tabela de Pessoas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL, -- 'student' ou 'teacher'
        email TEXT,
        phone TEXT,
        birth_date TEXT,
        has_guardian INTEGER DEFAULT 0,
        guardian_name TEXT,
        guardian_phone TEXT
    )
    ''')

    # Adicionar novas colunas se não existirem
    new_people_columns = [
        ('birth_date', 'TEXT'),
        ('has_guardian', 'INTEGER DEFAULT 0'),
        ('guardian_name', 'TEXT'),
        ('guardian_phone', 'TEXT')
    ]
    for col_name, col_type in new_people_columns:
        try:
            cursor.execute(f"ALTER TABLE people ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass

    # Tabela de Cursos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        workload INTEGER,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES people (id)
    )
    ''')

    # Tabela de Agenda (Disponibilidade dos Professores)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        day_of_week TEXT NOT NULL, -- 'segunda-feira', 'terça-feira', etc.
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        course_name TEXT,
        room TEXT,
        FOREIGN KEY (teacher_id) REFERENCES people (id)
    )
    ''')

    # Garantir que a coluna 'room' existe caso a tabela já tenha sido criada anteriormente
    try:
        cursor.execute("ALTER TABLE schedules ADD COLUMN room TEXT")
    except sqlite3.OperationalError:
        # Coluna já existe
        pass

    # Tabela de Presença (Assinatura de aula)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_id INTEGER,
        student_id INTEGER,
        date TEXT NOT NULL,
        status TEXT NOT NULL, -- 'presente' ou 'ausente'
        FOREIGN KEY (schedule_id) REFERENCES schedules (id),
        FOREIGN KEY (student_id) REFERENCES people (id)
    )
    ''')

    # Tabela Financeira
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS finance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL, -- 'receita' ou 'despesa'
        date TEXT NOT NULL,
        status TEXT NOT NULL -- 'pago' ou 'pendente'
    )
    ''')

    # Inserir dados de exemplo se a tabela people estiver vazia
    cursor.execute("SELECT COUNT(*) FROM people")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO people (name, type) VALUES (?, ?)", ('Professor Mozart', 'teacher'))
        cursor.execute("INSERT INTO people (name, type) VALUES (?, ?)", ('Professor Beethoven', 'teacher'))

        days = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
        today_idx = datetime.now().weekday()
        today_str = days[today_idx]

        cursor.execute("INSERT INTO schedules (teacher_id, day_of_week, start_time, end_time, course_name) VALUES (?, ?, ?, ?, ?)",
                       (1, today_str, '08:00', '10:00', 'Piano Clássico'))
        cursor.execute("INSERT INTO schedules (teacher_id, day_of_week, start_time, end_time, course_name) VALUES (?, ?, ?, ?, ?)",
                       (1, today_str, '14:00', '16:00', 'Teoria Musical'))
        cursor.execute("INSERT INTO schedules (teacher_id, day_of_week, start_time, end_time, course_name) VALUES (?, ?, ?, ?, ?)",
                       (2, today_str, '09:00', '11:00', 'Violino'))
        cursor.execute("INSERT INTO schedules (teacher_id, day_of_week, start_time, end_time, course_name) VALUES (?, ?, ?, ?, ?)",
                       (2, today_str, '13:00', '15:00', 'Composição'))

    db.commit()
    db.close()
