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
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    result = []
    for contact in contacts:
        contact_data = {
            'id': contact.id,
            'nome': contact.nome,
            'endereco': contact.endereco,
            'email': contact.email,
            'telefone': contact.telefone,
            'linkedin': contact.linkedin
        }
        result.append(contact_data)
    return jsonify(result)

# Rota para adicionar um novo contato
@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    nome = data['nome']
    endereco = data['endereco']
    email = data['email']
    telefone = data['telefone']
    linkedin = data['linkedin']
    contact = Contact(nome, endereco, email, telefone, linkedin)
    db.session.add(contact)
    db.session.commit()
    return jsonify({'message': 'Contato adicionado com sucesso!'})

# Rota para obter os detalhes de um contato específico
@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)
    if contact:
        contact_data = {
            'id': contact.id,
            'nome': contact.nome,
            'endereco': contact.endereco,
            'email': contact.email,
            'telefone': contact.telefone,
            'linkedin': contact.linkedin
        }
        return jsonify(contact_data)
    else:
        return jsonify({'message': 'Contato não encontrado'}), 404

# Rota para atualizar os detalhes de um contato
@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get(id)
    if contact:
        data = request.get_json()
        contact.nome = data['nome']
        contact.endereco = data['endereco']
        contact.email = data['email']
        contact.telefone = data['telefone']
        contact.linkedin = data['linkedin']
        db.session.commit()
        return jsonify({'message': 'Contato atualizado com sucesso!'})
    else:
        return jsonify({'message': 'Contato não encontrado'}), 404

# Rota para excluir um contato
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contato excluído com sucesso!'})
    else:
        return jsonify({'message': 'Contato não encontrado'}), 404

#Inicialização da API
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
