from DAO import *
import DTO
import atexit
import sqlite3


class _Repository:
    def __init__(self):
        self._con = sqlite3.connect("database.db")
        self.logistics = Logistics(self._con)
        self.clinics = Clinics(self._con)
        self.suppliers = Suppliers(self._con)
        self.vaccines = Vaccines(self._con)
        self._output = None

    def update_output(self, output):
        self._output = output

    def _close(self):
        self._con.commit()
        self._con.close()

    def create_tables(self):
        self._con.executescript("""
        CREATE TABLE logistics(id INT PRIMARY KEY,
                               name TEXT NOT NULL,
                               count_sent INT NOT NULL,
                               count_received INTEGER NOT NULL);
        CREATE TABLE clinics  (id INT PRIMARY KEY,
                               location TEXT NOT NULL,
                               demand INT NOT NULL,
                               logistic INT REFERENCES logistics(id));
        CREATE TABLE suppliers(id INT PRIMARY KEY,
                               name TEXT NOT NULL,
                               logistic INT REFERENCES logistics(id));
        CREATE TABLE vaccines (id INT PRIMARY KEY,
                               date DATE NOT NULL,
                               supplier INT REFERENCES suppliers(id),
                               quantity INT NOT NULL);                                
        """)

    def fill_tables(self, path):
        config = open(path)
        numbers = [int(x) for x in config.readline().split(",")]
        numOfVaccines = numbers[0]
        numOfSuppliers = numbers[1]
        numOfClinics = numbers[2]
        numOfLogistics = numbers[3]

        vaccines = [config.readline().replace("\n", "") for x in range(numOfVaccines)]
        suppliers = [config.readline().replace("\n", "") for x in range(numOfSuppliers)]
        clinics = [config.readline().replace("\n", "") for x in range(numOfClinics)]
        logistics = [config.readline().replace("\n", "") for x in range(numOfLogistics)]
        self.fill_logistics_table(logistics)
        self.fill_clinics_table(clinics)
        self.fill_suppliers_table(suppliers)
        self.fill_vaccines_table(vaccines)
        config.close()

    def fill_logistics_table(self, props):
        for x in range(len(props)):
            logistic = self.create_DTO(DTO.Logistic, props[x])
            self._output.increase_total_received(logistic.count_received)
            self._output.increase_total_sent(logistic.count_sent)
            self.logistics.insert(logistic)

    def fill_clinics_table(self, props):
        for x in range(len(props)):
            clinic = self.create_DTO(DTO.Clinic, props[x])
            self._output.increase_total_demand(clinic.demand)
            self.clinics.insert(clinic)

    def fill_suppliers_table(self, props):
        for x in range(len(props)):
            self.suppliers.insert(self.create_DTO(DTO.Supplier, props[x]))

    def fill_vaccines_table(self, props):
        for x in range(len(props)):
            vaccine = self.create_DTO(DTO.Vaccine, props[x])
            self._output.increase_total_inventory(vaccine.quantity)
            self.vaccines.insert(vaccine)

    def create_DTO(self, dto_type, props):
        toInsert = props.split(",")
        return dto_type(*toInsert)

    def receive_orders(self, path):
        orders = open(path)
        all_orders = orders.readlines()
        orders_list = [order.replace("\n", "") for order in all_orders]
        for order in orders_list:
            args = [arg for arg in order.split(",")]
            if len(args) == 2:
                self.send_shipment(args[0], int(args[1]))
            else:
                self.receive_shipment(args[0], int(args[1]), args[2])
        orders.close()

    def send_shipment(self, location, amount):
        self._output.decrease_total_inventory(amount)
        self._output.decrease_total_demand(amount)
        self._output.increase_total_sent(amount)
        clinic = self.clinics.find_by_location(location)
        self.logistics.increase_count_sent(amount, clinic.logistic)
        self.clinics.decrease_demand(amount, location)
        cursor = self._con.cursor()
        vaccines_by_date = self.vaccines.get_vaccines_by_date(cursor)
        for vaccine in vaccines_by_date:
            if vaccine.quantity < amount:
                self.vaccines.remove(vaccine.id)
                amount -= vaccine.quantity
            else:
                self.vaccines.update_quantity(vaccine.quantity-amount, vaccine.id)
                break
        self._output.update_output()

    def receive_shipment(self, name, amount, date):
        self._output.increase_total_inventory(amount)
        self._output.increase_total_received(amount)
        id_supplier = self.suppliers.find_by_name(name).id
        cursor = self._con.cursor()
        next_id = self.vaccines.get_new_index(cursor)
        self.vaccines.insert(DTO.Vaccine(next_id, date, id_supplier, amount))
        logistic_id = self.suppliers.find_by_name(name).logistic
        self.logistics.increase_count_received(amount, logistic_id)
        self._output.update_output()


repo = _Repository()
atexit.register(repo._close)
