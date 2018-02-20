from typing import Tuple
from collections import defaultdict
import math
from typing import Dict

import time


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
        coordinate = (line[1], line[2])
        service_duration = line[3]
        demand = line[4]
        customers[customer_id].extend([coordinate, service_duration, demand])
    for i in range(number_of_depots):
        line = list(map(lambda e: int(e), file.readline().split()[0:3]))
        depot_id = line[0]
        coordinate = (line[1], line[2])
        max_duration = tmp_depots[i][0]
        max_load = tmp_depots[i][1]
        depots[depot_id].extend([coordinate, max_duration, max_load])

    return customers, depots, max_vehicles


def copy_dict(to_copy: Dict) -> Dict:
    result = defaultdict(list)
    for key in to_copy:
        result[key] = to_copy[key][:]
    return result


def write_results_to_file(chromosome, file_number):
    file_name = "../data/our_solution/" + file_number + ".res"
    file = open(file_name, "w")
    file.write('%s\n' % (chromosome.calculate_distance()[0]))
    for depot_id, routes in chromosome.routes.items():
        depot_coordinates = chromosome.depots[depot_id][0]
        for i in range(len(routes)):
            customer_demand = 0
            distance = 0
            previous_coordinates = None
            for j in range(len(routes[i])):
                customer_id = routes[i][j]
                current_coordinates = chromosome.customers[customer_id][0]
                if j == 0:
                    previous_coordinates = depot_coordinates

                elif j == len(routes[i]):
                    print("test")
                    current_coordinates = depot_coordinates

                distance += euclidean_distance(current_coordinates, previous_coordinates)
                previous_coordinates = current_coordinates
                customer_demand += chromosome.customers[routes[i][j]][2]
            if len(routes[i]) > 0:
                routes[i].insert(0, 0)
                routes[i].insert(len(routes[i]), 0)
                route = ' '.join([str(customer) for customer in routes[i]])
                file.write('{:d}   {:d}   {:.2f}   {:d}   {}\n'.format(depot_id, i, distance, customer_demand, route))


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def timeit(method):
    def measure_time(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('function %r used %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return measure_time
