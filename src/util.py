from typing import Tuple


def parse_problem(filename: str) -> Tuple:
    file = open(filename, "r")
    line1 = list(map(lambda e: int(e), file.readline().split()))
    number_of_vehicles = line1[0]
    number_of_customers = line1[1]
    number_of_depots = line1[2]
    depots = []
    customers = []
    for i in range(number_of_depots):
        depots.append(list(map(lambda e: int(e), file.readline().split())))
    for i in range(number_of_customers):
        customers.append(list(map(lambda e: int(e), file.readline().split())))
    for i in range(number_of_depots):
        depots[i].extend(list(map(lambda e: int(e), file.readline().split())))
    return customers, depots, number_of_vehicles


if __name__ == '__main__':
    parse_problem("../data/problem/p01")
