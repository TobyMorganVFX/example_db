"""
A Dictionary to configure the database.
"""
from collections import OrderedDict
basic = {
    "DATABASE": "small_db.db",
    "TABLE": {"name": "users",
              "columns": OrderedDict([("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                                      ("name", "TEXT NOT NULL"),
                                      ("address", "TEXT"),
                                      ("phone", "TEXT")
                                      ])
              },
    # "HTML_TEMPLATE": "basic_page.html"
}
