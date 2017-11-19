from flask import send_file

from src.models.produto import Produto
from src.common.database import Database

from io import BytesIO
import bson.binary
from io import StringIO
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = '123456'

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/catalogo')
def abre_catalogo():
    post_data = Database.find(collection='produtos3', query={})
    posts = [post for post in post_data]
    return render_template('home_produtos.html', posts=posts)

@app.route('/registro')
def registra_produto():
    return render_template('insere_produto.html')

@app.route('/auth/produto', methods=['POST'])
def register_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    email = request.form['email']
    telefone = request.form['telefone']
    cep = request.form['cep']
    imagem = request.files['imagem']
    content = StringIO(imagem.read())
    content = bson.binary.Binary(content.getvalue())
    Produto2 = Produto(nome, descricao, email, telefone, cep, content, _id=None)
    Produto2.save_to_mongo()
    return render_template("produto_cadastrado.html", produto=nome)

@app.route('/logo.png')
def serve_file():
    post_data = Database.find(collection='produtos3', query={})
    for rec in post_data:
        return send_file(BytesIO(rec['imagem']),attachment_filename='logo.png',mimetype='image/png')

@app.route('/produto/<key>')
def produto(key):
    product = Database.find_one(collection='produtos3', query={"_id":key})
    return render_template("produto.html", product=product)

@app.route('/imagem/<key>')
def imagem(key):
    product = Database.find_one(collection='produtos3', query={"_id":key})
    return send_file(BytesIO(product['imagem']), attachment_filename='logo.png', mimetype='image/png')

@app.before_first_request
def initialize_database():
    Database.initialize()

if __name__ == '__main__':
    app.debug = True
    app.run(port=4995, debug=True)
