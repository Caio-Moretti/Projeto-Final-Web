from flask import Flask, render_template, redirect, request, session
from flask_pymongo import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = 60  # session duration time (60s)

CONNECTION_STRING = 'seu link copiado'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('seu database')
usuarios_collection = db.sua-collection


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


@app.route('/edit/<string:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuarios_collection.update_one({'_id': ObjectId(user_id)},
                                       {'$set': {'nome': nome, 'email': email, 'senha': senha}})

        return redirect('/admin')

    usuario = usuarios_collection.find_one({'_id': ObjectId(user_id)})
    return render_template('edit_user.html', usuario=usuario)


@app.route('/delete/<string:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session:
        return redirect('/login')

    usuarios_collection.delete_one({'_id': ObjectId(user_id)})
    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True)
