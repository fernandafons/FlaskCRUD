from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import Pessoa as formPessoa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # caminho até o bd

db = SQLAlchemy(app) # instancia da classe importada. db é default

class Pessoa(db.Model): # definindo modelo de classe. classe mae entre ()

    __tablename__= 'clientes'   # nome da tabela do bd. comum estar no plural

# criando colunas da tabela
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    dropdown = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, nome, telefone, dropdown, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.dropdown = dropdown
        self.email = email
        self.cpf = cpf


db.create_all() # cria a tabela


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        dropdown = request.form.get("dropdown")
        cpf = request.form.get("cpf")
        email = request.form.get("email")

        if nome and telefone and dropdown and cpf and email:
            p = Pessoa(nome, telefone, dropdown, cpf, email) #objeto p recebe novo obj da classe
            db.session.add(p)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)


@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)


@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    form = formPessoa()
    if request.method == "GET":
        form.nome.data = pessoa.nome
        form.telefone.data = pessoa.telefone
        form.dropdown.data = pessoa.dropdown
        form.cpf.data = pessoa.cpf
        form.email.data = pessoa.email

    elif request.method == "POST":
        pessoa.nome = request.form['nome']
        pessoa.telefone = request.form['telefone']
        pessoa.dropdown = request.form['dropdown']
        pessoa.cpf = request.form['cpf']
        pessoa.email = request.form['email']

        db.session.commit()

        return redirect(url_for("lista"))

    return render_template("atualizar.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
