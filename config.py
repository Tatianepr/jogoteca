import os
# variáveis universais em maiúsculas

# é necessário configurar o secret_key para criptografar a senha no cookie
SECRET_KEY= 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'tati1234',
        servidor = 'localhost',
        database = 'jogoteca'
    )
# o "os" importa uma classe que permite selecinar o caminho absoluto onde esse arquivo está criado
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
