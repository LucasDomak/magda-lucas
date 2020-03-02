import pika
import time
from app.broker.broker_rabbitmq import BrokerRabbitMq
from app.database.mongo_db import ConnectionDataBase
import os


_INSTANCE_DATABASE = ConnectionDataBase()
_MESSAGE_PERSISTENCE = 2
_BROKER_INSTANCE = BrokerRabbitMq()


class SendRabbitMQ:
    def __init__(self, boby, exchange_name, routing_key: str = None):
        self.instance_connection = _BROKER_INSTANCE.connecting_to_the_broker()
        self.calling_the_chanel = _BROKER_INSTANCE.channel(self.instance_connection)
        self._MENU_CONTROL_FLAG = True
        self.message_sender_or_receiver_flag = 'sender'

    def start_sending_message(self, body, exchange_name: str, queue_name: str, defined_type_of_exchange: str,
                              routing_key: str = None) -> None:
        _BROKER_INSTANCE.connecting_to_the_broker()
        _BROKER_INSTANCE.exchange_declare_(exchange_name, defined_type_of_exchange)
        _BROKER_INSTANCE.queue_declare(queue_name, exchange_name)
        self.calling_the_chanel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=body,

            properties=pika.BasicProperties(
                delivery_mode=_MESSAGE_PERSISTENCE
            ))
        _INSTANCE_DATABASE.include_message_in_json(body, queue_name, self.message_sender_or_receiver_flag)

