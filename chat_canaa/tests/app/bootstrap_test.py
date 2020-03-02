from app.bootstrap import excecute_send, excecute_receive
import mongomock
import unittest
from unittest.mock import Mock, patch, call
from app.models.session.begin_session import Session


class TestBootstrap(unittest.TestCase):

    @patch('start_receive.excecute_receive')
    @patch.object(Session, 'open_session_send')
    @patch.object(Session, 'open_session_receive')
    @patch('app.models.session.begin_session.Session.__init__')
    def test_calls_the_send_and_receive_execution_methods_to_start_the_chat(self, session_mock, send_mock, receive_mock,
                                                                            start_receive_mock):
        session_mock.return_value = None
        send_mock.return_value = Mock()
        receive_mock.return_value = excecute_receive()
        start_receive_mock.return_value = excecute_send()

        session_mock.assert_called()
        send_mock.assert_called_once()
        receive_mock.assert_called_once()
