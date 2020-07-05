# example db
Toby Morgan
toby@toby-morgan.com
A small database app that shows an example of creating a database with user name/address/phone
Built to be used by command line on either python 2.7 or 3. To keep things simple the aim is to only use in-built modules.

## Usage
python app.py {command} |-options|<br>
###### For help: <br>
    python app.py --help 
    python app.py command --help

## Commands
* add_user | Add user entries one at a time or with csv/json
* delete_user | Remove user entry by id
* update_user | Update an entry using id to identify
* search | Search by id or glob search any of the columns
* display | Return either the whole table or search result to console or export to html|csv|json

## Configuration
    /core/settings.py
This python file contains a dictionary of settings to be passed to the rest of the app.
- database file, table name, table columns can be set.

Note: while extra columns can be set in settings they can't be managed by all commands.

## Testing
    python test_app.py


## Current known Issues
Currently a csv exported can be re-imported in python 2.7 but not in 3+

