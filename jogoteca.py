from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# carrega as variáveis universais do arquivo config.py
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

# importa tudo de views_game.py
from views_game import *
from views_user import *

# garante que toda vez que colocar para rodar que faça as multiplas importações dos outros arquivoss
if __name__ == '__main__':
    app.run(debug=True)