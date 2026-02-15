from app import create_app, db
from app.models import User

app = create_app()

def setup_app():
    with app.app_context():
        # Cria as tabelas se não existirem
        db.create_all()
        # Garante que o usuário adm existe
        if not User.query.filter_by(username='adm').first():
            user = User(username='adm')
            user.set_password('adm')
            db.session.add(user)
            db.session.commit()
            print(">>> Usuário administrador 'adm' (senha 'adm') configurado.")

if __name__ == "__main__":
    setup_app()
    print(">>> Iniciando Safira Music Cloud...")
    app.run(debug=True)
