from .database import Sqlite
from . import data_parser


class UserApp(object):
    def __init__(self, settings):
        """UserApp is a collection of commands to manage the user interaction with the database object.
        :arg settings dictionary to

        """
        self.database_path = settings.get("DATABASE", ":memory:")
        self.database = None
        self.table = settings.get("TABLE")

    def get_database(self, args):
        if args.database:
            return Sqlite(args.database, self.table)
        else:
            return Sqlite(self.database_path, self.table)

    def check_db(self, args):
        user_db = self.get_database(args)

    def add_user(self, args):
        user_db = self.get_database(args)
        user_db.create_user(args.name, args.address, args.phone)

    def delete_user(self, args):
        user_db = self.get_database(args)
        user_db.delete_user(args.id)

    def update_user(self, args):
        user_db = self.get_database(args)
        user_db.update_user(args.id, name=args.name, address=args.address, phone=args.phone)

    def search(self, args):
        user_db = self.get_database(args)
        result = user_db.search(id=args.id, name=args.name, address=args.address, phone=args.phone)
        if result:
            for user in result:
                print("id: {0} | user: {1} | address: {2} | Phone Contact: {3}".format(*user))
        return result

    def display(self, args):
        user_db = self.get_database(args)
        result = user_db.get_table(self.table.get("name"))
        if result:
            table_view = data_parser.TableView(self.table)
            table_view.add_rows(result)

        if args.html:
            formatted_rows = table_view.print_table_html()
            print(formatted_rows)
        elif args.html and args.output:
            table_view.print_table_html(write=True, path=args.output)
        elif args.json and not args.output:
            formatted_rows = table_view.serialize_json()
            print(formatted_rows)
        elif args.json and args.output:
            formatted_rows = table_view.serialize_json(write=True, path=args.output)
        elif args.csv and args.output:
            formatted_rows = table_view.serialize_csv(write=True, path=args.output)
        else:
            formatted_rows = table_view.print_table_lines()
            for row in formatted_rows:
                print(row)
        return formatted_rows
