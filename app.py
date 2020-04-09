from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db
from myqueue import Queue


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)
Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

cola = Queue()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/new', methods=['POST'])
def new_element():
    nombre = request.json.get("nombre", None)
    apellido = request.json.get("apellido", None)
    telefono =  request.json.get("telefono", None)
    if cola.enqueue({"nombre": nombre, "apellido": apellido, "telefono": telefono}):
        return {"nombre": nombre, "apellido": apellido},200
    else:
        return {"msj":"unexpected error"}, 422


@app.route('/next')
def next_element():
    if cola.dequeue():
        return {"msj":"message sent succesfully"}, 200
    else:
        return {"msj":"unexpected error"}, 422

@app.route('/all')
def all_element():
    return jsonify(cola.get_queue()),200


if __name__ == '__main__':
    manager.run()
