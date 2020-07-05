#!/bin/python
"""A small database app that stores columns name, address, phone_number
   Out comes are:
   * build a simple API allowing you to add new records, filter users (e.g "name=Joe*") based on some simple search syntax like Glob.
   * support serialisation in 2 or more formats (e.g JSON, Yaml, XML, CSV etc)
   * Display the data in 2 or more different output formats (no need to use a GUI Framework, use e.g text output/HTML or any other human readable format).
   * Add a command line interface to add records, and display/convert/filter the whole data set
"""
import argparse
import sys
from core import settings
from core.commands import UserApp


def app_parser(args):
    # Get our Application Commands object
    user_app = UserApp(settings.basic)

    # print(args)
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument('-db', "--database", help="""specify another database location, 
                                                          use the :memory: filename to store in ram for testing""")

    subparsers = main_parser.add_subparsers(help='sub-command help')

    checkdb = subparsers.add_parser('checkdb', help='This is to check that the database exists')
    checkdb.set_defaults(func=user_app.check_db)

    # Add User
    add_user_parser = subparsers.add_parser('add_user', help='Add a user record, must have a name')
    add_user_parser.add_argument('-n', "--name")
    add_user_parser.add_argument('-a', "--address")
    add_user_parser.add_argument('-p', "--phone")
    add_user_parser.set_defaults(func=user_app.add_user)

    # Delete User
    delete_user_parser = subparsers.add_parser('delete_user', help='Delete a user record from database')
    delete_user_parser.add_argument('-id', type=int, help="A unique id number")
    delete_user_parser.set_defaults(func=user_app.delete_user)

    # update User
    update_user_parser = subparsers.add_parser('update_user', help='Update a user record in the database')
    update_user_parser.add_argument('-id', type=int, help="A unique id number")
    update_user_parser.add_argument('-n', "--name", help="Users name")
    update_user_parser.add_argument('-a', "--address", help="Users Address")
    update_user_parser.add_argument('-p', "--phone", help="Users Phone Number")
    update_user_parser.set_defaults(func=user_app.update_user)

    # search
    search_user_parser = subparsers.add_parser('search', help='Search for a user record in the database')
    search_user_parser.add_argument('-id', type=int, help="A unique id number")
    search_user_parser.add_argument('-n', "--name", help="Users name")
    search_user_parser.add_argument('-a', "--address", help="Users Address")
    search_user_parser.add_argument('-p', "--phone", help="Users Phone Number")
    search_user_parser.set_defaults(func=user_app.search)

    # display
    display_user_parser = subparsers.add_parser('display',
                                                help='Display records in the database to terminal or to file.')
    display_group = display_user_parser.add_mutually_exclusive_group()
    display_group.add_argument("-html", action="store_true", help="Will display as a html")
    display_group.add_argument("-json", action="store_true", help="Will display as a json")
    display_group.add_argument("-csv", action="store_true", help="Will display as a xml")
    display_user_parser.add_argument('-o', "--output", help="write to file instead of display")
    display_user_parser.set_defaults(func=user_app.display)

    return main_parser.parse_args(args)


if __name__ == "__main__":
    app_args = app_parser(sys.argv[1:])
    app_args.func(app_args)

