import sqlite3

def connect():
    return sqlite3.connect("database.db")

def create_table(connection):
    with connection:
        connection.execute(
            "CREATE TABLE vaccines(id INTEGER PRIMARY KEY, date DATE NOT NULL, supplier INTEGER, quantity INTEGER NOT NULL);"
        )

def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    connect()
