import sqlite3


class Database:
    """
    Class to abstract data persistence layer.
    """

    def __init__(self):
        self.connection = None

    def initialize(self, db_name):
        self.connection = sqlite3.connect(db_name)
        cursor = self.connection.cursor()
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS PAIRS (KEY TEXT, VALUE TEXT)''')
        cursor.execute(
            ''' CREATE INDEX IF NOT EXISTS KEY_INDEX ON PAIRS(KEY)''')

    def insert_pair(self, key, value):
        # todo: implement
        print('inserting pair')
    
    def get_value(self, key):
        # todo: implement
        print('getting value')
