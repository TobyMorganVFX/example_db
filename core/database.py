"""
Database Manager Object
"""

import sqlite3
from sqlite3 import Error


class Sqlite(object):
    """A general convenince to handle the database"""
    def __init__(self, database, table):
        self.connection = self.connect_to_database(database)
        self.setup_table(table)
        self.database = database

    def connect_to_database(self, database):
        connection = None
        try:
            connection = sqlite3.connect(database)
            print("Connection to SQLite DB successful")
        except Error as e:
            print("Error: {}".format(e))

        return connection

    def setup_table(self, table):
        """Set up the table as described in settings if it does not already exist"""
        create_string = "CREATE TABLE IF NOT EXISTS {} (".format(table.get("name", "default"))
        columns = table.get("columns")
        columns_string = ""
        for key, value in columns.items():
            columns_string += "{} {},".format(key, value)

        self.execute_query(create_string + columns_string[:-1] + ");")

    def execute_query(self, query, args_tuple=()):
        """
        Returns a sql cursor with the query committed to the database.
        To protect against injection add any variable substitutions as an optional tuple
        :param query: A string for sql to execute
        :param args: a set of arguments to be substituted into place holders.
        :return: Sqlite3.Cursor
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, args_tuple)
            self.connection.commit()
            # print("Query: {}".format(query))
            return cursor
        except Error as e:
            print("Error: {}".format(e))

    def create_user(self, name="", address="", phone_number=""):
        self.execute_query("INSERT INTO users (name, address, phone) VALUES (?, ?, ?);", (name, address, phone_number))

    def delete_user(self, id):
        self.execute_query("DELETE FROM users WHERE id=?", (id, ))

    def update_user(self, id, **kwargs):
        update_table = "UPDATE users"
        update_string = "SET"
        update_data = {"id": id}

        for key, value in kwargs.items():
            if value:
                update_string += " %s=:%s" % (key, key)
                update_data.update({key: value})

        self.execute_query("""{} {} WHERE id=:id""".format(update_table, update_string),
                           update_data)

    def search(self, id, **kwargs):
        search_string = ""
        search_data = {}
        if id:
            query = self.execute_query("SELECT * FROM users WHERE id=?", (id,))
            return query.fetchone()
        else:
            for key, value in kwargs.items():
                if value:
                    search_string += " %s GLOB :%s AND" % (key, key)
                    search_data.update({key: value})
            query = self.execute_query("""SELECT * FROM users
                                        WHERE {}""".format(search_string[:-3]), search_data)
            return query.fetchall()

    def get_table(self, table):
        query = self.execute_query("SELECT * FROM {};".format(table))
        return query.fetchall()

    def clear_data(self):
        self.execute_query("DROP TABLE users;")
        self.setup_table()
