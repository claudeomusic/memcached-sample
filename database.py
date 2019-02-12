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
            ''' CREATE TABLE IF NOT EXISTS MEMCACHED
                (KEY TEXT PRIMARY KEY, FLAGS UNSIGNED INTEGER, VALUE TEXT)''')

    def show_all(self):
        print('(KEY, FLAGS, VALUE)')
        try:
            cursor = self.connection.cursor()
            for row in cursor.execute('SELECT * FROM MEMCACHED'):
                print(row)
        except:
            print('Database error.')

    def insert_value(self, key, flags, value):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO MEMCACHED VALUES (?, ?, ?)",
                           (key, flags, value))
            self.connection.commit()
            return True
        except:
            return False

    def get_value(self, key):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT FLAGS, VALUE FROM MEMCACHED WHERE KEY = ?", (key,))
            first_match = cursor.fetchone()
            return first_match[0], first_match[1]
        except:
            return False

    def delete_key(self, key):
        try:
            cursor = self.connection.cursor()
            impact = cursor.execute(
                "DELETE FROM MEMCACHED WHERE KEY = ?", (key,)).rowcount
            self.connection.commit()
            return False if impact == 0 else True
        except:
            return False
