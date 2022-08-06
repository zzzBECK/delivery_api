from email.policy import default
from enum import unique
from operator import methodcaller
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
# from datetime import datetime
# import enum
# from sqlalchemy import Enum

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

# class Status(enum.Enum):
#     received = "RECEIVED"
#     confirmed = "CONFIRMED"
#     dispatched = "DISPATCHED"
#     delivered = "DELIVERED"
#     canceled = "CANCELED"

# class MyDateTime(db.TypeDecorator):
#     impl = db.DateTime
    
#     def process_bind_param(self, value, dialect):
#         if type(value) is str:
#             return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
#         return value

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), unique=True)
    produto = db.Column(db.String(100))
    valor = db.Column(db.Integer)
    entregue = db.Column(db.Boolean)
    estado = db.Column(db.String(15))
    timestamp = db.Column(db.String(100))

    def __init__(self, cliente, produto, valor, entregue, estado, timestamp):
        self.cliente = cliente
        self.produto = produto
        self.valor = valor
        self.entregue = entregue
        self.estado = estado
        self.timestamp = timestamp

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'cliente', 'produto', 'valor', 'entregue', 'estado', 'timestamp')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@app.route('/order', methods=['POST'])
def add_order():
    cliente = request.json['cliente']
    produto = request.json['produto']
    valor = request.json['valor']
    entregue = request.json['entregue']
    estado = request.json['estado']
    timestamp = request.json['timestamp']

    new_order = Order(cliente, produto, valor , entregue, estado, timestamp)

    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)

#mostra todos os pedidos cadastrados
@app.route('/order', methods=['GET'])
def get_orders():
    all_orders = Order.query.all()
    result = orders_schema.dump(all_orders)

    return jsonify(result)

#mostra apenas um pedido específico cadastrado pela id
@app.route('/order/<id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)

    return order_schema.jsonify(order)

#atualiza dados do pedido
@app.route('/order/<id>', methods=['PUT'])
def uptade_order(id):
    order = Order.query.get(id)

    cliente = request.json['cliente']
    produto = request.json['produto']
    valor = request.json['valor']
    entregue = request.json['entregue']
    estado = request.json['estado']
    timestamp = request.json['timestamp']

    order.cliente = cliente
    order.produto = produto
    order.valor = valor
    order.entregue = entregue
    order.estado = estado
    order.timestamp = timestamp

    db.session.commit()

    return order_schema.jsonify(order)


#deleta um pedido
@app.route('/order/<id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    
    return order_schema.jsonify(order)



if __name__ == '__main__':
    app.run(debug=True)