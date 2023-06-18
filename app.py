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
def getContatos():

  contatos = Contact.query.all()

  resultados = []

  for contact in contatos:
        # Cria um dicionário com os dados do contato
        contact_data = {
            'id': contact.id,
            'nome': contact.nome,
            'endereco': contact.endereco,
            'email': contact.email,
            'telefone': contact.telefone,
            'linkedin': contact.linkedin
        }
        resultados.append(contact_data)

  return jsonify(resultados)

# Rota para adicionar um novo contato
@app.route('/contacts', methods=['POST'])
def add_contact():
    try:
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
    except KeyError as e:
        return jsonify({'error': 'Campo obrigatório ausente: ' + str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Contate a área de desenvolvimento' + str(e)}), 500

# Rota para obter os detalhes de um contato específico (de acordo com o ID)
@app.route('/contacts/<int:usuarioId>', methods=['GET'])
def getContatoUnico(usuarioId):

  contatos = Contact.query.filter_by(id=usuarioId)

  resultado = []

  if contatos is None:
    return print('Não foi possivel achar este usuário')
    
  else:
    for contact in contatos:
      tabelaContato = {
        'id'      : contact.id,
        'nome'    : contact.nome,
        'endereco': contact.endereco,
        'email'   : contact.email,
        'telefone': contact.telefone,
        'linkedin': contact.linkedin
      }
  
    resultado.append(tabelaContato)
    
    return jsonify(resultado)

# Rota para atualizar os detalhes de um contato
@app.route('/contacts/<int:usuarioId>', methods=['PUT'])
def putAlterarContato(usuarioId):

  contato = Contact.query.get(usuarioId)

  if contato:
    inputJson = request.get_json()
    contato.nome = inputJson['nome']
    contato.endereco = inputJson['endereco']
    contato.email = inputJson['email']
    contato.telefone = inputJson['telefone']
    contato.linkedin = inputJson['linkedin']

    db.session.commit()

    return jsonify({'message': 'Contato atualizado com sucesso!'})
  else:
    return jsonify({'message': 'Contato não encontrado'}), 404

# Rota para excluir um contato
@app.route("/contacts/<int:id>", methods=['DELETE'])
def deletar_contato(id):
    contato = Contact.query.get(id)

    if contato: 
        db.session.delete(contato)
        db.session.commit()
        return jsonify({'message' : 'Contato excluido com sucesso.'})
    else:
        return jsonify({'massage' : 'Contato não encontrado.'}), 404
    
    
#Inicialização da API
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
