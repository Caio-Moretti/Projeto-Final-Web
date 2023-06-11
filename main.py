from flask import Flask, render_template, redirect, request, session
from flask_pymongo import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = 60  # duração da sessão de login

CONNECTION_STRING = 'mongodb atlas connection string'  # string do mongodb atlas com seu login
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('usuarios_db')  # database = usuarios_db
usuarios_collection = db.usuarios  # collection = usuarios


# depois de conectar corretamente ao banco de dados do mongodb atlas, o Flask toma conta do backend do site:
@app.route('/')
def home():
    return render_template('landing_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = usuarios_collection.find_one({'email': email, 'senha': senha})
        if usuario:
            session.permanent = True
            session['user_id'] = str(usuario['_id'])
            return redirect('/admin')

        return redirect('/login')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = {'nome': nome, 'email': email, 'senha': senha}

        usuarios_collection.insert_one(usuario)

        return redirect('/register')
    else:
        return render_template('register.html')


@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect('/login')

    usuarios = usuarios_collection.find()

    return render_template('admin.html', usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)
