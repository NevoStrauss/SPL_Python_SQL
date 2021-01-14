import os
import sys
from _Repository import *


def main(argv):
    output = Output(argv[3])
    repo.update_output(output)
    repo.create_tables()
    repo.fill_tables(argv[1])
    repo.receive_orders(argv[2])
    output.close()


class Output:
    def __init__(self, path):
        self.total_inventory = 0
        self.total_demand = 0
        self.total_received = 0
        self.total_sent = 0
        self.output = open(path, "w")

    def close(self):
        self.output.close()

    def increase_total_inventory(self, new_vaccines):
        int_new_vaccines = int(new_vaccines)
        self.total_inventory += int_new_vaccines

    def decrease_total_inventory(self, sent_vaccines):
        int_sent_vaccines = int(sent_vaccines)
        self.total_inventory -= int_sent_vaccines

    def increase_total_demand(self, new_demand):
        int_new_demand = int(new_demand)
        self.total_demand += int_new_demand

    def decrease_total_demand(self, satisfied_demand):
        self.total_demand -= satisfied_demand

    def increase_total_received(self, new_received):
        int_new_received = int(new_received)
        self.total_received += int_new_received

    def increase_total_sent(self, vaccines_sent):
        int_vaccines_sent = int(vaccines_sent)
        self.total_sent += int_vaccines_sent

    def update_output(self):
        output_line = str(self.total_inventory)+","+str(self.total_demand)+","+\
                 str(self.total_received)+","+str(self.total_sent)+"\n"
        self.output.write(output_line)


if __name__ == '__main__':
    main(sys.argv)



