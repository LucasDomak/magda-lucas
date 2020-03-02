import mongomock
import unittest
from unittest.mock import Mock, patch, call
import datetime
from app.models.session.begin_session import Session
from app.models.receive.receive_message import ReceiveRabbitMQ
import sys
import builtins

mock_collection = mongomock.MongoClient().db.collection


class TestSession(unittest.TestCase):
    def setUp(self) -> None:
        self.object_session = Session()

    def test_generated_object_is_an_instance_of_the_class(self):
        self.assertIsInstance(self.object_session, Session)

    @patch('app.models.session.begin_session.Session.define_exchange_to_be_used')
    @patch('app.models.session.begin_session.input')
    def test_checks_if_the_user_who_continues_to_send_a_message_option_1(self, input, define_exchange_to_be_used):
        input.return_value = '1'
        define_exchange_to_be_used.return_value = Mock()
        self.object_session.checks_if_the_user_who_continues_to_send_a_message()
        input.assert_called()
        define_exchange_to_be_used.assert_called()

    @patch('builtins.print')
    @patch('builtins.input')
    def test_checks_if_the_user_who_continues_to_send_a_message_option_2(self, input_mock, print_mock):
        sys = Mock()
        sys.exit.return_value = Mock()
        input_mock.return_value = '2'
        with self.assertRaises(SystemExit):
            self.object_session.checks_if_the_user_who_continues_to_send_a_message()
        print_mock.assert_called_with('Conversation ended......')

    @patch('builtins.print', Mock())
    @patch('builtins.input', Mock())
    def test_check_if_the_checks_if_the_user_who_continues_to_send_a_message_method_returns_a_print_when_the_chosen_option_is_3(
            self):
        sys = Mock()
        sys.exit.return_value = Mock()

        def print_foo(text):
            nonlocal test_case
            test_case = text

        builtins.input.return_value = '3'
        builtins.print = print_foo
        test_case = ""
        with self.assertRaises(SystemExit):
            self.object_session.checks_if_the_user_who_continues_to_send_a_message()
        self.assertEqual(test_case, "leaving the chat.......")

    @patch('builtins.print', Mock())
    @patch('builtins.input', Mock())
    def test_check_if_the_checks_if_the_user_who_continues_to_send_a_message_method_returns_a_print_when_the_chosen_option_is_5(
            self):
        def print_foo(text):
            nonlocal test_case
            test_case = text
            exit()

        builtins.input.return_value = '5'
        builtins.print = print_foo
        test_case = ""
        with self.assertRaises(SystemExit):
            self.object_session.checks_if_the_user_who_continues_to_send_a_message()
        self.assertEqual(test_case, "Option not found")

    @patch('app.models.session.begin_session.Session.checks_if_the_user_who_continues_to_send_a_message')
    def test_open_session_send(self, send_mock):
        send_mock.return_value = 'test_queue'
        self.object_session.open_session_send()
        send_mock.assert_called()

    @patch('app.models.receive.receive_message.ReceiveRabbitMQ.receiving_queue_information')
    @patch('app.models.session.begin_session.Session.define_message_you_want_to_consume')
    def test_open_session_receive(self, consume_mock, receive_mock):
        queue = 'test_queue'
        consume_mock.return_value = 'test_queue'
        receive_mock.return_value = ''
        self.object_session.open_session_receive()
        receive = ReceiveRabbitMQ(queue)
        self.assertIsNotNone(receive)
        consume_mock.assert_called()
        receive_mock.assert_called()

    @patch('builtins.print')
    @patch('app.models.session.begin_session.Session.access_to_the_message_log')
    def test_define_queue_for_message_addressing(self, log_mock, print_mock):
        database = [{
            'destination': 'queue_lucas',
            'active': True,
            'body': 'test message',
            'send_date': 13,
            'sending_time': '20:44',
            'message_identifier': 1,
            'message_sender_or_receiver': 'sender'},
            {
                'destination': 'queue_lucas',
                'active': True,
                'body': 'test message',
                'send_date': 13,
                'sending_time': '20:44',
                'message_identifier': 1,
                'message_sender_or_receiver': 'receiver'}
        ]
        log_mock.return_value = database
        data = self.object_session.define_queue_for_message_addressing('queue_lucas')
        log_mock.assert_called()
        print_mock.assert_called_with('Starting conversation with', 'queue_lucas')
        self.assertIsNotNone(data)
        self.assertEqual(data, 'queue_lucas')

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('app.models.session.begin_session.Session.collects_the_message_typed_by_the_user')
    def test_verifies_which_type_of_exchange_to_use_according_to_menu_option_1(self,
                                                                               collects_mock, print_mock, input_mock):
        input_mock.return_value = '1'

        collects_mock.return_value = Mock()
        self.object_session.define_exchange_to_be_used()
        print_mock.assert_called_with('Choose destination')

    @patch('builtins.print')
    @patch('builtins.input')
    @patch('app.models.session.begin_session.Session.collects_the_message_typed_by_the_user')
    def test_verifies_which_type_of_exchange_to_use_according_to_menu_option_2(self,
                                                                               collects_mock, input_mock, print_mock):
        exchange = 'GRUPO_CANAA'
        input_mock.return_value = '2'

        collects_mock.return_value = Mock()
        return_queue = self.object_session.define_exchange_to_be_used()
        self.assertEqual(return_queue, exchange)
        print_mock.assert_called_with('Choose destination')

    @patch('builtins.print', Mock())
    @patch('builtins.input', Mock())
    def test_if_option_3_is_chosen_return_the_print_ending_the_chat(self):
        sys = Mock()
        sys.exit.return_value = Mock()

        def print_foo(text):
            nonlocal test_case
            test_case = text

        builtins.input.return_value = '3'
        test_case = ""
        builtins.print = print_foo

        with self.assertRaises(SystemExit):
            return_method = self.object_session.define_exchange_to_be_used()
            self.assertEqual(return_method, True)
        self.assertEqual(test_case, 'Leaving the chat.....')

    @patch('builtins.input', Mock())
    @patch('builtins.print', Mock())
    def test_checks_behavior_of_the_define_exchange_to_be_used_method_when_an_invalid_value_is_entered(self):
        builtins.input.return_value = '5'
        sys = Mock()
        sys.exit.return_value = Mock()

        def print_foo(text):
            nonlocal test_case
            test_case = text

        builtins.print.side_effect = print_foo
        test_case = ""
        with self.assertRaises(SystemExit):
            self.object_session.define_exchange_to_be_used()
        self.assertEqual(test_case, "Invalid option")

    @patch('app.models.send.send_message.SendRabbitMQ.clean_terminal')
    @patch('app.database.mongo_db.ConnectionDataBase.disable_message_history')
    @patch('builtins.input', Mock())
    def test_if_option_1_is_chosen_the_clean_terminal_and_disable_message_history_methods_must_be_called(self,
                                                                                                         test_mock,
                                                                                                         clean_terminal_mock):
        builtins.input.return_value = '1'
        test_mock.return_value = Mock()
        clean_terminal_mock.return_value = Mock()
        self.object_session.access_to_the_message_log('destination')

    @patch('app.models.send.send_message.SendRabbitMQ.clean_terminal')
    @patch('app.database.mongo_db.ConnectionDataBase.get_message_by_destination')
    @patch('builtins.input', Mock())
    def test_if_option_2_is_chosen_the_clean_terminal_and_get_message_by_destination_methods_must_be_called(self,
                                                                                                            test_mock,
                                                                                                            clean_terminal_mock):
        builtins.input.return_value = '2'
        test_mock.return_value = Mock()
        clean_terminal_mock.return_value = Mock()
        self.object_session.access_to_the_message_log('destination')

    @patch('builtins.input', Mock())
    def test_if_option_3_is_chosen_return_true(self):
        builtins.input.return_value = '3'
        return_method = self.object_session.access_to_the_message_log('destination')
        self.assertEqual(return_method, True)

    @patch('builtins.print', Mock())
    @patch('builtins.input', Mock())
    def test_if_option_4_is_chosen_return_the_print_ending_the_chat(self):
        sys = Mock()
        sys.exit.return_value = Mock()

        def print_foo(text):
            nonlocal test_case
            test_case = text

        builtins.input.return_value = '4'
        test_case = ""
        builtins.print = print_foo

        with self.assertRaises(SystemExit):
            return_method = self.object_session.access_to_the_message_log('destination')
            self.assertEqual(return_method, True)
        self.assertEqual(test_case, 'Leaving the chat.....')

    @patch('builtins.print', Mock())
    @patch('builtins.input', Mock())
    def test_checks_the_behavior_of_the_access_to_the_message_log_method_if_an_invalid_value_is_entered(self):
        builtins.input.return_value = '5'

        def print_foo(text):
            nonlocal test_case
            test_case = text

        test_case = ""
        builtins.print = print_foo
        self.object_session.access_to_the_message_log('destination')
        self.assertEqual(test_case, 'Option not found')

    @patch('builtins.print', Mock())
    @patch('builtins.input', Mock())
    def test_define_message_you_want_to_consume_option_1(self):
        builtins.input.return_value = '1'
        builtins.print.return_value = Mock()
        return_logs = self.object_session.define_message_you_want_to_consume()
        self.assertEqual(return_logs, 'MAGDA_CANAA')

    @patch.object(builtins, 'print')
    @patch('builtins.input', Mock())
    def test_define_message_you_want_to_consume_option_2(self, print_moc):
        builtins.input.return_value = '2'
        return_logs = self.object_session.define_message_you_want_to_consume()
        print_moc.assert_called()
        self.assertEqual(return_logs, 'GRUPO_CANAA')

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_define_message_you_want_to_consume_option_3(self, input_mock, print_mock, exit_mock):
        sys = Mock()
        sys.exit.return_value = Mock()
        exit_mock.return_value = Mock()
        builtins.input.return_value = '3'
        return_logs = self.object_session.define_message_you_want_to_consume()

        self.assertEqual(return_logs, None)
        print_mock.assert_called()
        input_mock.assert_called()

    @patch('app.models.session.begin_session.print')
    @patch('builtins.input', Mock())
    def test_define_message_you_want_to_consume_option_invalid(self, print_mock):
        builtins.input.return_value = '4'
        return_logs = self.object_session.define_message_you_want_to_consume()

        self.assertEqual(return_logs, print_mock.return_value)
        print_mock.assert_called_with('Error')

    @patch('app.models.send.send_message.SendRabbitMQ.start_sending_message')
    @patch.object(Session, 'access_to_the_message_log')
    @patch('app.database.mongo_db.ConnectionDataBase.get_all_message_logs')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_collects_the_message_typed_by_the_user(self, print_mock, input_mock, get_all_mock,
                                                    log_mock,
                                                    send_mock):
        queue_name = 'test_queue'
        exchange_name = 'test'
        type_exchange = 'topic'
        routing_key = ''
        input_mock.return_value = 'test'
        get_all_mock.return_value = Mock()
        log_mock.return_value = ''
        send_mock.return_value = Mock()
        self.object_session.collects_the_message_typed_by_the_user(queue_name, exchange_name, type_exchange,
                                                                   routing_key)

        print_mock.assert_called_with('Starting conversation with', 'test_queue')
