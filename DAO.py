from DTO import *
import sqlite3

class Vaccines:
    def __init__(self, con):
        self._con = con

    def insert(self, vaccines_dto):
        self._con.execute("""
                INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
        """, [vaccines_dto.id, vaccines_dto.date, vaccines_dto.supplier, vaccines_dto.quantity])

    def find_by_id(self, id):
        c = self._con.cursor()
        c.execute("""
                SELECT * FROM vaccines WHERE id = ?
            """, [id])

        return Vaccine(*c.fetchone())

    def remove(self, id):
        self._con.execute("DELETE FROM vaccines WHERE id = ?",[id])

    def get_vaccines_by_date(self, cursor):
        cursor.execute("SELECT * FROM vaccines ORDER BY date ASC")
        return orm(cursor, Vaccine)

    def update_quantity(self, new_quantity, id):
        self._con.execute("UPDATE vaccines SET quantity = ? WHERE id = ?", [new_quantity, id])

    def get_new_index(self, cursor):
        cursor.execute("SELECT MAX(id) FROM vaccines")
        return cursor.fetchone()[0]+1


    def find_all(self):
        c = self._con.cursor()
        c.execute("SELECT * FROM vaccines")
        return orm(c, Vaccine)


class Clinics:
    def __init__(self, con):
        self._con = con

    def insert(self, clinic_dto):
        self._con.execute("""
                INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [clinic_dto.id, clinic_dto.location, clinic_dto.demand, clinic_dto.logistic])

    def find_by_id(self, id):
        c = self._con.cursor()
        c.execute("""
                SELECT * FROM clinics WHERE id = ?
            """, [id])

        return Clinic(*c.fetchone())

    def find_by_location(self, location):
        c = self._con.cursor()
        c.execute("""
                SELECT * FROM clinics WHERE location = ?
            """, [location])
        return Clinic(*c.fetchone())

    def decrease_demand(self, amount, location):
        self._con.execute("UPDATE clinics SET demand = (demand - ?) WHERE location = ?", [amount, location])

    def find_all(self):
        c = self._con.cursor()
        c.execute("SELECT * FROM clinics")
        return orm(c, Clinic)


class Logistics:
    def __init__(self, con):
        self._con = con

    def insert(self, logistic_dto):
        self._con.execute("""
                INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
        """, [logistic_dto.id, logistic_dto.name, logistic_dto.count_sent, logistic_dto.count_received])

    def find(self, id):
        c = self._con.cursor()
        c.execute("""
                SELECT * FROM logistics WHERE id = ?
            """, [id])

        return Logistic(*c.fetchone())

    def find_all(self):
        c = self._con.cursor()
        c.execute("SELECT * FROM logistics")
        return orm(c, Logistic)

    def increase_count_sent(self, amount, id):
        self._con.execute("UPDATE logistics SET count_sent = (count_sent + ?) WHERE id = ?", [amount, id])

    def increase_count_received(self, amount, logistic_id):
        self._con.execute("UPDATE logistics SET count_received = (count_received + ?) WHERE id = ?",
                          [amount, logistic_id])


class Suppliers:
    def __init__(self, con):
        self._con = con

    def insert(self, supplier_dto):
        self._con.execute("""
                INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
        """, [supplier_dto.id, supplier_dto.name, supplier_dto.logistic])

    def find_by_name(self, name):
        c = self._con.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE name = ?""", [name])

        return Supplier(*c.fetchone())

    def find_all(self):
        c = self._con.cursor()
        c.execute("SELECT * FROM suppliers")
        return orm(c, Supplier)