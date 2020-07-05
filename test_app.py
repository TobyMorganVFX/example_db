"""
This is the unittest file I have been working with.
Not all test throw errors some are printing just so I can see that files are being read.
Adjust the test db location in the base class.

"""

import unittest
import app
import sqlite3
from sqlite3 import Error
import os

import logging

logging.basicConfig(level=logging.DEBUG)


# Setup a base class to be subclassed to all tests mainly to chose which Database to use as a test
class CheckDB(unittest.TestCase):
    def setUp(self):
        self.database = "test_small_db.db"
        self.db_connection = self.connect_to_database(self.database)

    def tearDown(self):
        self.db_connection.execute("DROP TABLE users;")
        self.db_connection.commit()

    def connect_to_database(self, database):
        connection = None
        try:
            connection = sqlite3.connect(database)
            print("Connection to SQLite DB successful")
        except Error as e:
            print("Error: {}".format(e))

        return connection

    def create_db(self):
        self.db_connection.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      address TEXT,
                      phone TEXT
                    );
                    """)
        self.db_connection.commit()


# lets make sure that the settings.py are being read in correctly
class TestDatabase(unittest.TestCase):
    def test_basic_settings(self):
        args = app.app_parser(["checkdb"])
        result = args.func(args)
        logging.info("Can connect to the db defined in settings")


class TestAddingToDB(CheckDB):
    """ Anything that can be added to the db and teared down later does not require data to be already existing"""

    def setUp(self):
        super(TestAddingToDB, self).setUp()

    ## manage records
    # Add new user
    def test_001_add_user_nameOnly(self):
        # User Action
        name = "TestName"
        args = app.app_parser(["-db", self.database, "add_user", "-n", name])
        args.func(args)

        # Check DB
        query = self.db_connection.execute("SELECT * FROM users WHERE id=(SELECT MAX(ID) FROM users) AND name=?",
                                           (name,))
        result = query.fetchone()
        self.assertIsNotNone(result, msg="The test name has not been updated into the database")
        logging.info("%s was successfully added" % str(result))

    def test_002_add_user(self):
        name = "TestName"
        args = app.app_parser(["-db", self.database, "add_user", "-n", name, "-a", "test address", "-p", "90000000"])
        args.func(args)
        query = self.db_connection.execute("SELECT * FROM users WHERE id=(SELECT MAX(ID) FROM users) AND name=?",
                                           (name,))
        result = query.fetchone()
        self.assertIsNotNone(result, msg="The    test name has not been updated into the database")
        logging.info("%s was successfully added" % str(result))

    def test_003_add_from_csv(self):
        # user
        args = app.app_parser(["-db", self.database, "add_user", "-csv", ".\\test.csv"])
        args.func(args)
        query = self.db_connection.execute("SELECT * FROM users")
        result = query.fetchall()
        # I need a way to test this
        logging.info(result)

    def test_003_add_from_json(self):
        # user
        args = app.app_parser(["-db", self.database, "add_user", "-json", ".\\test.json"])
        args.func(args)
        query = self.db_connection.execute("SELECT * FROM users")
        result = query.fetchall()
        # I need a way to test this
        logging.info(result)



class TestRemovingFromDB(CheckDB):
    """removing data from the db, and updating current entries"""
    def setUp(self):
        super(TestRemovingFromDB, self).setUp()
        self.test_users = [
            ["Janice James", "1 Mountainview Rd", "0408651221"],
            ["Dave Strong", "9 AppleTree Rd", "0404985257"],
            ["Tani Nguyen", "12 CandleStick", "0401731668"],
            ["David Smith", "12 CandleStick", "0401635548"],
        ]

        self.create_db()

        for user in self.test_users:
            self.db_connection.execute("INSERT INTO users (name, address, phone) VALUES (?, ?, ?);", (user[0],
                                                                                                      user[1],
                                                                                                      user[2]))
            self.db_connection.commit()

    # remove user
    def test_001_remove_user_with_id(self):
        # User commands
        id = 2
        args = app.app_parser(["-db", self.database, "delete_user", "-id", str(id)])
        args.func(args)

        query = self.db_connection.execute("SELECT * FROM users WHERE id=?",
                                           (id,))
        result = query.fetchone()
        self.assertIsNone(result, msg="delete_user failed to remove user with id: %s" % id)
        logging.info("delete_user command is successful")

    # update user
    def test_002_update_user(self):
        # user input
        id = 3
        new_phone = "0416354865"
        args = app.app_parser(["-db", self.database, "update_user", "-id", str(id), "-p", new_phone])
        args.func(args)

        query = self.db_connection.execute("SELECT * FROM users WHERE id=? AND phone=?",
                                           (id, new_phone))
        result = query.fetchone()
        self.assertIsNotNone(result, msg="update_user failed to update user with id: %s" % id)
        logging.info("User with id: %s has successfully been updated" % id)

    def test_003_SearchName(self):
        # user should return 2 users
        name_search_term = "Dav*"
        args = app.app_parser(["-db", self.database, "search", "-n", name_search_term])
        result = args.func(args)
        # Check result
        self.assertIs(len(result), 2, "The name search didn't return the expected amount of names")
        logging.info("2 results have successfully been found by the search term Dav*")

    def test_004_display_to_screen(self):
        # User
        args = app.app_parser(["-db", self.database, "display"])
        result = args.func(args)
        # check that the correct data is returned list of lists with headers
        self.assertEqual(len(result), len(self.test_users) + 1)
        logging.info("Table has the correct number of returned lines")

    def test_005_display_to_html(self):
        # User
        args = app.app_parser(["-db", self.database, "display", "-html"])
        result = args.func(args)

    def test_006_display_to_json(self):
        # User
        args = app.app_parser(["-db", self.database, "display", "-json"])
        result = args.func(args)

    def test_007_write_to_csv(self):
        # User
        args = app.app_parser(["-db", self.database, "display", "-csv", "-o", ".\\test.csv"])
        result = args.func(args)
        self.assertTrue(os.path.exists(os.path.abspath(".\\test.csv")))
        logging.info("A json file has been writen")

    def test_008_writing_json_file(self):
        # User
        args = app.app_parser(["-db", self.database, "display", "-json", "-o", ".\\test.json"])
        result = args.func(args)
        self.assertTrue(os.path.exists(os.path.abspath(".\\test.json")))
        logging.info("A json file has been writen")

    def test_009_display_to_screen_search(self):
        # User
        args = app.app_parser(["-db", self.database, "display", "-n", "Da*"])
        result = args.func(args)
        # check that the correct data is returned list of lists with headers
        self.assertIs(len(result)-1, 2, "The name search didn't return the expected amount of names")
        logging.info("2 results have successfully been found by the search term Dav*")

    def test_005_display_to_html(self):
        # User
        args = app.app_parser(["-db", self.database, "display", "-html", "-o", ".\\test.html"])
        result = args.func(args)

if __name__ == '__main__':
    unittest.main(verbosity=2)
