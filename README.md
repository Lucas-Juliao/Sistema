# Safira Music Cloud

Sistema de gestão para escolas de música.

## Como configurar e rodar o projeto

1. **Instalar dependências:**
   Certifique-se de ter o Python instalado. No terminal, na raiz do projeto, execute:
   ```bash
   pip install -r requirements.txt
   ```

2. **Inicializar o Banco de Dados:**
   Execute os seguintes comandos para criar as tabelas:
   ```bash
   set FLASK_APP=run.py
   flask db init
   flask db migrate -m "Primeira migracao"
   flask db upgrade
   ```

3. **Criar usuário Administrador:**
   Para criar o usuário `adm` com senha `adm`, execute:
   ```bash
   python create_admin.py
   ```

4. **Rodar o sistema:**
   **IMPORTANTE:** Sempre rode o sistema através do arquivo `run.py`. Não execute arquivos dentro da pasta `app/` diretamente.
   ```bash
   python run.py
   ```

O sistema estará disponível em `http://127.0.0.1:5000/`.
O acesso principal após o login é pela rota `/menu`.
