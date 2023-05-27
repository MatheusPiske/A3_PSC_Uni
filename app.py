#pip install flask
#pip install flask_sqlalchemy

#Importação das bibliotecas utilizadas na aplicação
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Início da aplicação e definição do banco de dados em nuvem
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

# Dados para a agenda de contatos
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    linkedin = db.Column(db.String(100))

    def __init__(self, nome, endereco, email, telefone, linkedin):
        self.nome = nome
        self.endereco = endereco
        self.email = email
        self.telefone = telefone
        self.linkedin = linkedin

#---------------------------------------------------------------------
#-------------------------- (ROTAS DA API) ---------------------------
#---------------------------------------------------------------------

# Rota para listar todos os contatos

# Rota para adicionar um novo contato

# Rota para obter os detalhes de um contato específico (de acordo com o ID)

# Rota para atualizar os detalhes de um contato

# Rota para excluir um contato

#Inicialização da API
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
