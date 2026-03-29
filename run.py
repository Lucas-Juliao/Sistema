from app import create_app

app = create_app()

if __name__ == "__main__":
    print(">>> Iniciando Safira MusiCloud (Versão Simplificada)...")
    app.run(debug=True)
