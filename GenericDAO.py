from DTO import *
import sqlite3


class Dao:
    def __init__(self, dto_type, con):
        self._con = con
        self._dto_type = dto_type
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)
        column_names = ','.join(ins_dict.keys())
        params = ins_dict.values()
        q_marks = ','.join(['?'] * len(ins_dict))
        statement = "INSERT INTO {} ({}) VALUES ({})".format(self._table_name, column_names, q_marks)
        self._con.execute(statement, list(params))

    def find_all(self):
        c = self._con.cursor()
        c.execute("SELECT * FROM{}".format(self._table_name))
        return orm(c, self._dto_type)

    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = keyvals.values()
        statement = "SELECT * FROM {} WHERE {}".format(self._table_name,
                                                       "AND".join([col + " = ?" for col in column_names]))
        c = self._con.cursor()
        c.execute(statement, list(params))
        # c.execute("SELECT * FROM {} WHERE {}".format(self._table_name,
        #                                                "AND".join([col + " = ?" for col in column_names])),list(params))
        return orm(c, self._dto_type)

    def update(self, set_values, cond):
        set_column_names = set_values.keys()
        set_params = set_values.values()

        cond_column_names = cond.keys()
        cond_params = cond.values()

        params = dict(set_params.items() + cond_params.items())

        stmt = "UPDATE {} SET ({}) WHERE ({})".format(self._table_name,
                                                      ', '.join([set + '=?' for set in set_column_names]),
                                                      ' AND '.join([cond + '=?' for cond in cond_column_names]))
        self._con.execute(stmt, params)

    def remove(self, id):
        pass
