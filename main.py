import sqlite3
import os

def connect():
    return sqlite3.connect("database.db")


def create_tables(connection):
    with connection:
        connection.execute("CREATE TABLE logistics"
            "(id INTEGER PRIMARY KEY, name STRING NOT NULL, count_sent INTEGER NOT NULL, count_received INTEGER NOT NULL);")
        connection.execute("CREATE TABLE clinics"
            "(id INTEGER PRIMARY KEY,location STRING NOT NULL, demand INTEGER NOT NULL, logistic INTEGER REFERENCES logistics(id));")
        connection.execute("CREATE TABLE suppliers"
            "(id INTEGER PRIMARY KEY, name STRING NOT NULL, logistic INTEGER REFERENCES logistics(id));")
        connection.execute("CREATE TABLE vaccines"
            "(id INTEGER PRIMARY KEY, date DATE NOT NULL, supplier INTEGER REFERENCES suppliers(id), quantity INTEGER NOT NULL);")


def fill_logistics_table(props, connection):
    logistic = props.split(",")
    id_ = int(logistic[0])
    name_ = logistic[1]
    count_sent_ = int(logistic[2])
    count_received_ = int(logistic[3])
    with connection:
        connection.execute("INSERT INTO logistics"
                           "VALUES(id_,name_,count_sent_,count_received_);")



def fill_clinics_table(props):
    return


def fill_suppliers_table(props):
    return


def fill_vaccines_table(props):
    return


def parse_config_file(path, connection):
    with open(path) as data:
        lines = data.readlines()
        int_numbers = [int(x)for x in lines[0].split(",")]
        for i in range(len(lines)-int_numbers[3], len(lines)):
            print(type(lines[i]))
            fill_logistics_table(lines[i],connection)




def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    connection = connect()
    create_tables(connection)
    parse_config_file("./config.txt",connection)
    #os.remove("./database.db")