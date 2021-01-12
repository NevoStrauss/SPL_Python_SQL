from DTO import *
from GenericDAO import *
from _Repository import repo


if __name__ == '__main__':
    repo.create_tables()
    repo.fill_tables("./config.txt")
    repo.receive_orders("./orders.txt")
    repo.send_shipment("Tel_Aviv", 40)
    repo.receive_shipment('Pfizer', 20, "2021−01−6")