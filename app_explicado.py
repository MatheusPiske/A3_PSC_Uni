from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

# Definição do modelo de dados para o contato
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

# Rota para listar todos os contatos
@app.route('/contacts', methods=['GET'])
def get_contacts():
    # Consulta todos os contatos no banco de dados
    contacts = Contact.query.all()

    result = []
    for contact in contacts:
        # Cria um dicionário com os dados do contato
        contact_data = {
            'id': contact.id,
            'nome': contact.nome,
            'endereco': contact.endereco,
            'email': contact.email,
            'telefone': contact.telefone,
            'linkedin': contact.linkedin
        }
        result.append(contact_data)

    # Retorna a lista de contatos como resposta no formato JSON
    return jsonify(result)

# Rota para adicionar um novo contato
@app.route('/contacts', methods=['POST'])
def add_contact():
    # Obtém os dados do contato enviados no corpo da requisição
    data = request.get_json()
    nome = data['nome']
    endereco = data['endereco']
    email = data['email']
    telefone = data['telefone']
    linkedin = data['linkedin']

    # Cria um novo objeto Contact com os dados recebidos
    contact = Contact(nome, endereco, email, telefone, linkedin)

    # Adiciona o contato ao banco de dados
    db.session.add(contact)
    db.session.commit()

    # Retorna uma mensagem de sucesso como resposta
    return jsonify({'message': 'Contato adicionado com sucesso!'})

# Rota para obter os detalhes de um contato específico
@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    # Consulta o contato no banco de dados pelo ID
    contact = Contact.query.get(id)

    # Se o contato informado existir
    if contact:
        # Cria um dicionário com os dados do contato
        contact_data = {
            'id': contact.id,
            'nome': contact.nome,
            'endereco': contact.endereco,
            'email': contact.email,
            'telefone': contact.telefone,
            'linkedin': contact.linkedin
        }

        # Retorna os detalhes do contato como resposta no formato JSON
        return jsonify(contact_data)
    else:
        # Retorna uma mensagem de erro se o contato não for encontrado
        return jsonify({'message': 'Contato não encontrado'}), 404

# Rota para atualizar os detalhes de um contato
@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    # Consulta o contato no banco de dados pelo ID
    contact = Contact.query.get(id)

    # Se o contato informado existir
    if contact:
        # Obtém os dados atualizados do contato enviados no corpo da requisição
        data = request.get_json()
        contact.nome = data['nome']
        contact.endereco = data['endereco']
        contact.email = data['email']
        contact.telefone = data['telefone']
        contact.linkedin = data['linkedin']

        # Salva as alterações no banco de dados
        db.session.commit()

        # Retorna uma mensagem de sucesso como resposta
        return jsonify({'message': 'Contato atualizado com sucesso!'})
    else:
        # Retorna uma mensagem de erro se o contato não for encontrado
        return jsonify({'message': 'Contato não encontrado'}), 404

# Rota para excluir um contato
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    # Consulta o contato no banco de dados pelo ID
    contact = Contact.query.get(id)

    # Se o contato informado existir
    if contact:
        # Remove o contato do banco de dados
        db.session.delete(contact)
        db.session.commit()

        # Retorna uma mensagem de sucesso como resposta
        return jsonify({'message': 'Contato excluído com sucesso!'})
    else:
        # Retorna uma mensagem de erro se o contato não for encontrado
        return jsonify({'message': 'Contato não encontrado'}), 404

if __name__ == '__main__':
    # Cria as tabelas do banco de dados se não existirem
    db.create_all()

    # Inicia o servidor Flask em modo de depuração
    app.run(debug=True)
