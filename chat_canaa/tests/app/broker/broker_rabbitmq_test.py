import unittest
from app.broker.broker_rabbitmq import BrokerRabbitMq
import pika
import unittest
from unittest.mock import patch, Mock, MagicMock
import pytest
import builtins


class TestBrokerRabbitMq(unittest.TestCase):
    def setUp(self) -> None:
        self.connection_instance = BrokerRabbitMq()
        self.channel_instance = self.connection_instance.channel(Mock())

    def test_queue_declare(self):
        queue_name = 'test'
        exchange_name = 'name_exchange'
        channel = Mock()
        channel.queue_declare.return_value = ''
        return_method = self.connection_instance.queue_declare(queue_name, exchange_name)
        #self.assertEqual(return_method,channel.queue_declare)
        self.assertIsNotNone(return_method)

    def test_exchange_declare(self):
        defined_type_of_exchange = 'topic'
        exchange_name = 'name_exchange'
        channel = Mock()
        channel.exchange_declare.return_value = ''
        return_method = self.connection_instance.exchange_declare_(exchange_name,defined_type_of_exchange)
        #self.assertEqual(return_method, channel.exchange_declare)
        self.assertIsNotNone(return_method)

    def test_declare_queue_bind(self):
        queue_declaration = Mock()
        exchange_name = Mock()
        channel = Mock()
        channel.queue_bind.return_value = Mock()
        return_method = self.connection_instance.declare_queue_bind(exchange_name, queue_declaration)
        # self.assertEqual(return_method, channel.queue_bind)
        self.assertIsNotNone(return_method)
