from typing import Tuple
from collections import defaultdict
import math
from typing import Dict


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


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
