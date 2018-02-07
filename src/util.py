from typing import Tuple
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def read_problem_file(filename: str) -> Tuple:
    file = open(filename, "r")
    line1 = list(map(lambda e: int(e), file.readline().split()))
    max_vehicles = line1[0]
    number_of_customers = line1[1]
    number_of_depots = line1[2]
    tmp_depots = []
    depots = defaultdict(list)
    customers = defaultdict(list)
    for i in range(number_of_depots):
        line = list(map(lambda e: int(e), file.readline().split()))
        tmp_depots.append(line)
    for i in range(number_of_customers):
        line = list(map(lambda e: int(e), file.readline().split()[0:5]))
        customer_id = line[0]
        coordinate = np.array([line[1], line[2]])
        service_duration = line[3]
        demand = line[4]
        customers[customer_id].extend([coordinate, service_duration, demand])
    for i in range(number_of_depots):
        line = list(map(lambda e: int(e), file.readline().split()[0:3]))
        depot_id = line[0]
        coordinate = np.array([line[1], line[2]])
        max_duration = tmp_depots[i][0]
        max_load = tmp_depots[i][1]
        depots[depot_id].extend([coordinate, max_duration, max_load])
    return customers, depots, max_vehicles


"""
def plot_problem(data):
    customers = data.customers
    depots = data.depots
    number_of_vehicles = data.number_of_vehicles

    for c in customers:
        x = c[1]
        y = c[2]
        plt.scatter(x, y, color='blue')

    for d in depots:
        x = d[3]
        y = d[4]
        plt.scatter(x, y, color='red', s=100)
        for i in range(number_of_vehicles):
            plt.scatter(x, y, color='yellow')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5,
               handles=[mpatches.Patch(color='blue', label=str(len(customers)) + ' Customers'),
                        mpatches.Patch(color='red', label=str(len(depots)) + ' Depots'),
                        mpatches.Patch(color='yellow', label=str(number_of_vehicles) + ' Vehicles')])
    plt.show()
"""
