import os

from pymongo import MongoClient, ReturnDocument
from datetime import datetime

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://db:27017')


class ConnectionDataBase:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI, connect=False)
        self.db = self.client['chat']
        self.collection = self.db['hbsis']

    def include_message_in_json(self, body, destination_name, message_sender_or_receiver_flag):
        identifier = 1
        for records in self.collection.find({'destination': destination_name,
                                             'message_sender_or_receiver': message_sender_or_receiver_flag}):
            identifier += 1
        date = datetime.now()
        new_date_format = date.strftime("%d %B, %Y")
        new_time_format = date.strftime("%H:%M:%S")
        json = {
            'destination': destination_name,
            'active': True,
            'body': body,
            'send_date': new_date_format,
            'sending_time': new_time_format,
            'message_identifier': identifier,
            'message_sender_or_receiver': message_sender_or_receiver_flag
        }
        ConnectionDataBase.insert_message_to_database(self, json)

    def insert_message_to_database(self, json):
        self.collection.insert_one(json)

    def get_all_message_logs(self, destination_name, message_sender_or_receiver):
        teste = self.collection.find(
            {'destination': destination_name, 'message_sender_or_receiver': message_sender_or_receiver,
             'active': True})

        return teste

    def get_message_by_destination(self, destination_name):
        for records in self.collection.find({'destination': destination_name, 'active': True}):
            print(records['send_date'], records['body'])
            print("")

    def disable_message_history(self, message_identifier):
        self.collection.find_one_and_update({'message_identifier': int(message_identifier)},
                                            {'$set': {'active': False}})

        # print("Message record successfully deleted")
