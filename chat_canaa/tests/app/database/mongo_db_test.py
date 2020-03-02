import mongomock
import unittest
from unittest.mock import Mock, patch, MagicMock, call
from app.database.mongo_db import ConnectionDataBase
import datetime
import pymongo
import builtins


class TestCrudDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = ConnectionDataBase()

    @patch.object(datetime, 'datetime')
    def test_include_message_in_json_method_and_insert_message_to_database(self, datetime_mock):
        connection_mock = ConnectionDataBase()
        datetime_mock.strftime("%d %B, %Y").return_value = '19 february,2020'
        datetime_mock.strftime("%H:%M:%S").return_value = '19:25:15'
        destination_name = 'queue_lucas'
        message_sender_or_receiver_flag = 'sender'
        body = 'test message'
        connection_mock.collection = Mock()
        connection_mock.collection.find.return_value = ''
        connection_mock.collection.insert_one.return_value = ''
        json = {'destination': 'queue_lucas',
                'active': True,
                'body': 'test message',
                'send_date': '19:25:15',
                'sending_time': '19 february,2020',
                'message_identifier': 1,
                'message_sender_or_receiver': 'sender'}

        return_include = connection_mock.include_message_in_json(body, destination_name,
                                                                 message_sender_or_receiver_flag)
        return_insert = connection_mock.insert_message_to_database(json)
        connection_mock.collection.find.assert_called_once()
        connection_mock.collection.insert_one.assert_called_with(json)
        self.assertIsNone(return_include)
        self.assertIsNone(return_insert)

    @patch('builtins.print')
    def test_get_message_by_destination_method(self, print_mock):
        json = [{'destination': 'queue_lucas',
                 'active': True,
                 'body': 'test message',
                 'send_date': '19:25:15',
                 'sending_time': '19 february,2020',
                 'message_identifier': 1,
                 'message_sender_or_receiver': 'sender'}]

        destination_name = 'queue_lucas'
        connection_mock = ConnectionDataBase()
        connection_mock.collection = Mock()
        connection_mock.collection.find.return_value = json
        return_message = connection_mock.get_message_by_destination(destination_name)
        self.assertIsNone(return_message)
        print_mock.assert_called()
        connection_mock.collection.find.assert_called_once_with(
            {'destination': 'queue_lucas', 'active': True})

    @patch.object(builtins, 'print')
    def test_disable_message_history(self, print_mock):
        message_identifier = 1
        print_mock.side_effect = ['ok', 'ok', 'ok']
        connection_mock = ConnectionDataBase()
        connection_mock.collection = Mock()
        connection_mock.collection.find_one_and_update.return_value = ''

        return_message = connection_mock.disable_message_history(message_identifier)

        self.assertIsNone(return_message)
        print_mock.assert_called_once()
        connection_mock.collection.find_one_and_update.assert_called_once_with({'message_identifier': 1},
                                                                               {'$set': {'active': False}})

    @patch.object(builtins, 'print')
    def test_get_all_message_logs(self, print_mock):
        json = [{'destination': 'queue_lucas',
                 'active': True,
                 'body': 'test message',
                 'send_date': '19:25:15',
                 'sending_time': '19 february,2020',
                 'message_identifier': 1,
                 'message_sender_or_receiver': 'sender'}]
        destination_name = 'lucas_canaa'
        message_sender_or_receiver = 'sender'
        print_mock.side_effect = ['ok', 'ok', 'ok', 'ok']
        connection_mock = ConnectionDataBase()
        connection_mock.collection = Mock()
        connection_mock.collection.find.return_value = json
        return_message = connection_mock.get_all_message_logs(destination_name, message_sender_or_receiver)

        print_mock.assert_called_with('--------Message history-----------------')

        self.assertIsNone(return_message)
