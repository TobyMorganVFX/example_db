"""
Data IO, convert
"""
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

    def print_table_html(self, title="default", write=False, path=None):
        table_string = ""
        for row in self._data:
            table_string += "<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>\n".format(*row)
        # Hardcoding the template for now but would be better to have this as a file that can be set by settings.py
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
        if write:
            with open(os.path.abspath(path), "w") as html_file:
                html_file.write(basic_html)
        elif not write:
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


class FileReader(object):
    def __init__(self, read_file):
        self.file = os.path.abspath(read_file)

    def read_csv(self):
        with open(self.file, "rb") as csv_file:
            reader = csv.reader(csv_file)
            return list(reader)

    def read_json(self):
        with open(self.file, "r") as json_file:
            return json.load(json_file)
