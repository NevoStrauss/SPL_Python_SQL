import sqlite3


def connect():
    return sqlite3.connect("database.db")


def create_tables(connection):
    with connection:
        connection.execute("CREATE TABLE logistics"
            "(id INTEGER PRIMARY KEY, name STRING NOT NULL,count_sent INTEGER NOT NULL, count_received INTEGER NOT NULL);")
        connection.execute("CREATE TABLE clinics"
            "(id INTEGER PRIMARY KEY,location STRING NOT NULL, demand INTEGER NOT NULL, logistic INTEGER REFERENCES logistics(id));")
        connection.execute("CREATE TABLE suppliers"
            "(id INTEGER PRIMARY KEY, name STRING NOT NULL, logistic INTEGER REFERENCES logistics(id));")
        connection.execute("CREATE TABLE vaccines"
            "(id INTEGER PRIMARY KEY, date DATE NOT NULL, supplier INTEGER REFERENCES suppliers(id), quantity INTEGER NOT NULL);")


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    connection = connect()
    create_tables(connection)
