import mongomock
import unittest
from unittest.mock import Mock, patch, MagicMock
import datetime
from app.models.receive.receive_message import ReceiveRabbitMQ
import builtins

mock_collection = mongomock.MongoClient().db.collection
from app.database.mongo_db import ConnectionDataBase


class TestReceiveRabbitMQ(unittest.TestCase):

    def test_generated_object_is_an_instance_of_the_class(self):
        object_receive = ReceiveRabbitMQ(Mock())
        self.assertIsInstance(object_receive, ReceiveRabbitMQ)

    @patch('os.system')
    def test_checking_if_the_method_of_cleaning_the_console_is_being_called(self, os_mock):
        ReceiveRabbitMQ.clean_terminal()
        os_mock.assert_called()

    @patch('builtins.print', Mock())
    @patch('app.models.receive.receive_message.ReceiveRabbitMQ.callback')
    @patch('app.broker.broker_rabbitmq.BrokerRabbitMq.connecting_to_the_broker')
    def test_checks_if_the_methods_for_consuming_messages_are_being_called(self, callback_mock, broker_mock):
        callback_mock.return_value = Mock()
        broker_mock.return_value = Mock()
        ReceiveRabbitMQ.receiving_queue_information(Mock())
        builtins.print.assert_called_once()
        callback_mock.assert_called()

    @patch('builtins.print')
    @patch.object(ConnectionDataBase, 'include_message_in_json')
    @patch.object(ConnectionDataBase, 'get_all_message_logs')
    def test_callback(self, get_all_mock, json_mock, print_mock):
        body = Mock()
        ch = Mock()
        method = Mock()
        properties = Mock()
        body.decode()
        get_all_mock.return_value = Mock()
        json_mock.return_value = Mock()
        print_mock.side_effect = [f"Received : {body}"]
        receive = ReceiveRabbitMQ(Mock(), Mock())
        receive.callback(ch, method, properties, body)
        get_all_mock.assert_called()
        print_mock.assert_called()
