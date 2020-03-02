import unittest
from unittest.mock import Mock, patch
import datetime
from app.models.send.send_message import SendRabbitMQ
import builtins


class TestSendRabbitMQ(unittest.TestCase):

    def test_generated_object_is_an_instance_of_the_class(self):
        object_send = SendRabbitMQ(Mock(), Mock())
        self.assertIsInstance(object_send, SendRabbitMQ)

    @patch('os.system')
    def test_checking_if_the_method_of_cleaning_the_console_is_being_called(self, os_mock):
        SendRabbitMQ.clean_terminal()
        os_mock.assert_called()

    @patch('builtins.print')
    @patch('app.broker.broker_rabbitmq.BrokerRabbitMq.queue_declare')
    @patch('app.broker.broker_rabbitmq.BrokerRabbitMq.exchange_declare_')
    @patch('app.broker.broker_rabbitmq.BrokerRabbitMq.connecting_to_the_broker')
    def test_start_sending_message(self, brocker, exchange_declare_, queue_declare,print_mock):
        brocker.return_value = Mock()
        exchange_declare_.return_value = Mock()
        queue_declare.return_value = Mock()
        body = 'sending message'
        queue_name = 'test'
        exchange_name = 'exchange test'
        defined_type_of_exchange = 'topic'
        channel = Mock()
        channel.basic_publish.return_value = Mock()
        SendRabbitMQ(body, queue_name).start_sending_message(body, exchange_name, queue_name, defined_type_of_exchange)
        brocker.assert_called()
        exchange_declare_.assert_called()
        queue_declare.assert_called()
        print_mock.assert_called_with(" [x]Sending 'sending message'")
