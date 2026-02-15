import sqlite3
import os
from werkzeug.security import generate_password_hash

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

    # Outras tabelas do escopo
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL, -- 'student' ou 'teacher'
        email TEXT,
        phone TEXT
    )
    ''')

    db.commit()
    db.close()
