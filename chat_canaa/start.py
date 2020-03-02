from app.views.settings import DEBUG, HOST, PORT
from flask import Flask, Blueprint, request, jsonify, render_template, redirect
from app.database.mongo_db import ConnectionDataBase
from app.models.send.send_message import SendRabbitMQ
from app.models.receive.receive_message import ReceiveRabbitMQ
from app.broker.broker_rabbitmq import BrokerRabbitMq

lista_de_contatos = ['MAGDA_CANAA', 'GRUPO_CANAA']
lista_exchanges = ['exchange_topic', 'exchange_fanout']
list_routing_key = ['#.MAGDA_CANAA.#', 'GRUPO_CANAA']
list_queues = ['LUCAS_CANAA', 'GRUPO_CANAA']
shipping_routes_according_to_destination = {'LUCAS_CANAA': 'Send/lucas', 'GRUPO_CANAA': 'Send/canaa'}
connection = ConnectionDataBase()
app = Flask(__name__)
login = ''


@app.route('/')
def messages():
    return render_template('contacts.html', lista_de_rotas=list_queues)


@app.route('/destinations', methods=['POST'])
def message_destinations():
    message = request.form['Send']
    destination = request.args['destination']
    return redirect("/" + shipping_routes_according_to_destination[destination] + "?message=" + message)


@app.route('/LUCAS_CANAA')
def LUCAS_CANAA():
    prod = connection.get_all_message_logs(list_queues[0], 'sender')
    x = connection.get_all_message_logs(list_queues[0], 'receiver')

    return render_template('contacts_lucas.html', prod=prod, x=x, queue_destination=list_queues[0])


@app.route('/GRUPO_CANAA')
def GRUPO_CANAA():
    prod = connection.get_all_message_logs(list_queues[1], 'sender')
    x = connection.get_all_message_logs(list_queues[1], 'receiver')

    return render_template('contacts_lucas.html', prod=prod, x=x, queue_destination=list_queues[1])


@app.route('/Send/lucas', methods=['GET'])
def send_lucas():
    route = '/LUCAS_CANAA'
    routing_key = list_routing_key[0]
    queue = list_queues[0]
    message = request.args.get('message')

    SendRabbitMQ(message, lista_exchanges[0], list_queues[0]).start_sending_message(message, lista_exchanges[0],
                                                                                    list_queues[0],
                                                                                    'topic', list_routing_key[0])

    ReceiveRabbitMQ(list_queues[0], list_routing_key[0]).callback(message)
    return redirect("/receive?queue=" + queue + "&routing_key=" + routing_key + "&route=" + route)


@app.route('/Send/canaa', methods=['GET'])
def send_canaa():
    route = '/GRUPO_CANAA'
    routing_key = list_routing_key[1]
    queue = list_queues[1]
    message = request.args.get('message')
    SendRabbitMQ(message, lista_exchanges[1], list_queues[1]).start_sending_message(message, lista_exchanges[1],
                                                                                    list_queues[1],
                                                                                    'fanout', list_routing_key[1])
    ReceiveRabbitMQ(list_queues[1], list_routing_key[1]).callback(message)

    return redirect("/receive?queue=" + queue + "&routing_key=" + routing_key + "&route=" + route)


@app.route('/receive', methods=['GET'])
def receive():
    selected_queue = request.args.get('queue')
    selected_routing_key = request.args.get('routing_key')
    redirect_to_page = request.args.get('route')
    ReceiveRabbitMQ(selected_queue, selected_routing_key).receiving_queue_information()

    return redirect(redirect_to_page)


@app.route('/delete')
def delete_message():
    identifier = request.args['identifier']
    destination = request.args['destination']
    connection.disable_message_history(identifier)
    return redirect("/" + destination)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5005,
        debug=DEBUG

    )
