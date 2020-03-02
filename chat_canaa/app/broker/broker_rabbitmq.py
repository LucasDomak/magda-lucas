import os

import pika

_HOST = os.getenv('_HOST', '104.41.37.14')
_PORT = '5672'
_VIRTUAL_HOST = 'padawan'
_USERNAME = 'padawan'
_PASSWORD = 'padawan2020'
_QUEUE_SHOULD_BE_DURABLE = True
_MESSAGE_PERSISTENCE = 2


class BrokerRabbitMq:
    def __init__(self):
        self.credentials = ''
        self.connection = self.connecting_to_the_broker()
        self.calling_channel = ''

    def channel(self, connected_session: str):
        self.calling_channel = connected_session.channel()
        return self.calling_channel

    def connecting_to_the_broker(self):

        self.credentials = pika.PlainCredentials(
            username=_USERNAME,
            password=_PASSWORD)

        establishing_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=_HOST,
                port=_PORT,
                virtual_host=_VIRTUAL_HOST,
                credentials=self.credentials)
        )
        return establishing_connection

    def queue_declare(self, queue_name, exchange_name):
        queue_declaration = self.calling_channel.queue_declare(queue=queue_name,
                                                               durable=_QUEUE_SHOULD_BE_DURABLE
                                                               )
        self.declare_queue_bind(queue_declaration, exchange_name)
        return queue_declaration

    def exchange_declare_(self, exchange_name: str, defined_type_of_exchange):
        return self.calling_channel.exchange_declare(exchange=exchange_name,
                                                     exchange_type=defined_type_of_exchange
                                                     )

    def declare_queue_bind(self, queue_declaration, exchange_name):
        return self.calling_channel.queue_bind(exchange=exchange_name,
                                               queue=queue_declaration.method.queue
                                               )
