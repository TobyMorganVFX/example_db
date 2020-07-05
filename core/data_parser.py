import json
import os
import csv

class TableView(object):
    """ A helper poject to format table data into various outputs"""

    def __init__(self, table_settings):
        self.name = table_settings.get("name")
        self.columns = tuple(table_settings.get("columns").keys())
        self._data = [self.columns]

    def add_rows(self, rows=[]):
        self._data.extend(rows)

    def clear(self):
        del self._data[:]

    def print_table_lines(self):
        row_string = ""
        rows = []
        for row in self._data:
            for col in row:
                row_string += "{} |".format(str(col).ljust(20, " "))
            rows.append(row_string)
            row_string = ""

        return rows

    def print_table_html(self, title="default", output=None):
        table_string = ""

        for row in self._data:
            table_string += "<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>\n".format(*row)

        basic_html = """<!doctype html>
                            <html>
                                <head>
                                    <title>{}</title>
                                    <style style="width:690px">
                                        table, th, td {{
                                        border-style: solid;
                                        border-collapse: collapse;
                                        }}
                                    </style>
                                </head>
                            <body>
                                <table>
                                    {}
                                </table>
                            </body>
                        </html>""".format(title, table_string)

        return basic_html

    def serialize_json(self, write=False, path=None):
        if write:
            with open(os.path.abspath(path), "w") as output:
                json.dump(self._data, output)
        else:
            return json.dumps(self._data)

    def serialize_csv(self, write=False, path=None):
        if write:
            with open(os.path.abspath(path), "w") as output:
                writer = csv.writer(output)
                writer.writerows(self._data)
            return True
