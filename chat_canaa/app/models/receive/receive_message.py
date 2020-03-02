import sys
from app.broker.broker_rabbitmq import BrokerRabbitMq
from app.database.mongo_db import ConnectionDataBase
from app.models.send.send_message import SendRabbitMQ
import os

_MESSAGE_PERSISTENCE = 2
_MESSAGE_SENDING_CODE = 1
_BROKER_INSTANCE = BrokerRabbitMq()

_INSTANCE_DATABASE = ConnectionDataBase()


class ReceiveRabbitMQ:
    def __init__(self, queue, routing_key: str = None):
        self.instance_connection = _BROKER_INSTANCE.connecting_to_the_broker()
        self.calling_the_chanel = _BROKER_INSTANCE.channel(self.instance_connection)
        self.queue = queue
        self.message_sender_or_receiver_flag = 'receiver'

    def callback(self, body, ch=None, method=None, properties=None):
        message_copy = body
        _INSTANCE_DATABASE.get_all_message_logs(self.queue, self.message_sender_or_receiver_flag)

        _INSTANCE_DATABASE.include_message_in_json(message_copy, self.queue, self.message_sender_or_receiver_flag)

    def receiving_queue_information(self):
        _BROKER_INSTANCE.connecting_to_the_broker()
        self.calling_the_chanel.basic_qos(prefetch_count=_MESSAGE_SENDING_CODE)
        self.calling_the_chanel.basic_consume(queue=self.queue, auto_ack=True,
                                              on_message_callback=self.callback)

        self.calling_the_chanel.start_consuming()
